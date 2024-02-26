"""
Grapher to display free food resources around UO (as well as eugene, if development goes there)
"""
import plotly.express as px 
from database import get_all_events

def graph_scatterplot(input_data, title_name):
    ''' This function graphs a plotly.express.scatter_mapbox() type with a dictionary
    of inputted plot points.
    inputs:
        input_data:dict - a dictionary with types 'lat', 'lon', 'sizes', 'text', 'comment', 'Food Resources'
        title_name:str - a string that pertains to the title of the given graph 
    '''
    fig = px.scatter_mapbox(input_data, lat="Latitude", lon="Longitude", title=title_name,
        height=650, width=1200, zoom=14.4, hover_name="Event Title",
        hover_data={
            "Description": True,
            "Date": True,
            "Location": True,
            "Organizer(s)": True,
            "sizes": False,
            "Latitude": False,
            "Longitude": False
        },
        size='sizes', color="Event Title", color_continuous_scale="red", labels={'Description':''})

    fig.update_traces(hoverinfo='text', hovertemplate='%{hovertext}')

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})

    fig.show()

def clean_coordinate(value):
    if isinstance(value, str):
        # Remove semicolon and any other non-numeric characters (except for the decimal point)
        clean_value = ''.join(c for c in value if c.isdigit() or c == '.')
        return float(clean_value) if clean_value else None
    else:
        # If value is already a float (or other non-string), return it directly
        return value

def main():
    # Call the get_all_events function from database.py to fetch event data
    event_data = get_all_events('Free_Food_Database.csv')
    
    for event in event_data:
        # Convert lat and lon values to float
        event['Latitude'] = clean_coordinate(event['Latitude']) if event['Latitude'] is not None else None
        event['Longitude'] = clean_coordinate(event['Longitude']) if event['Longitude'] is not None else None

    graph_scatterplot(event_data, "Food Resources on Specific Date")

    return 0

if __name__ == "__main__":
    main()
