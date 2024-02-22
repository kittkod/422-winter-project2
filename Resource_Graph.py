"""
Grapher to display free food resources around UO (as well as eugene, if development goes there)
Jasmine Wallin
"""
# requires two imports - plotly and pandas. plotly requires pandas to work. 

import pandas as pd
import plotly.express as px 

us_cities = pd.read_csv("./testlocations.csv")

fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", title="Map of Food Resources", 
    height=650, width=1200, zoom=14.6, text=us_cities.comment, hover_name=us_cities.comment,
    hover_data={"text":True, "Food Resources":False, "sizes":False, "comment":False, "lat":False, "lon":False}, 
    size=us_cities.sizes, color="Food Resources", color_continuous_scale="red", labels={'text':''})

fig.update_layout(mapbox_style='open-street-map')#, 

# changing spacing from sides of screen - r=right, t=top, l=left, b=bottom
fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})

#fig.write_image("testfile.png") #</3
fig.show()