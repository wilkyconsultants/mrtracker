##########################################################################################################
# Purpose:    transfer airtag data via API so you can use MR Tracker iOS app to visualize it
# Date:       Feb 14, 2024
# Version:    1.3 βeta
# Written by: Rob Wilkinson
# Changes:    1.3 - Add icloud ID
# Company:    Wilky Consultants Inc.
#
# Customization requests: All of this and more can be customized for your needs by engaging Rob Wilkinson
#                         Send email to MrTracker.416@gmail.com for a quote and timeline of your customizations
#
#                         Happy to help is any consulting engagement in Linux, Unix, web, iOS, Windows, python, django... 
#                         and much more, just ask
#
# IMPORTANT: change to provided client ID, PM Rob W for your ID
#
client_ID = "202400001"
#
##########################################################################################################
#  SET UP required to use this script:
######################################
#  Change first line to where your python is installed : run 
#     which python3
#  - if no python3 installed:
#    - download the Python 3 installer from the official Python website and follow the installation instructions and install
#      https://www.python.org/downloads/release/python-3122/
#   Install support modules:
#   - install url with "pip3 install urllib3==1.26.15"
#   - install requests with "pip3 install requests"
#
#   Start findmy on your mac to let it create the cache files that we will pull from with this script
#
#  To grant full disk access to the Terminal program on a Mac, you can follow these steps:
#    Open "System Preferences" and click on "Security & Privacy"
#    Select the "Privacy" tab, then choose "Full Disk Access" from the left-hand menu
#    Click the lock icon at the bottom left to make changes, then enter your system administrator password
#    Click the "+" button, then navigate to and select the Terminal program
#    Once the Terminal program is added, it will have full disk access.
#    Following these steps will grant the Terminal program full disk access on your Mac.
#    ** if unable to figure this out PM Rob and I will help :) **
#
#  Change permissions of the script:
#    chmod 775 client_transfer.py
#
# for testing how to run:
#     python3 ./client_transfer.py
#
# For production how to run:
#    crontab -e  # update the job to run every 5 minutes
#    Insert line, and save:
#    0,5,10,15,20,25,30,35,40,45,50,55 * * * * /usr/bin/python3 ~/client_transfer.py >/dev/null 2>&1
#    Change /usr/bin above to the path of your python3 binary. You determine this with "which python3" command
#    Assumes your client_transfer.py is in your home directory, if not adjust it!

import requests
import json
from datetime import datetime
import getpass

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def load_data(file_path):
    try:
        with open(file_path, encoding="utf-8") as input_file:
            return json.load(input_file)
    except Exception as e:
        print(f"Error loading data from file {file_path}: {e}")
        return None

def map_serial(serial):
    if serial.startswith("T"):
        return serial[4:16], "EufyTag"
    elif serial.startswith("W"):
        return serial[4:16], "AtuvosTag"
    elif serial.startswith("F"):
        return serial[4:16], "iTag"
    elif serial.startswith("H"):
        return serial[0:12], "AirTag"
    else:
        return serial[4:16], "NewTag"

def map_battery_status(status):
    # Add your mapping logic for battery status here
    if status == "1":
        return "100%"
    elif status == "2":
        return "80%"
    elif status == "3":
        return "60%"
    elif status == "4":
        return "40%"
    elif status == "5":
        return "20%"
    else:
        return "0%"

def process_data(data):
#   Get the icloud ID
    icloud_ID="None"
    import subprocess
    try:
       result = subprocess.run(["defaults", "read", "MobileMeAccounts", "Accounts"], capture_output=True, text=True)
       output_lines = result.stdout.split('\n')
       account_lines = [line for line in output_lines if "AccountID" in line]
       account_ids = [line.split()[2] for line in account_lines]
       cleaned_account_ids = [account_id.replace('"', '').replace(';', '') for account_id in account_ids]
       for account_id in cleaned_account_ids:
           icloud_ID=account_id
    except:
           icloud_ID = "Error"
#
    results = []
    for item in data:
        try:
            D_LAST_UPDATE = datetime.fromtimestamp(item['location']['timeStamp'] / 1000).replace(microsecond=0)
            LAT = str(round(item['location']['latitude'], 5))
            LONG = str(round(item['location']['longitude'], 5))
            SERIAL, tag_type = map_serial(item['serialNumber'].upper())
            emoji = item['role']['emoji'] 
            name = item['name']
            BATTERYSTATUS = map_battery_status(str(item['batteryStatus']))
            MAPFULLADDRESS = item['address'].get('mapItemFullAddress', '')
            MAPFULLADDRESS = MAPFULLADDRESS.replace("'", "")
            #D = datetime.now().isoformat()
            now = datetime.now()
            D = now.strftime("%Y-%m-%d_%H:%M:%S")
            D_DIFF = round((datetime.now() - D_LAST_UPDATE).total_seconds() / 60)
            LAST_UPDATE = "✅" if D_DIFF <= 5 else "✔️" if D_DIFF <= 59 else "❌"
            SERIAL = SERIAL.upper()
            username = getpass.getuser()            
            formatted_date = D_LAST_UPDATE.strftime("%Y-%m-%d %H:%M:%S")
            json_data = {
                'client_ID': client_ID,
                'username': username,
                'type': tag_type,
                'serialnumber': SERIAL,
                'date_time': D,
                'latitude': float(LAT),
                'longitude': float(LONG),
                'lastupdate': formatted_date,
                'ago': f"{D_DIFF} Min",
                'LAST_UPDATE': LAST_UPDATE,
                'FULL_serialnumber': item['serialNumber'],
                'MAPFULLADDRESS': MAPFULLADDRESS,
                'BATTERYSTATUS': BATTERYSTATUS,
                'emoji': emoji,
                'name': name,
                'icloud_ID': icloud_ID,
            }
            results.append(json_data)
        except Exception as e:
            print(f"Error processing item: {e}")
    return results

def send_data(url, json_data,port):
    if port == '':
       headers = {'Content-type': 'application/json', 'HTTPMRTRACKER': json.dumps(json_data, cls=DateTimeEncoder)}
    else:
       headers = {'Content-type': 'application/json', 'HTTP_HTTPMRTRACKER': json.dumps(json_data, cls=DateTimeEncoder)}
    try:
        response = requests.post(url, headers=headers)
        return response.status_code
    except Exception as e:
        print(f"Failed to send data to {url}: {e}")
        return None

def main():
    username = getpass.getuser() 
    file_path = '/Users/'+username+'/Library/Caches/com.apple.findmy.fmipcore/Items.data'
    port = ''        # production
    #port = ':8443'  # test
    url = 'https://mrrobby.ca'+port+'/theme/AcceptFile_api'
    data = load_data(file_path)
    if data:
        processed_data = process_data(data)
        for json_data in processed_data:
            status_code = send_data(url, json_data,port)
            if status_code is not None:
                print(f"{status_code} {json_data['date_time']} {json_data['serialnumber']} {json_data['LAST_UPDATE']} {json_data['lastupdate']} {json_data['emoji']} {json_data['name']}")

if __name__ == "__main__":
    main()
