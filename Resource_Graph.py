"""
Grapher to display free food resources around UO (as well as eugene, if development goes there)
"""
import plotly.express as px 
<<<<<<< Updated upstream
from database import clean_coordinate
import database # testing - jasmine
import pandas as pd # testing too - jasmine
=======
from utils import clean_coordinate
import database # testing - jasmine
import pandas as pd # testing too - jasmine
from datetime import date, timedelta
>>>>>>> Stashed changes

def graph_scatterplot(input_data, title_name):
    ''' This function graphs a plotly.express.scatter_mapbox() type with a dictionary
    of inputted plot points.
    inputs:
        input_data:dict - a dictionary with types 'lat', 'lon', 'sizes', 'text', 'comment', 'Food Resources'
        title_name:str - a string that pertains to the title of the given graph 
    '''
    
    fig = px.scatter_mapbox(input_data, lat="Latitude", lon="Longitude", title=title_name, 
<<<<<<< Updated upstream
        height=650, width=1200, zoom=14.4, hover_name="Event Title",  # Use "Event Title" for hover name
=======
        height=650, width=1200, zoom=14.4, hover_name="Event Title",  # Using "Event Title" for hover name
>>>>>>> Stashed changes
        hover_data={"Description": True, 
                    "Start Time": True, "End Time": True, 
                    "Location": True,
                    "Organizer(s)": True, 
<<<<<<< Updated upstream
                    "Date": True, 
                    "Food Resources": False,
                    "sizes": False, 
                    "Latitude": False, 
                    "Longitude": False}, 
        size='sizes', color="Food Resources", color_continuous_scale="red", labels={'Description':''},
        custom_data=["Description", "Start Time", "End Time", "Location", "Organizer(s)", "Date"]) 
=======
                    "Formatted Date": True, 
                    "sizes": False, 
                    "Latitude": False, 
                    "Longitude": False}, 
        size='sizes', color_continuous_scale="red", labels={'Description':''},
        custom_data=["Description", "Start Time", "End Time", "Location", "Organizer(s)", "Formatted Date"]) 
>>>>>>> Stashed changes

    fig.update_traces(hovertemplate='<b>%{customdata[4]}</b><br>%{customdata[0]}<br>Start: %{customdata[1]}<br>End: %{customdata[2]}<br>Location: %{customdata[3]}<br>Date: %{customdata[5]}')

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})
    
    fig.show()

<<<<<<< Updated upstream
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
=======
def create_dict_from_dataframe(df):
    # Clean coordinates and break strings for Description and Event Title within DataFrame
    df.loc[:, 'Latitude'] = df['Latitude'].apply(clean_coordinate)
    df.loc[:, 'Longitude'] = df['Longitude'].apply(clean_coordinate)
    df.loc[:, 'Description'] = df['Description'].apply(lambda x: database.break_str(x, 35))
    df.loc[:, 'Event Title'] = df['Event Title'].apply(lambda x: database.break_str(x, 35))
    df.loc[:, 'Date'] = df['Date'].dt.strftime('%B %d, %Y')
    
    # Add a sizes column with a constant size for all points
    df.loc[:, 'sizes'] = 8
    
    # Convert the DataFrame to a dictionary for plotting
    plot_dict = df[['Latitude', 'Longitude', 'sizes', 'Description', 'Event Title', 'Start Time', 'End Time', 'Location', 'Organizer(s)', 'Formatted Date']].to_dict(orient='list')
    return plot_dict

def main(date_filter='today'):
    # Get dates
    today = date.today()
    tomorrow = today + timedelta(days=1)
    one_week = today + timedelta(weeks=1)

    # Load data and convert date strings to datetime objects
    df = pd.read_csv('Free_Food_Database.csv')

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # This will convert invalid formats to NaT
    df = df.dropna(subset=['Date'])  # This will drop rows where 'Date' is NaT (not a time)
    df['Formatted Date'] = df['Date'].dt.strftime('%B %d, %Y')  # This creates a new column with formatted dates

    # Clean coordinates and descriptions within DataFrame
    df.loc[:, 'Latitude'] = df['Latitude'].apply(clean_coordinate)
    df.loc[:, 'Longitude'] = df['Longitude'].apply(clean_coordinate)
    df.loc[:, 'Description'] = df['Description'].apply(lambda x: database.break_str(x, 35))
    df.loc[:, 'Event Title'] = df['Event Title'].apply(lambda x: database.break_str(x, 35))
    
    # Add a sizes column with a constant size for all points
    df.loc[:, 'sizes'] = 8

    # Define the date filter based on the input parameter
    if date_filter == 'today':
        df_filtered = df[df['Date'] == pd.Timestamp(today)]
    elif date_filter == 'tomorrow':
        df_filtered = df[df['Date'] == pd.Timestamp(today + timedelta(days=1))]
    elif date_filter == 'week':
        df_filtered = df[(df['Date'] >= pd.Timestamp(today)) & (df['Date'] <= pd.Timestamp(today + timedelta(weeks=1)))]
    else:
        df_filtered = df  # If no filter is specified, default to showing all events

    # Prepare the data for plotting
    plot_data = create_dict_from_dataframe(df_filtered)
    
    # Plot the data
    graph_scatterplot(plot_data, "Food Resources on Specific Date")
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()
