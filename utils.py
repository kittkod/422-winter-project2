#######################################################################
# utils.py                                                            #
# created: 2/22/24                                                    # 
# Authors: Max Hermens and Jasmine Wallin                             #
#                                                                     #
# Description: This file holds helper functions for two files in the  #
# Dollarless Dining program.                                          #                             
# Functions: break_str(), flexible_match_location(), get_lat_lon(),   #
# address_converter(), filter_events(), clean_description(),          #
# format_time(), clean_coordinate(), get_all_events(), find_ranges(), #
# in_filter().                                                        #                
#                                                                     #
# Interactions:                                                       #
# - Remodeled_Food_Information_User_Interface.py: This file uses      #
#   get_all_events() for the scrollable frame.                        #
# - database.py: This file uses find_ranges(), in_filter(),           #
#   clean_coordinate(), break_str() and format_time(). for creating   #
#   the dictionary for the map.                                       #
####################################################################### 

import re # used for finding patterns in dates
import pandas as pd # parsing through csv's 
from datetime import date, datetime # finding dates based on today's date 
import os.path # checks if food data file is present
import csv # for reading through unprocessed admin events
from UO_scraper import CSV_data_inputter, CSV_file_creator

################################################################################## 
# DICTIONARIES                                                                   #
# dictionaries for find_ranges() and in_filter() functions.                      # 
################################################################################## 

weekday_dict = {0:"monday", 1:"tuesday", 2:"wednesday", 3:"thursday", 
                4:"friday", 5:"saturday", 6:"sunday"}
days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
month_dict = {"january":1, "february":2, "march":3, "april":4, "may":5,
                "june":6, "july":7, "august":8, "september":9, "october":10,
                    "november":11, "december":12}
abbr_mon = {'jan':'january', 'feb':'february', 'mar':'march', 'apr':'april', 'jun':'june', 'jul':'july',
            'aug':'august', 'sep':'september', 'sept':'september', 'oct':'october'}


################################################################################## 
# FUNCTIONS                                                                      #
##################################################################################  

# Function to break up long strings
def break_str(input_string, size):
    ''' Function to break up long strings with <br> every 'size'
    characters.
    inputs:
        input_str:str - the string wishing to be broken up
        size:int - the index in the string that will be split
    '''
    words = input_string.split(' ')
    new_str = ''
    line = ''
    
    for word in words:
        if len(line) + len(word) + 1 <= size:  # +1 for space
            line += word + ' '
        else:
            new_str += line.rstrip() + '<br>'  # Remove trailing space and add line break
            line = word + ' '  # Start a new line with the current word
    
    new_str += line.rstrip()  # Add the last line
    return new_str

# function to format the description in a mark in the graph
def clean_description(description):
    '''format the text to remove patterns
    inputs: description:str - text string to be improved
    outputs: a string of the cleaned up description
    '''
    
    patterns_to_remove = ['==> Eligibility:', '=', '=Eligibility:', 'Eligibility:']
    for pattern in patterns_to_remove:
        description = description.replace(pattern, '')
    return ' '.join(description.split())  # This removes extra spaces between words

# format the time string in the graph
def format_time(row):
    '''format the start time - end time string for the marks in the graph
    inputs:
        row:pandas row type - row with 'Start Time' and 'End Time' to be used 
                              for formatting.
    outputs:
        time_str:str - the created string of either start-end, start or 'Time not available'
    '''
    # Get the start and end time from the row; use None as a default if they don't exist
    start_time = row.get('Start Time', None)
    end_time = row.get('End Time', None)

    # Check if either start_time or end_time is nan
    # Convert to string and strip whitespace for comparison
    start_time_str = str(start_time).strip() if start_time else None
    end_time_str = str(end_time).strip() if end_time else None

    # Format the time string based on the presence of start and end times
    if start_time_str and start_time_str.lower() != 'nan' and end_time_str and end_time_str.lower() != 'nan':
        time_str = f"{start_time_str} - {end_time_str}"
    elif start_time_str and start_time_str.lower() != 'nan':
        time_str = start_time_str
    else:
        time_str = "Time not available"

    return time_str

# function to improve coordinates
def clean_coordinate(value):
    '''clean non numeric characters from coordinates
    input:
        value:str or float - the current coordinate
    output:
        clean_value: cleaned float form of 'value'
        None: if 'value' is invalid
        value: if already a float or non string
    '''
    if isinstance(value, str):
        # Remove semicolon and any other non-numeric characters (except for the decimal point)
        clean_value = ''.join(c for c in value if c.isdigit() or c == '.')
        return float(clean_value) if clean_value else None
    else:
        # If value is already a float (or other non-string), return it directly
        return value

# get all events from a csv into a dictionary
def get_all_events(csv_file_path, filtered_by):
    '''put all events from a csv into a dictionary by a filter
    inputs:
        csv_file_path:str file path - the csv with event info
        filtered_by:str - either 'all', 'today', 'tomorrow', or 'next 7 days'. 
                            controlls what events are shown
    outputs:
        new_dict, scrollable_name - the created dictionary and the string of the 
                                     created scrollable frame name
    '''
    df = pd.read_csv(csv_file_path)
    df['sizes'] = 8
    new_dict = [] # dictionary to be created
    scrollable_name = '' # name to be created
    is_all = False # if 'all' was the 'filtered_by' value 
    if filtered_by.lower() == "all":
        is_all = True
    else:
        start_date, end_date, weekday_date, is_week, _, scrollable_name = find_ranges(filtered_by)
    
    for event in df.to_dict(orient='records'):
        # if there is a filter and the events is not in the filter range
        if is_all == False:
            if in_filter(event, start_date, end_date, weekday_date, is_week) == False:
                continue
        new_dict.append(event)

    return new_dict, scrollable_name

# function to find the ranges of days from an input button press
def find_ranges(button_press):
    '''Find ranges of days depending on the button press value
    inputs:
        button_press:str - either 'today', 'tomorrow', 'this week' or 'next week'
    outputs:
        start_date, end_date, weekday_date, is_week, map_name, scrollable_name:
            int list, int list, str, bool, str, str
            [month, day], [month, day], 'WeekdayName', True/False, 'MapName', 'ScrollableFrameName'
    '''
    curr_year = date.today().strftime('%y') # str this year
    todays_month = date.today().strftime('%m') # str this month
    todays_day = date.today().strftime('%d') # str this day
    # inclusive start and end date
    start_date = None # a list of ints: [date, month]
    end_date = None # a list of ints: [date, month]
    weekday_date = '' # a string of the weekday
    is_week = False # if 'this week' or 'next week' was chosen
    map_name = 'Free Food Resources ' # name of map
    scrollable_name = ''
    
    if button_press == "today":
        start_date = [int(todays_day), int(todays_month)] # to get rid of the leading '0'
        end_date = [int(todays_day), int(todays_month)]
        weekday_date = weekday_dict[date.today().weekday()]
        map_name += 'on ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year
        scrollable_name += ' on ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year
        
    elif button_press == "tomorrow":
        month_days = days_in_month[int(todays_month)] # how many days in the current month
        # if tomorrow goes into the next month
        if int(todays_day) + 1 > month_days:
            start_date = [1, int(todays_month)+1]
            end_date = [1, int(todays_month) + 1]
        # if tomorrow is in the same month
        else:
            start_date = [int(todays_day) + 1, int(todays_month)]
            end_date = [int(todays_day) + 1, int(todays_month)]
        weekday_date = weekday_dict[(date.today().weekday() + 1)%6]
        map_name += 'on ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year
        scrollable_name += ' on ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year

    elif button_press == "this week":
        days_till_weekend = 6 - date.today().weekday()
        month_days = days_in_month[int(todays_month)]
        # if the next 6 days go into the next month
        if int(todays_day) + days_till_weekend > month_days:
            days_forward = (int(todays_day) + days_till_weekend) - month_days
            start_date = [int(todays_day), int(todays_month)]
            end_date = [int(days_forward), int(todays_month) + 1]
        # if the next 6 days stay in the current month
        else:
            start_date = [int(todays_day), int(todays_month)]
            end_date = [int(todays_day) + days_till_weekend, int(todays_month)]
        is_week = True
        map_name += 'for the week of Monday ' + str(start_date[1]) + '/' + str(int(start_date[0]) -int(date.today().weekday())) + '/' + curr_year + ' to Sunday ' + str(end_date[1]) + '/' + str(end_date[0]) + '/' + curr_year
        scrollable_name += ' from ' + str(start_date[1]) + '/' + str(int(start_date[0]) -int(date.today().weekday())) + '/' + curr_year + ' to ' + str(end_date[1]) + '/' + str(end_date[0]) + '/' + curr_year

    elif button_press == "next week":
        starting_day = int(todays_day) + (6 - date.today().weekday() + 1)
        month_days = days_in_month[int(todays_month)]
        # if the starting day is past this month
        if starting_day > month_days:
            days_forward = starting_day-month_days 
            start_date = [days_forward, int(todays_month)+1]
            end_date = [days_forward+6, int(todays_month)+1]
        # if the ending day is past this month
        elif starting_day + 6 > month_days:
            days_forward = (starting_day + 6) - month_days
            start_date = [starting_day, int(todays_month)]
            end_date = [int(days_forward), int(todays_month) + 1]
        # if next week stays within this current month
        else:
            start_date = [starting_day, int(todays_month)]
            end_date = [starting_day+6, int(todays_month)]
        is_week = True
        map_name += 'for the week of Monday ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year + ' to Sunday ' + str(end_date[1]) + '/' + str(end_date[0]) + '/' + curr_year
        scrollable_name += ' from ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year + ' to ' + str(end_date[1]) + '/' + str(end_date[0]) + '/' + curr_year

    return start_date, end_date, weekday_date, is_week, map_name, scrollable_name

# for a single row, see if it satisfies the filter
def in_filter(row, start_date, end_date, weekday_date, is_week):
    ''' See if a single row satisfies the filter
    inputs:
        row:pandas row type - row to be used for checking
        start_date:list - list of ints [month, day] 
        end_date:list -  list of ints [month, day]
        weekday_date:str - day of the week i.e. Monday
        is_week:bool - True/False if 'this week' or 'next week'
    outputs: 
        True: if it is in the filter range
        False: if it is not in the filter range
    '''
    # if its not reoccurring event
    if str(row["Reoccurring"]).strip().lower() == "false":
        row_day = 0 # int of the row's day
        row_month = 0 # int of the row's month
        find_list = re.findall("[a-zA-Z]+\s\d{1,2}", row["Date"])
        if len(find_list) > 0:
            # getting the day from the date string
            row_day = int((re.findall("\d{1,2}", find_list[0]))[0])
            # getting the month string (full month name) from date string
            str_month = find_list[0].replace(str(row_day), '').strip().lower()
            if str_month not in month_dict:
                if str_month in abbr_mon:
                    tmp = abbr_mon[str_month]
                    str_month = tmp
                else:
                    return False
            # getting the month number from the month string
            row_month = month_dict[str_month]
        else:
            return False

        # seeing if the date is in the range 
    
        # if the row's month is larger than the starting range month and the row's date is less than the ending range date
        if (start_date[1] < row_month and (end_date[1] == row_month and end_date[0] >= row_day)):
            pass
        # if the row's month is in the starting and ending range and the row's day is within range 
        elif (start_date[1] == row_month and start_date[0] <= row_day) and (end_date[1] == row_month and end_date[0] >= row_day):
            pass
        # if the row's month is less than the ending range month and the row's date is more than the starting range date
        elif (start_date[1] == row_month and start_date[0] <= row_day) and (end_date[1] > row_month):
            pass
        # not in date bounds
        else:
            return False

    # if its reocurring
    else:
        # if the graph output is for a single day and the day's weekday does not match with the event's weekdays
        if is_week == False and weekday_date not in row["Date"].lower():
            return False
    
    return True

def is_valid_date(input_str):
    ''' checks if date matches 'March 10 2024' or 'March 10' like format. Returns boolean
    Input: input_str:str - the input date 
    Output: False - if the date is in the invalid format
            True - if the date is in valid format
    '''
    pass

# function that adds unprocessed new admin events to the database 
def update_database():
    ''' if there are new admin inputs, new admin inputs get added to the database
    upon the next run. 
    ''' 
    # if not the first run
    if os.path.isfile("./dollarless_database_files/unprocessed_admin_info.csv") is True:
        new_inputs = pd.read_csv('./dollarless_database_files/unprocessed_admin_info.csv')

        # checking if there has been any new additions
        if not new_inputs.empty:
            # checking if admin_info exists
            if os.path.isfile("./dollarless_database_files/admin_info.csv") is False:
                CSV_file_creator("./dollarless_database_files/admin_info.csv")

            # going through the inputted events
            with open('./dollarless_database_files/unprocessed_admin_info.csv') as file_obj: 
                # skipping the heading
                heading = next(file_obj) 
                reader_obj = csv.reader(file_obj) 
                # adding each inputted event to the main admin intake form
                for row in reader_obj: 
                    CSV_data_inputter(row, "./dollarless_database_files/admin_info.csv")
                    CSV_data_inputter(row, "./dollarless_database_files/Free_Food_Database.csv")
            
            # deleting contents of the file - but not the heading
            with open("./dollarless_database_files/unprocessed_admin_info.csv", 'r+') as f:
                f.readline() # read header line
                f.truncate(f.tell()) # terminate rest of the file
            