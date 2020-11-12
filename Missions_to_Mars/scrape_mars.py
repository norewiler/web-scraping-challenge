#Import Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# Global Variable to hold all info scraped
info_dict = {}

def initialize_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    # TODO: make headless TRUE once done debugging
    return Browser('chrome', **executable_path, headless=False)


def scrape_NASA_Mars_News():
    browser = initialize_browser()
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    top_article_sect = soup.find("li", class_="slide")
    news_title = top_article_sect.find("div", class_="content_title").find("a").text
    info_dict["news_title"] = news_title
    news_p = top_article_sect.find("div", class_="article_teaser_body").text
    info_dict["news_p"] = news_p

    browser.quit()

def scrape_JPL_images():
    browser = initialize_browser()
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    base_url = "https://www.jpl.nasa.gov"
    featured_image_url_end = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = base_url + featured_image_url_end
    info_dict["featured_image_url"] = featured_image_url

    browser.quit()


def scrape_Mars_Facts():
    facts_url = "https://space-facts.com/mars/"
    facts_tables = pd.read_html(facts_url)

    facts_df = facts_tables[0]
    facts_df.columns = ['Description','Mars']
    facts_df.set_index('Description', inplace=True)

    # facts_df.to_html("facts_table.html")
    facts_html = facts_df.to_html()
    info_dict["facts"] = facts_html


def scrape_Mars_Hemispheres():
    browser = initialize_browser()
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemi_descs = soup.find_all("div", class_="description")
    base_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []
    for desc in hemi_descs:
        hemi_dict = {}
        title = desc.find("h3").text
        browser.click_link_by_partial_text(title)
        soup = BeautifulSoup(browser.html)
        img_path = soup.find("img", class_="wide-image")["src"]
        hemi_dict["title"] = title
        hemi_dict["img_url"] = base_url + img_path
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

    info_dict["hemisphere_image_urls"] = hemisphere_image_urls
    browser.quit()

def scrape():
    scrape_NASA_Mars_News()
    scrape_JPL_images()
    scrape_Mars_Facts()
    scrape_Mars_Hemispheres()
    return info_dict