#######################################################################
# UO_scraper.py                                                       #
# created: TODO                                                       # 
# Authors: Kylie Griffiths                                                     #
#                                                                     #
# Description: Form to take in administrative input and add to        #
# database.                                                           #                             
#                                                                     #
# Interactions:                                                       #
# - TODO                                                              #
####################################################################### 

from datetime import datetime 
import pandas as pd
import re
import os.path
import json

from coordinate_finder import lat_and_long, address_converter
from UO_scraper import CSV_file_creator, CSV_data_inputter, food_CSV_file

unprocessed_admin_CSV_file = "dollarless_database_files/unprocessed_admin_info.csv"
admin_CSV_file = "dollarless_database_files/admin_info.csv"

def add_to_admin_file(dictionary):

    with open('campus_buildings.txt') as f: 
        data = f.read() 
    #pull data to be read from
      
    #reconstructing the data as a dictionary 
    js_file = json.loads(data) 
    class_dictionary = js_file

    admin_CSV_entry = []
    admin_location = dictionary.get("location")
    admin_CSV_entry.append(dictionary.get("title"))
    admin_CSV_entry.append(dictionary.get("date"))
    admin_CSV_entry.append(dictionary.get("start_time"))
    admin_CSV_entry.append(dictionary.get("end_time"))
    admin_CSV_entry.append(admin_location)
    admin_CSV_entry.append(dictionary.get("desc"))
    admin_CSV_entry.append(dictionary.get("organizers"))
    matched_location = None
    if admin_location:
        for location in class_dictionary.keys():
            if location in admin_location:
                matched_location = location
                break
        if matched_location == None:
            new_location = address_converter(admin_location)
            lat, long = lat_and_long(new_location)
        else:
            latlong = class_dictionary.get(matched_location).split(" ")
            lat = latlong[0]
            long = latlong[1]
    admin_CSV_entry.append(lat)
    admin_CSV_entry.append(long)
    admin_CSV_entry.append(False)

    if os.path.isfile("./dollarless_database_files/unprocessed_admin_info.csv") is False:
        CSV_file_creator(unprocessed_admin_CSV_file)
        CSV_data_inputter(admin_CSV_entry, unprocessed_admin_CSV_file)
    else:
        CSV_data_inputter(admin_CSV_entry, unprocessed_admin_CSV_file)
    '''
    if os.path.isfile("./dollarless_database_files/admin_info.csv") is False:
        CSV_file_creator(admin_CSV_file)
        CSV_data_inputter(admin_CSV_entry, admin_CSV_file)
    else: 
        CSV_data_inputter(admin_CSV_entry, admin_CSV_file)

    CSV_data_inputter(admin_CSV_entry, food_CSV_file)
    '''
    
    return

def contains_year(input_string):
    pattern = r'\b\d{4}\b'  # Regular expression pattern for a four-digit number
    match = re.search(pattern, input_string)
    return match is not None

def convert_time_format(time_str):
    try:
        # Parse the input time string
        time_obj = datetime.strptime(time_str, '%I:%M%p')
        # Format the time object with AM/PM
        formatted_time = time_obj.strftime('%I:%M %p')
    except ValueError:
        # If parsing fails, return the original string
        formatted_time = time_str
    return formatted_time

def admin_file_updater():
    """Checks if admin file contains out-of-date data
    - should only be called in conjunction with updating data"""

    original_admin_df = pd.read_csv("./dollarless_database_files/admin_info.csv")
    admin_df = original_admin_df[["Date", "Start Time", "End Time"]]
    admin_df = pd.DataFrame(admin_df)

    index = 0
    values = []
    time = datetime.now()
    time_hour = int(datetime.now().time().strftime('%H%M'))
    for date in admin_df['Date']:

        if contains_year(date) == False:
            """if year is not in the time string"""
            fixed_date = datetime.strptime(date, '%B %d')
            if fixed_date.date() < time.replace(year=fixed_date.year).date:
                original_admin_df = original_admin_df.drop(index)
            if fixed_date.date() == time.replace(year=fixed_date.year).date:
                target_time = int(datetime.strptime(admin_df.at[index, "Start Time"], '%I:%M %p').time().strftime('%H%M'))
                if time_hour > target_time:
                    original_admin_df = original_admin_df.drop(index)
                else:
                    values.append(index)
            else:
                values.append(index)

        else:
            """if year is in the time string"""
            given_datetime = datetime.strptime(date, "%B %d %Y")
            # Compare the parsed datetime with the current datetime
            if given_datetime.date() < time.date():
                original_admin_df = original_admin_df.drop(index)
            if given_datetime.date() == time.date():
                editted_time = convert_time_format(admin_df.at[index, "Start Time"])
                target_time = int(datetime.strptime(editted_time, '%I:%M %p').time().strftime('%H%M'))
                if time_hour > target_time:
                    original_admin_df = original_admin_df.drop(index)
                else:
                    values.append(index)
            else:
                values.append(index)

        index += 1
    
    CSV_file_creator(admin_CSV_file)

    for val in values:

        CSV_file_list = original_admin_df.loc[val, :].values.flatten().tolist()
        CSV_data_inputter(CSV_file_list, admin_CSV_file)
        CSV_data_inputter(CSV_file_list, food_CSV_file)

def delete_from_admin(event_title: str):
    """Function to remove admin entered data - once admin has selected an event title to delete"""
    ##should be no errors in event_title because event_title is a button press grab
    
    df_admin_1 = pd.read_csv(admin_CSV_file)
    df_admin = pd.DataFrame(df_admin_1)
    df_food_1 = pd.read_csv(food_CSV_file)
    df_food = pd.DataFrame(df_food_1)
    admin_index = df_admin.index.get_loc(df_admin[df_admin['Event Title'] == event_title].index[0])
    food_index = df_food.index.get_loc(df_food[df_food['Event Title'] == event_title].index[0])
    df_admin = df_admin.drop([admin_index])
    df_food = df_food.drop([food_index])

    CSV_file_creator(admin_CSV_file)
    df_admin.to_csv('./dollarless_database_files/admin_info.csv', index=False)
    CSV_file_creator(food_CSV_file)
    df_food.to_csv('./dollarless_database_files/Free_Food_Database.csv', index=False)
    return  

def delete_only_from_admin(event_title: str):
    """Function to remove admin entered data (but only on admin list)
    -for debugging purposes
    """
    ##should be no errors in event_title because event_title is a button press grab
    
    df_admin_1 = pd.read_csv(admin_CSV_file)
    df_admin = pd.DataFrame(df_admin_1)
    admin_index = df_admin.index.get_loc(df_admin[df_admin['Event Title'] == event_title].index[0])
    df_admin = df_admin.drop([admin_index])

    CSV_file_creator(admin_CSV_file)
    df_admin.to_csv('./dollarless_database_files/admin_info.csv', index=False)
    return  

if __name__ == "__main__":
    "Test cases - don't run unless you are prepared to refresh the data afterwards"
    
