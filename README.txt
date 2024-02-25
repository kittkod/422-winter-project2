###### Dollarless Dining

**Project Proposal**  
K. Griffiths (kg) 
S. Badaruddin (sb)  
N. Deivanayagam (nd)  
M. Hermens (mh)  
J. Wallin (jw)

## SRS Concept of Operations

### (1.1) Current Situation
At the University of Oregon (UO), over 22% of students are considered food insecure, which is double the national percentage (1).

### (1.2) Justification for a New System
Dollarless Dining aims to address the limitations of existing services and provide an interactive map of campus free food options with less stringent regulations for providers.

### (1.3) Operational Features
- View current and upcoming free food locations on campus.
- Interactive map display.
- Informative user interface for future food events.

### (1.4) User Classes
1. UO student users: View upcoming week's free food offerings.
2. Administrators: Update the database with new information.

### (1.5) Modes of Operation
The system has one primary mode of operation, with User and Administrator selections affecting the visual display.

### (1.6) Operational Scenarios
- **Student User:** View current free food information on the UO campus and greater Eugene area, and interact with the map.
- **Administrator:** Update the database manually or run the web scraper.

## Software Design Specifications

### (2.1) Software Architecture
1. **Web Scraping Module:** Gathers data from relevant websites.
2. **UO Food Database:** Holds scraped and administrator-entered data.
3. **Food Display Mapper:** Connects to the Food Information User Interface.
4. **Backend Connector to Map:** Builds the interactive map.
5. **Food Information User Interface:** Displays current free food information and allows administrators to input new events.

### Applicable Technologies
- **Web Scraping Module:** Python, Beautiful Soup, Requests.
- **UO Food Database:** MongoDB or SQL.
- **Food Display Mapper:** Under consideration (Google Maps API, ArcGIS API).

## Project Timeline

| Date Assigned | Assignee | Task |
| --- | --- | --- |
| 2-15-2024 | kg | Web Scraping UO Free Food Services (as CSV) |
| 2-15-2024 | sb | Frontend UI & Visuals for Dollarless Dining Interface |
| 2-15-2024 | nd | Frontend Mapping for Dollarless Dining Interface |
| 2-15-2024 | mh | Connect Free Food Database & Web Scraper |
| 2-15-2024 | jw | Map Research and Development |

*Initial meeting (2/15/24):* Plan out project, find relevant food source information, and set requirements.

*Final Meeting (3/9/24):* Discuss any final issues and finalize the SDS, SRS, project plan, and related documents.

## References and Acknowledgments
- [EMU - Food Equity](https://emu.uoregon.edu/food-equity#:~:text=A%20report%20from%20the%20UO,to%20fresh%20and%20healthy%20food.)
- [Trillium Produce Plus](https://www.foodforlanecounty.org/get-help/trillium-produce-plus/)
- [SNAP - Oregon](https://www.oregon.gov/odhs/food/pages/snap.aspx)
- [Leftover Textover](https://emu.uoregon.edu/leftover-textover)

**Acknowledgements:**  
This SRS builds on the template from [CS422 Class - UO](https://classes.cs.uoregon.edu/24W/cs422/P2/index.html).
