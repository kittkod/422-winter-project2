#######################################################################
# Remodeled Food Information User Interface                           # 
# Authors:                                                            #
#                                                                     #
# Last Edited: 05/03/2024 by: sb                                      #   
# Log: Added classes functionality                                    # 
#######################################################################

#######################################################################
# CustomTkinter was made by Tom Schimansky.                           #
# Documentation here:                                                 #
# https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file   #
#######################################################################

import customtkinter as ctk 
import tkinter as tk
import csv
from utils import get_all_events
from database import run_map
import Resource_Graph
import webbrowser

csv_file_path = 'Free_Food_Database.csv'

#######################################################################
# Imports which may be helpful in the future                          #
#######################################################################

# from tkinter import ttk
# from tkinter import filedialog
# from PIL import ImageTk, Image

#######################################################################
# Overall Application Section:                                        #
#                                                                     #
# Description:                                                        #
#   Creates the Dollarless Dining application.                        #   
#   #FIXME Insert upon compeltion.                                    #
# Contains:                                                           #   
#   #FIXME List upon completion.                                      #
#######################################################################

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dollarless Dining")
        self.geometry("440x300")
        self.minsize(440, 300)
        self.maxsize(700, 550)

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
        self.grid_rowconfigure((0, 7), 
                               weight=2)

        ###############################################################
        # Place Internal Frames onto the Left Sidebar Grid System     #   
        ###############################################################
        # Light and Dark Appearance Mode Frame
        self.appearance_mode_frame = AppearanceModeFrame(self)
        self.appearance_mode_frame.grid(row=0, 
                                        column=0, 
                                        padx=(5), 
                                        pady=(5),
                                        sticky="n")
        
        # Spacing Block 1, a disabled and transparent button
        self.spacing_frame_1 = SpacingOne(self)
        self.spacing_frame_1.grid(row=1, 
                                  column=0, 
                                  padx=(5), 
                                  pady=(5),
                                  sticky="news")
        
        # Spacing Block 2, a disabled and transparent button
        self.spacing_frame_1 = SpacingTwo(self)
        self.spacing_frame_1.grid(row=2, 
                                  column=0, 
                                  padx=(5), 
                                  pady=(5),
                                  sticky="news")
        
        # Spacing Block 3, a disabled and transparent button
        self.spacing_frame_3 = SpacingThree(self)
        self.spacing_frame_3.grid(row=3, 
                                  column=0, 
                                  padx=(5), 
                                  pady=(5),
                                  sticky="news")
        
        # Admin Mode Button Frame
        self.admin_mode_frame = AdminModeButton(self)
        self.admin_mode_frame.grid(row=4, 
                                    column=0, 
                                    padx=5, 
                                    pady=5, 
                                    sticky="news")

        # Additional Resources Button Frame
        self.resources_button = ResourcesButton(self)
        self.resources_button.grid(row=5, 
                               column=0, 
                               padx=5, 
                               pady=5, 
                               sticky="news")

        # About Button Frame
        self.about_button = AboutButton(self)
        self.about_button.grid(row=6, 
                               column=0, 
                               padx=5, 
                               pady=5, 
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
        
########################################################################
# Spacing Frame 1                                                      #   
# ######################################################################
class SpacingOne(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text="",
                         state="disabled",
                         fg_color="transparent")
        
########################################################################
# Spacing Frame 2                                                      #   
# ######################################################################
class SpacingTwo(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text="",
                         state="disabled",
                         fg_color="transparent")
        
########################################################################
# Spacing Frame 3                                                      #   
# ######################################################################
class SpacingThree(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text="",
                         state="disabled",
                         fg_color="transparent")
        
#######################################################################
# Admin Mode Button                                                   #   
#######################################################################
class AdminModeButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text='Admin Mode')
        
        #FIXME add Nithi's the fuctionality from og :D
    
#######################################################################
# Resources Button                                                    #   
#######################################################################
class ResourcesButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master,
                         text='Resources')
        
        #FIXME add Nithi's the fuctionality from og :D
        
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

    Developed by Simone Badaruddin, Nithi Deivanayagam, Kylie Griffiths, Max Hermens, Jasmine Wallin

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

        # View Map Button
        self.view_map_button = ctk.CTkButton(self, text='View Map', command=lambda: Resource_Graph.main())
        self.view_map_button.grid(row=2, 
                                  column=0, 
                                  padx=5, 
                                  pady=5, 
                                  sticky="sew")

#######################################################################
# Free Food Event Tab View                                            #   
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
        # Create the Grid System for Tab View                        #   
        ###############################################################
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #######################################################################
        # Tabs Funcitonality                                                  #   
        #######################################################################
        # Today Tab
        # def populate_scrollable_frame():
        #     # Retrieve all events
        #     events = get_all_events(csv_file_path)

        #     # Clear existing data in the scrollable frame
        #     for widget in scrollable_frame_food_list.winfo_children():
        #         widget.destroy()

        #     for event in events:
        #         event_text = event['Event Title']

        #         # Create the Tkinter Text widget 
        #         event_textbox = tk.Text(scrollable_frame_food_list, wrap=tk.WORD, width=60, height=2)
        #         event_textbox.insert(tk.END, event_text)  # Insert the text into the Text widget
        #         event_textbox.pack()
        
                


        # # Call the populate function to initially populate the frame
        # populate_scrollable_frame()

########################################################################
# View Map Function                                                    #
#                                                                      #
########################################################################

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
# Run application :)                                                  #   
#######################################################################

app = App()
app.mainloop()
