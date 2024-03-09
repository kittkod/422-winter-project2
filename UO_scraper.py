#######################################################################
# UO_scraper.py                                                       #
# created: TODO                                                       # 
# Authors: Kylie Griffiths                                            #
#                                                                     #
# Description: Web Scraper for University of Oregon Club Free Food    #                             
#                                                                     #
# Interactions:                                                       #
# -                                                              #
####################################################################### 

from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
import csv
import datetime
import json
import re
import coordinate_finder
import pandas as pd
from selenium import webdriver 

food_CSV_file = "Free_Food_Database.csv"
#CSV file to store Food data

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#to be used when parsing date strings

with open('campus_buildings.txt') as f: 
    data = f.read() 
#pull data to be read from
      
#reconstructing the data as a dictionary 
js_file = json.loads(data) 
class_dictionary = js_file

################################################################
## Function block for scraping "Engage Free Food Club Events" ##
################################################################

def extract_date_time(string):
    """Function for the Engage Free Food Club Events scraping to extract date and time
    Input: string: str -- string containing date and time
    """

    # Define regular expressions to match date, start time, and end time
    date_pattern = r'(\w+\s+\d{1,2}\s+\d{4})'  
    time_pattern = r'(\d{1,2}:\d{2}\s+[AP]M)'  
    
    # Find all matches of date, start time, and end time
    dates = re.findall(date_pattern, string)
    times = re.findall(time_pattern, string)
    
    # Combine date and time information into a list of tuples
    extracted_info = []
    extracted_info.append(dates[0]) #dates[0] has the event date

    for vals in times: #add start and end times 
        extracted_info.append(vals)
    
    #return list of date, start time, end time 
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

    split_string = ' '.join(split_string)
    
    # Join the split components with a space
    string = split_string
    
    return string.strip() 

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
    chrome_options.add_argument("--offline")
    chrome_options.add_argument("--headless")  # Enable headless mode
    proxy = "user:pass@myproxy:8080"
    chrome_options.add_argument(f"--proxy={proxy}")

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

    driver.quit()

    return new_data

def engage_site_scraper(list):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--offline")
    chrome_options.add_argument("--headless")  # Enable headless mode
    proxy = "user:pass@myproxy:8080"
    chrome_options.add_argument(f"--proxy={proxy}")

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
                org_list = " ".join(org_list)
                CSV_data.append(org_list)
        else:
            CSV_data.append("N/A")

        matched_location = None

        for words in location_text.split(" "):
            if class_dictionary.get(words.strip()) != None: 
                matched_location = class_dictionary.get(words.strip())
                break
        for location in class_dictionary.keys():
            if location in location_text:
                matched_location = location
                break
        if matched_location == None:
            new_location = coordinate_finder.address_converter(location_text)
            lat, long = coordinate_finder.lat_and_long(new_location)
            try:
                isinstance(lat, int) == True
            except:
                lat, long = [None, None]
                CSV_data.append(lat)
                CSV_data.append(long)
            else:
                CSV_data.append(lat)
                CSV_data.append(long)
        else: 
            latlong = class_dictionary.get(matched_location).split(" ")
            lat = latlong[0]
            long = latlong[1]
            CSV_data.append(lat)
            CSV_data.append(long)
        
        CSV_data.append("False")

        #add to CSV file
        CSV_data_inputter(CSV_data, food_CSV_file)

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

def event_calender_site_scraper(list_of_links):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    link_list = []

    df = pd.read_csv('Free_Food_Database.csv')
    df = pd.DataFrame(df)
    list_of_event_titles = df['Event Title'].to_list()

    for link in list_of_links:
        link_list.append("https://calendar.uoregon.edu/event/"+link)

    for links in link_list:
        CSV_data = []
        driver.get(links)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        total_info = soup.find('div', class_='box_content vevent grid_8')
        event_name = total_info.find('h1', class_='summary')
        event_name = event_calendar_fixup(event_name.text)
        if event_name not in list_of_event_titles:
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

            matched_location = None

            if event_location:
                for location in class_dictionary.keys():
                    if location in event_location:
                        matched_location = location
                        break
                if matched_location == None:
                    new_location = coordinate_finder.address_converter(event_location)
                    lat, long = coordinate_finder.lat_and_long(new_location)
                    try:
                        isinstance(lat, int) == True
                    except:
                        lat, long = ["N/A", "N/A"]
                        CSV_data.append(lat)
                        CSV_data.append(long)
                    else:
                        CSV_data.append(lat)
                        CSV_data.append(long)
                else: 
                    latlong = class_dictionary.get(matched_location).split(" ")
                    lat = latlong[0]
                    long = latlong[1]
                    CSV_data.append(lat)
                    CSV_data.append(long)
            else:
                CSV_data.append("N/A")
                CSV_data.append("N/A")
        
            CSV_data.append("False")
            
            CSV_data_inputter(CSV_data, food_CSV_file)


############################################
## Function Block for Student Life Events ##
############################################
        
def time_compare(current_date, event_date, event_start_time):

    current_year = datetime.datetime.now().year
    parsed_date = datetime.datetime.strptime(event_date, "%b %d").replace(year=current_year)
    formatted_date_str = parsed_date.strftime("%Y-%m-%d")
                    # Compare the given date with the current date
    if str(current_date) == formatted_date_str:
        edit_event_time= event_start_time.replace('a.m.', 'AM').replace('p.m.', 'PM')
        new_hour = datetime.datetime.strptime(edit_event_time, '%I:%M %p').time()
        current_hour = datetime.datetime.now().hour
        target_hour = new_hour.hour

        return current_hour, target_hour
    else:
        return None, None
                    
def student_life_scraper():
    current_date = datetime.datetime.now().date()
    food_terms = ['snack', 'snacks', 'treat', 'treats', 'refreshment', 'refreshments', 'food']

    df = pd.read_csv('Free_Food_Database.csv')
    df = pd.DataFrame(df)
    list_of_event_titles = df['Event Title'].to_list()

    raw_link = "https://studentlife.uoregon.edu/events"

    req = Request(raw_link, headers={'User-Agent': 'Mozilla/5.0'})
    #avoid error 403
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    list_of_events = soup.find("div",class_="uo__calender-default-wrapper")
    list_of_all_events = list_of_events.find_all("div", class_="event-cell active photo_default")

    for event in list_of_all_events:
        list_of_details = event.find("div", class_="event-header")
        event_title_tag = list_of_details.find("div", class_='event-title')
        event_title = event_title_tag.find('span', class_='title').text

        if event_title not in list_of_event_titles:
            #check if not in CSV file
            event_summary = []
            event_summary_list = event.find("div", class_="event-info-block").find_all("p")
            for text in event_summary_list:
                event_summary.append(text.text)
            event_summary = " ".join(event_summary).replace("Invite my friends Add to my calendar", "").strip()
            
            for item in food_terms:
                if item in event_summary:
                    CSV_list = []
                    event_date = event.find("div", "event-date").text.replace("\n", " ").strip()

                    event_start_time = event_title_tag.find('span', class_='event-time').text.strip()

                    current_hour, target_hour = time_compare(current_date, event_date, event_start_time)

                    if current_hour != None and target_hour != None and current_hour >= target_hour:
                        break
                        
                    event_location = event.find("div", class_='event-detail event-room-number').text.replace("\n", " ").strip()
                    event_location = re.sub(r'\s+', ' ', event_location)

                    matched_location = None
                    if event_location:
                        for location in class_dictionary.keys():
                            if location in event_location:
                                matched_location = location
                                break
                        if matched_location == None:
                            new_location = coordinate_finder.address_converter(event_location)
                            lat, long = coordinate_finder.lat_and_long(new_location)
                        else:
                            latlong = class_dictionary.get(matched_location).split(" ")
                            lat = latlong[0]
                            long = latlong[1]
                    CSV_list.append(event_title)
                    CSV_list.append(event_date)
                    CSV_list.append(event_start_time)
                    CSV_list.append("N/A")
                    CSV_list.append(event_location)
                    CSV_list.append(event_summary)
                    CSV_list.append(event_title)
                    CSV_list.append(lat)
                    CSV_list.append(long)
                    CSV_list.append(False)
                    CSV_data_inputter(CSV_list, food_CSV_file)

                    break

    return
        
############################################
## 211 Food Pantry Scraper Function Block ##
############################################
        
def pantry_address_splitter(address: str):
    #split addresses into usable text
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', address)
    return result

def extract_date(string: str):
    length = 0
    delimiters = ["/",","]
 
    for delimiter in delimiters:
        string = " ".join(string.split(delimiter))
        
    result = []
    result = string.split()
    data = []

    if result[0] == 'Daily':
        return days_of_week
    
    for part in result:
        if "-" in part:
            part = part.split("-")
            for indices in part: 
                if indices in days_of_week:
                    length += 1
            if length % 2 == 0:
                index_num = 0
                while index_num < length:
                    start_index = part[index_num]
                    return_index = part[index_num+1]
                    main_index = days_of_week.index(start_index)
                    end_index = days_of_week.index(return_index)
                    i = main_index
                    while i <= end_index:
                        data.append(days_of_week[i])
                        i += 1
                    return data
        else:
            data = result
            return data

def food_pantry_211_scraper():
    #scrape food pantry data from 211
    raw_link = 'https://www.211info.org/search/97408/10/?search_term=Food%20Pantries'
    link = requests.get(raw_link)
    soup = BeautifulSoup(link.text, 'html.parser')
    #create soup object from data

    list_of_all_pantries = soup.find_all("div", class_="search-result-item")

    list_of_addresses = []
    #list of all pantries
    for link in list_of_all_pantries:
        CSV_list = []
        check_location = link.find("div", class_="search-result-item-address")
        if check_location:
            fixed_location = re.findall('[A-Z][^A-Z]*', check_location.text)
            for street_details in fixed_location:
                if 'Eugene' in street_details or 'Coburg' in street_details or 'Springfield' in street_details:
                    pantry_address = pantry_address_splitter(check_location.text)
                    if pantry_address in list_of_addresses:
                        break
                    else:
                        list_of_addresses.append(pantry_address)
                    
                    pantry_name = link.find("div", class_="search-result-item-name").text
                    pantry_hours = link.find("div", class_="search-result-item-hours").text

                    text = re.sub('Hours:','', pantry_hours)
                    text = re.sub(r'\n', '', text)
                    text = text.split(" ")

                    daily_info = []
                    hours_info = []

                    for day in text:
                        if 'Monday' in day or 'Tuesday' in day or 'Wednesday' in day or 'Thursday' in day or 'Friday' in day or 'Saturday' in day or 'Sunday' in day:
                            daily_info.append(day)
                            hours_info.append(day)
                        if 'am' in day or 'pm' in day or 'noon' in day and day not in daily_info:
                            hours_info.append(day)

                    pantry_hours = " ".join(hours_info)
                    daily_info = " ".join(daily_info)
                    pantry_date = extract_date(daily_info)

                    repeat_date = []        
                    for data in pantry_date:
                        if data in days_of_week and data not in repeat_date:
                            repeat_date.append(data)
                    pantry_date = repeat_date

                    pantry_organizer = []
                    pantry_organizer_list = link.find_all("div", class_="search-result-item-sub-name")
                    if pantry_organizer_list:
                        for pantry in pantry_organizer_list:
                            pantry_organizer.append(pantry.text.lower().capitalize())
                        pantry_organizer = (" ").join(pantry_organizer)
                    else:
                        pantry_organizer = "N/A"

                    pantry_description = link.find("div", "search-result-item-eligibility").text.strip()
                    pantry_description = re.sub("\n", " ", pantry_description)
                    
                    fixed_address = coordinate_finder.address_converter(pantry_address)
                    if fixed_address:
                        lat, long = coordinate_finder.lat_and_long(fixed_address)
                    else:
                        lat, long = "N/A"
                    pantry_date = ", ".join(pantry_date)
                    CSV_list = []
                    CSV_list.append(pantry_name)
                    CSV_list.append(pantry_date)
                    CSV_list.append(pantry_hours)
                    CSV_list.append("N/A")
                    CSV_list.append(pantry_address)
                    CSV_list.append(pantry_description)
                    CSV_list.append(pantry_organizer)
                    CSV_list.append(lat)
                    CSV_list.append(long)
                    CSV_list.append(True)
                    CSV_data_inputter(CSV_list, food_CSV_file)                 

    return 

#########################################
## Food for Lane County Hot Meal Sites ##
#########################################

def date_time_splitter(string: str):
    new_strings = []
    new_strings = string.split(": ", 1)
    return new_strings

def string_split(string, separator, position):
    string = string.split(separator)
    return separator.join(string[:position]), separator.join(string[position:])

def food_for_lane_scraper():
    """
    Function to scrape foodforlanecounty.org -- searches for key words and non-repeating events
    -- internet connection required --
    """

    raw_link = 'https://www.foodforlanecounty.org/find-a-meal-site/'

    req = Request(raw_link, headers={'User-Agent': 'Mozilla/5.0'})
    #avoid error 403
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')
    #create a soup object of webpage

    h2_tag = soup.find('h2', string='Lane County Meal Sites*')
    #find all <p> text containers between <h2> and <h3>

    meal_sites = []
    temp_entry = []

    current_tag = h2_tag.find_next_sibling() #cycle through <p> containers

    while current_tag and current_tag.name != 'h3':
        #checks for correct amount of <p> tags -- accounts for split up text
        if len(current_tag.text.split("\n")) != 4:
            temp_entry.append(current_tag)
        else:
            meal_sites.append(current_tag.text)
            if len(temp_entry) != 0:
                meal_sites.append(temp_entry) #append the current meal site
            temp_entry = []
        current_tag = current_tag.find_next_sibling()

    if len(temp_entry) != 0:
        final = []
        if '\n' not in temp_entry[0].text and '\n' not in temp_entry[1].text:
            #format strings in the case that temp_entry collected some poorly formatted data
            meal_sites.append(temp_entry[0].text+' '+temp_entry[1].text+' '+temp_entry[2].text+' ')
        else:
            for text in temp_entry:
                final.append(text.text)
            meal_sites.append(" ".join(final))

    for site in meal_sites:
            #go through each entry in the meal_sites list (
 
            details = site.split("\n")
 
            if details:
                location_name = details[0].strip()

                address_details = details[0].split(",")
                if len(address_details) == 2:
                    location_address = address_details[1].strip()
                else:
                    location_address = details[1]+" Eugene OR"
                lat,long = coordinate_finder.lat_and_long(location_address)

                if lat == 'N/A' or long == 'N/A':
                    lat, long = coordinate_finder.lat_and_long(location_name+" Eugene OR")

                if len(details) == 4:
                    location_desc = details[2]
                    date_details = details[3] 
                    date_time = date_time_splitter(date_details)
                    dates = extract_date(date_time[0])
                    a = 0
                    times = date_time[1].split("-")
                    if len(times) > 2: 
                        new_times = []
                        for item in times:
                            if "&" in item:
                                split_list = item.split("&")
                                for split in split_list:
                                    new_times.append(split.strip())
                            elif "and" in item:
                                item.split("and")
                                for split in split_list:
                                    new_times.append(split.strip())
                            else:
                                new_times.append(item)
                        start_times = []
                        end_times = []
                        while a < len(new_times):
                            start_times.append(new_times[a])
                            end_times.append(new_times[a+1])
                            a = a + 2
                        start_time = ", ".join(start_times)
                        end_time = ", ".join(end_times)
                    else:
                        start_time = times[0]
                        end_time = times[1]

                    dates = ", ".join(dates)
                    CSV_list = []
                    CSV_list.append(location_name)
                    CSV_list.append(dates)
                    CSV_list.append(start_time)
                    CSV_list.append(end_time)
                    CSV_list.append(location_address)
                    CSV_list.append(location_desc)
                    CSV_list.append(location_name)
                    CSV_list.append(lat)
                    CSV_list.append(long)
                    CSV_list.append(True)
                    CSV_data_inputter(CSV_list, food_CSV_file)     
                else:
                #catch odd cases of poor HTML tagging
                    location_desc = details[1]+". "+details[2]
                    new_details_tuple = string_split(details[2], ".", 2)
                    new_details=[]
                    for item in new_details_tuple:
                        new_details.append(item)
                    date_details = extract_date(new_details[0])
                    dates = date_details[0] 
                    start_time = date_details[1].split("-")[0]+" "+date_details[2]+"."
                    end_time = date_details[1].split("-")[1]+" "+date_details[2]+"."
                    i = 0
                    if type(dates) == str:
                        CSV_list = []
                        CSV_list.append(location_name)
                        CSV_list.append(dates)
                        CSV_list.append(start_time)
                        CSV_list.append(end_time)
                        CSV_list.append(location_address)
                        CSV_list.append(location_desc)
                        CSV_list.append(location_name)
                        CSV_list.append(lat)
                        CSV_list.append(long)
                        CSV_list.append(True)
                        CSV_data_inputter(CSV_list, food_CSV_file)
                        i += 1     
                    else:
                        dates = ", ".join(dates)
                        CSV_list = []
                        CSV_list.append(location_name)
                        CSV_list.append(dates)
                        CSV_list.append(start_time)
                        CSV_list.append(end_time)
                        CSV_list.append(location_address)
                        CSV_list.append(location_desc)
                        CSV_list.append(location_name)
                        CSV_list.append(lat)
                        CSV_list.append(long)
                        CSV_list.append(True)
                        CSV_data_inputter(CSV_list, food_CSV_file)
    return  
                    
######################################
## CSV File Creation Function Block ##
######################################
        
def CSV_file_creator(CSV_file):
    """Creates an empty CSV file with specific event headers
    CSV_file: str - name of CSV file to be created
    """
    header = ['Event Title', 'Date', 'Start Time', 'End Time', 'Location', 'Description', 'Organizer(s)', 'Latitude', 'Longitude', 'Reoccurring']
    with open(CSV_file, 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        return
    
def CSV_data_inputter(data, CSV_file):
    """Adds a list to a CSV file
    data: list - containing data formatted for CSV file
    CSV_file: str - name of CSV file to be added to
    """
    with open(CSV_file, 'a', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(data)
        return

if __name__ == '__main__':
    """Testing purposes only"""

    #create CSV file
    CSV_file_creator(food_CSV_file)

    #scrape locations
    coordinate_finder.main()

    #scrape engage
    URL_list = engage_URL_web_scraper()
    engage_site_scraper(URL_list)
    #print("Scraping resources")

    #scrape events calender
    events_calendar_URL_scraper()
    #print("Scraping resources")

    #scrape food from studentlife
    student_life_scraper()

    #scrape 211 Food Pantry data
    food_pantry_211_scraper()

    #scrape food for lane county hot meal sites
    food_for_lane_scraper()
