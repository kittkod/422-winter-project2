'''
needs to: sort through data in .csv to look for if user wants specific hours/days (from input from tkinter)
and make functions to make dictionaries like this: 

us_cities = {
    'lat':[44.0430978, 44.04358895589884, 44.04358546139572, 44.0461586, 44.043320, 44.045], 
    'lon': [-123.0670994, -123.07538151741028, -123.07766889687626, -123.0874064, -123.077728, -123.066], 
    'sizes': [8, 8, 8, 8, 8, 8],
    'text': ['there is free pizza today <br>in deschutes hall from 5-7.', 'there is a grocery drop today<br>at the EMU', 'Potatoes at east main', 'Every tuesday from 1-2<br>there is a gardening feast.', 'There is MEAT at the library', 'stuff at MATTHEW!!'],
    'comment': ['Deschutes Hall', 'EMU', '33 east main', 'some place', 'Knight Library', 'Matthew knight'], 
    'Food Resources': ['Free Pizza', 'Grocery Drop', 'Potatoes', 'Gardening Feast', 'Meat', 'stuff']
}

with the corresponding data 
'''

import csv
from tkinter import Tk, Label, Button, Entry
import customtkinter as ctk
import pandas as pd
from datetime import datetime

csv_file_path = 'Free_Food_Database.csv'

# Function to convert address to lat and lon
def get_lat_lon(address):
    # Replace with actual logic
    return 44.0, -123.0

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
    return df.to_dict(orient='records')

if __name__ == "__main__":
    print("Running database.py script...")
    print(f"Attempting to read CSV file from path: {csv_file_path}")
    events = get_all_events(csv_file_path)
    print("CSV file read successfully. Number of events found:", len(events))
    for event in events:
        print(event['Event Title'])
