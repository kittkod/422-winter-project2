Dollarless Dining
-----------------
Authors : Simone Badaruddin, Nithi Deivanayagam, Kylie Griffiths, Max Hermens, 
Jasmine Wallin 
April-March 2024
created for CS 422 Winter '24 project 2

Dollarless Dining is a program that aims to establish larger accessiblilty to 
free food resources around UO and the Eugene area. Users of this program can either 
view current and upcoming free food resources through the information menu and 
interactive map, or add their own free food resources and refresh the database 
(if they are administrators). 

- all working files (.py and README.txt) are in the main folder (422-winter-project2):
admin_intake_form.py, coordinate_finder.py, database.py, Remodeled_Food_Information_User_Interface.py, 
refresh_data.py, Resource_Graph.py, UO_scraper.py, utils.py, README.txt
- all database files are in (422-winter-project2/dollarless_database_files):
admin_info.csv, campus_buildings.txt, Free_Food_Database.csv


Running Instructions:
---------------------
Installations/Modules needed: Python, Pandas, plotly.express, bs4, requests, customtkinter,
                              selenium, webbrowser

1) after all modules from above are installed, download or clone this repository to your
computer
2) through terminal or a code editor (like virtual studio code), run the Remodeled_Food_Information_User_Interface.py 
script
3) if this is the first time running: enter admin mode through the 'Admin Mode' button on the 
main page, and click the 'Refresh Data' button
4) wait for output that the scraping has been finished in terminal, and now the program is set up
and ready to use
