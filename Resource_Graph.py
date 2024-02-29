"""
Grapher to display free food resources around UO (as well as eugene, if development goes there)
"""
import plotly.express as px 
from database import clean_coordinate
import database # testing - jasmine
import pandas as pd # testing too - jasmine

def graph_scatterplot(input_data, title_name):
    ''' This function graphs a plotly.express.scatter_mapbox() type with a dictionary
    of inputted plot points.
    inputs:
        input_data:dict - a dictionary with types 'lat', 'lon', 'sizes', 'text', 'comment', 'Food Resources'
        title_name:str - a string that pertains to the title of the given graph 
    '''
    
    fig = px.scatter_mapbox(input_data, lat="Latitude", lon="Longitude", title=title_name, 
        height=650, width=1200, zoom=14.4, hover_name="Event Title",  # Use "Event Title" for hover name
        hover_data={"Description": True, 
                    "Start Time": True, "End Time": True, 
                    "Location": True,
                    "Organizer(s)": True, 
                    "Date": True, 
                    "Food Resources": False,
                    "sizes": False, 
                    "Latitude": False, 
                    "Longitude": False}, 
        size='sizes', color="Food Resources", color_continuous_scale="red", labels={'Description':''},
        custom_data=["Description", "Start Time", "End Time", "Location", "Organizer(s)", "Date"]) 

    fig.update_traces(hovertemplate='<b>%{customdata[4]}</b><br>%{customdata[0]}<br>Start: %{customdata[1]}<br>End: %{customdata[2]}<br>Location: %{customdata[3]}<br>Date: %{customdata[5]}')

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})
    
    fig.show()

def main():
    df = pd.read_csv('Free_Food_Database.csv')
    dict = {
        'Latitude':[], 
        'Longitude': [], 
        'sizes': [],
        'Description': [],
        'Event Title': [], 
        'Food Resources': [],
        'Start Time' : [],
        'End Time' : [],
        'Location' : [],
        'Organizer(s)' : [],
        'Date' : []
    }

    for _, row in df.iterrows():
        latitude_tmp = clean_coordinate(row['Latitude']) if row['Latitude'] else None
        longitude_tmp = clean_coordinate(row['Longitude']) if row['Longitude'] else None
        dict['Latitude'].append(latitude_tmp)
        dict['Longitude'].append(longitude_tmp)
        dict['sizes'].append(8)
        new_desc = database.break_str(row['Description'], 35)
        dict['Description'].append(new_desc) 
        new_name = database.break_str(row['Event Title'], 35)
        dict['Event Title'].append(new_name)
        dict['Food Resources'].append(database.break_str(row['Event Title'], 20))
        dict['Start Time'].append(row['Start Time'])
        dict['End Time'].append(row['End Time'])
        dict['Location'].append(row['Location'])
        dict['Organizer(s)'].append(row['Organizer(s)'])
        dict['Date'].append(row['Date'])
    
    graph_scatterplot(dict, "Food Resources on Specific Date")

    return 0

if __name__ == "__main__":
    main()
