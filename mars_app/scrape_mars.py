from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from io import StringIO
from flask import Markup
import requests
import os
from pprint import pprint

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    # [NASA Mars News Site] -- Latest News Title and Paragraph Text
    try:
        url = 'https://mars.nasa.gov/news'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        news_div = soup.find('div', class_='content_title')
        news_title = news_div.find('a').get_text()
        news_p = soup.find('div', class_='article_teaser_body').get_text()
        news_link = url + news_div.find('a')['href']
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/news'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        news_div = soup.find('div', class_='content_title')
        news_title = news_div.find('a').get_text()
        news_p = soup.find('div', class_='article_teaser_body').get_text()
        news_link = url + news_div.find('a')['href']
    # JPL -- Featured Space Image 
    try:
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        url = url[:24]
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_btn = soup.find('a', class_='button fancybox')
        div_url = img_btn['data-fancybox-href']
        img_title = soup.find('h1', class_='media_feature_title').get_text()
    except:
        url = 'http://web.archive.org/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        url = url[:47]
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_btn = soup.find('a', class_='button fancybox')
        div_url = img_btn['data-fancybox-href']
        img_title = soup.find('h1', class_='media_feature_title').get_text()
    featured_image_url = url + div_url
    # Weather twitter account -- Latest Mars Weather tweet
    try:
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        tweet_div = soup.find('div', class_='tweet')
        mars_weather = tweet_div.find('p').get_text()
    except:
        url = 'http://web.archive.org/https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        tweet_div = soup.find('div', class_='tweet')
        mars_weather = tweet_div.find('p').get_text()
    # USGS Astrogeology site -- high res images of each of Mars' hemispheres
    try:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        time.sleep(1)
        url = url[:29]
        html = browser.html
        soup = bs(html, 'html.parser')
        page_div = soup.find('div', class_='results')
        page_divs = page_div.find_all('div', class_='item')
    except:
        url = 'http://web.archive.org/web/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        time.sleep(1)
        url = url[:22]
        html = browser.html
        soup = bs(html, 'html.parser')
        page_div = soup.find('div', class_='results')
        page_divs = page_div.find_all('div', class_='item')
    page_links = []
    for page_link in page_divs:
        html = browser.html
        soup = bs(html, 'html.parser')
        page_link = page_link.find('a')['href']
        page_link = url + page_link
        page_links.append(page_link)
    img_links = []
    titles = []
    for page in page_links:
        browser.visit(page)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_link = soup.find('div', class_='downloads').find('a')['href']
        title = soup.find('div', class_='content').find('h2').get_text()
        img_links.append(img_link)
        titles.append(title)
    title_link = list(zip(titles, img_links))
    hemisphere_image_urls = [{'title': title, 'img_url': link} for title, link in title_link]
    # Mars Rover Mission Data 
    try:
        url = 'https://mars.nasa.gov/mer/mission/status.html'
        browser.visit(url)
        url = url[:34]
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        content = soup.find(attrs={"name":"opportunity"} )
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/mer/mission/status.html'
        browser.visit(url)
        url = url[:57]
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        content = soup.find(attrs={"name":"opportunity"} )
    content_list = []
    for sibling in content.next_siblings:
        content_list.append(sibling)
    spirit_content = Markup(content_list[3])
    opportunity_content = Markup(content_list[15])
    
    # Mars Curiosity Rover
    try:
        url = 'https://mars.nasa.gov/msl/mission/overview/'
        browser.visit(url)
        url = url[:25]
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        curio_title = soup.find('h1').get_text()
        curio_content = soup.find('div', class_='columntype_main').find('br')
        curio_fact_title = soup.find('div', class_='columntype_sidebar').find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('b').get_text()
        curio_fact_link = soup.find('div', class_='columntype_sidebar').find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('a')['href']
        curio_fact_link = url + curio_fact_link[5:]
        curio_nav_list = [x for x in soup.find('div', id='MidNavContainer').find_all('a')]
        curio_mission_update = curio_nav_list[-1]['href']
        curio_mission_update = url + curio_mission_update[5:]
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/msl/mission/overview/'
        browser.visit(url)
        url = url[:48]
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        curio_title = soup.find('h1').get_text()
        curio_content = soup.find('div', class_='columntype_main').find('br')
        curio_fact_title = soup.find('div', class_='columntype_sidebar').find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('b')
        curio_fact_link = soup.find('div', class_='columntype_sidebar').find('p').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('a')['href']
        curio_fact_link = url + curio_fact_link[5:]
        curio_nav_list = [x for x in soup.find('div', id='MidNavContainer').find_all('a')]
        curio_mission_update = curio_nav_list[-1]['href']
        curio_mission_update = url + curio_mission_update[5:]

    sibling_list = []
    for sibling in curio_content.next_siblings:
        sibling_list.append(sibling)
    curio_text_1 = sibling_list[0]
    curio_text_2 = sibling_list[3]
    curio_subtitle_1 = sibling_list[7].get_text()
    curio_text_3 = sibling_list[10]
    curio_subtitle_2 = sibling_list[14].get_text()
    curio_text_4 = sibling_list[17]
    sci_stud = sibling_list[18].get_text()
    sci_stud_link = url + sibling_list[18]['href']
    curio_text_5 = sibling_list[19]
    curio_subtitle_3 = sibling_list[23].get_text()
    curio_text_6 = sibling_list[26]
    innov_text = sibling_list[27].get_text()
    innov_link = url + sibling_list[27]['href']
    curio_text_7 = sibling_list[28]
    curio_subtitle_4 = sibling_list[32].get_text()
    curio_text_8 = sibling_list[35]
    bullet_subtitle = sibling_list[39].get_text()
    bullet_list = [bullet.get_text() for bullet in sibling_list[43].find_all('li')]
    commented_info = sibling_list[45]
    tech_info = sibling_list[49].find('a').get_text()
    tech_info_link = sibling_list[49].find('a')['href']
    try:
        url = 'https://mars.nasa.gov/msl/mission/mars-rover-curiosity-mission-updates/'
        browser.visit(url)
        html = browser.html
        time.sleep(1)
        soup = bs(html, 'html.parser')
        curio_update_text = soup.find('h2').get_text()
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/msl/mission/mars-rover-curiosity-mission-updates/'
        browser.visit(url)
        html = browser.html
        time.sleep(1)
        soup = bs(html, 'html.parser')
        curio_update_text = soup.find('h2').get_text()

    # Mars Rover traverse maps
    # Spirit Rover Traverse Map
    try:
        url = 'https://mars.nasa.gov/mer/mission/tm-spirit/index.html'
        browser.visit(url)
        url = url[:44]
        html = browser.html
        soup = bs(html, 'html.parser')
        all_links = soup.find_all('a')
        spirit_map = all_links[18]['href']
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/mer/mission/tm-spirit/index.html'
        browser.visit(url)
        url = url[:67]
        html = browser.html
        soup = bs(html, 'html.parser')
        all_links = soup.find_all('a')
        spirit_map = all_links[18]['href']
    sp_map_link = url + spirit_map
    # Opportunity Rover Traverse Map
    try:
        url = 'https://mars.nasa.gov/mer/mission/tm-opportunity/index.html'
        browser.visit(url)
        url = url[:49]
        html = browser.html
        soup = bs(html, 'html.parser')
        all_links = soup.find_all('a')
        opportunity_map = all_links[32]['href']
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/mer/mission/tm-opportunity/index.html'
        browser.visit(url)
        url = url[:72]
        html = browser.html
        soup = bs(html, 'html.parser')
        all_links = soup.find_all('a')
        opportunity_map = all_links[32]['href']
    opp_map_link = url + opportunity_map
    # Curiosity Rover Traverse Map
    try:
        url = 'https://mars.nasa.gov/msl/mission/whereistherovernow/?ImageID=9752'
        browser.visit(url)
        url = url[:25]
        html = browser.html
        soup = bs(html, 'html.parser')
        curio_map_title = soup.find('h1').get_text()
        curio_map_link = url + soup.find('div', id="twocolumnwrap").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('img')['src']
        curio_map_alt = soup.find('div', id="twocolumnwrap").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('img')['alt']
        curio_map_title2 = soup.find('a', class_="fancybox").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        curio_map_text = soup.find('div', id="twocolumnwrap").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('tr').next_sibling.next_sibling.next_sibling.next_sibling.find('td').get_text()
        curio_map_text = curio_map_text[1:-50]
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/msl/mission/whereistherovernow/?ImageID=9752'
        browser.visit(url)
        url = url[:48]
        html = browser.html
        soup = bs(html, 'html.parser')
        curio_map_title = soup.find('h1').get_text()
        curio_map_link = url + soup.find('div', id="twocolumnwrap").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('img')['src']
        curio_map_alt = soup.find('div', id="twocolumnwrap").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('img')['alt']
        curio_map_title2 = soup.find('a', class_="fancybox").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        curio_map_text = soup.find('div', id="twocolumnwrap").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find('tr').next_sibling.next_sibling.next_sibling.next_sibling.find('td').get_text()
        curio_map_text = curio_map_text[1:-50]
    # Mars Facts Table    
    try:
        url = 'http://space-facts.com/mars'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        key_list = []
        value_list = []
        soup = bs(html, 'html.parser')
        for x in range(1,10):
            class_ = f"row-{x}"
            table = soup.find('table')
            key = table.find('tr', class_=class_).find('td').find('strong').get_text()
            value = table.find('tr', class_=class_).find('td', class_='column-2').get_text()
            key_list.append(key)
            value_list.append(value)
    except:
        url = 'http://web.archive.org/http://space-facts.com/mars'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        key_list = []
        value_list = []
        soup = bs(html, 'html.parser')
        for x in range(1,10):
            class_ = f"row-{x}"
            table = soup.find('table')
            key = table.find('tr', class_=class_).find('td').find('strong').get_text()
            value = table.find('tr', class_=class_).find('td', class_='column-2').get_text()
            key_list.append(key)
            value_list.append(value)
    dict_list = [{k:v} for k,v in zip(key_list, value_list)]


    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "news_link": news_link,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls": hemisphere_image_urls,
        "sp_map_link": sp_map_link,
        "opp_map_link": opp_map_link,
        "spirit_content": spirit_content,
        "opportunity_content": opportunity_content,
        "dict_list": dict_list,
        "img_title": img_title,
        "curio_title": curio_title,
        "curio_update_text": curio_update_text,
        "curio_text_1": curio_text_1,
        "curio_text_2": curio_text_2,
        "curio_subtitle_1": curio_subtitle_1,
        "curio_text_3": curio_text_3,
        "curio_subtitle_2": curio_subtitle_2,
        "curio_text_4": curio_text_4,
        "sci_stud": sci_stud,
        "sci_stud_link": sci_stud_link,
        "curio_text_5": curio_text_5,
        "curio_subtitle_3": curio_subtitle_3,
        "curio_text_6": curio_text_6,
        "innov_text": innov_text,
        "innov_link": innov_link,
        "curio_text_7": curio_text_7,
        "curio_subtitle_4": curio_subtitle_4,
        "curio_text_8": curio_text_8,
        "bullet_subtitle": bullet_subtitle,
        "bullet_list": bullet_list,
        "commented_info": commented_info,
        "tech_info": tech_info,
        "tech_info_link": tech_info_link,
        "curio_fact_title": curio_fact_title,
        "curio_fact_link": curio_fact_link, 
        "curio_mission_update": curio_mission_update,
        "curio_map_title": curio_map_title, 
        "curio_map_link": curio_map_link,
        "curio_map_alt": curio_map_alt, 
        "curio_map_title2": curio_map_title2,
        "curio_map_text": curio_map_text, 
    }
    browser.quit()
    pprint(mars_data)

    return mars_data
    
if __name__ == "__main__":
    scrape_info()

# why don't we write to database after scrape maybe if name==main..?