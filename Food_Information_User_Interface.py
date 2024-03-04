#######################################################################
#                                                                     # 
# Food Information User Interface                                     #   
# Update upon completion                                              #
#                                                                     # 
#######################################################################

# CustomTkinter was made by Tom Schimansky,
# Documentation here: https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file
import customtkinter as ctk
import tkinter as tk
import csv
from database import get_all_events, run_map
import Resource_Graph

# Below, imports which may be needed in the future
# from tkinter import ttk
# from tkinter import filedialog
# from PIL import ImageTk, Image

csv_file_path = 'Free_Food_Database.csv'

#######################################################################
# Main Canvas Section
#######################################################################

# Create Dollarless Dining application window
# This CTk window inherets from the Tk window
window = ctk.CTk() 
window.title('Dollarless Dining')
window.geometry('777x777')

# Commented out to go for consistent user interface idk
# header_label = ctk.CTkLabel(
#     window,
#     text='Dollarless Dining',
#     font=('Helvetica', 25, 'bold'),
#     bg_color='pink')
# header_label.pack(fill=tk.X)  # fill=tk.X expands the label horizontally

#######################################################################
#                                                                     # 
# Interface Section                                                   #   
#                                                                     #
#######################################################################

# Left Frame
left_frame = ctk.CTkFrame(window, width=300)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

# Right Frame 
#right_frame = ctk.CTkFrame(window)
#right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

#######################################################################
#
# Widgets Section:
#
#######################################################################

#######################################################################
# Light Mode and Dark Mode Buttons
#######################################################################

# Create a frame for the appearance mode header and buttons
mode_frame = ctk.CTkFrame(left_frame)

# Light Mode and Dark Mode Buttons
light_mode_button = ctk.CTkButton(mode_frame, text='☀', width=6, command=lambda: ctk.set_appearance_mode('light'))
light_mode_button.pack(side=tk.LEFT, padx=5, pady=5)

dark_mode_button = ctk.CTkButton(mode_frame, text='☾', width=6, command=lambda: ctk.set_appearance_mode('dark'))
dark_mode_button.pack(side=tk.LEFT, padx=5, pady=5)

mode_frame.pack(side=tk.TOP, padx=10, pady=10)

#######################################################################
# Today and Tomorrow Buttons
#######################################################################

# Today and Tomorrow Buttons
today_button = ctk.CTkButton(
    left_frame, 
    text='Today',
    command=lambda: print('The Today Button was pressed.')
)
today_button.pack(pady=5)

tomorrow_button = ctk.CTkButton(
    left_frame, 
    text='Tomorrow',
    command=lambda: print('The Tomorrow Button was pressed.')
)
tomorrow_button.pack(pady=5)

#######################################################################
# Scrolling List of Free Food Resources
#######################################################################

# FIXME Simone wants to implement text wrapping with 'textbox' (not 
# Critical Path).

scrollable_frame_food_list = ctk.CTkScrollableFrame(
    #right_frame
    window, 
    label_text = 'UO Free Food Resources',
    width = 555
    )
scrollable_frame_food_list.pack(pady=5)

# Function to populate the scrollable frame with data
def populate_scrollable_frame():
    # Retrieve all events
    events = get_all_events(csv_file_path)

    # Clear existing data in the scrollable frame
    for widget in scrollable_frame_food_list.winfo_children():
        widget.destroy()

    for event in events:
        event_text = event['Event Title']

        # Create the Tkinter Text widget
        event_textbox = tk.Text(scrollable_frame_food_list, wrap=tk.WORD, width=60, height=2)
        event_textbox.insert(tk.END, event_text)  # Insert the text into the Text widget
        event_textbox.pack()

# Call the populate function to initially populate the frame
populate_scrollable_frame()

#######################################################################
#                                                                     #
# Additional Resources Section                                        #
#                                                                     #
#######################################################################

#######################################################################
# Additional Resources Button from Main to Pop-Up
#######################################################################

def show_resource_list():
    resource_list_window = ctk.CTkToplevel()
    resource_list_window.title('Additional Resources')
    resource_list_window.geometry('333x333')
    resource_list_window.resizable(False, False)  # width, height are constant

    # Create a Label to display additional resources
    resource_label = ctk.CTkLabel(resource_list_window, text="Additional Resources:")
    resource_label.pack(padx=10, pady=10)

    # Insert some sample text into the Label
    sample_text = """
    1. Resource 1
    - Description 1

    2. Resource 2
    - Description 2

    3. Resource 3
    - Description 3
    """
    resource_text = ctk.CTkLabel(resource_list_window, text=sample_text, wraplength=300)
    resource_text.pack(padx=10, pady=10)

    # Create an instance of CTkToplevel for focus management
    toplevel_window = None

    resource_list_window.mainloop()

# Additional Resources Button
resource_button = ctk.CTkButton(left_frame, text='Additional Resources', command=show_resource_list) 
resource_button.pack(pady=5)


#######################################################################
#                                                                     #
# User Input Section - Admin module                                   #
#                                                                     #
#######################################################################

#######################################################################
# Create dictionary to append user's New Event to the csv.
#######################################################################

new_event = {'title': '',
             'date': '',
             'start_time': '',
             'end_time': '',
             'loc': '',
             'desc': '',
             'org': ''}

#######################################################################
# Input Submission Button Functionality
#######################################################################

#FIXME Simone's current critical path is getting this to work :)

def submit_form():
    event_title = {event_title_input.get()}
    date = {date_input.get()}
    start_time = {start_time_input.get()}
    end_time = {end_time_input.get()}
    loc = {location_input.get()}
    desc = {description_input.get()}
    org = {organizers_input.get()}

    # Create New Event as a dictionary 
    new_event['title'] = event_title
    new_event['date'] = date
    new_event['start_time'] = start_time
    new_event['end_time'] = end_time
    new_event['location'] = loc
    new_event['desc'] = desc
    new_event['organizers'] = org

    event_title_input.delete()
    date_input.delete()
    start_time_input.delete()
    end_time_input.delete()
    location_input.delete()
    description_input.delete()
    organizers_input.delete()

    return(new_event)

#######################################################################
# User Input Event Entry Fields
#######################################################################

def show_user_input_window():
    # Set up New Event User Input Window
    user_input_window = ctk.CTkToplevel(window)
    user_input_window.title('New Event')
    user_input_window.geometry('555x555')

    # Make a frame to hold all input boxes
    inputs_frame = ctk.CTkFrame(
        user_input_window, 
        width = 4555,
        height = 455)
    inputs_frame.pack(padx=10, pady=10)

    #######################################################################
    # Input Boxes Configuration
    #######################################################################

    # Event Title
    event_title_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="Event Title",
        #corner_radius=50 If you want it to be round.
        # width=50,
        )
    event_title_input.pack(padx=10, pady=10)

    # Date
    date_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="Date (i.e. March 26 2024)")
    date_input.pack(padx=10, pady=10)

    # Start Time
    start_time_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="Start Time (i.e. 1:00 PM)")
    start_time_input.pack(padx=10, pady=10)

    # End Time (Optional)
    end_time_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="End Time (i.e. 4:00 PM)")
    end_time_input.pack(padx=10, pady=10)

    # Organizer(s)
    organizers_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="Organizer(s) (i.e. Women in Computer Science)")
    organizers_input.pack(padx=10, pady=10)

    # Location (Street, City, State)
    location_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="Location (i.e. Knight Library, 122 DREAM Lab 1501 Kincaid Street, Eugene, OR)")
    location_input.pack(padx=10, pady=10)

    # Description
    desc_input = ctk.CTkEntry(
        inputs_frame,
        placeholder_text="Description")
    desc_input.pack(padx=10, pady=10)

#######################################################################
# Input Submission Button
#######################################################################

    submit_form = ctk.CTkButton(
        inputs_frame,
        text="Submit Event"
        #command=submit_form
    )
    submit_form.pack(padx=5, pady=5)

#######################################################################
# Add New Event Button on Main Window - Admin mode
#######################################################################
    
new_event_button = ctk.CTkButton(left_frame, text='Admin Mode', command=show_user_input_window) 
new_event_button.pack(side='bottom', anchor='w', padx=10, pady=10)

#######################################################################
#                                                                     # 
# Map Section                                                         #   
#                                                                     #
#######################################################################

#######################################################################
# Our 'View Map' Button brings you to a page with the interactive map
#######################################################################

view_map_popup_button = ctk.CTkButton(
    left_frame,
    text = 'View Map',
    command = lambda: Resource_Graph.main()
)
view_map_popup_button.pack(pady=5)

#######################################################################
# View Map Function
#######################################################################

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
    event_dict = run_map(filtered_df, None, None)
    
    # Here, pass event_dict to plotting function
    # plot_events(event_dict)  # This function should handle the plotting
    
    print(event_dict)  # Placeholder to show the dictionary in the console


#######################################################################
# About Pop-up Button
#######################################################################

def show_about_popup():
    about_text = """
    Dollarless Dining

    This program helps you discover free food resources on campus.

    Developed by Simone, Nithi, Max, Jasmine, Kylie

    Copyright © 2024 University of Oregon
    """

    about_popup = ctk.CTkToplevel(window)
    about_popup.title('About Dollarless Dining')
    about_popup.geometry('300x200')

    about_label = ctk.CTkLabel(about_popup, text=about_text, wraplength=280)
    about_label.pack(padx=10, pady=10)

# Add the About button
about_button = ctk.CTkButton(left_frame, text='About', command=show_about_popup)
about_button.pack(pady=5)


#######################################################################
#                                                                     # 
# Run canvas                                                          #   
#                                                                     #
#######################################################################

window.mainloop()