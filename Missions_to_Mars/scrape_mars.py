#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd


# # In[2]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


db = client.mars_db
collection = db.collection


# # In[4]:

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()



    # URL of page to be scraped
    mars_url = 'https://mars.nasa.gov/news/'

    browser.visit(mars_url)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')


    # In[6]:


    # get the first <li> item under <ul> list of headlines to get latest news title and paragraph text
    first_li_item = soup.find('li', class_='slide')

    # save news title under the <div> tag with a class of 'content_title'
    news_title = first_li_item.find('div', class_='content_title').text

    # save paragraph text under the <div> tag with a class of 'article_teaser_body'
    news_p = first_li_item.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)


    # In[8]:


    # URL of page to be scraped
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(url)

    # Find and click the full image button
    browser.click_link_by_partial_text('FULL IMAGE')

    browser.is_element_present_by_text('more info', wait_time=1)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    img_soup = BeautifulSoup(html, 'html.parser')


    # In[9]:


    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    print(img_url_rel)


    # In[10]:


    img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + img_url_rel
    img_url


    # In[ ]:





    # In[11]:


    # URL of page to be scraped
    fact_url = 'https://space-facts.com/mars/'

    table = pd.read_html(fact_url)
    table


    # In[12]:


    facts_df = table[0]
    facts_df.columns =['Description', 'Value']
    facts_df


    # In[13]:


    mars_facts = facts_df.to_html('marsfacts.html', index=False)


    # In[ ]:





    # In[14]:


    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[15]:


    browser.visit(hem_url)


    # In[16]:


    # create HTML object
    html = browser.html
    # print(html)


    # In[17]:


    # parse HTML with BeautifulSoup
    hem_soup = BeautifulSoup(html, 'html.parser')


    # In[20]:


    # get all the parent div tags for each hemisphere
    hem_divs = hem_soup.find_all('div', class_="item")

    # create empty list to store the python dictionary
    hemisphere_image_urls = []

    # loop through each div item to get hemisphere data
    for hem in range(len(hem_divs)):

        # use splinter to click on each hemisphere link to get image data
        hem_link = browser.find_by_css("a.product-item h3")
        hem_link[hem].click()

        # create beautiful soup object with the image detail page html
        img_detail_html = browser.html
        img_detail_soup = BeautifulSoup(img_detail_html, 'html.parser')

        # create the base url for link to full size image
        base_url = 'https://astrogeology.usgs.gov'

        # get gull size image url and save to a variable
        hem_url = img_detail_soup.find('img', class_="wide-image")['src']

        # get whole featured image url
        feat_img_url = base_url + hem_url

        # get image title using the title class and save to variable
        feat_img_title = browser.find_by_css('.title').text

        # append values to a dictionary
        hemisphere_image_urls.append({"title": feat_img_title,
                            "img_url": feat_img_url})

        # go back to main page
        browser.back()

    hemisphere_image_urls

    # close browser session   
    browser.quit()

    scraped_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featuredimage_url": img_url,
        "mars_fact_table": mars_facts, 
        "hemisphere_images": hemisphere_image_urls
    }
    collection.drop()
    collection.insert_one(scraped_data)

    # --- Return results ---
    return scraped_data

