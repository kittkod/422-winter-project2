'''
Database for graph function helpers and UI-database connectors
needs to: sort through data in .csv to look for if user wants specific hours/days 
'''

import csv
import json
from tkinter import Tk, Label, Button, Entry
import customtkinter as ctk
import pandas as pd
from coordinate_finder import address_converter
from datetime import datetime
from Resource_Graph import clean_coordinate

# Load campus buildings data
with open('campus_buildings.txt') as f:
    campus_buildings = json.load(f)

csv_file_path = 'Free_Food_Database.csv'

# Function to break up long strings
def break_str(input_string, size):
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

# Finds location within building dict. with partial string matching
def flexible_match_location(event_location, buildings_dict):
    # Convert the event location to lowercase for case-insensitive comparison
    event_location_lower = event_location.lower()

    for building_key, coords in buildings_dict.items():
        # Check if the building name (in lowercase) is contained within the event location string
        if building_key.lower() in event_location_lower:
            lat_lon_str = coords.split("; ")
            return float(lat_lon_str[0]), float(lat_lon_str[1])
        
    return None, None

# Function to convert address to lat and lon using flexible match
def get_lat_lon(address):
    transformed_address = address_converter(address)  # Use existing address transformation

    # Attempt to find the transformed address in the campus buildings data
    lat, lon = flexible_match_location(transformed_address, campus_buildings)
    if lat is not None and lon is not None:
        return lat, lon
    else:
        print(f"Location: {address} not found in campus buildings.")
        return None, None

# Function to filter events based on date and time range
def filter_events(csv_file_path, date_str, start_time_str, end_time_str):
    df = pd.read_csv(csv_file_path)

    # Convert date and time strings to objects
    date = datetime.strptime(date_str, '%B %d %Y')
    start_time = datetime.strptime(start_time_str, '%I:&M &p').time()
    end_time = datetime.strptime(end_time_str, '%I:%M %p').time()

    # Filter dataframe
    filtered_df = df[
        (pd.to_datetime(df['Date']) == date) &
        (pd.to_datetime(df['Start Time']).dt.time >= start_time) &
        (pd.to_datetime(df['End Time']).dt.time <= end_time)
    ]

    return filtered_df


# Function to convert filtered dataframe to dictionary
def convert_to_dict(filtered_df):
    event_data = {
        'lat': [],
        'lon': [],
        'sizes': [],
        'text': [],
        'comment': [],
        'Food Resources': []
    }
    for _, row in filtered_df.iterrows():
        lat, lon = get_lat_lon(row['Location'])
        event_data['lat'].append(lat)
        event_data['lon'].append(lon)
        event_data['sizes'].append(8)  # Static size for all points
        event_data['text'].append(row['Description'])
        event_data['comment'].append(row['Location'])
        event_data['Food Resources'].append(row['Event Title'])

    return event_data

def get_all_events(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['sizes'] = 8
    return df.to_dict(orient='records')

def run_map(input_csv, start_day, end_day):
    ''' 
    This function processes events from a CSV file and formats them for use in a scatterplot map.
    It filters events based on a date range and extracts the necessary information for plotting.
    '''
    df = pd.read_csv(input_csv) 

    event_dict = {
        'lat': [], 
        'lon': [], 
        'sizes': [],
        'text': [],
        'comment': [], 
        'Food Resources': [],
        'Location': [],
        'Time': [],
        'Organizer': []
    }

    for _, row in df.iterrows():
        latitude_tmp = None
        longitude_tmp = None
        if str(row['Latitude']) != 'nan':
            latitude_tmp = clean_coordinate(row['Latitude'])
        if str(row['Longitude']) != 'nan':
            longitude_tmp = clean_coordinate(row['Longitude'])
        if latitude_tmp is None or longitude_tmp is None:
            continue
        
        event_dict['lat'].append(latitude_tmp)
        event_dict['lon'].append(longitude_tmp)
        event_dict['sizes'].append(8)

        # Process the Description field to remove specific unwanted parts
        description = str(row['Description'])
        if description != 'nan':
            # Remove unwanted patterns
            patterns_to_remove = ['==> Eligibility:', '=', '=Eligibility:']
            for pattern in patterns_to_remove:
                description = description.replace(pattern, '')
            description = description.strip()
            # Add the cleaned description to the event_dict
            event_dict['text'].append(break_str(description, 40))
        else:
            event_dict['text'].append(' ')

        # Add event title to the comment and Food Resources
        event_title = break_str(str(row['Event Title']), 40)
        event_dict['comment'].append(event_title)
        event_dict['Food Resources'].append(break_str(event_title, 25))

        # Process the Time field to replace "=" with ":"
        start_time = str(row['Start Time'])
        end_time = str(row['End Time'])
        if start_time != 'nan' and end_time != 'nan':
            time_str = f"{start_time}-{end_time}"
        elif start_time != 'nan':
            time_str = start_time
        elif end_time != 'nan':
            time_str = end_time
        else:
            time_str = " "
        time_str = time_str.replace('=', ':').strip()
        event_dict['Time'].append(break_str(time_str, 40))

        # Process the Location field
        location = str(row['Location'])
        event_dict['Location'].append(break_str(location if location != 'nan' else ' ', 40))

        # Process the Organizer(s) field
        organizer = str(row['Organizer(s)'])
        event_dict['Organizer'].append(break_str(organizer if organizer != 'nan' else ' ', 40))

    return event_dict

if __name__ == "__main__":
    print("Running database.py script...")
    events = get_all_events(csv_file_path)
    print(f"CSV file read successfully. Number of events found: {len(events)}")
    for event in events:
        converted_address = address_converter(event['Location']) # Using address_converter logic
        lat, lon = get_lat_lon(converted_address)
        if lat is not None and lon is not None:
            print(f"Event Title: {event['Event Title']}, Location: {converted_address}, Latitude: {lat}, Longitude: {lon}")
        else:
            print(f"Event Title: {event['Event Title']}, Location: {converted_address} : Not found in campus buildings.")
