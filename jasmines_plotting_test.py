# using code from https://plotly.com/python/mapbox-layers/ 

import pandas as pd
us_cities = pd.read_csv("./test.csv")

import plotly.express as px # only import!

fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()