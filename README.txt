Dollarless Dining
-----------------
Authors : Simone Badaruddin, Nithi Deivanayagam, Kylie Griffiths, Max Hermens, Jasmine Wallin 
Created : February-March 2024 for CS 422 Winter '24 project 2

Dollarless Dining is a program that aims to establish larger accessibility to 
free food resources around UO and the Eugene area. Users of this program can either 
view current and upcoming free food resources through the information menu and 
interactive map, or add their free food resources and refresh the database 
(if they are administrators). 

- All working files (.py and README.txt) are in the main folder (422-winter-project2):
admin_intake_form.py, coordinate_finder.py, database.py, DollarlessDining.py, ect..
refresh_data.py, Resource_Graph.py, UO_scraper.py, utils.py, README.txt
- All database files are in (422-winter-project2/dollarless_database_files):
admin_info.csv, Free_Food_Database.csv, unprocessed_admin_info.csv

Running Instructions:
---------------------
Installations/Modules needed: Python, Pandas, plotly.express, BeautifulSoup4, requests, customtkinter,
                              selenium, webbrowser.

1) After all modules from above are installed, download or clone this repository to your
computer
2) through terminal or a code editor (like virtual studio code), run the Dollarless_Dining.py
script
3) if this is the first time running: enter admin mode through the 'Admin Mode' button on the 
main page, and click the 'Refresh Data' button
4) wait for output that the scraping has been finished in terminal and a window popout on your 
screen, and now the program is set up and ready to use
