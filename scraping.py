#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
   
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_images": hemisphere_images(browser)        
    }

    #stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    #scrape Red Planet Science featured article
    #Visit the mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    #Optional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object 
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #error handling
    try:
        #define parent element
        slide_elem = news_soup.select_one('div.list_text')
        #Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_paragraph

def featured_image(browser):

    #scrape JPL Space Images Featured Images
    #Visit the url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #error handling
    try:
        #find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None    

    #Use the base url to create absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    #scrape Mars Facts
    #error handling
    try:    
        #convert html table to Dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #convert DataFrame to html, add bootstrap
    return df.to_html()

def hemisphere_images(browser):
    #Scrape Mars hemispheres images
    #visit the url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #Create list to hold images and titles
    hemisphere_image_urls = []

    #error handling
    try:
        #loop through hemispheres
        for hemis in range(4):
            #create empty dictionary
            hemispheres = {}
            #click hemisphere title link
            browser.find_by_tag('h3')[hemis].click()
            #find full image url
            element = browser.links.find_by_text('Sample')
            img_url = element['href']
            #find title 
            title = browser.find_by_tag('h2').text
            #save title and url to dictionary and append to list
            hemispheres['img_url'] = img_url
            hemispheres['title'] = title
            hemisphere_image_urls.append(hemispheres)
            #set browser back to initial url for next loop
            browser.back()
    except AttributeError:
        return None 
    
    return hemisphere_image_urls

if __name__ == '__main__':
    #if running as script, print scraped data
    print(scrape_all())