'''
Database for graph function helpers and UI-database connectors
needs to: sort through data in .csv to look for if user wants specific hours/days 
'''
import pandas as pd
import utils

csv_file_path = 'Free_Food_Database.csv'


def run_map(input_csv, input_button):
    '''function to create a dictionary for a scatterplot map input from data from an input csv.
    inputs:
        input_csv:csv - the csv with scraped data
        input_button:str - the string telling which button was pressed to run the map
                            input_button can be 'today', 'tomorrow' or 'next 7 days'
    outputs:
        event_dict:dict - the created dictionary with scatterplot points
        map_name:str - the name of the map with corresponding dates
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
        'Organizer': [],
        'Date': [],
        'Reoccurring': []
    }
    
    start_date, end_date, weekday_date, is_week, map_name = utils.find_ranges(input_button.lower())
    
    
    # looping through each row in the input csv
    for _, row in df.iterrows():
        
        # if this row is out of the filtered range, skip
        if utils.in_filter(row, start_date, end_date, weekday_date, is_week) == False:
            continue
      
        # title with dates if is_week is true
        new_event_title = ''
        if is_week == True and str(row["Reoccurring"]).strip().lower() == "false":
            new_event_title = utils.break_str((row.get('Event Title', '')+' - '+row['Date']), 28)#'+str(row_month)+'/'+str(row_day)+'/'+datetime.date.today().strftime('%y')), 28)
        if is_week == True and str(row["Reoccurring"]).strip().lower() == "true":
            new_event_title = utils.break_str((row.get('Event Title', '')+' - '+ row['Date']), 28)
        if is_week == False:
            new_event_title = utils.break_str(row.get('Event Title', ''), 28)

        # Assuming clean_coordinate handles non-string inputs correctly.
        latitude_tmp = utils.clean_coordinate(row['Latitude'])
        longitude_tmp = utils.clean_coordinate(row['Longitude'])

        if latitude_tmp is None or longitude_tmp is None:
            continue
        
        event_dict['lat'].append(latitude_tmp)
        event_dict['lon'].append(longitude_tmp)
        event_dict['sizes'].append(8)

        # Process and validate the Description field
        description = row.get('Description', '')
        if isinstance(description, str) and description.lower() != 'nan':
            description = description.strip()  # Remove leading/trailing whitespace
            description = utils.clean_description(description)
            description+='<br>'
            event_dict['text'].append(utils.break_str(description, 40))
        else:
            event_dict['text'].append('')

        # Process and add other event details (apply similar validation if necessary)
        event_dict['comment'].append(new_event_title)
        event_dict['Food Resources'].append(new_event_title)
        event_dict['Time'].append(utils.break_str(utils.format_time(row), 40))

        location = str(row.get('Location', ' '))
        # Check if location is 'nan' which is the string representation of NaN for floats
        if location.lower() != 'nan':
            event_dict['Location'].append(utils.break_str(location, 40))
        else:
            event_dict['Location'].append(' ')

        # Check and format the 'Organizer(s)' field
        organizer = row.get('Organizer(s)', '')
        if pd.isna(organizer):  # If it's NaN, use an empty string instead
            organizer = ''
        event_dict['Organizer'].append(utils.break_str(str(organizer), 40))

        # Check if the event is reoccurring and adjust the Date field accordingly
        reoccurring = row.get('Reoccurring', False)
        event_dict['Reoccurring'].append(reoccurring)
        
        date = str(row.get('Date', '')).strip()
        if reoccurring and date.lower() != 'nan' and date:
            date = f"Every {date}"
        event_dict['Date'].append(utils.break_str(date, 40))

    return event_dict, map_name

if __name__ == "__main__":
    print("Running database.py script...")
    events = utils.get_all_events(csv_file_path)
    print(f"CSV file read successfully. Number of events found: {len(events)}")
    for event in events:
        converted_address = utils.address_converter(event['Location']) # Using address_converter logic
        lat, lon = utils.get_lat_lon(converted_address)
        if lat is not None and lon is not None:
            print(f"Event Title: {event['Event Title']}, Location: {converted_address}, Latitude: {lat}, Longitude: {lon}")
        else:
            print(f"Event Title: {event['Event Title']}, Location: {converted_address} : Not found in campus buildings.")