'''
Database for graph function helpers and UI-database connectors
needs to: sort through data in .csv to look for if user wants specific hours/days 
'''
import pandas as pd
from utils import clean_description, break_str, format_time, get_all_events, get_lat_lon, address_converter, clean_coordinate

csv_file_path = 'Free_Food_Database.csv'

def run_map(input_csv, start_day, end_day):
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
        'Organizer': [],
        'Date': []
    }

    for _, row in df.iterrows():
        # Assuming clean_coordinate handles non-string inputs correctly.
        latitude_tmp = clean_coordinate(row['Latitude'])
        longitude_tmp = clean_coordinate(row['Longitude'])

        if latitude_tmp is None or longitude_tmp is None:
            continue
        
        event_dict['lat'].append(latitude_tmp)
        event_dict['lon'].append(longitude_tmp)
        event_dict['sizes'].append(8)

        # Process and validate the Description field
        description = row.get('Description', '')
        if isinstance(description, str) and description.lower() != 'nan':
            description = description.strip()  # Remove leading/trailing whitespace
            description = clean_description(description)
            event_dict['text'].append(break_str(description, 40))
        else:
            event_dict['text'].append('')

        # Process and add other event details (apply similar validation if necessary)
        event_dict['comment'].append(break_str(row.get('Event Title', ''), 40))
        event_dict['Food Resources'].append(break_str(row.get('Event Title', ''), 25))
        event_dict['Time'].append(format_time(row))
        location = str(row.get('Location', ' '))
        # Check if location is 'nan' which is the string representation of NaN for floats
        if location.lower() != 'nan':
            event_dict['Location'].append(break_str(location, 40))
        else:
            event_dict['Location'].append(' ')
        event_dict['Organizer'].append(break_str(row.get('Organizer(s)', ' '), 40))
        event_dict['Date'].append(row.get('Date', None))

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
