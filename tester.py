import datetime

import pandas as pd

import re

import utils
'''
todays_date = datetime.date.today().strftime('%y')
print(todays_date)
pattern1 = "[a-zA-Z]+\s\d{1,2}\s\d{4}"
pattern2 = "[a-zA-Z]+\s\d{1,2}"
pattern3 = "[a-zA-Z]+\s\d{1,2}\s[a-zA-Z]"

df = pd.read_csv('Free_Food_Database.csv')
file = open('./some_file.txt', 'w')
for _, row in df.iterrows():
    file.write(row["Date"])
    find_list = re.findall(pattern2, row["Date"])
    if len(find_list) > 0:
        date = re.findall("\d{1,2}", find_list[0])
        file.write(' - ' + str(date[0]))
        month = find_list[0].replace(date[0], '').strip()
        file.write(' ' + month + 'f')
    file.write("\n")
'''
file = open('./some_file.txt', 'w')

weekday_dict = {0:"monday", 1:"tuesday", 2:"wednesday", 3:"thursday", 
                4:"friday", 5:"saturday", 6:"sunday"}
month_dict = {"january":1, "february":2, "march":3, "april":4, "may":5,
                "june":6, "july":7, "august":8, "september":9, "october":10,
                    "november":11, "december":12}
days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
# this is kind of a bad dictionary, theres probably better ways of doing this
abbr_mon = {'jan':'january', 'feb':'february', 'mar':'march', 'apr':'april', 'jun':'june', 'jul':'july',
            'aug':'august', 'sep':'september', 'sept':'september', 'oct':'october'}



input_button = "today"

df = pd.read_csv('Free_Food_Database.csv')

event_dict = {
    'lat': [],
    'lon': [],
    'sizes': [],
    'text': [],
    'comment': [],
    'Food Resources': [],
    'Location': [],
    'Time': [],
    'Organizer': [],
    'Date': [],
    'Reoccurring': []
}

todays_date = datetime.date.today().strftime('%m-%d')
curr_year = datetime.date.today().strftime('%y')
todays_month = todays_date[:2]
todays_day = todays_date[-2:]
# inclusive start and end date
start_date = None # a list of ints: [date, month]
end_date = None # a list of ints: [date, month]
weekday_date = '' # a string of the weekday
is_week = False
map_name = 'Free Food Resources ' # name of map

if input_button.lower() == "today":
    start_date = [int(todays_day), int(todays_month)] # to get rid of the leading '0'
    end_date = [int(todays_day), int(todays_month)]
    weekday_date = weekday_dict[datetime.date.today().weekday()]
    map_name += 'on ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year
    
if input_button.lower() == "tomorrow":
    month_days = days_in_month[int(todays_month)] # how many days in the current month
    # if tomorrow goes into the next month
    if int(todays_day) + 1 > month_days:
        start_date = [1, int(todays_month)+1]
        end_date = [1, int(todays_month) + 1]
    # if tomorrow is in the same month
    else:
        start_date = [int(todays_day) + 1, int(todays_month)]
        end_date = [int(todays_day) + 1, int(todays_month)]
    weekday_date = weekday_dict[datetime.date.today().weekday() + 1]
    map_name += 'on ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year

if input_button.lower() == "next 7 days":
    month_days = days_in_month[int(todays_month)]
    # if the next 6 days go into the next month
    if int(todays_day) + 6 > month_days:
        days_forward = (int(todays_day) + 6) - month_days
        start_date = [int(todays_day), int(todays_month)]
        end_date = [int(days_forward), int(todays_month) + 1]
    # if the next 6 days stay in the current month
    else:
        start_date = [int(todays_day), int(todays_month)]
        end_date = [int(todays_day) + 6, int(todays_month)]
    is_week = True
    map_name += 'from ' + str(start_date[1]) + '/' + str(start_date[0]) + '/' + curr_year + ' to ' + str(end_date[1]) + '/' + str(end_date[0]) + '/' + curr_year

print(str(start_date) + ' ' + str(end_date) + ' ' +  str(weekday_date))
print(map_name)
file.write("RANGE IS: " + str(start_date[1]) + '/' + str(start_date[0]) + '/24' + ' to ' + str(end_date[1]) + '/' + str(end_date[0]) + '/24' + ' on ' +  str(weekday_date) + '\n')


# looping through each row in the input csv
for _, row in df.iterrows():
    file.write(str(row['Event Title'])[:20] + ' ' + row['Date'] + ' ')
    #TODO: some sort of way to see if there are occurences IN THE SAME INDEX of same title, same location, and same date
    # right now its checking if there exists a same title and if there exists a same location and if there
    # exists a same date throughout all of the matches.

    # checking for clone events (the same event in the same location)
    #if (utils.break_str(row.get('Event Title', ''), 25) in event_dict['Food Resources']) and (utils.break_str(str(row.get('Location', ' ')), 40) in event_dict['Location']):
    #    file.write(" f\n")
    #    continue
    # if its not reoccurring event
    if str(row["Reoccurring"]).strip().lower() == "false":
        row_day = 0 # int of the row's day
        row_month = 0 # int of the row's month
        find_list = re.findall("[a-zA-Z]+\s\d{1,2}", row["Date"])
        if len(find_list) > 0:
            # getting the day from the date string
            row_day = int((re.findall("\d{1,2}", find_list[0]))[0])
            # getting the month string (full month name) from date string
            str_month = find_list[0].replace(str(row_day), '').strip().lower()
            if str_month not in month_dict:
                if str_month in abbr_mon:
                    tmp = abbr_mon[str_month]
                    str_month = tmp
                else:
                    file.write(" f \n")
                    continue
            # getting the month number from the month string
            row_month = month_dict[str_month]
        else:
            file.write(" f \n")
            continue
        file.write(str(row_month) + '/' + str(row_day) + '/24 ')

        # seeing if the date is in the range 
        # if the row's month is larger than the starting range month and the row's date is less than the ending range date
        if (start_date[1] < row_month and (end_date[1] == row_month and end_date[0] >= row_day)):
            pass
        # if the row's month is in the starting and ending range and the row's day is within range 
        elif (start_date[1] == row_month and start_date[0] <= row_day) and (end_date[1] == row_month and end_date[0] >= row_day):
            pass
        # if the row's month is less than the ending range month and the row's date is more than the starting range date
        elif (start_date[1] == row_month and start_date[0] <= row_day) and (end_date[1] > row_month):
            pass
        # not in date bounds
        else:
            file.write(" f \n")
            continue 

    # if its reocurring
    else:
        file.write("--reocurring--")
        # if the graph output is for a single day and the day's weekday does not match with the event's weekdays
        if is_week == False and weekday_date not in row["Date"].lower():
            file.write(" f \n")
            continue
    event_dict["Date"].append(str(row.get('Date', '')).strip())
    #if is_week == True:
    event_dict['Food Resources'].append(utils.break_str((row.get('Event Title', '')), 25))
    #file.write('\t' + event_dict['Food Resources'][-1] + '\n')
    event_dict['Location'].append(utils.break_str(str(row.get('Location', ' ')), 40))
    file.write("nice\n")

file.close()
