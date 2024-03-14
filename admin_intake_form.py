#######################################################################
# UO_scraper.py                                                       #
# created: 2/29/2024                                                  # 
# Authors: Kylie Griffiths                                            #
#                                                                     #
# Description: Form to take in administrative input and add to        #
# database.                                                           #                             
#                                                                     #
# Interactions:                                                       #
# - coordinate_finder: Calls lat_and_long, address_converter          #
# - UO_scraper: Calls CSV_file_creator, CSV_data_inputter             #
# - food_CSV_file: inputs admin information into CSV file             # 
# - admin_CSV_file: inputs admin information into CSV file            #
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
    """Function to add manual input into admin_info.csv
    input: dict
    output: void
    """

    with open('campus_buildings.txt') as f: 
        data = f.read() 
    #pull data to be read from
      
    #reconstructing the data as a dictionary 
    js_file = json.loads(data) 
    class_dictionary = js_file

    admin_CSV_entry = []
    #Pull location from the dictionary received from the Food_Information_User_Interface
    admin_location = dictionary.get("location")
    admin_CSV_entry.append(dictionary.get("title"))
    admin_CSV_entry.append(dictionary.get("date"))
    admin_CSV_entry.append(dictionary.get("start_time"))
    admin_CSV_entry.append(dictionary.get("end_time"))
    admin_CSV_entry.append(admin_location)
    admin_CSV_entry.append(dictionary.get("desc"))
    admin_CSV_entry.append(dictionary.get("organizers"))

    #Code to check if a location is a building on campus or an address in Eugene
    matched_location = None
    if admin_location:
        for location in class_dictionary.keys():
            #check keys of dictionary for a match
            if location in admin_location:
                matched_location = location
                break
        if matched_location == None:
            #if match is not found, use raw address
            new_location = address_converter(admin_location)
            lat, long = lat_and_long(new_location)
        else:
            #if a match is found, pull information from dictionary
            latlong = class_dictionary.get(matched_location).split(" ")
            lat = latlong[0]
            long = latlong[1]

    admin_CSV_entry.append(lat)
    admin_CSV_entry.append(long)
    admin_CSV_entry.append(False) #mark reoccuring event as FALSE

    if os.path.isfile("./dollarless_database_files/unprocessed_admin_info.csv") is False:
        #check if file exists
        CSV_file_creator(unprocessed_admin_CSV_file) #add to unprocessed_admin and admin_CSV
        CSV_data_inputter(admin_CSV_entry, unprocessed_admin_CSV_file)
    else:
        CSV_data_inputter(admin_CSV_entry, unprocessed_admin_CSV_file)
    return

def contains_year(input_string):
    """Function to check if a string contains a year
    input: str
    output: bool
    """
    pattern = r'\b\d{4}\b'  #regular expression pattern for a four-digit number
    match = re.search(pattern, input_string)
    return match is not None

def convert_time_format(time_str):
    """Function to convert a time string into a datetime object
    input: str
    output: datetime object
    """
    try:
        #parse the input time string
        time_obj = datetime.strptime(time_str, '%I:%M%p')
        # Format the time object with AM/PM
        formatted_time = time_obj.strftime('%I:%M %p')
    except ValueError:
        #if parsing fails, return the original string
        formatted_time = time_str
    return formatted_time

def admin_file_updater():
    """Function to update admin_file in congruence with "refresh data" - updates CSV if event has passed
    input: void
    output: void
    """

    #checks admin file inputs to see if they have passed
    original_admin_df = pd.read_csv("./dollarless_database_files/admin_info.csv")

    if original_admin_df.empty == True:
        #if no admin input, exit
        return
    
    admin_df = original_admin_df[["Date", "Start Time", "End Time"]]
    admin_df = pd.DataFrame(admin_df)

    index = 0   
    values = []
    time = datetime.now()
    time_hour = int(datetime.now().time().strftime('%H%M')) #check the current time

    for date in admin_df['Date']:
        #check the date on each event
        if contains_year(date) == False:
            # if the year is not in the string, add the year
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
            # if year is in the string
            given_datetime = datetime.strptime(date, "%B %d %Y")
            # compare the parsed datetime with the current datetime
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
    
    CSV_file_creator(admin_CSV_file) #re-create the admin file to only input valid events 

    for val in values:

        CSV_file_list = original_admin_df.loc[val, :].values.flatten().tolist()
        CSV_data_inputter(CSV_file_list, admin_CSV_file) #add upcoming events into the admin_CSV and food_CSV 
        CSV_data_inputter(CSV_file_list, food_CSV_file)

    #unprocessed admin file checker - same process as above but for the unprocessed_admin file
    original_admin_df = pd.read_csv("./dollarless_database_files/unprocessed_admin_info.csv")
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
    
    CSV_file_creator(unprocessed_admin_CSV_file)

    for val in values:

        CSV_file_list = original_admin_df.loc[val, :].values.flatten().tolist()
        CSV_data_inputter(CSV_file_list, "unprocessed_admin_info.csv")

def delete_from_admin(event_title: str):
    """Function to delete manual admin data
    input: str
    output: void
    """
    #Read both CSV files
    df_admin_1 = pd.read_csv(admin_CSV_file)
    df_admin = pd.DataFrame(df_admin_1)

    df_food_1 = pd.read_csv(food_CSV_file)
    df_food = pd.DataFrame(df_food_1)
    
    #get the index of the event to be deleted
    admin_index = df_admin.index.get_loc(df_admin[df_admin['Event Title'] == event_title].index[0])
    food_index = df_food.index.get_loc(df_food[df_food['Event Title'] == event_title].index[0])
    df_admin = df_admin.drop([admin_index]) #remove from admin_info.csv
    df_food = df_food.drop([food_index]) #remove from free_food_database.csv

    CSV_file_creator(admin_CSV_file)
    df_admin.to_csv('./dollarless_database_files/admin_info.csv', index=False) #remake dataframe into CSV file 

    CSV_file_creator(food_CSV_file)
    df_food.to_csv('./dollarless_database_files/Free_Food_Database.csv', index=False) #remake dataframe into CSV file 
    return  

def delete_only_from_admin(event_title: str):
    """Function to delete manual admin data but only from admin event - test function
    input: str
    output: void
    """
    
    df_admin_1 = pd.read_csv(admin_CSV_file)
    df_admin = pd.DataFrame(df_admin_1)
    admin_index = df_admin.index.get_loc(df_admin[df_admin['Event Title'] == event_title].index[0])
    df_admin = df_admin.drop([admin_index])

    CSV_file_creator(admin_CSV_file)
    df_admin.to_csv('./dollarless_database_files/admin_info.csv', index=False)
    return  

if __name__ == "__main__":
    "Test cases - don't run unless you are prepared to refresh the data afterwards"
    admin_file_updater()
