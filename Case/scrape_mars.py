#!/usr/bin/env python
# coding: utf-8

# # Step 1 - Scraping

# # NASA MARS NEWS

# In[1]:


#get_ipython().system('pip install bs4 --user')


# In[27]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
import pandas as pd


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# URL of NASA MARS NEWS to be scraped
def mars_news():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    
    news_soup = BeautifulSoup(html, 'html.parser')

    article_container = news_soup.find('ul', class_='item_list')

    headline_date = article_container.find('div', class_='list_date').text
    news_title = article_container.find('div', class_='content_title').find('a').text
    news_p = article_container.find('div', class_='article_teaser_body').text

    return headline_date,news_title, news_p




# In[33]:

# # JPL Mars Space Images
# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



def featured_image():
    
    base_url = 'https://www.jp1.nasa.gov'

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #method1 :parsing through the style attribute in the article tag
    try:
        img_elem = img_soup.find('article', class_='carousel_item')['style']
        img_rel_url = img_elem.replace("background-image: url('", '')
        img_rel_url = img_rel_url.replace("');",'')
        
    except Exception as e:
        print(e)

    #method2: clicking the FULL TEXT button and pulling the image
    try:
        full_image_elem = browser.find_by_id('full_image')[0]
        full_image_elem.click()

        html= browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        img_rel_url = img_soup.find('img', class_='fancybox-image')['src']
        print(img_rel_url)
    except Exception as e:
        print(e)

    featured_image_url = f'{base_url}{img_rel_url}'

    return(featured_image_url)




# In[37]:
# # Mars Facts - Using Pandas to scrape the table

def mars_facts():
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0]
    mars_facts_df.columns = ['Description', 'Mars']
    mars_facts_df
    
    mars_facts_html = mars_facts_df.to_html(classes='table table-striped')
    
    return mars_facts_html


# In[38]:


#if you want to pull the HTML table directly from the page

html = browser.html
facts_soup = BeautifulSoup(html, 'html.parser')

facts_soup.find(id = 'tablepress-p-mars')



# # Mars Hemispheres



# URL of NASA MARS NEWS to be scraped
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# Retrieve page with the requests module
response = requests.get(url)
response.text


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')


# Examine the results, then determine element that contains sought info
print(soup.prettify())



# results are returned as an iterable list
results = soup.find_all('div', class_="item")
len(results)


#check if results contain what we need
print(results[0].prettify())


# Loop through returned results
img_url = []
title = []
hemisphere_image_urls = []
for result in results:
    # Error handling
    try:
        # Identify and return news titles
        h3 = result.find('h3').text
        # Identify and return news teasers 
        img = result.find('img', class_='thumb')['src']
        

        # Print results only if title, and url are available
        if (h3 and img):
            data = {
                "title": h3,
                "image": img
            }
            
            print(data)
            hemisphere_image_urls.append({"title": h3, "image": img})
            
    except Exception as e:
        print(e)




# In[47]:
# # Insert into Mongo DB

def scrape_all():
    
    #populated variables from the functions
    headline_date,news_title, news_p  = mars_news()
    featured_img_url = featured_image()
    mars_facts_html = mars_facts()

    #assemble the document to insert into the database
    nasa_document = {
        'news_date': headline_date,
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_img_url': featured_img_url,
        'mars_facts_html': mars_facts_html
    }

    #consider closing browser here
    browser.quit()
    
    return nasa_document


# In[50]:
#Run Script

if __name__ == '__main__':
    scrape_all()



# In[ ]:





# In[ ]:




