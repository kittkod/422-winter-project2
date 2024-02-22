# import CustomTkinter module for GUI
# CustomTkinter was made by Tom Schimansky,
# Documentation here: https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file
import customtkinter as ctk
import tkinter as tk
import csv
from database import filter_events, convert_to_dict, get_all_events
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

label = ctk.CTkLabel(
    window,  
    corner_radius = 5) # rounded-rectangle effect
label.pack() # placing widget on window with layout method 'pack'

#######################################################################
# Light Mode and Dark Mode Buttons
#######################################################################

# Note capitalization; 'window' is master
light_mode_button = ctk.CTkButton(
    window, 
    text = '☀',
    # fg_color = ('black', 'grey'),
    # hover_color = ('grey', 'white'),
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

view_map_popup_button = ctk.CTkButton(
    window,
    text = 'View Map',
    command=on_view_map_click
    #FIXME command to go to map goes here! <3
)

view_map_popup_button

#######################################################################
#######################################################################
#######################################################################

# run
window.mainloop()
