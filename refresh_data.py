#######################################################################
# UO_scraper.py                                                       #
# created:                                                          # 
# Authors: Kylie Griffiths                                            #
#                                                                     #
# Description: Function to refresh data if option is chosen by admin  #                             
#                                                                     #
# Interactions:                                                       #
# - UO_scraper.py: Calls CSV_file_creator to and populates the CSV                                                       #
####################################################################### 

from UO_scraper import food_CSV_file, CSV_file_creator, engage_URL_web_scraper, engage_site_scraper, events_calendar_URL_scraper,food_pantry_211_scraper, student_life_scraper
import coordinate_finder
from admin_intake_form import admin_file_updater

def refresh_data():
    """refreshes data using scraper and admin data list"""
    
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