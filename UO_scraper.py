"""
Web Scraper for University of Oregon Club Free Food
"""

from bs4 import BeautifulSoup
import requests
import csv
import json
import re
import coordinate_finder

from selenium import webdriver 

import re

CSV_file = "Free_Food_Database.csv"

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

with open('campus_buildings.txt') as f: 
    data = f.read() 
      
# reconstructing the data as a dictionary 
js_file = json.loads(data) 
class_dictionary = js_file

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

    for vals in times: #add start and end times 
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
        CSV_data_inputter(CSV_data)

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
            
        CSV_data_inputter(CSV_data)
        
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
    times = []
    result = []

    """for hour in hours:
        if 'am' in hour or 'pm' in hour:
            print(hour)
            pattern = r'\b\d{1,2}(?::\d{2})?(?:am|pm)\b'
            #match = re.search(pattern, hour)
            time = re.sub(r'(?<=[a-z])([A-Z])', r' \1', hour)
            for tim in time:
                ans = re.findall(pattern, tim)
                for answer in ans:
                    times.append(answer)
        if 'noon' in hour:
            times.append('noon')"""

    result = string.split()
    data = []
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
    #
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

                    #print(pantry_hours)

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
                    print(pantry_description)
                    
                    fixed_address = coordinate_finder.address_converter(pantry_address)
                    if fixed_address:
                        lat, long = coordinate_finder.lat_and_long(fixed_address)
                    else:
                        lat, long = "N/A"
                    i = 0
                    while i < len(pantry_date):
                        CSV_list = []
                        CSV_list.append(pantry_name)
                        CSV_list.append(pantry_date[i])
                        CSV_list.append(pantry_hours)
                        CSV_list.append("N/A")
                        CSV_list.append(pantry_address)
                        CSV_list.append(pantry_description)
                        CSV_list.append(pantry_organizer)
                        CSV_list.append(lat)
                        CSV_list.append(long)
                        CSV_list.append(True)
                        CSV_data_inputter(CSV_list)
                        i += 1                   

    return 
                

######################################
## CSV File Creation Function Block ##
######################################
        
<<<<<<< Updated upstream
def CSV_file_creator():
=======
def CSV_file_creator(CSV_file):
>>>>>>> Stashed changes
    header = ['Event Title', 'Date', 'Start Time', 'End Time', 'Location', 'Description', 'Organizer(s)', 'Latitude', 'Longitude', 'Reoccuring']
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

    #scrape locations
    coordinate_finder.main()

    #scrape engage
    URL_list = engage_URL_web_scraper()
    engage_site_scraper(URL_list)
    #print("Scraping resources")

    #scrape events calender
    events_calendar_URL_scraper()
    #print("Scraping resources")

    #scrape 211 Food Pantry data
    food_pantry_211_scraper()

