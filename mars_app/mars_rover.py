from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from io import StringIO
from flask import Markup
import os 
import requests

# Mars Rover Mission
# Scraped in a different file in order to be able to render the markup string correctly in flask
# ? is there a more secure workaround ?

def scrape_rover():
    executable_path = {'executable_path': '/Users/soria/Anaconda3/Scripts/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    try:
        url = 'https://mars.nasa.gov/mer/mission/status.html'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        content = soup.find(attrs={"name":"opportunity"} )
    except:
        url = 'http://web.archive.org/https://mars.nasa.gov/mer/mission/status.html'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        content = soup.find(attrs={"name":"opportunity"} )
    content_list = []
    for sibling in content.next_siblings:
        content_list.append(sibling)
    slice1 = content_list[0:8]
    slice2 = content_list[17:22]
    spirit_string = ""
    for i in slice1:
        spirit_string = spirit_string + str(i)
    spirit_string
    opportunity_string = ""
    for i in slice2:
        opportunity_string = opportunity_string + str(i)
    rover_string = Markup(spirit_string + opportunity_string)
    #print(rover_string)
    browser.quit()
    return rover_string
    

if __name__ == "__main__":
    scrape_rover()
    
