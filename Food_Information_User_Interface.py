# CustomTkinter was made by Tom Schimansky,
# Documentation here: https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file
import customtkinter as ctk
import tkinter as tk
import csv
from database import filter_events, convert_to_dict, get_all_events
import Resource_Graph
# from tkinter import ttk
# from tkinter import filedialog
# from PIL import ImageTk, Image

csv_file_path = 'Free_Food_Database.csv'

#######################################################################
# Test customtkinter
#######################################################################

# Create Dollarless Dining application window
# This CTk window inherets from the Tk window
window = ctk.CTk() 
window.title('Dollarless Dining')
window.geometry('444x444')

# Create widgets for the application
# Split into multiple lines for readability.

#######################################################################
# Light Mode and Dark Mode Buttons
#######################################################################

# Note capitalization of 'CTkButton'
light_mode_button = ctk.CTkButton(
    window, # 'window' is master
    text = '☀',
    width = 6,
    command = lambda: ctk.set_appearance_mode('light'))
light_mode_button.pack()

dark_mode_button = ctk.CTkButton(
    window, 
    text = '☾',
    width = 6,
    # fg_color = ('black', 'grey'),
    # hover_color = ('grey', 'white'),
    command = lambda: ctk.set_appearance_mode('dark'))
dark_mode_button.pack()

#######################################################################

<<<<<<< Updated upstream
# Test and implement 'Today button'
today_button = ctk.CTkButton(
    window, 
    text = 'Today',
    command = lambda: print('The Today Button was pressed.')) #FIXME Get from Max
today_button.pack()

# Test and implement 'Tomorrow button'
tomorrow_button = ctk.CTkButton(
    window, 
    text = 'Tomorrow',
    command = lambda: print('The Tomorrow Button was pressed.')) #FIXME Get from Max
tomorrow_button.pack()
=======
# Functions to handle button clicks
def filter_today():
    Resource_Graph.main('today')

def filter_tomorrow():
    Resource_Graph.main('tomorrow')

def filter_this_week():
    Resource_Graph.main('week')

# Buttons in the GUI
today_button = ctk.CTkButton(window, text='Today', command=filter_today)
tomorrow_button = ctk.CTkButton(window, text='Tomorrow', command=filter_tomorrow)
this_week_button = ctk.CTkButton(window, text='This Week', command=filter_this_week)

today_button.pack(pady=5)
tomorrow_button.pack(pady=5)
this_week_button.pack(pady=5)
>>>>>>> Stashed changes

#######################################################################

scrollable_frame_food_list = ctk.CTkScrollableFrame(
    window,
    label_text = 'UO Free Food Resources'
    )
scrollable_frame_food_list.pack()

#######################################################################

# Function to populate the scrollable frame with data
def populate_scrollable_frame():
    # Retrieve all events
    events = get_all_events(csv_file_path)
    
    # Clear existing data in the scrollable frame
    for widget in scrollable_frame_food_list.winfo_children():
        widget.destroy()
    
    # Create a new widget for each event
    for event in events:
        event_label = ctk.CTkLabel(scrollable_frame_food_list, text=event['Event Title'])
        event_label.pack()

# Call the populate function to initially populate the frame
populate_scrollable_frame()

# Function to handle View Map button click
def on_view_map_click():
    # placeholder values:
    date = "February 20 2024"
    start_time = "5:00 PM"
    end_time = "7:00 PM"
    
    # Path to CSV file
    csv_file_path = 'Free_Food_Database.csv'
    
    # Filter events and convert to dictionary
    filtered_df = filter_events(csv_file_path, date, start_time, end_time)
    event_dict = convert_to_dict(filtered_df)
    
    # Here, pass event_dict to plotting function
    # plot_events(event_dict)  # This function should handle the plotting
    
    print(event_dict)  # Placeholder to show the dictionary in the console

#######################################################################
# Our 'View Map' Button 
#    Brings you to a page with the interactive map
#######################################################################

view_map_popup_button = ctk.CTkButton(
    window,
    text = 'View Map',
    command = lambda: Resource_Graph.main()
)
view_map_popup_button.pack()

# run
window.mainloop()
