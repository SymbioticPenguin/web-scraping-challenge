# Import Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape():

    ###### We are starting by scraping the NASA website for the latest news update. We are also scraping twitter for
    ###### the latest weather report on Mars.

    # NASA news URL
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Twitter URL for weather
    twitter = "https://twitter.com/marswxreport?lang=en"

    # Requesting HTML from websites
    response = requests.get(news_url)
    weather_tweet = requests.get(twitter)

    # NASA soup
    soup = BeautifulSoup(response.text,'html.parser')
    # Twitter soup
    bird_soup = BeautifulSoup(weather_tweet.text, 'html.parser')

    ###### Where the scraping of various sites happens

    # NASA website for news headline and flavor text
    titles = soup.find_all('div', class_="content_title")
    paragraphs = soup.find_all('div', class_ = "image_and_description_container")

    # Twitter for the weather update
    all_weather = bird_soup.find('div', class_ = 'js-tweet-text-container')

    ###### Finishing the scrape job of NASA and Twitter



    ###### Starting the scraping of the "Mars Facts Data table"

    # Mars facts URL
    facts = 'https://space-facts.com/mars/'

    # Reading fact table from Mars Facts URL
    fact_table = pd.read_html(facts)[0].rename(columns = {0:"Metric",1:"Value"}).set_index("Metric")

    ###### Finishing the scrape of the basic data table



    ###### Defining all the variables that will go into MongoDB later

    # Title
    news_title = titles[0].find('a').text.replace("\n","")

    # Flavor text of article
    news_p = paragraphs[0].find('div',class_ = 'rollover_description_inner').text.replace("\n","").replace("\"",'')

    ### URL for image on JPL website (Hard coded?)
    img_url = "https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA14293_ip.jpg"

    # This gives the tweet for the latest weather update. If there is a picture, the scrape trashes the pic URL
    # from the string.
    one_weather = all_weather.find('p').text.replace("\n","").replace("\"",'')

    if("pic.twitter" in one_weather):
        one_weather = one_weather[:one_weather.find("pic.twitter")]
    

    # create the dictionary with the URL to the pictures of the 4 hemispheres of Mars

    hemi_pics = [{'title':'Cerberus Hemisphere','url':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
                {'title':'Schiaparelli Hemisphere','url':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
                {'title':'Syrtis Major Hemisphere','url':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
                {'title':'Valles Marineris Hemisphere','url':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]



    ##### Final Dictionary that will be depoloyed through MONGO

    big_boy_book = {"title":news_title,
                   "news":news_p,
                   'main_img':img_url,
                   'weather':one_weather,
                   'basic_data':fact_table,
                   'hemi_pics':hemi_pics}

    return(big_boy_book)

