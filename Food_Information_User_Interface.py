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
from utils import get_all_events
from database import run_map
import Resource_Graph
import admin_intake_form

import webbrowser
import pandas as pd

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
window.geometry('850x700')

#######################################################################
#                                                                     # 
# Interface Section                                                   #   
#                                                                     #
#######################################################################

#######################################################################
# Left Frame - for various buttons
#######################################################################

left_frame = ctk.CTkFrame(window, width=300)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

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

mode_frame.pack(side=tk.TOP, padx=5, pady=5)

#######################################################################
# Today and Tomorrow Buttons
#######################################################################

today_button = ctk.CTkButton(
    left_frame, 
    text='Today',
    #TODO: when the button is pressed, it stores the 'today' value in a global variable that can be accessed by another function.
    command=lambda: print('The Today Button was pressed.')
)
today_button.pack(pady=5)

tomorrow_button = ctk.CTkButton(
    left_frame, 
    text='Tomorrow',
    #TODO: same as above
    command=lambda: print('The Tomorrow Button was pressed.')
)
tomorrow_button.pack(pady=5)

#######################################################################
# Scrolling List of Free Food Resources
#######################################################################

# FIXME implement text wrapping without 'textbox' (it is editable unfortunately)
# instead, let's use 'CTkLabel'

scrollable_frame_food_list = ctk.CTkScrollableFrame(
    window, 
    label_text = 'UO Free Food Resources',
    width = 450
    )
scrollable_frame_food_list.pack(anchor="n", pady=5, expand=True)

# Function to populate the scrollable frame with data
def populate_scrollable_frame():
    #TODO: the get_all_events second argument is the global variable that stores words like 'today' based on button input
    # Retrieve all events
    events = get_all_events(csv_file_path, 'all') # second argument can be 'all', 'today', 'tomorrow','this week' or 'next week'

    # Clear existing data in the scrollable frame
    for widget in scrollable_frame_food_list.winfo_children():
        widget.destroy()

    for event in events:
        event_text = event['Event Title'] #+ '-' + event['Date']

        # Create the Tkinter Text widget 
        event_textbox = tk.Text(scrollable_frame_food_list, wrap=tk.WORD, width=60, height=2)
        event_textbox.insert(tk.END, event_text)  # Insert the text into the Text widget
        event_textbox.pack()

        # #FIXME CHANGING THE ABOVE TO CTkLabel instead
        # event_label = ctk.CTkLabel(scrollable_frame_food_list, text=event_text)
        
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
    resource_list_window.title('Online Resources')
    resource_list_window.geometry('666x666')
    resource_list_window.resizable(False, False)  # width, height are constant

    # Create a Label to display additional resources
    resource_label = ctk.CTkLabel(resource_list_window, text="Online Resources", font=("bold", 30))
    resource_label.pack(padx=10, pady=10)

    # Create a Text widget to display sample text with hyperlinks
    resource_text = tk.Text(resource_list_window, wrap=tk.WORD, height=20, width=80)
    resource_text.pack(padx=10, pady=10)

    # Insert text into the Text widget
    description_text = """
    1. 211info: 
        More than 1,000 food services in Oregon and Southwest Washington, such as food pantries, farmers markets, community gardens, fresh food distribution, and summer feeding programs for children, are listed and referred to by 211info.

    2. UOregon Engage: 
        Shows all the events that the University of Oregon organizes for thier students!

    3. FOOD FOR LANE COUNTY:
        FOOD For Lane County is committed to getting fruits and vegetables to community members who cannot typically afford such nutritious food. This is part of the solution to fighting both hunger and obesity and establishing positive lifelong eating habits.

        - Meal Sites:
            The meal sites are dedicated to providing hot and nutritious meals to individuals in need. 
        
        - Mobile Food Pantry:
            Mobile Pantry will provide a three- to five-day supply of nutritionally balanced groceries. 

        - Trillium Produce Plus
            Trillium Produce Plus brings high-quality fresh fruits and vegetables to people in need at community and neighborhood locations free of charge.

    4. UOregon Basic Needs Program:
        Provides people, espeically students, a list of resources to get free food!

    5. Burrito Brigade: Waste to Taste - Free Food Boxes
        Waste to Taste is a food rescue and free food box program through Burrito Brigade. We work in collaboration with local grocery stores, bakeries, restaurants, and farms to rescue food and redistribute it to the community.

    6. SNAP Food Benefits
        SNAP is a federal program that provides individuals and families with financial support that can be used to purchase a variety of foods. 

    7. UOregon Leftover Textover
        The Leftover Textover program alerts current UO students via text message when leftover, free food is available on campus. These leftover portions come from campus events where food was ordered from UO Catering, but not all of it was consumed. 
   
    """

    # Add sample text with hyperlinks
    resource_text.insert(tk.END, description_text)

    # Create an instance of CTkToplevel for focus management
    toplevel_window = None

    #to show the full list
    resource_label2 = ctk.CTkLabel(resource_list_window, text="Can be used without wifi", font=("bold", 20))
    resource_label2.pack()

    # Create a button to open a new popup with the list
    open_list_button = ctk.CTkButton(resource_list_window, text='Open List', command=lambda: show_list_popup(description_text), fg_color="#7e57c2")
    open_list_button.pack(pady=1)

    # Full list as buttons to be used with wifi
    resource_label1 = ctk.CTkLabel(resource_list_window, text="Only can be used with wifi!", font=("bold", 20))
    resource_label1.pack()

    # Create a frame to contain the wifi buttons in a grid
    wifi_frame = ctk.CTkFrame(resource_list_window)
    wifi_frame.pack()

    # Create a dictionary with button text and corresponding URLs
    wifi_buttons_data = {
        '211info': 'https://www.211info.org/get-help/food/',
        'UOregon Engage': 'https://uoregon.campuslabs.com/engage/events?categories=16973',
        'Food for Lane County: Meal Sites': 'https://www.foodforlanecounty.org/find-a-meal-site/',
        'Food for Lane County: Mobile Food Pantry': 'https://www.foodforlanecounty.org/mobile-pantry/',
        'Food for Lane County: Trillium Produce Plus': 'https://www.foodforlanecounty.org/get-help/trillium-produce-plus/',
        'UOregon Basic Needs Program': 'https://basicneeds.uoregon.edu/food',
        'UOregon Free Food Events': 'https://calendar.uoregon.edu/search/events?event_types[]=15630',
        'Burrito Brigade: Waste to Taste - Free Food Boxes': 'https://burritobrigade.org/waste-to-taste/',
        'SNAP Food Benefits': 'https://www.oregon.gov/odhs/food/pages/snap.aspx',
        'UOregon Leftover Textover': 'https://emu.uoregon.edu/leftover-textover',
    }

    # Create buttons in a grid
    for row, (button_text, url) in enumerate(wifi_buttons_data.items()):
        button = ctk.CTkButton(wifi_frame, text=button_text, command=lambda u=url: webbrowser.open(u),  fg_color="#9c27b0")
        button.grid(row=row // 2, column=row % 2, padx=5, pady=5)

    resource_list_window.mainloop()


# Function to show a popup with a list
def show_list_popup(text):
    list_popup = ctk.CTkToplevel()
    list_popup.title('Resource List')
    list_popup.geometry('500x500')

    list_label = ctk.CTkLabel(list_popup, text="Resource List:")
    list_label.pack(padx=10, pady=10)

    # Create a Text widget to display sample text with hyperlinks
    resource_text = tk.Text(list_popup, wrap=tk.WORD, height=20, width=80)
    resource_text.pack(padx=10, pady=10)

    # Insert text into the Text widget
    sample_text = """
    1. 211info
    - Link: 
        https://www.211info.org/get-help/food/

    2. UOregon Engage
    - Link: 
        https://uoregon.campuslabs.com/engage/events?categories=16973

    3. Food for Lane County
    - Meal Sites: 
        https://www.foodforlanecounty.org/find-a-meal-site/

    - Mobile Food Pantry: 
        https://www.foodforlanecounty.org/mobile-pantry/ 

    - Trillium Produce Plus: 
        https://www.foodforlanecounty.org/get-help/trillium-produce-plus/ 

    4. UOregon Basic Needs Program
    - Link: 
        https://basicneeds.uoregon.edu/food

    5. UOregon Free Food Events
    - Link: 
        https://calendar.uoregon.edu/search/events?event_types[]=15630

    6. Burrito Brigade: Waste to Taste - Free Food Boxes
    - Link: 
        https://burritobrigade.org/waste-to-taste/ 

    7. SNAP Food Benefits:
    - Link: 
        https://www.oregon.gov/odhs/food/pages/snap.aspx

    8. UOregon Leftover Textover:
    - Link: 
        https://emu.uoregon.edu/leftover-textover 
    """

    # Add sample text with hyperlinks
    resource_text.insert(tk.END, sample_text)

    # Create an instance of CTkToplevel for focus management
    toplevel_window = None

    list_popup.mainloop()

# Additional Resources Button
resource_button = ctk.CTkButton(left_frame, text='Additional Resources', command=show_resource_list) 
resource_button.pack(pady=5)


#######################################################################
#                                                                     #
# User Input Section                                                  #
#                                                                     #
#######################################################################

#######################################################################
# Create dictionary to append user's New Event to the csv.
#######################################################################


#######################################################################
# Input Submission Button Functionality
#######################################################################

#######################################################################
# User Input Event Entry Fields
#######################################################################

def show_user_input_window():
    # Set up New Event User Input Window
    user_input_window = ctk.CTkToplevel(window)
    user_input_window.title('')
    user_input_window.geometry('555x555')

    # title and description
    text_var = ctk.StringVar(value="Add New Event")
    label = ctk.CTkLabel(user_input_window,
                               textvariable=text_var,
                               width=120,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
    label.configure(font = ("TkDefaultFont", 25))
    desc = ctk.CTkLabel(user_input_window, text="Input a new Free Food resource into our database. \nAll resources inputted by admins will be reviewed prior to being displayed.")
    label.pack(pady=20)
    desc.pack()

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

    ############################################################
    # Input Submission Button
    ############################################################
    new_event = {'title': '',
             'date': '',
             'start_time': '',
             'end_time': '',
             'loc': '',
             'desc': '',
             'org': ''}

#######################################################################
# Input Submission Button
#######################################################################

    def my_function():
        event_title = event_title_input.get()
        date = date_input.get()
        start_time = start_time_input.get()
        end_time = end_time_input.get()
        organizers = organizers_input.get()
        location = location_input.get()
        desc = desc_input.get()
        new_event['title'] = str(event_title)
        new_event['date'] = str(date)
        new_event['start_time'] = str(start_time)
        new_event['end_time'] = str(end_time)
        new_event['location'] = str(location)
        new_event['desc'] = str(desc)
        new_event['organizers'] = str(organizers)
        event_title_input.delete(0, len(event_title))
        date_input.delete(0, len(date))
        start_time_input.delete(0, len(start_time))
        end_time_input.delete(0, len(end_time))
        location_input.delete(0, len(location))
        desc_input.delete(0, len(desc))
        organizers_input.delete(0, len(organizers))
        admin_intake_form.add_to_admin_file(new_event) 
        succ = ctk.CTkToplevel()
        succ.geometry("300x100")
        succ.configure(bg="gray92")
        succ.wm_title("Success")
        l = ctk.CTkLabel(succ, text="'" + event_title + "' has been added and \nis waiting to be approved.")
        l.pack(padx=20, pady=10)

    submit_form = ctk.CTkButton(
        inputs_frame,
        text="Submit Event",
        command=lambda:my_function()
    )
    submit_form.pack(padx=5, pady=5)

    # Create a button to close the popup window
    close_button = ctk.CTkButton(show_user_input_window, text='Close', command=show_user_input_window.destroy())
    close_button.pack(pady=5)

#######################################################################
#                                                                     #
# Admin mode                                                          #
#                                                                     #
#######################################################################

# Function to handle the "Add New Event" button click
def on_add_new_event_click():
    show_user_input_window()

# Function to handle the "Refresh Data" button click
def on_refresh_data_click():
    populate_scrollable_frame()

def on_delete_data_click():
    # Load the admin_info.csv file into a DataFrame
    admin_df = pd.read_csv('admin_info.csv')

    # Create a new popup window to display the contents
    delete_data_popup = ctk.CTkToplevel(window)
    delete_data_popup.title('Admin Data Contents')
    delete_data_popup.geometry('600x400')

    # Create a Text widget to display the contents
    contents_text = tk.Text(delete_data_popup, wrap=tk.WORD, height=20, width=50)
    contents_text.pack(padx=10, pady=10)

    # Insert the contents into the Text widget
    contents_text.insert(tk.END, admin_df.to_string(index=False))

    # Create a button to close the popup window
    close_button = ctk.CTkButton(delete_data_popup, text='Close', command=delete_data_popup.destroy())
    close_button.pack(pady=5)


# Admin mode button
def show_admin_mode_popup():
    admin_mode_popup = ctk.CTkToplevel(window)
    admin_mode_popup.title('Admin Mode')
    admin_mode_popup.geometry('300x200')

    # Add New Event button
    add_new_event_button = ctk.CTkButton(admin_mode_popup, text='Add New Event', command=on_add_new_event_click)
    add_new_event_button.pack(pady=5)

    # Refresh Data button
    refresh_data_button = ctk.CTkButton(admin_mode_popup, text='Refresh Data', command=on_refresh_data_click)
    refresh_data_button.pack(pady=5)

    # Refresh Data button
    delete_data_button = ctk.CTkButton(admin_mode_popup, text='Delete Data', command=on_delete_data_click)
    delete_data_button.pack(pady=5)

    # Create a button to close the popup window
    close_button = ctk.CTkButton(admin_mode_popup, text='Close', command=admin_mode_popup.destroy)
    close_button.pack(pady=5)

# Admin mode button
new_event_button = ctk.CTkButton(left_frame, text='Admin Mode', command=show_admin_mode_popup) 
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
    #TODO: instead of 'next week' the argument should be the global variable that stores things like 'today' made when the button is pressed
    command = lambda:Resource_Graph.run_map_function('next week') # arguments can be 'today', 'tomorrow', 'this week', or 'next week'
)

view_map_popup_button.pack(pady=5)

#######################################################################
# View Map Function
#######################################################################
# TODO: we don't need this function!
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

    This program helps you find free food resources on campus.

    Developed by Simone Badaruddin, Nithi Deivanayagam, Kylie Griffiths, Max Hermens, Jasmine Wallin

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