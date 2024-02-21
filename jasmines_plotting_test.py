# using code from https://plotly.com/python/mapbox-layers/  
# requires three imports - plotly, kaleido and pandas. plotly requires pandas to work. kaleido is to export the graphs as images.

import pandas as pd
from PIL import Image
img = Image.open("testimport.png") # because using it as background
source="https://raw.githubusercontent.com/empet/Datasets/master/Images/sun-flower.jpg"
us_cities = pd.read_csv("./testlocations.csv")

import plotly.express as px 
# these are the settings to get exactly the campus and same frame every time (if only the png thing worked)
fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", color_discrete_sequence=[us_cities.Color], height=300, width=400, size=us_cities.sizes,center={"lat": 44.0436082, "lon":-123.0716908}, zoom=14.1)

#'open-street-map' would work, but since I have to use kaleido, only white-bg works so I have to use a static image
fig.update_layout(mapbox_style='open-street-map')#, 
'''
mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": 'raster', #was 'raster'
            "sourceattribution": "",#University of Oregon Campus Map",
            "source": [img]
        }
      ])

fig.add_layout_image(
        dict(
            source=img,
            sizing="stretch",
            opacity=0.5,
            layer="below"
            )
)


fig.update_mapboxes(
            layers=[{
                'below': 'traces',
                'sourcetype': 'raster',
                'source': [img]
            }],
            #style='white-bg'
) 
'''

# making it fit the screen
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_image("testfile.png")
fig.show()