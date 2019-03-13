# -*- coding: utf-8 -*
import time
import json
import codecs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

fileout = 'eventbrite.json'
options = Options()
options.add_argument("start-maximized")
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

browser = webdriver.Chrome(chrome_options=options)
number_of_pages = 5

array = []

for page_no in range(1, number_of_pages+1):
    browser.get('https://www.eventbrite.com/d/vietnam--hanoi/all-events/?page=%s' % str(page_no))
    #loop through all the links and launch one by one
    links = [link.get_attribute('href') for link in browser.find_elements_by_css_selector('div.eds-show-up-md.eds-l-mar-top-4 aside.eds-media-card-content__image-container a')]

    for link in links:
        browser.get(link)
        try:
            data_element = {}
            event_name = browser.find_element_by_css_selector('div.listing-hero-body h1').text
            data_element['event_name'] = event_name
            event_start_time = browser.find_element_by_css_selector('div.event-details.hide-small div:nth-child(2) meta:nth-child(1)').get_attribute("content")
            data_element['event_start_time'] = event_start_time
            event_end_time = browser.find_element_by_css_selector('div.event-details.hide-small div:nth-child(2) meta:nth-child(2)').get_attribute("content")
            data_element['event_end_time'] = event_end_time
            location_count = len(browser.find_elements_by_css_selector('div.event-details.hide-small div:nth-child(4) p'))
            event_location = ""

            for no in range(0, location_count-1):
                event_location += browser.find_elements_by_css_selector('div.event-details.hide-small div:nth-child(4) p')[no].text + ", "
            data_element['event_location'] = event_location
            event_url = link
            data_element['event_url'] = event_url
            array.append(data_element)
        except NoSuchElementException:
            pass
    time.sleep(1)

with codecs.open(fileout,'w',encoding='utf8') as out:
    json.dump(array,out,ensure_ascii=False)
    out.close()
browser.quit()
