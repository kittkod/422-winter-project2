#######################################################################
# Resource_Graph.py                                                   #
# created: 2/22/24                                                    # 
# Authors: Jasmine Wallin and Max Hermens                             #
#                                                                     #
# Description: This file creates a map with the use of plotly.express #
# with data points from a dictionary created with the                 #
# Free_Food_Database.csv file.                                        #                             
#                                                                     #
# Interactions:                                                       #
# - database.py: This file needs the run_map() function from          #
#   database.py to create the dictionary of scatterplot points that   #
#   graph_scatterplot needs.                                          #
####################################################################### 

import plotly.express as px # used for creating the plot/map
import pandas as pd # creates a dataframe object from dictionary
import database # needed for run_map function to create dictionary


# function to create the map with plotly.express.scatter_mapbox()
def graph_scatterplot(input_data, title_name):
    ''' This function graphs a plotly.express.scatter_mapbox() type with a dictionary
    of inputted plot points.
    inputs:
        input_data:dict - a dictionary with types 'lat', 'lon', 'sizes', 'text', 'comment', 'Food Resources'
        title_name:str - a string that pertains to the title of the given graph 
    '''
    # Convert input_data to a DataFrame first
    df = pd.DataFrame(input_data)
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", title=title_name, height=650, width=1200, zoom=10.5, text="comment",
                            hover_data={
                                "comment": True,
                                "text": True,
                                "Time": True,
                                "Location": True,
                                "Organizer": True,
                                "Date": True,
                                "Food Resources": False,
                                "sizes": False,
                                "lat": False,
                                "lon": False},
                            size='sizes', color="Food Resources", color_continuous_scale="red", labels={'text':''})

    # formatting the text boxes for each mark
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>' +  # Event Title
                  '%{customdata[1]}<br>' +                           # Description
                  'Time: %{customdata[2]}<br>' +                     # Time
                  'Location: %{customdata[3]}<br>' +                 # Location
                  'Organizer: %{customdata[4]}<br>' +                # Organizer
                  'Date: %{customdata[5]}<extra></extra>')           # Date

    # formatting the map screen
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})

    fig.show()

def run_map_function(input_button):
    ''' connect the creation of the dictionary to creating the map.
    inputs: input_button:str - a string of 'today', 'tomorrow', 'this week' or 'next week'
                         for database.run_map()
    '''
    # event_dict : the dictionary created from run_map()
    # mapname : the string of the name of the map
    event_dict, mapname = database.run_map("./dollarless_database_files/Free_Food_Database.csv", input_button)
    graph_scatterplot(event_dict, mapname)
    
def main():
    # soley for testing
    run_map_function('today')

if __name__ == "__main__":
    main()