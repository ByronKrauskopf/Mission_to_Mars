
#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


### Featured Article

#Visit the mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)
#Optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)

#HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

#find new article title
slide_elem.find('div', class_='content_title')

#Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

### Featured Images

#Visit the url
url = 'https://spaceimages-mars.com'
browser.visit(url)

#Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

#Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#Use the base url to create absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

### Mars Facts

#convert html table to Dataframe
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

#convert DataFrame back to html
df.to_html()

# Challenge Delivery 1  code

### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

