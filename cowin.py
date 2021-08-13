import subprocess
import requests
from datetime import date
import time

districtIds = [] # District ids to query
vaccines = ['COVISHIELD'] # Choice of vaccines
queryPinCodes = [209217, 208016, 208017] # Pin codes to query
queryAgeLimit = 18 # Age limit to query. Values - 18 or 45
minimumCapacityRequiredDose1 = 10 # Number of minimum available slots for dose 1 for which notification is to be fired. For example, if minimumCapacityRequired = 5, and a center does not have atleast 5 slots available, notification won't be fired
minimumCapacityRequiredDose2 = 10 # Number of minimum available slots for dose 2 for which notification is to be fired. For example, if minimumCapacityRequired = 5, and a center does not have atleast 5 slots available, notification won't be fired

def processAndNotify(response):
    try:
        data = response.json()
        centers = data['centers']

        found = 0

        for center in centers:
            sessions = center['sessions']
            for session in sessions:
                capacity1 = session['available_capacity_dose1']
                capacity2 = session['available_capacity_dose2']
                ageLimit = session['min_age_limit']
                vaccine = session['vaccine']
                if (ageLimit == queryAgeLimit and (capacity1 >= minimumCapacityRequiredDose1 or capacity2 >= minimumCapacityRequiredDose2) and (vaccine in vaccines)):
                    found = 1
                    subprocess.call(['osascript', '-e' , 'display notification "Check and book vaccine slot" with title "Vaccine slot(s) available"'])

        if (found == 1):
            print ('Found slots')
        else:
            print ('Slots not found')
    except:
        print('Something went wrong')
        print(response)

counter = 0
while(1):
    time.sleep(5)

    counter = counter + 1
    print ('Attempt ' + str(counter))

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

    for pinCode in queryPinCodes:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + str(pinCode) + "&date=" + day + "-" + month + "-2021"
        headers = {'User-Agent': 'Postman', 'Accept-Language': 'en_IN', 'accept': 'application/json'}
        try:
            response = requests.get(url = URL, headers = headers)
            processAndNotify(response)
        except:
            print('Failed to make request ' + URL)

    for districtId in districtIds:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + str(districtId) + "&date=" + day + "-" + month + "-2021"
        headers = {'User-Agent': 'Postman', 'Accept-Language': 'en_IN', 'accept': 'application/json'}
        try:
            response = requests.get(url = URL, headers = headers)
            processAndNotify(response)
        except:
            print('Failed to make request ' + URL)
