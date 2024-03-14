#######################################################################
# refresh_data.py                                                     #
# created: 03/02/2024                                                 # 
# Authors: Kylie Griffiths                                            #
#                                                                     #
# Description: Function to refresh data if option is chosen by admin  #                             
#                                                                     #
# Interactions:                                                       #
# - UO_scraper.py: This file calls UO_Scraper() to                    # 
# populate the CSV                                                    # 
# - coordinate_fnder.py: This file calls coordinate_finder to update  #
# campus_buildings.txt                                                #
# - admin_intake.py: This file calls admin_intake to update admin     #
# CSVs                                                                #
####################################################################### 

from UO_scraper import food_CSV_file, CSV_file_creator, engage_URL_web_scraper, engage_site_scraper, events_calendar_URL_scraper,food_pantry_211_scraper, student_life_scraper
import coordinate_finder
from admin_intake_form import admin_file_updater

def refresh_data():
    """Function to refresh the data on button press
    input: void
    output: void
    """
    print("Starting to refresh data.")
    CSV_file_creator(food_CSV_file)
    coordinate_finder.main()
    URL_list = engage_URL_web_scraper()
    engage_site_scraper(URL_list)
    events_calendar_URL_scraper()
    student_life_scraper()
    food_pantry_211_scraper()
    admin_file_updater()
    print("Data has been refreshed.")

if __name__ == "__main__":
    refresh_data()