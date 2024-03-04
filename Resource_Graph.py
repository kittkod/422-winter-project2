"""
Grapher to display free food resources around UO (as well as eugene, if development goes there)
"""
import plotly.express as px 
import pandas as pd
import database
import webbrowser
import tempfile

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

    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>' +  # Event Title
                  '%{customdata[1]}<br>' +                      # Description
                  'Time: %{customdata[2]}<br>' +                # Time
                  'Location: %{customdata[3]}<br>' +            # Location
                  'Organizer: %{customdata[4]}<br>' +           # Organizer
                  'Date: %{customdata[5]}<extra></extra>')      # Date

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":70,"l":40,"b":0})

    # Convert to an HTML div string
    graph_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Define custom HTML string with buttons
    custom_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title_name}</title>
    </head>
    <body>
        <div style="margin: 20px;">
            <button onclick="alert('Filtering for today\'s events')">Today</button>
            <button onclick="alert('Filtering for tomorrow\'s events')">Tomorrow</button>
            <button onclick="alert('Filtering for this week\'s events')">This Week</button>
        </div>
        {graph_div}
        <script>
            // Add any JavaScript needed to handle button clicks
        </script>
    </body>
    </html>
    """

    # Write the HTML content to a temporary file and open it in the default web browser
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(custom_html)
    webbrowser.open(url)

def main():
    event_dict = database.run_map('Free_Food_Database.csv', '2/2/24', '2/5/24')
    graph_scatterplot(event_dict, "Food Resources on Specific Date")

if __name__ == "__main__":
    main()