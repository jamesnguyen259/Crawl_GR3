# -*- coding: utf-8 -*
import time
import json
import codecs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

fileout = 'allevent.json'
options = Options()
options.add_argument("start-maximized")
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

browser = webdriver.Chrome(chrome_options=options)
number_of_pages = 6

array = []

for page_no in range(1, number_of_pages+1):
    browser.get('https://allevents.in/hanoi/all?page=%s' % str(page_no))
    #loop through all the links and launch one by one
    links = [link.get_attribute('href') for link in browser.find_elements_by_css_selector('div.event-body.clearfix div.left h3 a')]

    for link in links:
        browser.get(link)
        try:
            data_element = {}
            event_name = browser.find_element_by_css_selector('h1.overlay-h1').text
            data_element['event_name'] = event_name
            print event_name
            event_time_temp = browser.find_element_by_css_selector('#event-detail-fade > div.event-head.wdiv > div.pd-lr-10.span9 > ul > li:nth-child(1)').text
            event_time = event_time_temp.replace('TIME ','').replace(' Add to calendar','')
            data_element['event_time'] = event_time
            # print event_time
            event_location_temp = browser.find_element_by_css_selector('li.venue-li').text
            event_location = event_location_temp.replace('VENUE ','')
            # print event_location
            data_element['event_location'] = event_location
            event_url = link
            data_element['event_url'] = event_url
            # time.sleep()
            array.append(data_element)
        except NoSuchElementException:
            pass
        # if index == 2:
        #     break
    time.sleep(2)

with codecs.open(fileout,'w',encoding='utf8') as out:
    json.dump(array,out,ensure_ascii=False)
    out.close()
browser.quit()
