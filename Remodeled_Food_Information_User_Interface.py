#######################################################################
# Remodeled Food Information User Interface                           # 
# Created: TODO                                                       #
# Authors: All team                                                   #
#                                                                     #
# Description/Interactions:                                           #
# TODO                                                                #
# Last Edited: 05/08/2024 by: sb                                      #   
# Log: Added description functionality                                # 
#######################################################################

#######################################################################
# CustomTkinter was made by Tom Schimansky.                           #
# Documentation here:                                                 #
# https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file   #
#######################################################################

import customtkinter as ctk 
import tkinter as tk
from utils import get_all_events, get_title_name
from database import run_map
import admin_intake_form
import Resource_Graph
import pandas as pd
import webbrowser
import refresh_data
from coordinate_finder import coordinate_validity

csv_file_path = './dollarless_database_files/Free_Food_Database.csv'

#######################################################################
# Overall Application Section:                                        #
#                                                                     #
# Description:                                                        #
#   Creates the Dollarless Dining application.                        #   
# Contains:                                                           #   
#   #FIXME List upon completion.                                      #
#######################################################################

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dollarless Dining")
        self.geometry("444x333")
        self.minsize(511, 477)
        self.maxsize(777, 667)

        ###############################################################
        # Create the Grid System for the entire App                   #   
        ###############################################################
        self.grid_columnconfigure((0, 3), 
                                  weight=1)
        self.grid_rowconfigure((0, 1), 
                               weight=1)

        ###############################################################
        # Place Internal Frames onto the Main App Grid System         #   
        ###############################################################
        # Left Sidebar 
        self.l_sidebar = LeftSideBar(self)
        self.l_sidebar.grid(row=0, 
                            column=0, 
                            padx=(5, 0), # padx=(5,0) so that the center isn't spaced by 10 
                            pady=(5, 5),
                            sticky="news",
                            rowspan=2,
                            columnspan=1) 

        # Main Area
        self.main_area = MainArea(self)
        self.main_area.grid(row=0, 
                            column=1, 
                            padx=(5, 5), 
                            pady=(5, 5), 
                            sticky="news",
                            rowspan=3,
                            columnspan=3)

#######################################################################
# Left Sidebar (containing various buttons & modes of operation)      #
#                                                                     #
# Contains:                                                           #   
#   - Light and Dark Appearance Mode Buttons                          #
#   - Administrator Mode Button                                       #
#   - Resources Button                                                #
#   - About Button                                                    #    
#######################################################################
class LeftSideBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Create the Grid System for Left Sidebar                     #   
        ###############################################################
        self.grid_columnconfigure(0,
                                  weight=1)
        self.grid_rowconfigure((0, 1), 
                               weight=1)

        ###############################################################
        # Place Internal Frames onto the Left Sidebar Grid System     #   
        ###############################################################
        # Light and Dark Appearance Mode Frame
        self.appearance_mode_frame = AppearanceModeFrame(self)
        self.appearance_mode_frame.grid(row=0, 
                                        column=0, 
                                        padx=(10, 10), 
                                        pady=(10, 10),
                                        sticky="n")
        
        # Admin Mode Button Frame
        self.admin_mode_frame = AdminModeButton(self)
        self.admin_mode_frame.grid(row=4, 
                                    column=0, 
                                    padx=(5, 5), 
                                    pady=(5, 5), 
                                    sticky="news")

        # Additional Resources Button Frame
        self.resources_button = ResourcesButton(self)
        self.resources_button.grid(row=5, 
                               column=0, 
                               padx=(5, 5), 
                               pady=(5, 5), 
                               sticky="news")

        # About Button Frame
        self.about_button = AboutButton(self)
        self.about_button.grid(row=6, 
                               column=0, 
                               padx=(5, 5), 
                               pady=(5, 5), 
                               sticky="news")

#######################################################################
# Light and Dark Appearance Mode Buttons                              #   
#######################################################################
class AppearanceModeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Create the Grid System for Appearance Mode Frame            #   
        ###############################################################
        self.grid_columnconfigure((0, 1), 
                                  weight=1)
        self.grid_rowconfigure((0), 
                               weight=0)

        ###############################################################
        # Place Light and Dark Mode Buttons onto Mode Grid System     #   
        ###############################################################
        self.light_mode_button = ctk.CTkButton(self, 
                                               text='☀', 
                                               width=5,
                                               command=lambda: ctk.set_appearance_mode('light'))
        self.light_mode_button.grid(row=0, 
                                    column=0, 
                                    padx=5, 
                                    pady=5, 
                                    sticky="ns")

        self.dark_mode_button = ctk.CTkButton(self, 
                                              text='☾', 
                                              width=5, 
                                              command=lambda: ctk.set_appearance_mode('dark'))
        self.dark_mode_button.grid(row=0, 
                                   column=1, 
                                   padx=5, 
                                   pady=5, 
                                   sticky="ns")
        
#######################################################################
# Admin Mode Button                                                   #   
#######################################################################
class AdminModeButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text='Admin Mode',
                         command=self.show_admin_mode_popup)  # Set the command to open admin mode popup
    
    def on_add_new_event_click(self):
        # Set up New Event User Input Window
        user_input_window = ctk.CTkToplevel(self.master)
        user_input_window.title('Add Event')
        user_input_window.geometry('370x373')
        user_input_window.minsize(370, 373)
        user_input_window.maxsize(777, 373)

        # Make a frame to hold all input boxes
        inputs_frame = ctk.CTkFrame(
            user_input_window
        )
        inputs_frame.pack(padx=15, pady=15, fill=tk.BOTH)

        #######################################################################
        # Input Boxes Configuration
        #######################################################################
        # Brief Formatting instructions for administrator inputting new event
        input_new_event_instr = ctk.CTkLabel(
            inputs_frame,
            text = "Input must match form as seen below",
        )
        input_new_event_instr.pack(padx=5, pady=5, fill=tk.X)

        # Event Title
        event_title_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Event Title",
        )
        event_title_input.pack(padx=5, pady=5, fill=tk.BOTH)

        # Date
        date_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Date (i.e. March 26 2024)"
        )
        date_input.pack(padx=5, pady=5, fill=tk.BOTH)

        # Start Time
        start_time_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Start Time (i.e. 1:00 PM)"
        )
        start_time_input.pack(padx=5, pady=5, fill=tk.BOTH)

        # End Time (Optional)
        end_time_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="End Time (i.e. 4:00 PM)"
        )
        end_time_input.pack(padx=5, pady=5, fill=tk.BOTH)

        # Organizer(s)
        organizers_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Organizer(s) (i.e. Women in Computer Science)"
        )
        organizers_input.pack(padx=5, pady=5, fill=tk.BOTH)

        # Location (Street, City, State)
        location_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Location (i.e. Erb Memorial Union (full building name) or 944 W 5th Avenue, Eugene OR (address))"
        )
        location_input.pack(padx=5, pady=5, fill=tk.BOTH)

        # Description
        desc_input = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Description"
        )
        desc_input.pack(padx=5, pady=5, fill=tk.BOTH)

        ###############################################################
        # Input Submission Button                                     #
        ###############################################################
        new_event = {'title': '',
                    'date': '',
                    'start_time': '',
                    'end_time': '',
                    'location': '',
                    'desc': '',
                    'organizers': ''}

        def my_function():
            # Getting the input box elements
            event_title = event_title_input.get()
            date = date_input.get()
            start_time = start_time_input.get()
            end_time = end_time_input.get()
            organizers = organizers_input.get()
            location = location_input.get()
            desc = desc_input.get()
            # Adding them to the new dictionary
            new_event['title'] = str(event_title)
            new_event['date'] = str(date)
            new_event['start_time'] = str(start_time)
            new_event['end_time'] = str(end_time)
            new_event['location'] = str(location)
            new_event['desc'] = str(desc)
            new_event['organizers'] = str(organizers)
            # deleting the input values (so new values can be inputted)
            event_title_input.delete(0, len(event_title))
            date_input.delete(0, len(date))
            start_time_input.delete(0, len(start_time))
            end_time_input.delete(0, len(end_time))
            location_input.delete(0, len(location))
            desc_input.delete(0, len(desc))
            organizers_input.delete(0, len(organizers))

            checked_loc = False # boolean to quit if invalid lat and long
            # checking if location can become valid coordinate
            if location != '':
                yes_no = coordinate_validity(str(location))
                if yes_no == False:
                    err1 = ctk.CTkToplevel()
                    err1.geometry("300x100")
                    err1.configure(bg="gray92")
                    err1.wm_title("Error")
                    l = ctk.CTkLabel(
                        err1,
                        text="location '" + location + "'is invalid."
                    )
                    l.pack(padx=20, pady=10)
                    checked_loc = True

            if checked_loc != True:
                # checking if all inputs have been placed
                if (event_title != '' and date != '' and start_time != '' and end_time != '' and organizers != '' and location != '' and desc != ''):
                    succ = ctk.CTkToplevel()
                    succ.geometry("300x100")
                    succ.configure(bg="gray92")
                    succ.wm_title("Success")
                    l = ctk.CTkLabel(
                        succ,
                        text="'" + event_title + "' has been added."
                    )
                    l.pack(padx=20, pady=10)
                    # adding new valid event to the database csv
                    admin_intake_form.add_to_admin_file(new_event)
                else:
                    err = ctk.CTkToplevel()
                    err.geometry("300x100")
                    err.configure(bg="gray92")
                    err.wm_title("Error")
                    l = ctk.CTkLabel(
                        err,
                        text="please input all fields."
                    )
                    l.pack(padx=20, pady=10)

        # submit buttom
        submit_form = ctk.CTkButton(
            inputs_frame,
            text="Submit Event",
            command=lambda: my_function()
        )
        submit_form.pack(padx=5, pady=5)
        
    
    def on_refresh_data_click(self):
        refresh_data.refresh_data()

    def populate_delete_buttons(self):
        # Clear existing data in the scrollable frame
        for widget in self.scrollable_frame_delete_list.winfo_children():
            widget.destroy()

        try:
            # Load the admin_info.csv file into a DataFrame
            admin_df = pd.read_csv('./dollarless_database_files/admin_info.csv')
 
            for _, row in admin_df.iterrows():
                print(row)

            # Check if the DataFrame is not empty
            if not admin_df.empty:
                # Use the first column as the event_text (change this if needed)
                event_text_column = admin_df.columns[0]

                # Create the Tkinter Text widgets for the scrollable frame
                for index, event in admin_df.iterrows():
                    event_text = str(event[event_text_column])  # Convert to string
                    event_button = ctk.CTkButton(self.scrollable_frame_delete_list,
                                                 text=event_text,
                                                 text_color=("black", "white"),
                                                 command=lambda i=index: self.delete_selected_data(i),
                                                 fg_color=("grey88", "gray33"),
                                                 hover_color=("lightgrey", "grey"))
                    event_button.pack(fill=tk.X)
            else:
                print("DataFrame is empty.")
                # Display a message in the scrollable frame
                empty_label = ctk.CTkLabel(self.scrollable_frame_delete_list,
                                           text="No events to display.")
                empty_label.pack()

        except FileNotFoundError:
            print("CSV file not found.")
        except pd.errors.EmptyDataError:
            print("CSV file is empty.")
        except pd.errors.ParserError:
            print("Error parsing CSV file.")

    def on_delete_data_click(self):
        delete_data_popup = ctk.CTkToplevel(self.master)
        delete_data_popup.title('Admin Delete Events')
        delete_data_popup.geometry('400x300')

        self.scrollable_frame_delete_list = ctk.CTkScrollableFrame(delete_data_popup,    
                                                                    label_text='Delete Events')
        self.scrollable_frame_delete_list.pack(fill=tk.BOTH, expand=True)

        self.populate_delete_buttons()

    def delete_selected_data(self, index):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this event?")
        if confirmation:
            try:
                admin_df = pd.read_csv('./dollarless_database_files/admin_info.csv')
                admin_df.drop(index, inplace=True)
                admin_df.to_csv('./dollarless_database_files/admin_info.csv', index=False)
                self.populate_delete_buttons()
            except FileNotFoundError:
                print("CSV file not found.")
            except pd.errors.EmptyDataError:
                print("CSV file is empty.")
            except pd.errors.ParserError:
                print("Error parsing CSV file.")

    def show_admin_mode_popup(self):
        admin_mode_popup = ctk.CTkToplevel(self.master)
        admin_mode_popup.title('Admin Mode')
        admin_mode_popup.geometry('200x185')
        admin_mode_popup.resizable(False, False)

        # Add New Event button
        add_new_event_button = ctk.CTkButton(admin_mode_popup, text='Add Event', command=self.on_add_new_event_click)
        add_new_event_button.pack(pady=(25, 10), anchor="center")

        # Refresh Data button
        refresh_data_button = ctk.CTkButton(admin_mode_popup, text='Refresh Data', command=self.on_refresh_data_click)
        refresh_data_button.pack(padx=5, pady=10, anchor="center")

        # Refresh Data button
        delete_data_button = ctk.CTkButton(admin_mode_popup, text='Delete Data', command=self.on_delete_data_click)
        delete_data_button.pack(padx=5, pady=(10, 5), anchor="center")

#######################################################################
# Resources Button                                                    #   
#######################################################################
class ResourcesButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text='Resources',
                         command=self.show_resource_list)  # Set the command to open the resource list

    # Function to show the resource list
    def show_resource_list(self):
        resource_list_window = ctk.CTkToplevel()
        resource_list_window.title('Online Resources')
        resource_list_window.geometry('667x595')
        resource_list_window.resizable(False, False)  # width, height are constant

        # Removed to match other windows
        # # Create a Label to display additional resources
        # resource_label = ctk.CTkLabel(resource_list_window, text="Online Resources", font=("bold", 30))
        # resource_label.pack(padx=10, pady=10)

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

        # to show the full list
        resource_label2 = ctk.CTkLabel(resource_list_window, text="Can be used without wifi", font=("bold", 20))
        resource_label2.pack()

        # Create a button to open a new popup with the list
        open_list_button = ctk.CTkButton(resource_list_window, text='Open List', command=lambda: self.show_list_popup(description_text))
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
            button = ctk.CTkButton(wifi_frame, text=button_text, command=lambda u=url: webbrowser.open(u))
            button.grid(row=row // 2, column=row % 2, padx=5, pady=5)

        resource_list_window.mainloop()

    # Function to show a popup with a list
    def show_list_popup(self, text):
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

#######################################################################
# About Pop-up Button
#######################################################################
class AboutButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master, 
                         text='About', 
                         command=lambda: show_about_popup())

def show_about_popup():
    about_text = """
    Dollarless Dining

    This program helps you find free food resources on campus.

    Developed by Simone Badaruddin, Nithi Deivanayagam, Kylie Griffiths, Max Hermens, and Jasmine Wallin

    Copyright © 2024 University of Oregon
    """

    about_popup = ctk.CTkToplevel()
    about_popup.title('About Dollarless Dining')
    about_popup.geometry('300x200')
    about_popup.resizable(False, False)

    about_label = ctk.CTkLabel(about_popup, 
                               text=about_text, 
                               wraplength=280)
    about_label.pack(padx=5, 
                     pady=5)
        
#######################################################################
# Main Area                                                           #
#                                                                     #       
# Contains:                                                           #   
#   1. Free Food Events Lists with Tab View                           #
#   2. View Map Button                                                #
#######################################################################
class MainArea(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        ###############################################################
        # Create the Grid System for Main Area (Larger, Rightmost)    #   
        ###############################################################
        self.grid_columnconfigure(0,
                                  weight=1)
        self.grid_rowconfigure((0, 2), 
                               weight=1)

        ###############################################################
        # Place Internal Frames onto the Main Area                    #   
        ###############################################################
        # Free Food Event Tab Views 
        self.food_event_tabs = FoodEventTabs(self)
        self.food_event_tabs.grid(row=0, 
                                  column=0, 
                                  padx=5, 
                                  pady=5, 
                                  sticky="news",
                                  rowspan=2)
        # Event Description Box
        self.event_description = EventDescription(self)
        self.event_description.grid(row=2,
                                    column=0,
                                    padx=5,
                                    pady=5,
                                    sticky="news",
                                    rowspan=1)

#######################################################################
#                                                                     #
# Free Food Event Overall Tab View                                    #
#                                                                     # 
# Contains:                                                           #
#   1. Scrollable Frame Events by timeframe                           #   
#   2. View Map Button by timeframe                                   # 
#                                                                     # 
#######################################################################
class FoodEventTabs(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Create Tabs                                                 #   
        ###############################################################
        today_tab = self.add("Today")
        tomorrow_tab = self.add("Tomorrow")
        this_week_tab = self.add("This Week")
        next_week_tab = self.add("Next Week")
        
        ###############################################################
        # Place View Map Button for Each Day                          #   
        # #############################################################
        # Today
        self.view_map_button = ctk.CTkButton(self.tab("Today"), 
                                             text="View Today's Food Map", 
                                             command=lambda: Resource_Graph.run_map_function("today")) 
        self.view_map_button.pack(padx=50, 
                                  expand=True) 
        
        # Tomorrow
        self.view_map_button = ctk.CTkButton(self.tab("Tomorrow"), 
                                             text="View Tomorrow's Food Map", 
                                             command=lambda: Resource_Graph.run_map_function("tomorrow"))
        self.view_map_button.pack(padx=50, 
                                  expand=True)
        
        # This Week
        self.view_map_button = ctk.CTkButton(self.tab("This Week"), bg_color="transparent",
                                             text="View This Week's Food Map", 
                                             command=lambda: Resource_Graph.run_map_function("this week"))
        self.view_map_button.pack(padx=50, 
                                  expand=True)

        # Next Week
        self.view_map_button = ctk.CTkButton(self.tab("Next Week"), 
                                             text="View Next Week's Food Map", 
                                             command=lambda: Resource_Graph.run_map_function("next week"))
        self.view_map_button.pack(padx=50,
                                  expand=True)
        
        ###############################################################
        # Add a scrollable frame to each tab                          #   
        ###############################################################
        
        # Today Tab
        self.today_scrollable_frame = TodayFrame(self.tab("Today"))
        self.today_scrollable_frame.pack(padx=5, fill=tk.BOTH)

        # Tomorrow Tab
        self.tomorrow_scrollable_frame = TomorrowFrame(self.tab("Tomorrow"))
        self.tomorrow_scrollable_frame.pack(padx=5, fill=tk.BOTH)

        # This Week Tab
        self.thisweek_scrollable_frame = ThisWeekFrame(self.tab("This Week"))
        self.thisweek_scrollable_frame.pack(padx=5, fill=tk.BOTH)

        # Next Week Tab
        self.nextweek_scrollable_frame = NextWeekFrame(self.tab("Next Week"))
        self.nextweek_scrollable_frame.pack(padx=5, fill=tk.BOTH)

#######################################################################
# Today Tab                                                           #
#                                                                     # 
# Contains:                                                           #
#   1. Scrollable Frame of Today's Events                             #   
#   2. View Map Button of Today's Events                              #   
#######################################################################
class TodayFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Place Events as Buttons onto the Today Scrollable Frame     #   
        ###############################################################

        title_name = get_title_name('today')

        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color=("#cfcfce","#333333"),
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 
        
        ###############################################################
        # Update the Description Frame Text for Today Buttons pressed #   
        ############################################################### 
        def update_description(event_desc):
            app.main_area.event_description.configure(text=event_desc)

        ###############################################################
        # Function to populate the scrollable frame with data         #   
        ############################################################### 
        def populate_scrollable_frame():
            events, _ = get_all_events(csv_file_path, 
                        'today') 
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                event_text = event['Event Title'] #+ '-' + event['Date']
                event_desc = event['Description']

                #######################################################
                # Create the Tkinter Text widgets for Today Frame     #   
                #######################################################  
                # Choosing colors since the CTkScrollableFrame header 
                # text becomes black on light mode which is 
                # inconcsistent with the light theme for most widgets.
                event_button = ctk.CTkButton(scrollable_frame_food_list,
                                             anchor="nw", 
                                             text= event_text, 
                                             text_color=("darkgrey", "white"),
                                             command = lambda desc=event_desc: update_description(desc),
                                             fg_color=("grey88", "gray33"),  
                                             hover_color=("lightgrey", "grey")) 
                
                event_button._text_label.configure(wraplength=267)

                # A disabled, invisible button with a small font acts 
                # as a spacer between each event button!
                spacing = ctk.CTkButton(scrollable_frame_food_list, 
                                        text= " ", 
                                        height=9, 
                                        font=("Helvetica", 1), 
                                        state="disabled", 
                                        fg_color="transparent") 
                spacing.pack()
                event_button.pack(fill=tk.X)

        # Call the populate function to populate the frame
        populate_scrollable_frame()

#######################################################################
# Tomorrow Tab                                                        #
#                                                                     # 
# Contains:                                                           #
#   1. Scrollable Frame of Tomorrow's Events                          #   
#   2. View Map Button of Tomorrow's Events                           #   
#######################################################################
class TomorrowFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Place Events as Buttons onto the Today Scrollable Frame     #   
        ###############################################################
        title_name = get_title_name('tomorrow')

        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color=("#cfcfce","#333333"),
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 
        
        ###############################################################
        # Update the Description Frame Text for Today Buttons pressed #   
        ############################################################### 
        def update_description(event_desc):
            app.main_area.event_description.configure(text=event_desc)

        ###############################################################
        # Function to populate the scrollable frame with data         #   
        ###############################################################
        def populate_scrollable_frame():
            events, _ = get_all_events(csv_file_path, 
                                    'tomorrow')
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                event_text = event['Event Title'] #+ '-' + event['Date']
                event_desc = event['Description']

                #######################################################
                # Create the Tkinter Text widgets for Frame           #   
                ####################################################### 
                event_button = ctk.CTkButton(scrollable_frame_food_list,
                                             anchor="nw", 
                                             text= event_text, 
                                             text_color=("darkgrey", "white"),
                                             command = lambda desc=event_desc: update_description(desc),
                                             fg_color=("grey88", "gray33"),  
                                             hover_color=("lightgrey", "grey")) 
                
                event_button._text_label.configure(wraplength=267)
                spacing = ctk.CTkButton(scrollable_frame_food_list, 
                                        text= " ", 
                                        height=9, 
                                        font=("Helvetica", 1), 
                                        state="disabled", 
                                        fg_color="transparent") # a disabled, invisible button with a small font acts as a spacer between each event button!
                spacing.pack()
                event_button.pack(fill=tk.X)

        # Call the populate function to initially populate the frame
        populate_scrollable_frame()

#######################################################################
# This Week Tab                                                       #
#                                                                     # 
# Contains:                                                           #
#   1. Scrollable Frame of This Week's Events                         #   
#   2. View Map Button of This Week's Events                          #   
#######################################################################
class ThisWeekFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Place Events as Buttons onto the This Week Scrollable Frame #  
        ###############################################################
        title_name = get_title_name('this week')

        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color=("#cfcfce","#333333"),
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 

        ###############################################################
        # Update the Description Frame Text for Today Buttons pressed #   
        ############################################################### 
        def update_description(event_desc):
            app.main_area.event_description.configure(text=event_desc)

        ###############################################################
        # Function to populate the scrollable frame with data         #   
        ###############################################################    
        def populate_scrollable_frame():
            events, _ = get_all_events(csv_file_path, 
                        'this week') 
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                event_text = event['Event Title'] #+ '-' + event['Date']
                event_desc = event['Description']

                #######################################################
                # Create the Tkinter Text widgets for This Week Frame #   
                #######################################################  
                event_button = ctk.CTkButton(scrollable_frame_food_list,
                                             anchor="nw", 
                                             text= event_text, 
                                             text_color=("darkgrey", "white"),
                                             command = lambda desc=event_desc: update_description(desc),
                                             fg_color=("grey88", "gray33"),  
                                             hover_color=("lightgrey", "grey")) 
                
                event_button._text_label.configure(wraplength=267)
                spacing = ctk.CTkButton(scrollable_frame_food_list, 
                                        text= " ", 
                                        height=9, 
                                        font=("Helvetica", 1), 
                                        state="disabled", 
                                        fg_color="transparent") 
                spacing.pack()
                event_button.pack(fill=tk.X)

        # Call the populate function to initially populate the frame
        populate_scrollable_frame()

#######################################################################
# Next Week Tab                                                       #
#                                                                     # 
# Contains:                                                           #
#   1. Scrollable Frame of Next Week's Events                         #   
#   2. View Map Button of Next Week's Events                          #   
#######################################################################
class NextWeekFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ###############################################################
        # Place Events as Buttons onto the Next Week Scrollable Frame #   
        ###############################################################
        title_name = get_title_name('next week')

        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color=("#cfcfce","#333333"),
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 

        ###############################################################
        # Update Description Frame Text for Next Week Buttons pressed #   
        ############################################################### 
        def update_description(event_desc):
            app.main_area.event_description.configure(text=event_desc)

        ###############################################################
        # Function to populate the scrollable frame with data         #   
        ############################################################### 
        def populate_scrollable_frame():
            events, _ = get_all_events(csv_file_path, 
                        'next week')
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                event_text = event['Event Title'] #+ '-' + event['Date']
                event_desc = event['Description']
                
                #######################################################
                # Create the Tkinter Text widgets for Today Frame     #   
                ####################################################### 
                event_button = ctk.CTkButton(scrollable_frame_food_list,
                                             anchor="nw", 
                                             text= event_text, 
                                             text_color=("darkgrey", "white"),
                                             command = lambda desc=event_desc: update_description(desc),
                                             fg_color=("grey88", "gray33"),  
                                             hover_color=("lightgrey", "grey")) 
                
                event_button._text_label.configure(wraplength=267)
                
                spacing = ctk.CTkButton(scrollable_frame_food_list, 
                                        text= " ", 
                                        height=9, 
                                        font=("Helvetica", 1), 
                                        state="disabled", 
                                        fg_color="transparent") 
                spacing.pack()
                event_button.pack(fill=tk.X)

        # Call the populate function to initially populate the frame.
        populate_scrollable_frame()

#######################################################################
#                                                                     #
# Event Description Frame                                             #
#                                                                     # 
# Contains:                                                           #
#   1. An event of the event from the Scrollable Frame which was      #
#      most recently clicked.                                         # 
#                                                                     #  
#######################################################################
class EventDescription(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master, 
                         state = "disabled",
                         fg_color=("#cfcfcf", "#333333"),
                         text= "Click an event for its description.")
        self._text_label.configure(wraplength=300)
  
#######################################################################
# Run application                                                     #   
#######################################################################

app = App()
app.mainloop()
