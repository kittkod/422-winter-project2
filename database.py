'''
needs to: sort through data in .csv to look for if user wants specific hours/days (from input from tkinter)
and make functions to make dictionaries like this: 

us_cities = {
    'lat':[], 
    'lon': [], 
    'sizes': [],
    'text': [],
    'comment': [], 
    'Food Resources': [],
    'location' : [],
    'time' : []
}

'text' should be 'Description', but format it like: '> there is free pizza today <br>in deschutes hall from 5-7.<br>' so theres breaks at the end and also a carrot at the beginning with a space next to it
'comment' should be 'Event Title'
'Food Resources' should be 'Event Title' + at + 'Location' like 'food at EMU'
'location' should be 'Location'
'time' should be 'Start time' - 'End time' like : '4pm - 6pm'

P.S. I made a function to break up long strings! its called break_str() below
'''

import csv
import json
from tkinter import Tk, Label, Button, Entry
import customtkinter as ctk
import pandas as pd
from coordinate_finder import address_converter
from datetime import datetime
<<<<<<< Updated upstream
=======
from utils import clean_coordinate, get_lat_lon
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
def clean_coordinate(value):
    if isinstance(value, str):
        # Remove semicolon and any other non-numeric characters (except for the decimal point)
        clean_value = ''.join(c for c in value if c.isdigit() or c == '.')
        return float(clean_value) if clean_value else None
    else:
        # If value is already a float (or other non-string), return it directly
        return value

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

=======
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
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

=======
>>>>>>> Stashed changes
def get_all_events(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['sizes'] = 8
    return df.to_dict(orient='records')

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
