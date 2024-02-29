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
    new_str = ''
    tmp = ''
    for letter in input_string:
        if len(tmp) == size:
            new_str += '<br>'
            tmp = ''
        tmp += letter
        new_str += letter
    
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

'''
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
'''

def get_all_events(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['sizes'] = 8
    return df.to_dict(orient='records')

def run_map(input_csv):
    ''' *Description
    also write some comments
    '''
    df = pd.read_csv(input_csv) 
    dict = {
        'lat':[], 
        'lon': [], 
        'sizes': [],
        'text': [],
        'comment': [], 
        'Food Resources': [],
        'location' : [],
        'time' : [],
        'organizer': []
    }

    for _, row in df.iterrows():
        latitude_tmp = None
        longitude_tmp = None
        if row['Latitude'] != 'nan':
            latitude_tmp = clean_coordinate(row['Latitude'])
        if row['Longitude'] != 'nan':
            longitude_tmp = clean_coordinate(row['Longitude'])
        if row['Latitude'] == 'nan' or row['Longitude'] == 'nan':
            continue
        dict['lat'].append(latitude_tmp)
        dict['lon'].append(longitude_tmp)
        dict['sizes'].append(8)
        dict['text'].append(break_str(('> ' + str(row['Description']) + '<br>'), 40))
        dict['comment'].append(break_str(str(row['Event Title']), 40))
        dict['Food Resources'].append(break_str(str(row['Event Title']), 25))
        if str(row['Start Time']) != 'nan' and str(row['End Time']) != 'nan':
            dict['time'].append(break_str((' ' + str(row['Start Time']) + '-' + str(row['End Time'])), 40))
        elif str(row['Start Time']) != 'nan' and str(row['End Time']) == 'nan':
            dict['time'].append(break_str((' ' + str(row['Start Time'])), 40))
        elif str(row['Start Time']) == 'nan' and str(row['End Time']) != 'nan':
            dict['time'].append(break_str((' ' + str(row['End Time'])), 40))
        else:
            dict['time'].append("specific time not found.")
        dict['location'].append(break_str(' ' + str(row["Location"]), 40))
        # this doesn't work because theyre all strings
        '''
        if type(row['Organizer(s)']) is list:
            organizer_str = ''
            for listnum in range(len(row['Organizer(s)'])):
                organizer_str += str(row['Organizer(s)'][listnum])
                if listnum != (len(row['Organizer(s)']) - 1):
                    organizer_str += ", "
            dict['organizer'].append(break_str(organizer_str, 40))
        else:
        '''
        dict['organizer'].append(break_str(' ' + str(row['Organizer(s)']), 40))

    return dict

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
