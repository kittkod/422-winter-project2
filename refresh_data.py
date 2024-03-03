"""Function to refresh data if option is chosen by admin"""

from UO_scraper import food_CSV_file, CSV_file_creator, engage_URL_web_scraper, engage_site_scraper, events_calendar_URL_scraper,food_pantry_211_scraper
import coordinate_finder
from admin_intake_form import admin_file_updater

def refresh_data():
    """refreshes data using scraper and admin data list"""
    
    CSV_file_creator(food_CSV_file)
    coordinate_finder.main()
    URL_list = engage_URL_web_scraper()
    engage_site_scraper(URL_list)
    events_calendar_URL_scraper()
    food_pantry_211_scraper()
    admin_file_updater()

if __name__ == "__main__":
    refresh_data()