#
# Written By:   Rob Wilkinson
# Date Written: Dec 26, 2022
# Purpose:
#  Control FindMy App like someone is using it, fool Apple :)
# Changes:

import subprocess
import time
import datetime
import applescript

name = "/System/Applications/FindMy.app/Contents/MacOS/FindMy"
while True:
    # Check if FindMy process is running
    result = subprocess.run(["ps", "ax"], capture_output=True, text=True)
    if name in result.stdout:
        print("Process FindMy already running, no action..")
    else:
        print("FindMy process was NOT running. Starting it..")
        r = applescript.run("findmy.scr")
        r.code
        #cmd = "nohup " + name + " &"
        #subprocess.run(cmd, shell=True)
        print("attempted FindMy start..")
        result = subprocess.run(["ps", "ax"], capture_output=True, text=True)
        if name in result.stdout:
           print("Process FindMy started successfully!!")

    # Refresh screen and wait 30 seconds
    now = datetime.datetime.now()
    D = now.strftime("%Y%m%d_%H:%M:%S")
    print(D, "Refreshing the screen in FindMy to get new data..")
    r = applescript.run("update_findmy.scr")
    r.code
    print("Waiting for a bit..")
    time.sleep(120)
