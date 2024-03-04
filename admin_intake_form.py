"""Form to take in administrative input and add to database"""

from datetime import datetime 
import pandas as pd
import re
import os.path

from coordinate_finder import lat_and_long
from UO_scraper import CSV_file_creator, CSV_data_inputter, food_CSV_file

admin_CSV_file = "admin_info.csv"

def add_to_admin_file(dictionary):
    "Called by the Food Information User Interface when an admin user enters input"

    admin_CSV_entry = []
    admin_CSV_entry.append(dictionary.get("title"))
    admin_CSV_entry.append(dictionary.get("date"))
    admin_CSV_entry.append(dictionary.get("start_time"))
    admin_CSV_entry.append(dictionary.get("end_time"))
    admin_CSV_entry.append(dictionary.get("location"))
    admin_CSV_entry.append(dictionary.get("desc"))
    admin_CSV_entry.append(dictionary.get("organizers"))
    lat, long = lat_and_long(dictionary.get("location"))
    admin_CSV_entry.append(lat)
    admin_CSV_entry.append(long)
    admin_CSV_entry.append(False)

    if os.path.isfile("./admin_info.csv") is False:
        CSV_file_creator(admin_CSV_file)
        CSV_data_inputter(admin_CSV_entry, admin_CSV_file)
    else: 
        CSV_data_inputter(admin_CSV_entry, admin_CSV_file)

    CSV_data_inputter(admin_CSV_entry, food_CSV_file)
    
    return

def contains_year(input_string):
    pattern = r'\b\d{4}\b'  # Regular expression pattern for a four-digit number
    match = re.search(pattern, input_string)
    return match is not None

def admin_file_updater():
    """Checks if admin file contains out-of-date data
    - should only be called in conjunction with updating data"""

    original_admin_df = pd.read_csv("admin_info.csv")
    admin_df = original_admin_df[["Date", "Start Time", "End Time"]]
    admin_df = pd.DataFrame(admin_df)
    time = datetime.now()

    index = 0
    values = []

    for date in admin_df['Date']:

        if contains_year(date) == False:
            """if year is not in the time string"""
            fixed_date = datetime.strptime(date, '%B %d')
            if fixed_date < time.replace(year=fixed_date.year):
                original_admin_df = original_admin_df.drop(index)
            else:
                values.append(index)

        else:
            """if year is in the time string"""
            given_datetime = datetime.strptime(date, "%B %d %Y")
            # Compare the parsed datetime with the current datetime
            if given_datetime < time:
                original_admin_df = original_admin_df.drop(index)
            else:
                values.append(index)

        index += 1
    
    CSV_file_creator(admin_CSV_file)

    for val in values:

        CSV_file_list = original_admin_df.loc[val, :].values.flatten().tolist()
        CSV_data_inputter(CSV_file_list, admin_CSV_file)
        CSV_data_inputter(CSV_file_list, food_CSV_file)
    

if __name__ == "__main__":
    "Test cases - don't run unless you are prepared to refresh the data afterwards"

    CSV_file_creator(admin_CSV_file)

    dictionary_1 = {"title": "Kylie Test", "date": "March 2", "start_time": "3:00 PM", "end_time": "4:00 PM", "location": "348 Lincoln St Eugene OR", "desc": "Climb with Kylie!", "organizers": "Kylie"}
    dictionary_2 = {"title": "Kylie Test number 2", "date": "March 4", "start_time": "3:00 PM", "end_time": "4:00 PM", "location": "348 Lincoln St Eugene OR", "desc": "Climb with Kylie a second time!", "organizers": "Simone :>"}
    
    add_to_admin_file(dictionary_1) 
    add_to_admin_file(dictionary_2) 
    admin_file_updater()

    