# import CustomTkinter module for GUI
# CustomTkinter was made by Tom Schimansky,
# Documentation here: https://github.com/TomSchimansky/CustomTkinter?tab=readme-ov-file
import customtkinter as ctk
import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
# from PIL import ImageTk, Image
# import csv

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

view_map_popup_button = ctk.CTkButton(
    window,
    text = 'View Map'
    #FIXME command to go to map goes here! <3
)

#######################################################################
#######################################################################
#######################################################################

# run
window.mainloop()
