import subprocess
import requests
from datetime import date
import time

queryPinCode = 208017 # Pin code to query
queryAgeLimit = 18 # Age limit to query. Values - 18 or 45
minimumCapacityRequired = 1 # Number of minimum available slots for which notification is to be fired. For example, if minimumCapacityRequired = 5, and a center does not have atleast 5 slots available, notification won't be fired

while(1):
    time.sleep(5)

    today = date.today()
    day = today.day
    month = today.month

    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    print (day)
    print (month)



    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + str(queryPinCode) + "&date=" + day + "-" + month + "-2021"
    headers = {'User-Agent': 'Postman', 'Accept-Language': 'en_IN', 'accept': 'application/json'}

    # sending get request and saving the response as response object
    r = requests.get(url = URL, headers = headers)

    print(r)

    # extracting data in json format
    data = r.json()

    print (data)

    centers = data['centers']

    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            capacity = session['available_capacity']
            ageLimit = session['min_age_limit']
            if (ageLimit == queryAgeLimit and capacity >= minimumCapacityRequired):
                subprocess.call(['osascript', '-e' , 'display notification "Check and book vaccine slot" with title "Vaccine slot(s) available"'])
