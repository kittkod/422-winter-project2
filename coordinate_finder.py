#######################################################################
# UO_scraper.py                                                       #
# created: 2/29/2024                                                  # 
# Authors: Kylie Griffiths                                            #
#                                                                     #
# Description: Code body to take in an address and return the         #
# latitude and longitude -- requires internet connection.             #                             
#                                                                     #
# Interactions:                                                       #
# - campus_buildings.txt: Add dictionary to text file                 #
####################################################################### 

from bs4 import BeautifulSoup
import requests 
import urllib.parse
import json
import re

raw_link = "https://en.wikipedia.org/wiki/List_of_University_of_Oregon_buildings"
acronym_link = "https://registrar.uoregon.edu/faculty-staff/academic-scheduling/classrooms-chart"
address_exceptions = {"Grace Evangelical Church": [44.0408363098272, -123.08166553148503]}

def class_dict_maker():
    class_dictionary = {}

    link_1 = requests.get(raw_link)
    soup = BeautifulSoup(link_1.text, 'html.parser')
    list_of_buildings = soup.find_all("tr")
    for row in list_of_buildings:
        row_of_buildings = row.find_all("td")
        for specific in row_of_buildings:
            coords = specific.find("span", class_="geo-inline")
            if coords != None:
                coordinates = coords.find("span", class_= "geo")
                building = (coords.find("span", class_="fn org"))
                if "Hall" in building.text:
                    no_hall_building = building.text.replace("Hall", "")
                    class_dictionary[no_hall_building] = coordinates.text
                class_dictionary[building.text] = coordinates.text

    ###acronyms being added to list of buildings -- for scraping usage
    acronym_info = requests.get(acronym_link)
    soup_stuff = BeautifulSoup(acronym_info.text, 'html.parser')
    specific_vals = soup_stuff.find("tbody")
    specific_vals = specific_vals.find_all("tr")
    items = list(class_dictionary.keys())
    for val in specific_vals:
        acryonym = val.find("td").text.replace("\xa0", "").split("(")
        if type(acryonym) == list:
            if len(acryonym) == 2:
                data = val.find("td").text.split("(")[0]
                acry = val.find("td").text.split("(")[1].replace(")", "")
                if acry != "International Classroom":
                    for item in items:
                        if data.strip() in item:
                            class_dictionary[acry.strip()] = class_dictionary.get(item)

    class_dictionary["EMU"] = class_dictionary.get("Erb Memorial Union")
    class_dictionary["PSC"] = class_dictionary.get("Allan Price Science Commons and Research Library")
    class_dictionary["SRC"] = class_dictionary.get("Student resource center")
    class_dictionary["Hamilton"] = class_dictionary.get("Hamilton Complex")
    class_dictionary["Knight Law School"] = class_dictionary.get("William Knight Law Center")
    class_dictionary["Redwood Auditorium"] = class_dictionary.get("Erb Memorial Union")
    class_dictionary["LLC"] = class_dictionary.get("Living Learning Center")
    class_dictionary["Knight Law"] = class_dictionary.get("William Knight Law Center")
    class_dictionary["Ford Alumni Center"] = class_dictionary.get("Cheryl Ramberg Ford and Allyn Ford Alumni Center")
    class_dictionary["Ford Lecture Hall"] = class_dictionary.get("Jordan Schnitzer Art Museum")
    class_dictionary["HEDCO"] = class_dictionary.get("HEDCO Education Building")
    class_dictionary["Redwood Room"] = class_dictionary.get("Erb Memorial Union")
    class_dictionary["Unthank Hall"] = '44.04386755; -123.06892427902709'
    class_dictionary["ASUO"] = class_dictionary.get("Erb Memorial Union")
    class_dictionary["Bartolotti's"] = class_dictionary.get("Erb Memorial Union")
    class_dictionary["Bartolotti"] = class_dictionary.get("Erb Memorial Union")
    class_dictionary["Barn"] = '44.04102377844486, -123.07411695536857'
    class_dictionary["Lylle Reynolds-Parker"] = '44.04321043698473, -123.06539574909931'
    class_dictionary["Black Cultural Center"] = class_dictionary.get("Lylle Reynolds-Parker")
    
    
    return class_dictionary

def address_converter(initial_address: str):
    #find specific address pattern
    pattern = r'^\D+\d+'

    # Use re.search() to find the matched pattern in the string
    match = re.search(pattern, initial_address)

    # If a match is found, return the matched substring, else return the original string
    if match:
        return match.group()
    else:
        return initial_address
    
def lat_and_long(address: str): 
    """Take an address and return the latitude and longitude"""
    match = None
    for location in address_exceptions:
            if location.lower() in address.lower():
                match = location
                lat_long = address_exceptions[match]
                return [lat_long[0], lat_long[1]]
    else:    
        url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json'

        try: 
            response = requests.get(url).json()
            response[0]["lat"]
        except:
            return ["N/A", "N/A"]
        else:
            if float(response[0]["lon"]) > -122 or float(response[0]["lon"]) < -124:
                return ["N/A", "N/A"]
            if float(response[0]["lat"]) > 45 or float(response[0]["lat"]) < 43:
                return ["N/A", "N/A"]
                
            return [response[0]["lat"], response[0]["lon"]]

def coordinate_validity(address: str):
    """Ensure the validity of an address - check if coordinates exist"""
    matched_location = None
    with open('campus_buildings.txt') as f:
        campus_buildings = json.load(f)
    if address != '':
        for location in campus_buildings.keys():
            if location in address:
                matched_location = location
                break
        if matched_location == None:
            new_location = address_converter(address)
            lat, long = lat_and_long(new_location)
        else:
            latlong = campus_buildings.get(matched_location).split(" ")
            lat = latlong[0]
            long = latlong[1]
    if lat != "N/A" and long != "N/A": 
        return True
    else:
        return False

def main():
    class_dict = class_dict_maker()
    with open('campus_buildings.txt', 'w') as convert_file: 
        convert_file.write(json.dumps(class_dict))

if __name__ == '__main__':
    main()