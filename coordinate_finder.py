"""
Code body to take in an address and return the latitude and longitude -- requires internet connection.
"""
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import json

raw_link = "https://en.wikipedia.org/wiki/List_of_University_of_Oregon_buildings"
class_dictionary = {}
address_exceptions = {"Grace Evangelical Church": [44.0408363098272, -123.08166553148503]}

def class_dict_maker():

    link = requests.get(raw_link)
    soup = BeautifulSoup(link.text, 'html.parser')
    list_of_buildings = soup.find_all("tr")
    for row in list_of_buildings:
        row_of_buildings = row.find_all("td")
        for specific in row_of_buildings:
            coords = specific.find("span", class_="geo-inline")
            if coords != None:
                coordinates = coords.find("span", class_= "geo")
                building = (coords.find("span", class_="fn org"))
                class_dictionary[building.text] = coordinates.text
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
    return class_dictionary
                
def address_converter(initial_address: str):

    pattern = r'^\D+\d+'

    # Use re.search() to find the matched pattern in the string
    match = re.search(pattern, initial_address)

    # If a match is found, return the matched substring, else return the original string
    if match:
        return (match.group()+" Eugene OR")
    else:
        return initial_address

def lat_and_long(address: str): 
    print("hi")
    """Take an address and return the latitude and longitude"""
    match = None
    for location in address_exceptions:
            if location in address:
                match = location
                print(address)
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
            print(response[0]["lat"])
            print(response[0]["lon"])

            return [response[0]["lat"], response[0]["lon"]]

if __name__ == '__main__':
    class_dict = class_dict_maker()
    with open('campus_buildings.txt', 'w') as convert_file: 
        convert_file.write(json.dumps(class_dict))