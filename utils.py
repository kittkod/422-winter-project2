<<<<<<< Updated upstream
from coordinate_finder import address_converter
import json
=======
import json
import re
import pandas as pd
from datetime import datetime
>>>>>>> Stashed changes

# Load campus buildings data
with open('campus_buildings.txt') as f:
    campus_buildings = json.load(f)

<<<<<<< Updated upstream
def clean_coordinate(value):
    if isinstance(value, str):
        # Remove semicolon and any other non-numeric characters (except for the decimal point)
        clean_value = ''.join(c for c in value if c.isdigit() or c == '.')
        return float(clean_value) if clean_value else None
    else:
        # If value is already a float (or other non-string), return it directly
        return value
=======
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
>>>>>>> Stashed changes

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
    
<<<<<<< Updated upstream
=======
def address_converter(initial_address: str):

    if not isinstance(initial_address, str):
        initial_address = str(initial_address)
        
    pattern = r'^\D+\d+'

    # Use re.search() to find the matched pattern in the string
    match = re.search(pattern, initial_address)

    # If a match is found, return the matched substring, else return the original string
    if match:
        return (match.group()+" Eugene OR")
    else:
        return initial_address
    
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
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
    return event_data
=======
    return event_data

def get_all_events(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['sizes'] = 8
    return df.to_dict(orient='records')

def clean_description(description):
    patterns_to_remove = ['==> Eligibility:', '=', '=Eligibility:', 'Eligibility:']
    for pattern in patterns_to_remove:
        description = description.replace(pattern, '')
    return ' '.join(description.split())  # This removes extra spaces between words

def format_time(row):
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

def clean_coordinate(value):
    if isinstance(value, str):
        # Remove semicolon and any other non-numeric characters (except for the decimal point)
        clean_value = ''.join(c for c in value if c.isdigit() or c == '.')
        return float(clean_value) if clean_value else None
    else:
        # If value is already a float (or other non-string), return it directly
        return value
>>>>>>> Stashed changes
