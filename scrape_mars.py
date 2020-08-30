from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    mars_data={}
    mars_news = MarsNews()
    mars_data["mars_title"] = mars_news[0]
    mars_data["mars_p"] = mars_news[1]
    mars_data["mars_image"] = MarsImage()
    mars_data["mars_fact"] = MarsFact()
    mars_data["mars_hemisphere"] = MarsHem()
    return mars_data

def MarsNews():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    article = soup.find('div', class_='list_text')
    mars_title = article.find('div', class_= 'content_title').text
    mars_p = article.find('div', class_ = 'article_teaser_body').text
    mars_news = [mars_title, mars_p]
    browser.quit()
    return mars_news
    

def MarsImage():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    relative_image_path = soup.find('img', class_='thumb')["src"]
    mars_image = "https://www.jpl.nasa.gov" + relative_image_path
    browser.quit()
    return mars_image
    

def MarsFact():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    fact_data = pd.read_html(url)
    fact_data = pd.DataFrame(fact_data[0])
    fact_data.columns=["Description","Mars"]
    fact_data.set_index("Description", inplace=True)
    # fact_data.find("tbody")
    mars_fact = fact_data.to_html(header = True, index = True)
    browser.quit()
    return mars_fact

def MarsHem():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        img_title = hemisphere.find("h3").text
        img_title = img_title.replace("Enhanced", "")
        url_end = hemisphere.find("a")["href"]
        product_url = "https://astrogeology.usgs.gov/" + url_end 
        browser.visit(product_url)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        img_url = downloads.find("a")["href"]
        mars_hemisphere.append({"img_title": img_title, "img_url": img_url})
        
    browser.quit()
    return mars_hemisphere
