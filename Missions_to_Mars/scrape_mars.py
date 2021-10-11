import os
import time
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    
    # Create dictionary
    mars_dictionary = {}
    
    # NASA Mars News
    browser.visit( "https://redplanetscience.com/")
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    
    
    # JPL Mars Space Images
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html,'html.parser')
    img_slug = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = (f'{img_url}{img_slug}')
    featured_image_url
    
    # Mars Facts
    facts_url = "https://galaxyfacts-mars.com/"
    facts_table = pd.read_html(facts_url, attrs = {'class': 'table-striped'})
    facts_df = facts_table[0]
    facts_html = facts_df.to_html()

    #Mars Hemispheres
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    imgs_url = 'https://marshemispheres.com/'
    browser.visit(imgs_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')

    pages = soup.find_all('div',class_='item')
    urls = []

    for page in pages:
        url = f"{imgs_url}{page.a['href']}"
        urls.append(url)
        
        
    hemisphere_image_urls = []
    title_img = {}
    for url in urls:
        html = browser.html
        soup = bs(html, 'html.parser')
        browser.visit(url)
        time.sleep(2)
        title_div = soup.findAll('div',attrs={"class":"cover"})
        for x in title_div:
            title = x.find('h2').text
            title_img['title'] = title
        img = browser.links.find_by_partial_href('full.jpg')
        img = img['href']
        title_img = {}
        title_img['img_url'] = img
        hemisphere_image_urls.append(title_img)
        
        
    mars_dictionary = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "fact_table": str(facts_html),
    "hemisphere_images": hemisphere_image_urls
    }
    
    return mars_dictionary

    browser.quit()