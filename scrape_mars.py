
# # Mision To Mars

import requests
import black
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo

def read_scrape():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    
    # Declare the database
    db = client.mars_db

    # Declare the collection
    collection = db.mars_data

    return db.mars_data.find({})
    

def save_scrape(scrape):
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    
    # Declare the database
    db = client.mars_db
    
    # Declare the collection
    collection = db.mars_data

    # Drop collection if exists
    if collection.count() > 0:
        collection.drop()

    collection.insert_one(scrape)


def scrape():
    # # NASA Mars News
    # Define NASA News url
    NASA_URL = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    driver = webdriver.Firefox()
    driver.get(NASA_URL)
    driver.implicitly_wait(10)
    nasa_html = driver.page_source

    # Loading page
    nasa_soup = BeautifulSoup(nasa_html, "lxml")

    # Extract News Title
    news_title = [
        tag.text
        for tag in [
            li for ul in nasa_soup for li in ul.findAll("div", class_="content_title")[0]
        ]
    ]

    # Extract News Paragraph
    news_p = [
        tag
        for tag in [
            li for ul in nasa_soup for li in ul.findAll("div", class_="article_teaser_body")[0]
        ]
    ]

    # Extract News Image
    driver.find_elements_by_class_name("list_image")[0].click()
    image_url = driver.find_element_by_id("main_image").get_attribute("src")

    driver.close()

    # Create the result list
    nasa_result = []
    nasa_result.append(news_title)
    nasa_result.append(news_p)
    nasa_result.append(image_url)


    # # Twitter Mars Weather

    # Define Twitter Mars Report url
    MARS_WEATHER_URL = "https://twitter.com/marswxreport?lang=en"

    # Loading page
    response = requests.get(MARS_WEATHER_URL)
    mars_weather_soup = BeautifulSoup(response.text, "html.parser")

    # Finding last tweet
    mars_weather_soup.find("a", {"class": "twitter-timeline-link u-hidden"}).decompose()
    tweet = mars_weather_soup.find("div", class_="js-tweet-text-container").text
    tweet


    # # Mars Space Facts

    # Define Space Facts url
    MARS_FACTS_URL = "https://space-facts.com/mars/"

    # Loading page
    response = requests.get(MARS_FACTS_URL)
    mars_facts_soup = BeautifulSoup(response.text, "html.parser")

    # Getting the facts about Mars
    facts = f'{mars_facts_soup.find("table", class_="tablepress tablepress-id-p-mars")}'
    facts


    # # Mars Hemispheres


    # Define Astrogeology url
    MARS_HEM_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    driver = webdriver.Firefox()
    driver.get(MARS_HEM_URL)
    driver.implicitly_wait(10)

    # Create and empty list
    hem_list = []

    # Find all the links
    links = driver.find_elements_by_class_name("thumb")

    # Loop through the links, click on each and extract title and image url into a list of dicts
    for l in range(len(links)):
        driver.find_elements_by_class_name("thumb")[l].click()
        
        title = driver.find_element_by_class_name("title")
        image_url = driver.find_element_by_link_text("Sample")

        hem_list.append({"title": title.text, "img_url": image_url.get_attribute("href")})
        driver.back()

    driver.close()

    scrape_dict = {"nr": nasa_result, "tw": tweet, "fc": facts, "hm":hem_list}

    # Review contents
    # print(nasa_result)
    # print("***")
    # print(tweet)
    # print("***")
    # print(facts)
    # print("***")
    # print(hem_list)
    save_scrape(scrape_dict)
    return ""




