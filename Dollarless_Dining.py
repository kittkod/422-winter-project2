"""
Runs Dollarless_Dining.py program
"""
import coordinate_finder
import Remodeled_Food_Information_User_Interface

def main():
    # I think we should have this actually when the scraper is run, because we don't want 
    # the user to need wifi every single time its run 
    coordinate_finder.main()
    # running UI
    Remodeled_Food_Information_User_Interface

if __name__ == "__main__":
    main()