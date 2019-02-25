from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from io import StringIO
from flask import Markup
import os
import requests

# Mars Facts webpage -- Table of facts including Diameter, Mass, etc.
# Scraped in a different file in order to be able to render the markup string correctly in flask
# ? is there a more secure workaround ?

def scrape_table():
    executable_path = {'executable_path': '/Users/soria/Anaconda3/Scripts/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    try:
        url = 'http://space-facts.com/mars'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        key_list = []
        value_list = []
        for x in range(1,10):
            soup = bs(html, 'html.parser')
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
        for x in range(1,10):
            soup = bs(html, 'html.parser')
            class_ = f"row-{x}"
            table = soup.find('table')
            key = table.find('tr', class_=class_).find('td').find('strong').get_text()
            value = table.find('tr', class_=class_).find('td', class_='column-2').get_text()
            key_list.append(key)
            value_list.append(value)
    facts_dict = {'key': key_list, 'value': value_list}
    facts_df = pd.DataFrame(data=facts_dict)
    output = StringIO()
    facts_df.to_html(output, index=False)
    table_string = Markup(output.getvalue())
    browser.quit()
    return table_string

if __name__ == "__main__":
    scrape_table()
