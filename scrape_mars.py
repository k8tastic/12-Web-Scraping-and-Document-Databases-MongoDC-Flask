# Mission to Mars

# Dependencies

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

from pymongo import errors as pymerr
from pymongo import MongoClient
import sys

# Create Browser object
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)

def scrape_mars():
    ### Scrape the NASA Mars news site for latest article

    # Create BeautifulSoup object; parse with 'html.parser'
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="rollover_description_inner").text

    print('The Latest News!')
    print (news_title, news_p)
 
    ###############################################################################
    ### JPL Mars Featured Image Scrape

    #Create Browser object
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
    url_2 = 'https://www.jpl.nasa.gov'
    search = '/spaceimages/?search=&category=Mars'
    browser_url = f"{url_2}{search}"
    browser.visit(browser_url)
    soup_2 = bs(browser.html, 'html.parser')

    # Make sure to find the image url to the full size `.jpg` image.
    # Make sure to save a complete url string for this image.

    # Find string with url
    image = soup_2.find('article', class_='carousel_item')['style']

    # Clean string
    image_url_1 = image[23:]
    image_url = image_url_1[:-3]

    # Create new url
    featured_image_url = f"{url_2}{image_url}"
    print(f"Follow link to the full size image: {featured_image_url}")

    ###############################################################################
    ### Mars Weather Scrape

    # Visit the Mars Weather twitter account
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    soup_3 = bs(browser.html, 'html.parser')

    # Scrape the latest Mars weather tweet from the page. 
    # Loop through the tweets to find weather report

    for tweet in soup_3.find_all('p', class_='tweet-text'):
        if tweet.text.startswith("Sol"):
            mars_weather_all = tweet.text
            break

    # Save the tweet text for the weather report as a variable called `mars_weather`.
    # Clean the text

    mars_weather = mars_weather_all[:-26]
    print(f"Here is the weather on Mars: {mars_weather}")

    ###############################################################################
    ### Mars Facts Scrape

    # Visit the Mars Facts webpage
    facts_url = "http://space-facts.com/mars/"

    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    table = pd.read_html(facts_url)
    mars_planet_profile_pd = table[0]

    # Use Pandas to convert the data to a HTML table string.
    mars_planet_profile_html = mars_planet_profile_pd.to_html(header=False, index=False)                  
    print(mars_planet_profile_html)   

    ###############################################################################
    ### Mars Hemispheres Scrape
    
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    base2_url = "https://astrogeology.usgs.gov"
    hemi_search = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser_hemi_url = f"{base2_url}{hemi_search}"
    browser.visit(browser_hemi_url)
    soup_5 = bs(browser.html, 'html.parser')

    # Click each of the hemisphere link in order to find the image url to the full resolution image.
    # Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.

    hemisphere_image_urls = []

    for x in soup_5.find_all('div', class_="description"):
        hemisphere_image_urls.append({'title':x.find('a').text})

    for y in hemisphere_image_urls:
        browser.visit(browser_hemi_url)
        browser.click_link_by_partial_text(y['title'])
        
        soup_6 = bs(browser.html, 'html.parser')
        hemi_url = soup_6.find('img', class_='wide-image')['src']
        y['img_url'] = f"{base2_url}{hemi_url}"

    hemisphere_image_urls

    ###############################################################################
 
    if __name__ == '__main__':
    app.run()