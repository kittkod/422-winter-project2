"""
Web Scraper for University of Oregon Club Free Food
"""

from bs4 import BeautifulSoup
import csv
import pandas as pd
import re

from selenium import webdriver 

import re

CSV_file = "Free_Food_Database.csv"

################################################################
## Function block for scraping "Engage Free Food Club Events" ##
################################################################


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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode

    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    for link in list:
        CSV_data = []
        new_link = "https://uoregon.campuslabs.com"+link

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
            CSV_data.append("N/A")
        CSV_data_inputter(CSV_data)
        print(CSV_data)

################################################################
## Function block for scraping Events Calendar for Free Food ##
################################################################

def events_calendar_time_fixup(date_and_time):

    date_and_time = date_and_time.replace("\n", "").replace(",", "")
    date_and_time = date_and_time.split()

    if len(date_and_time) == 7:
        date = date_and_time[1]+" "+date_and_time[2]+" "+date_and_time[0]
        start_time = date_and_time[4]
        end_time = date_and_time[6]
        return date, start_time, end_time
    if len(date_and_time) == 5:
        date = date_and_time[1]+" "+date_and_time[2]+" "+date_and_time[0]
        start_time = date_and_time[4]
        end_time = "N/A"
        return date, start_time, end_time
    if len(date_and_time) == 3:
        date=date_and_time[1]+" "+date_and_time[2]+" "+date_and_time[0]
        start_time = "N/A"
        end_time = "N/A"
        return date, start_time, end_time
    else:
        date = "N/A"
        start_time = "N/A"
        end_time = "N/A"
        return date, start_time, end_time

def event_calendar_fixup(string):

    cleaned_text = re.sub(r'\xa0|\n', ' ', string)
    cleaned_text = re.sub(r'\s+', ' ', string)
    return cleaned_text.strip()

def event_calendar_URL_fixup(link):
    
    # Split the link by '/'
    parts = link.split('/')
    URL = parts[-1]
    return URL


   
def events_calendar_URL_scraper():

    starting_link = 'https://calendar.uoregon.edu/search/events?event_types[]=15630'
    link_list = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode

    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(starting_link)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    
    list_of_data = soup.find_all('div', class_= "item event_item vevent")

    for link in list_of_data: 
        new_link = link.find('a', href=lambda href: href and '/event/' in href)
        new_link = new_link.get('href')
        new_link = event_calendar_URL_fixup(new_link)
        link_list.append(new_link)
    event_calender_site_scraper(link_list)
    return

    #return new_data

def event_calender_site_scraper(list_of_links):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    for link in list_of_links:

        CSV_data = []
        new_link = "https://calendar.uoregon.edu/event/"+link

        driver.get(new_link)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        total_info = soup.find('div', class_='box_content vevent grid_8')
        event_name = total_info.find('h1', class_='summary')
        event_name = event_calendar_fixup(event_name.text)
        CSV_data.append(event_name)

        date_and_time = total_info.find('p', class_='dateright')
        date, start_time, end_time = events_calendar_time_fixup(date_and_time.text)

        CSV_data.append(date)
        CSV_data.append(start_time)
        CSV_data.append(end_time)

        event_location = total_info.find('p', class_='location')
        event_location = event_calendar_fixup(event_location.text)
        if event_location:
            CSV_data.append(event_location) 
        else:
            CSV_data.append("N/A")

        event_description = total_info.find('div', class_='description')

        event_description = event_calendar_fixup(event_description.text)

        CSV_data.append(event_description)

        event_organizer = soup.find('dd', class_='filter-departments')

        event_organizer = event_calendar_fixup(event_organizer.text)

        CSV_data.append(event_organizer)

        CSV_data_inputter(CSV_data)
        
######################################
## CSV File Creation Function Block ##
######################################
        
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

    #create CSV file
    CSV_file_creator()

    #scrape engage
    URL_list = engage_URL_web_scraper()
    engage_URL_web_scraper()
    engage_site_scraper(URL_list)

    #scrape events calender
    events_calendar_URL_scraper()

