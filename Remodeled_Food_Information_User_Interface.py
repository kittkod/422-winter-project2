#######################################################################
# Remodeled Food Information User Interface                           # 
# Authors: All team                                                   #
#                                                                     #
# Last Edited: 05/08/2024 by: sb                                      #   
# Log: Added classes functionality                                    # 
#######################################################################

#######################################################################
# CustomTkinter was made by Tom Schimansky.                           #
# Documentation here:                                                 #
# https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file   #
#######################################################################

import customtkinter as ctk 
import tkinter as tk
from utils import get_all_events, filter_events
from database import run_map
import Resource_Graph

csv_file_path = 'Free_Food_Database.csv'

#######################################################################
# Imports which may be helpful in the future                          #
#######################################################################

# from PIL import ImageTk, Image

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
        self.minsize(555, 444)
        self.maxsize(777, 555)

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
                         text='Admin Mode')
        
        #FIXME add Nithi's frame
    
#######################################################################
# Resources Button                                                    #   
#######################################################################
class ResourcesButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text='Resources')
        
        #FIXME add Nithi's frame
        
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
                                    padx=33,
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
                                             command=lambda: Resource_Graph.main())
        self.view_map_button.pack(padx=50, 
                                  expand=True) 
        
        # Tomorrow
        self.view_map_button = ctk.CTkButton(self.tab("Tomorrow"), 
                                             text="View Tomorrow's Food Map", 
                                             command=lambda: Resource_Graph.main())
        self.view_map_button.pack(padx=50, 
                                  expand=True)
        
        # This Week
        self.view_map_button = ctk.CTkButton(self.tab("This Week"), bg_color="transparent",
                                             text="View This Week's Food Map", 
                                             command=lambda: Resource_Graph.main())
        self.view_map_button.pack(padx=50, 
                                  expand=True)

        # Next Week
        self.view_map_button = ctk.CTkButton(self.tab("Next Week"), 
                                             text="View Next Week's Food Map", 
                                             command=lambda: Resource_Graph.main())
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

        events, title_name = get_all_events(csv_file_path, 
                        'today') # second argument can be 'all', 'today', 'tomorrow','this week' or 'next week'

        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color="transparent",
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'UO Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey")) #maybe make fg transparent
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 

        # Function to populate the scrollable frame with data
        def populate_scrollable_frame():
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                
                event_text = event['Event Title'] #+ '-' + event['Date']

                # Create the Tkinter Text widget 
                event_button = ctk.CTkButton(scrollable_frame_food_list,
                                             anchor="nw", 
                                             text= event_text, 
                                             fg_color=("darkgrey", "gray33"),  
                                             hover_color=("lightgrey", "grey")) # choosing colors since the CTkScrollableFrame header text becomes black on light mode which is inconcsistent with the light theme for most widgets
                event_button._text_label.configure(wraplength=222)
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

        events, title_name = get_all_events(csv_file_path, 
                                    'tomorrow')

        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color="transparent",
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'UO Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 

        # Function to populate the scrollable frame with data
        def populate_scrollable_frame():
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                event_text = event['Event Title'] #+ '-' + event['Date']

                # Create the Tkinter Text widget 
                event_button = ctk.CTkButton(scrollable_frame_food_list, 
                                             anchor="nw",
                                             text= event_text, 
                                             fg_color=("darkgrey", "gray33"),  
                                             hover_color=("lightgrey", "grey")) # choosing colors since the CTkScrollableFrame header text becomes black on light mode which is inconcsistent with the light theme for most widgets
                event_button._text_label.configure(wraplength=222)
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
        # Place Events as Buttons onto the Today Scrollable Frame     #   
        ###############################################################

        events, title_name = get_all_events(csv_file_path, 
                        'this week') # second argument can be 'all', 'today', 'tomorrow','this week' or 'next week'


        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color="transparent",
                                                            fg_color=("grey88", "grey28"),
                                                            label_text = 'UO Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 

        # Function to populate the scrollable frame with data
        def populate_scrollable_frame():
             # Clear existing data in the scrollable frame
        #     for widget in scrollable_frame_food_list.winfo_children():
        #         widget.destroy()

            for event in events:
                
                event_text = event['Event Title'] #+ '-' + event['Date']

                # Create the Tkinter Text widget 
                event_button = ctk.CTkButton(scrollable_frame_food_list, 
                                             anchor="nw",
                                             text= event_text, 
                                             fg_color=("darkgrey", "gray22"),  
                                             hover_color=("lightgrey", "grey")) # choosing colors since the CTkScrollableFrame header text becomes black on light mode which is inconcsistent with the light theme for most widgets
                event_button._text_label.configure(wraplength=222)
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
        # Place Events as Buttons onto the Today Scrollable Frame     #   
        ###############################################################

        events, title_name = get_all_events(csv_file_path, 
                        'next week') # second argument can be 'all', 'today', 'tomorrow','this week' or 'next week'


        scrollable_frame_food_list = ctk.CTkScrollableFrame(self, 
                                                            bg_color="transparent",
                                                            fg_color=("grey88", "grey33"),
                                                            label_text = 'UO Free Food Resources' + title_name, 
                                                            label_text_color=("grey", "lightgrey"))
        scrollable_frame_food_list.pack(fill=tk.BOTH, 
                                        expand=True) 

        # Function to populate the scrollable frame with data
        def populate_scrollable_frame():
            # Clear existing data in the scrollable frame
            for widget in scrollable_frame_food_list.winfo_children():
                widget.destroy()

            for event in events:
                
                event_text = event['Event Title'] #+ '-' + event['Date']

                # Create the Tkinter Text widget 
                event_button = ctk.CTkButton(scrollable_frame_food_list, 
                                             anchor="nw",
                                             text= event_text, 
                                             fg_color=("darkgrey", "gray33"),  
                                             hover_color=("lightgrey", "grey")) # choosing colors since the CTkScrollableFrame header text becomes black on light mode which is inconcsistent with the light theme for most widgets
                event_button._text_label.configure(wraplength=222)
                
                # 'spacing' is a disabled, invisible button with a 
                # small font acts as a spacer between each event 
                # button! (see below). 
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
#                                                                     #
# Event Description Frame                                             #
#                                                                     # 
# Contains:                                                           #
#   1. An event of the event from the Scrollable Frame which was      #
#      most recently clicked.                                         # 
#                                                                     # 
#######################################################################
class EventDescription(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master, 
                         justify="left",
                         text= "Description here. <3")
  
#######################################################################
# Run application                                                     #   
#######################################################################

app = App()
app.mainloop()
