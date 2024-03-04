#!/bin/ksh
# change this to your home dir where script is located
DIR='/Users/tracker/airtag/DJANGO/wilkyconsultants'

# Check if connected to wifi network
if /sbin/ifconfig en1 | grep "status: active" > /dev/null; then
    echo "`date` Wifi is connected."
    TAGS_OK=$(cat $DIR/gps_current_TEXT_5min_LAST_1min.log | egrep '✔️|✅' | wc -l | awk '{print $1}')
    echo "`date` Tags online: $TAGS_OK"
    
    if [ $TAGS_OK -gt 10 ]; then
        echo "`date` No action, tags look ok > 10 active.."
    else
        echo "`date` Wifi is reconnecting to see if it helps..."
        /usr/sbin/networksetup -setairportpower en1 off
        sleep 5
        /usr/sbin/networksetup -setairportpower en1 on
        sleep 60
        
        TAGS_OK=$(cat $DIR/gps_current_TEXT_5min_LAST_1min.log | egrep '✔️|✅' | wc -l | awk '{print $1}')
        echo "`date` Tags online on re-check: $TAGS_OK"
        
        if [ $TAGS_OK -gt 10 ]; then
            echo "`date` Looks like bounce did the trick, > 10 active, tags look ok.."
        else
            echo "`date` Tags still not good after bounce. Check manually for the issue."
        fi
    fi
else
    echo "`date` Wifi is disconnected. Reconnecting..."
    /usr/sbin/networksetup -setairportpower en1 off
    sleep 5
    /usr/sbin/networksetup -setairportpower en1 on
    sleep 60
    if /sbin/ifconfig en1 | grep "status: active" > /dev/null; then
       echo "`date` Wifi is now connected on reconnect."
       TAGS_OK=$(cat $DIR/gps_current_TEXT_5min_LAST_1min.log | egrep '✔️|✅' | wc -l | awk '{print $1}')
       echo "`date` Tags online: $TAGS_OK"
    else
       echo "`date` Wifi is still disconnected on reconnect, manual intervention may be required."
    fi
fi
echo  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
