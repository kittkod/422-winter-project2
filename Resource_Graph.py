"""
Grapher to display free food resources around UO (as well as eugene, if development goes there)
"""
import plotly.express as px 


def graph_scatterplot(input_data, title_name):
    ''' This function graphs a plotly.express.scatter_mapbox() type with a dictionary
    of inputted plot points.
    inputs:
        input_data:dict - a dictionary with types 'lat', 'lon', 'sizes', 'text', 'comment', 'Food Resources'
        title_name:str - a string that pertains to the title of the given graph 
    '''
    fig = px.scatter_mapbox(input_data, lat="lat", lon="lon", title=title_name, 
        height=650, width=1200, zoom=14.6, text="comment", hover_name="comment",
        hover_data={"text":True, "Food Resources":False, "sizes":False, "comment":False, "lat":False, "lon":False}, 
        size='sizes', color="Food Resources", color_continuous_scale="red", labels={'text':''})
    
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})

    fig.show()

def main():
    # replace this test_data in the future with a dictionary from database.py
    test_data = {
    'lat':[44.0430978, 44.04358895589884, 44.04358546139572, 44.0461586, 44.043320, 44.045], 
    'lon': [-123.0670994, -123.07538151741028, -123.07766889687626, -123.0874064, -123.077728, -123.066], 
    'sizes': [8, 8, 8, 8, 8, 8],
    'text': ['there is free pizza today <br>in deschutes hall from 5-7.', 'there is a grocery drop today<br>at the EMU', 'Potatoes at east main', 'Every tuesday from 1-2<br>there is a gardening feast.', 'There is MEAT at the library', 'stuff at MATTHEW!!'],
    'comment': ['Deschutes Hall', 'EMU', '33 east main', 'some place', 'Knight Library', 'Matthew knight'], 
    'Food Resources': ['Free Pizza', 'Grocery Drop', 'Potatoes', 'Gardening Feast', 'Meat', 'stuff']
    }
    graph_scatterplot(test_data, "Test Data Food Resources")

    return 0

if __name__ == "__main__":
    main()
    
'''
fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", title="Map of Food Resources", 
    height=650, width=1200, zoom=14.6, text="comment", hover_name="comment",
    hover_data={"text":True, "Food Resources":False, "sizes":False, "comment":False, "lat":False, "lon":False}, 
    size='sizes', color="Food Resources", color_continuous_scale="red", labels={'text':''})

fig.update_layout(mapbox_style='open-street-map')#, 

# changing spacing from sides of screen - r=right, t=top, l=left, b=bottom
fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})

#fig.write_image("testfile.png") #</3
fig.show()
'''