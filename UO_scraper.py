"""
Web Scraper for University of Oregon Club Free Food
"""

from bs4 import BeautifulSoup
import mysql.connector
import csv
import pandas as pd
import re

from selenium import webdriver 
#from selenium.webdriver import Chrome 
#from selenium.webdriver.common.by import By 

import re

CSV_file = "EngageData.csv"

def extract_date_time(string):
    # Define regular expressions to match date, start time, and end time
    date_pattern = r'(\w+\s+\d{1,2}\s+\d{4})'  
    time_pattern = r'(\d{1,2}:\d{2}\s+[AP]M)'  
    
    # Find all matches of date, start time, and end time
    dates = re.findall(date_pattern, string)
    times = re.findall(time_pattern, string)
    
    # Combine date and time information into a list of tuples
    extracted_info = []
    extracted_info.append(dates[0])
    for vals in times:
        extracted_info.append(vals)
    
    return extracted_info

def remove_location_info(string):
    
    # Use re.sub() to remove the matched pattern
    string = re.sub(r'\s*View\s+Map$', '', string)

    # Remove "Location"
    string = re.sub(r'Location\s*', '', string)
    
    # Remove information after the state code (e.g., "OR")
    string = re.sub(r',\s*[A-Z]{2}.*', '', string)

    string = re.sub(r'(\d+)\s+(st|nd|rd|th)\b', r'\1\2', string)

    split_string = re.findall(r'[A-Za-z]+|\d+', string)
    
    # Join the split components with a space
    cleaned_string = ' '.join(split_string)
    
    return cleaned_string.strip() 

def get_organization_name(string):

    string = string.split('/')[3]
    words = string.split('-')
    capitalized = [word.capitalize() for word in words]
    string = ' '.join(capitalized)

    return string

def remove_desc_details(string):
    cleaned_text = re.sub(r'\xa0|\n', ' ', string)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()


def engage_URL_web_scraper():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode

    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    new_data = []
    original_link = "https://uoregon.campuslabs.com/engage/events?categories=16973"
    
    driver.get(original_link)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    
    list_of_data = soup.find_all('a', href=lambda href: href and '/engage/event/' in href)

    for link in list_of_data:
        new_data.append(link.get('href'))

    return new_data


def engage_site_scraper(list):
    for link in list:
        CSV_data = []
        new_link = "https://uoregon.campuslabs.com"+link
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Enable headless mode

        # Initialize the WebDriver with Chrome options
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(new_link)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        raw_title = soup.find_all('title')
        if raw_title:
            title = (raw_title[0].text.split(' - ')[0])
            CSV_data.append(title)

        else:
            pass
        
        event_description = soup.find('meta', property="og:description")

        list_of_event_data = soup.find_all('strong')

        raw_organizer = soup.find_all('a', href=lambda href: href and '/engage/organization/' in href)

        if list_of_event_data:
            parent_div = list_of_event_data[0].find_parent('div')
            raw_time_text = parent_div.text
            time_text = extract_date_time(raw_time_text)

            parent_div = list_of_event_data[1].find_parent('div')
            raw_location_text = parent_div.text
            location_text = remove_location_info(raw_location_text)

            #time_text.append(location_text)
            CSV_data.append(time_text[0])
            CSV_data.append(time_text[1])
            CSV_data.append(time_text[2])
            CSV_data.append(location_text)

        else:
            pass
    
        if event_description:
            description = BeautifulSoup(event_description['content'], 'html.parser').get_text()
            CSV_data.append(remove_desc_details(description))

        else:
            pass

        if raw_organizer:
            org_list = []
            for organization in raw_organizer:
                name = organization.find('h3')
                name = name.text.strip()
                org_list.append(name)
            if len(org_list) == 1:
                CSV_data.append(org_list[0])
            else:
                CSV_data.append(org_list)
        else:
            pass
        CSV_data_inputter(CSV_data)
        print(CSV_data)

def CSV_file_creator():
    header = ['Event Title', 'Date', 'Start Time', 'End Time', 'Location', 'Description', 'Organizer(s)']
    with open(CSV_file, 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        return
    
def CSV_data_inputter(data):
    with open(CSV_file, 'a', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(data)
        return

    
if __name__ == '__main__':
    URL_list = engage_URL_web_scraper()
    #URL_list = ['/engage/event/9833502']
    CSV_file_creator()
    #engage_URL_web_scraper()
    engage_site_scraper(URL_list)
