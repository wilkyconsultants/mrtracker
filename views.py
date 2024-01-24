# -*- coding: utf-8 -*-,
#
# Create Jan 23, 2024
# Change History:
#
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,ContactForm,Research_AssistantForm,dyn_menuForm,buttons_Form,dyn_menuForm_udpate,buttons_update,blog_update,blog_Form,DeviceItemSecurityForm,AuctGroupForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.http import HttpResponse
from .models import Contact
from .models import Research_Assistant
from .models import menu
from .models import Post
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic

from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import PostForm 
from .forms import chatbot
from .models import upload

# added Dec 30/2022
import psutil
from django.http import JsonResponse

def home(request):
    return redirect('/theme/menu/home')

def about(request): 
    return redirect('/theme/menu/about')

def blogmaint(request):
    return redirect('/theme/menu/blogmaint')

def sunandmoon(request):
    return render(request, "sunandmoon.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           email = form.cleaned_data.get('email')
           first_name = form.cleaned_data.get('first_name')
           last_name = form.cleaned_data.get('last_name')
           raw_password = form.cleaned_data.get('password1')
           user = authenticate(username=username, password=raw_password)
           message = Mail(
           from_email='xx@rogers.com',
           to_emails='xx@gmail.com',
           subject='New User Registration User : '+username,
           html_content='New user registered : '+username)
           print('message=',message)
           try:
              sg = SendGridAPIClient(api_key='')
              response = sg.send(message)
              print('response=',response)
           except Exception as e:
               print('Exception=',e.message)
           login(request, user)
           return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form":form})

def contactX(request):
    from .paths import CUST_DIR
    file_path = CUST_DIR+'/platform2.log'
    record="From contactX, Request method:"+str(request.method)+" - Request headers:"+str(request.headers)
    try:
        # Open file for append
        with open(file_path, "a") as file:
           file.write(record)
    except Exception as e:
        print(f"Error writing to file: {e}")

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            contact_phone = request.POST.get('contact_phone', '')
            form_content = request.POST.get('content', '')
            reason = request.POST.get('reason', '')
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_phone': contact_phone,
                'form_content': form_content,
            }
            content = template.render(context)
            from .models import menu
            menus = menu.objects.all().filter(menu_id=reason)
            for menu in menus:
                reason = menu.menu_title
            subj='Contact Form - '+reason
            message = Mail(
            from_email='xxx@rogers.com',
            to_emails='xx@gmail.com',
            subject=subj,
            html_content=content  )
            ## comment from here to after except to disable sending emails
            try:
               sg = SendGridAPIClient(api_key='')
               response = sg.send(message)
               print('response=',response)
            except Exception as e:
               print('Exception=',e.message)
            ## --here--
            p = Contact(reason=reason, name=contact_name, email=contact_email, phone=contact_phone, message=form_content)
            p.save()
            return redirect('/')
    else:
        form = ContactForm()
        from .models import menu
        list_menu_form = menu.objects.values("menu_id","menu_title","menu_admin","menu_dropdown","menu_status")
        return render(request, 'contact.html', {'form':form, 'list_menu_form':list_menu_form})

@user_passes_test(lambda u: u.is_superuser)
#
# URL: apache_log
#
def read_file(request):
#
# parse the django server log
#
    from .paths import CUST_DIR
    LOG=CUST_DIR+'/server.log'
    ip_counts = {}
    with open(LOG, 'r', encoding="utf-8") as run_log:
        lines = [
            ("<font color=black> " + line.strip() + "<font color=black>\n")
            if "99.255.148.37" not in line
            else "<font color=black> "+line.strip() + "\n"
            for line in run_log
            if "20" in line and "99.255.148.37" not in line and "wilkycon" not in line and "Users" not in line and "APPLE" not in line and "start_date" not in line and "." in line
        ]
            #if "GET" in line and "99.255.148.37" not in line

        # Count occurrences of each unique IP address
        for line in lines:
            ip_address = line.split()[2]  # Assuming the first string is the IP address
            ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1

        # Sort ip_counts by values in descending order
        sorted_ip_counts = dict(sorted(ip_counts.items(), key=lambda x: x[1], reverse=True))

    lines.reverse()
    reversed_content = ''.join(lines)
#
# parse the web log
#
    from .paths import CUST_DIR
    WEBLOG=CUST_DIR+'/chk_web.log'
    with open(WEBLOG, 'r', encoding="utf-8") as web_log:
         csv_reader = csv.reader(web_log)
         formatted_content = list(csv_reader)
         error_records = filter(lambda x: "ERROR" in x, formatted_content)
         sorted_content = sorted(error_records, key=lambda x: x[0], reverse=True)
#
# parse the function logs
#
    from .paths import CUST_DIR
    ACCESSLOG = CUST_DIR+'/platform2.log'
    with open(ACCESSLOG, 'r', encoding="utf-8") as access_log:
         csv_reader_accesslog = csv.reader(access_log)
         accesslog_content = list(csv_reader_accesslog)
         filtered_accesslog_content = [
             line for line in accesslog_content if "99.255.148.37" not in ' '.join(line)
        ]
         sorted_accesslog_content = sorted(filtered_accesslog_content, key=lambda x: x[0], reverse=True)

    ln = "<br><font color=red><font size=4><a href=/theme/menu/home>Home Page"
    args = {'accesslog': sorted_accesslog_content, 'result': "<font size=3>\n\n"+ reversed_content + "\n\n" + ln, 'ip_counts': sorted_ip_counts, 'web_log': sorted_content}
    return render(request, "view_log2.html", args)

@user_passes_test(lambda u: u.is_superuser)
def read_file_gps(request):
    from .paths import CUST_DIR
    f = open(CUST_DIR+'/gps_current.log', 'r',encoding="utf-8")
    file_contents = f.read()
    f.close()
    #ln="<br><font color=red><font size=4><a href=/theme/menu/home>Home Page</a>"
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

@user_passes_test(lambda u: u.is_superuser)
def read_file_gps_historical(request):
    from .paths import CUST_DIR
    f = open(CUST_DIR+'/gps.log', 'r',encoding="utf-8")
    file_contents = f.read()
    f.close()
    #ln="<br><font color=red><font size=4><a href=/theme/menu/home>Home Page</a>"
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

@user_passes_test(lambda u: u.is_superuser)
def read_file_gps_5min(request):
    from .paths import CUST_DIR
    f = open(CUST_DIR+'/gps_5min.log', 'r',encoding="utf-8")
    file_contents = f.read()
    f.close()
    #ln="<br><font color=red><font size=4><a href=/theme/menu/home>Home Page</a>"
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

@user_passes_test(lambda u: u.is_superuser)
def read_file_gps_5min_today(request):
    from .paths import CUST_DIR
    f = open(CUST_DUR+'/gps_current_5min.log', 'r',encoding="utf-8")
    file_contents = f.read()
    ###file_contents=file_contents.find("AirTag")
    f.close()
    #ln="<br><font color=red><font size=4><a href=/theme/menu/home>Home Page</a>"
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

def line_chart_distance_from_home(request,ser,dt):
    user = request.user.username
    file_contents=plot_distance_from_home_by_serial_and_date(user, ser, dt)
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

# mobile_check() returns 'mobile' or 'computer'
from django.shortcuts import render
from django_user_agents.utils import get_user_agent

def mobile_checkX(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet:
        return 'mobile'
    else:
        return 'computer'


import logging
from datetime import datetime
from django.shortcuts import render
from django_user_agents.utils import get_user_agent

# Configure the logging settings
from .paths import CUST_DIR
logging.basicConfig(filename=CUST_DIR+'/platform.log', level=logging.INFO)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def mobile_check(request):
    user_agent = get_user_agent(request)

    from datetime import datetime
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'AnonymousUser'

    if user_agent.is_mobile or user_agent.is_tablet:
        logging.info(f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | mobile | User: {username}")
        platform = 'mobile'
    else:
        logging.info(f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | computer | User: {username}")
        platform = 'computer'

    record = f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | {platform} | User: {username}\n"
    from .paths import CUST_DIR
    file_path = CUST_DIR+'/platform2.log'
    try:
        # Open file for append
        with open(file_path, "a") as file:
            # Write the record
            file.write(record)
        # File automatically closed when exiting the 'with' block
    except Exception as e:
        print(f"Error writing to file: {e}")

    return platform
#
# record all demo access
#
def mobile_check_demo(request):
    user_agent = get_user_agent(request)

    from datetime import datetime
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'AnonymousUser'
    
    if user_agent.is_mobile or user_agent.is_tablet:
        logging.info(f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | mobile | User: {username} | demo_access")
        platform = 'mobile'
    else:
        logging.info(f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | computer | User: {username} | demo_access")
        platform = 'computer'
         
    record = f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | {platform} | User: {username} | demo_access\n"
    from .paths import CUST_DIR
    file_path = CUST_DIR+'/platform2.log'
    try:
        # Open file for append
        with open(file_path, "a") as file:
            # Write the record
            file.write(record)
        # File automatically closed when exiting the 'with' block
    except Exception as e:
        print(f"Error writing to file: {e}")

    return platform

#
# convert Address to Lat/Long
#
from geopy.geocoders import Nominatim

def convert_address_to_lat_long(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    try:      
       location = geolocator.geocode(address)
       if location:
            latitude = location.latitude
            longitude = location.longitude
            #print(f"Address: {address}")
            #print(f"Latitude: {latitude}")
            #print(f"Longitude: {longitude}")
       else:
            address = ''
            #print(f"Unable to geocode the address: {address}")

    except Exception as e:
       address = ''
    return latitude,longitude

# changed 2023-01-09 to remove security to allow registered non admin users in
#@user_passes_test(lambda u: u.is_superuser)
#
# URL Mapping: /theme/gps_log_5min_today_last/ALL/
#
from .models import DeviceItemSecurity

@login_required
def read_file_gps_5min_today_last(request,category_selected):

    platform=mobile_check(request)
    # this is so I can over ride the view if needed, I select iPad on iphone and it will show full list
    #if category_selected == "iPad" and platform != "computer":
    #   platform="computer"
    #   category_selected="ALL"
    #print("platform=",platform)
    #platform='mobile'
    import json
    import csv
    item_counter=1
    from .paths import CUST_DIR
    file = open(CUST_DIR+'/gps_current_TEXT_5min_LAST_1min.log', 'r',encoding="utf-8")
    ###file = open(CUST_DIR+'/gps_current_TEXT_5min_LAST.log', 'r',encoding="utf-8")

    reader = csv.reader(file, delimiter=',', quotechar="'")
    # sort by category and Tag type
    reader = sorted(reader, key=lambda x: (x[12].upper(), x[0]),reverse=False)
    #reader = sorted(reader, key=lambda x: (x[0], x[1]),reverse=True)
    #
    found_user="false"
    heading_once=True
    # store elements in array so we can sort them
    col_row = []
    row_num=0
    file_contents=""
    #
    for row in reader:
        TYPE        = row[0]
        TAGNAME     = row[1]
        SAMPLE_DATE = row[2][0:16]
        SAMPLE_DATE=SAMPLE_DATE.replace("_", " ")
        LAT         = row[3]
        LONG        = row[4]
        APPLE_UPDATE_DATE      = row[5]
        TIME_SINCE_LAST_UPDATE = row[6]
        TIME_SINCE_LAST_UPDATE = TIME_SINCE_LAST_UPDATE.replace("Min","Min Ago")
        SERIAL_NUMBER          = row[1]
        STATUS_MARK            = row[8]
        DEGREES_LOCATION       = row[9]
        ADDRESS                = row[10][0:50]
        ADDRESS=ADDRESS.replace(","," ")
        BATTERYSTATUS          = row[11]
        B=int(BATTERYSTATUS.replace("%",""))
        if B == 100:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
        elif B > 79:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS) 
        elif B > 59:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
        elif B > 39:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
        elif B > 19:
           BATTERYSTATUS="🪫"+str(BATTERYSTATUS)
        elif B >0:   
           BATTERYSTATUS="🪫" +str(BATTERYSTATUS)
        else:   
           BATTERYSTATUS="💤" +str(BATTERYSTATUS)
        if TYPE == "Device":
           BOLD="<b>"
        else:
           BOLD=""
        #
        # Load up the security file in to a list to check if the user should have access to the device_item
        #
        from .paths import CUST_DIR
        DIR = CUST_DIR
        SHOW="0"
        if request.user.is_authenticated:
           logged_in_username = request.user.username
           # Call the function with the desired username and serial_number
           device_details = get_device_details(logged_in_username, SERIAL_NUMBER)
           # Check if the function returned a result
           if device_details:
              found_user = "true" 
              # Reference the values in the returned dictionary
              device_ID = str(device_details['id'])
              username = device_details['username']
              serial_number = device_details['Serial_Number']
              SERIALN = serial_number
              description = device_details['Description']
              DESCR = description
              X=DESCR[0:1]
              tag_type = device_details['Tag_Type']
              TYPE_OF_TAG = tag_type
              attributes = device_details['Attributes']
              SHOW = attributes
              lat = device_details['Lat']
              HOME_LAT = lat
              longi = device_details['Long']
              HOME_LONG = longi
              category=device_details['category']

              #feeder_value = str(device_details['feeder'])
              #feeder_prefix = feeder_value.replace(" ", "_").replace("/", "_").replace("@", "_").replace("-", "_")
              #feeder_form = FeederForm(prefix=feeder_prefix)
              #ip_address_value = feeder_form['ip_address'].value()

              #from .models import DeviceItemSecurity
              #feeder_instance = device_details.feeder
              #if feeder_instance is not None:
              #   feeder_form = FeederForm(instance=feeder_instance)
                 #ip_address_value = feeder_form['ip_address'].value()
              #else:
              #   ip_address_value = None
              #print("ip_address_value=",ip_address_value)

              #try:   
              #    device = DeviceItemSecurity.objects.get(username__iexact=username, Serial_Number__iexact=serial_number)
              #print("feeder=",feeder)
              # logged_in_username, SERIAL_NUMBER
              try:
                  device_item_security_instance = DeviceItemSecurity.objects.get(
                       username__iexact=logged_in_username,
                       Serial_Number__iexact=SERIAL_NUMBER
                  )

                  if device_item_security_instance.feeder:
                     feeder_instance = device_item_security_instance.feeder
                     ip_address = feeder_instance.ip_address
                     iphone = feeder_instance.iphone.replace("iphone","")
                     #print("IP Address:", ip_address)
                  else:
                     ip_address = ""
                     iphone = ""
                     #print("Feeder is not set for this DeviceItemSecurity instance.")

              except DeviceItemSecurity.DoesNotExist:
                  ip_address = ""
                  iphone = ""
                  print("DeviceItemSecurity instance not found.")

              if ADDRESS == "Home":
                  #formatted_distance_from_home="🏠"
                  formatted_distance_from_home="0 km"
                  distance_from_home=0
              else:
                 distance_from_home=home_distance_for_serial_number(float(HOME_LAT),float(HOME_LONG),float(LAT),float(LONG))
                 formatted_distance_from_home = "{:.0f}".format(distance_from_home)
                 formatted_distance_from_home=str(formatted_distance_from_home)+" km"

              #if SHOW == "1":
                 #ADDRESS="<font color=red>[🔐 Private]"
              #   perc=percentage(SERIAL_NUMBER)
              #
              # Call the function to get the lowest,highest date and days count for a serial number's data
              #
              #serial_number='B0P00224757D'
              #distance_from_home=home_distance_for_serial_number(float(HOME_LAT),float(HOME_LONG),float(LAT),float(LONG))
              #formatted_distance_from_home = "{:.2f}".format(distance_from_home)
#
              #  
              #   Add logic here to check platform == 'mobile' and show different simple screen for phones
              #  
              # change this later to have a more compressed view for mobile - hard coded until proper mobile design
              ###platform="computer"
              #
              #if platform == 'computer' and (category_selected == category or category_selected == "ALL" or (category_selected == "ACTIVE" and distance_today > 0)):
              if platform == 'computer' or platform =='mobile' and (category_selected == category or category_selected == "ALL" or category_selected == "ACTIVE" or category_selected == "AWAY" or category_selected == "ALERTS"):
               if heading_once == True:
                  if category_selected == "ACTIVE": 
                     head="<font size=5><center>{Tag Selection: Only <b>Active</b> Tags}"
                  else:
                     head="<font size=5><center>{Tag Selection: <b>"+category_selected+"}</b>"
                     #head="<font size=5><center>Tag Selection: <b>"+category_selected+"</b><font size=8><a href=/theme/ticket_list/>🎟️</a><font size=5>Create Ticket" 
                  fs="<font size=3>"
                  fc00="<tr><td><b><center>"+fs+"#</td>"
                  fc01="<td><b><center>"+fs+"Map</td>"
                  fc01a="<td><b><center>"+fs+"Trips</td>"
                  fc02="<td><center>"+fs+"🔌</td>"
                  fc03="<td><center>"+fs+"<b>🔋</td>"
                  fc04="<td nowrap>"+fs+"<b>Tag Type</td>"
                  fc05="<td>"+fs+"<b>🛠 </td>"
                  fc06="<td nowrap>"+fs+"<b>Tag Name/📌Current Location</td>"
                  fc06mobile="<td nowrap>"+fs+"<b>Tag Name/Location</td>"
                  fc07="<td nowrap>"+fs+"<b>Data Date/Time</td>"
                  fc08="<td ALIGN=CENTER>"+fs+"🚥</td>"
                  fc09="<td nowrap>"+fs+"<b>Updated</td>"
                  fc10="<td><b>"+fs+"<center><font size=3>#Days</b></td>"
                  #fc10="<td><b>"+fs+"<center><a href='javascript:void(0);' title='Total number of of days of data collection for this item'>#Days</b></td></a>"
                  fc11="<td><b>"+fs+"<a href=/theme/gps_log_5min_today_last/ACTIVE/><font color=black><b><center><font size=3>Today</a></td>"
                  ##fc11="<td><b>"+fs+"<font color=black><b><center><font size=2>Today</td>"
                  #fc11="<td><b>"+fs+"<font color=black><b><a href='javascript:void(0);' title='Total number of km this item has moved (as the crow flies)'><center>Today</td></a>"
                  fc12="<td><b>"+fs+"<font color=black><b><a href='javascript:void(0);' title='# of km this item has travelled since activation'><center>Total</td></a>"
                  fc13="<td nowrap><b>"+fs+"<a href=/theme/gps_log_5min_today_last/AWAY/><font size=3><center>km Home</a></td><td><center>"+fs+"<b><a href='/theme/map_chart_explain/' target='_blank' title='Click to get explanation of Clickable Symbols or see below:\n🌐=Current Google Location Map for a tag\n🌍=Map of ALL available data for a tag\n🗾=Map of route travelled today for a tag\n📊=Distance From Home Chart for a tag\n📉=Distance travelled per day for a tag\n📈=Distance From Home Chart for each day for a tag\n♨️=Heat Map for just today for a tag\n🔥=Heat Map for All available data for a tag'>Maps/Charts</a></td>"
                  #fc13="<td nowrap><b>"+fs+"<a href='javascript:void(0);' title='#km currently from Home'><center>Home</td>"
                  fc14="<td nowrap><b>"+fs+"<a href='javascript:void(0);' title='Distance from Home'><center>H</td>"
                  fc15="<td nowrap><b>"+fs+"<a href='javascript:void(0);' title='km each day'><center>T</td>"
                  #fc16="<td nowrap><b>"+fs+"<a href='javascript:void(0);' title='Edit Configuration'><center>Tag</td>"
                  #fc16="<td nowrap><b>"+fs+"<center>Tag</td>"
                  fc16a="<td nowrap><b>"+fs+"<center>Trip</td>"
                  fc17="<td><center>"+fs+"📂</td>"
                  fc18="<td nowrap><center>"+fs+"🌍</td>"
                  fc19="<td nowrap>"+fs+"<b>Current Location</td>"
                  fc20="<td nowrap>"+fs+"<b><center>Category</td>"
                  fc21="<td nowrap>"+fs+"<a href=/theme/gps_log_5min_today_last/ALERTS/><font size=3><center><b>Alerts</a></td>"
                  if platform == "mobile":
                     #file_contents=head+fc00+fc06mobile+"<tr>"
                     file_contents=head+fc00+fc06mobile+fc10+fc11+fc13+fc08+fc09+fc17+"<tr>"
                  else:
                     file_contents=head+fc00+fc06+fc10+fc11+fc13+fc08+fc09+fc17+fc03+fc02+fc21+fc01a+"<tr>"
                     # with category # file_contents=head+fc00+fc06+fc19+fc10+fc11+fc13+fc08+fc09+fc17+fc03+fc02+fc20+fc01a+fc21+"<tr>"
                  heading_once=False
               lowest_date,highest_date,count = data_get_low_high_count_dates(serial_number)
               distance_today,total_home,total_non_home,different_updated_dates_ctr,pct_diff=todays_distance_for_serial_number("",SERIAL_NUMBER)
               total_non_home=round(total_non_home*5/60,1)
               total_home=round(total_home*5/60,1)
               total_distance=0
               # add Dec 15, 2023 due to failing when feeder record has issue
               try:
                   percent_out=round(total_non_home/(total_home+total_non_home)*100)
               except:
                   percent_out = 0
               fs="<font size=3>"
               if SHOW == "0" and (category_selected == category or category_selected == "ALL" or category_selected == "ACTIVE" or category_selected == "AWAY" or category_selected == "ALERTS"):
                 # add trips
                 if 1 == 2:
                  from .models import Trip_Events
                  trip_data = Trip_Events.objects.filter(
                      trip_user=logged_in_username,
                      trip_serial=serial_number
                  ).values('trip_number', 'trip_description', 'start_date_time', 'end_date_time').first()

                  if trip_data:
                     trip_number = trip_data['trip_number']
                     start_date_time = trip_data['start_date_time']
                     end_date_time = trip_data['end_date_time']
                     trip_description = trip_data['trip_description']+" - date range: "+start_date_time+":"+end_date_time
                     trip_icon="💢"
                     trip_description = trip_description.replace("'", "") 
                     trip_link_string="<a href=/theme/show_map_trips_new/"+str(trip_number)+" target=_blank title='"+str(trip_description)+"'>"+trip_icon+"</a>"
                  else:
                     trip_number=""
                     trip_description=""
                     start_date_time=""
                     end_date_time=""
                     trip_icon=""
                     trip_link_string=""

                 from .models import Trip_Events

                 # Query the database to get all matching Trip_Events records
                 matching_records = Trip_Events.objects.filter(
                     trip_user=logged_in_username,
                     trip_serial=serial_number
                 ).values('trip_number', 'trip_description', 'start_date_time', 'end_date_time')

                 # Initialize an empty list to store trip_link_strings for all records
                 trip_link_strings = []
                 trip_link_string=""

                 # Loop through the matching records and create trip_link_strings
                 for record in matching_records:
                      trip_number = record['trip_number']
                      start_date_time = record['start_date_time']
                      end_date_time = record['end_date_time']
                      trip_description = "TRIP: "+record['trip_description'] + " - date range: " + start_date_time + ":" + end_date_time
                      trip_icon = "💢"
                      trip_description = trip_description.replace("'", "")
                      trip_link_string = f"<a href=/theme/show_map_trips_new/{trip_number} target=_blank title='{trip_description}'>{trip_icon}</a>"
                      trip_link_strings.append(trip_link_string)

                 # Check if any matching records were found
                 if trip_link_strings:
                     # Concatenate all the trip_link_strings into a single string
                     #trip_link_string = '\n'.join(trip_link_strings)
                     trip_link_string = ''.join(trip_link_strings)
                 else:
                     trip_link_string = ""

                 ###fc49="<tr><td><center>"+fs+str(item_counter)+"</td>"
                 fc49="<td nowrap><center>"+fs+"<a href=/theme/"+device_ID+"/device_update/ title='Device Update:"+tag_type+"' class='btn btn-outline-secondary btn-sm custom-btn btn-fixed-width30'>"+str(item_counter)+"</a></td>"
                 #fc49="<td nowrap><center>"+fs+"<a href=/theme/"+device_ID+"/device_update/ title='Device Update' class='btn btn-outline-secondary btn-sm custom-btn btn-fixed-width30'>"+str(item_counter)+"</a></td>"
                 fc50="<td><center>"+fs+"<a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank title='Day Map' class='btn btn-light btn-sm custom-btn'>Map</a></td>"
                 fc50a="<td><left>"+fs+"<a href=/theme/trip_new_init/"+SERIAL_NUMBER+"/ title='Create New Trip' class='btn btn-light btn-sm custom-btn'><font color=black><font size=3><b>+</a>"+trip_link_string+"</td>"
                 fc51="<td>"+fs+"<center>"+BATTERYSTATUS[0:1]+"</td>"
                 if int(BATTERYSTATUS[1:].replace("%","")) < 21: 
                    col="red"
                 else:
                    col="black"
                 fc52="<td><b><font color="+col+">"+fs+"<center>"+BATTERYSTATUS[1:]+"</td>"
                 fc53="<td>"+fs+BOLD+TYPE_OF_TAG+"</td>"
                 fc54="<td>"+fs+X+"</td>"
                 if ADDRESS == "Home":
                    c="<font color=black><b>"
                 else:
                    c="<font color=blue><b>"
                 fc55="<td nowrap>"+fs+DESCR[:42]+"("+iphone+")&nbsp;📌"+c+ADDRESS+"</td>"

                 #feeder_instance = Feeder.objects.get(pk=feeder) 
                 #ip_address = feeder_instance.referenced_model.ip_address

                 #fc55="<td nowrap>"+fs+DESCR[:42]+"&nbsp;📌"+c+ADDRESS+feeder+"</td>"
                 fc55mobile=fc68="<td nowrap>"+fs+DESCR+"<font size=1>("+iphone+")"+BATTERYSTATUS[0:1]+STATUS_MARK+"</font><br>&nbsp;📌"+c+ADDRESS+"</td>"
                 fc56="<td nowrap>"+fs+SAMPLE_DATE+"</td>"
                 fc57="<td>"+fs+STATUS_MARK+"</td>"
                 fc58="<td nowrap>"+fs+"<center>"+TIME_SINCE_LAST_UPDATE+"</td>"
                 fc59="<td><center>"+fs+str(count)+"</td>"
                 #fc59="<td><center>"+fs+"<button class='btn btn-outline-primary btn-sm custom-btn btn-fixed-width40' title='Map of ALL data'><font size=3>"+str(count)+"</button></td>"
                 #fc59="<td><center>"+fs+"<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ target=_blank class='btn btn-outline-primary btn-sm custom-btn btn-fixed-width40' title='Map of ALL data'><font size=3>"+str(count)+"</a></td>"
                 if distance_today == 0:
                    c="<font color=black>"
                 else:
                    c="<font color=red><b>"
                 fc60="<td style='text-align: right;'>"+fs+c+str(round(distance_today))+" km</td>"
                 #fc60="<td><center>"+fs+"<a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank class='btn "+btn+" btn-sm custom-btn btn-fixed-width60' title='Map of Today'><font size=3>"+str(round(distance_today))+" km</a></td>"

                 fc61="<td nowrap style='text-align: right;'>"+fs+"<font color=black>"+str(round(total_distance))+" km</td>"
                 fc63="<td nowrap><center>"+fs+"<a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/ALL target=_blank title='ALL Distance Map'>📉</a></td>"
                 fc64="<td nowrap><center>"+fs+"<a href=/theme/chart_distance_by_serial_by_day/"+SERIAL_NUMBER+"/ target=_blank title='Distance by day'>📊</a></td>"
                 fc66="<td>"+fs+"<a href=/theme/gps_log_5min_unit/"+SERIAL_NUMBER+" class='btn btn-light btn-sm custom-btn'>➕</a></td>"
                 fc67="<td nowrap>"+fs+"<a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank class='btn btn-light btn-sm custom-btn'>"+"📍"+"</a></td>"
                 if ADDRESS == "Home":
                    c="<font color=black>"
                 else:
                    c="<font color=blue><b>"
                 fc68="<td nowrap>"+fs+c+ADDRESS[:40]+"</td>"
                 #fc68="<td nowrap>"+fs+"<a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank class='btn btn-outline-secondary btn-sm custom-btn btn-fixed-width30'>"+fs+"📍</a> "+ADDRESS[:25]+"</td>"
                 # get the alerts, if any and put a bell with link to the alert and hover text of alert desc and date/time
                 from .paths import CUST_DIR
                 with open(CUST_DIR+'/tag_alerts_history.log') as csvfile:
                      data = csv.reader(csvfile)

                 import csv
                 from datetime import datetime, timedelta

                 # Assuming the 8th field is at index 7 (0-indexed)
                 alert_string=""
                 alert_message_index = 6
                 alert_serial_index = 7
                 alert_serial_values = []
                 alert_count=0
                 btn_color='btn-outline-success'
                 data = []
                 from .paths import CUST_DIR
                 with open(CUST_DIR+'/tag_alerts_history.log') as csvfile:
                      dataX = csv.reader(csvfile)
                      data = list(dataX)

                 filtered_data = [row for row in data if len(row) > alert_serial_index and row[alert_serial_index] == SERIAL_NUMBER]
                 first_message = filtered_data[0][alert_message_index] if filtered_data else None

                 alert_count=len(filtered_data)
                 # [0][0] is first field in the first row (ie. datetime)
                 first_record_datetime_str = filtered_data[0][0] if filtered_data else None
                 if first_record_datetime_str:
                    first_record_datetime = datetime.strptime(first_record_datetime_str, '%Y-%m-%d_%H:%M:%S')
                    time_difference = datetime.now() - first_record_datetime
                    time_difference_without_microseconds = (datetime.min + time_difference).replace(microsecond=0)
                    time_without_date = time_difference_without_microseconds.time()
                    days_difference = time_difference.days

                    if time_difference < timedelta(hours=1):
                        btn_color = 'btn-outline-danger'
                    elif timedelta(hours=1) <= time_difference < timedelta(hours=4):
                        btn_color = 'btn-outline-secondary'
                    else:
                       btn_color = 'btn-outline-success'
                 if alert_count == 0:
                    btn_color = 'btn-outline-success'
                    alert_string=""
                 else:
                    #alert_string = f"<center><a href=/theme/tagalert_history_list/{SERIAL_NUMBER}/ title='Last Alert was {first_record_datetime_str}' class='btn {btn_color} btn-sm custom-btn'><font size=3><b>{alert_count}</a>"
                    alert_string = f"<center><a href=/theme/tagalert_history_list/{SERIAL_NUMBER}/ title='Last Alert was {first_record_datetime_str}\n{days_difference} days and {time_without_date} hours ago\nMessage: {first_message}' class='btn {btn_color} btn-sm custom-btn'><font size=3><b>{alert_count}</a>"
                 fc70 = f"<td nowrap>{fs}{alert_string}</td>"

                 if distance_from_home > 0.6:
                    col='<font color=red>'
                 else:
                    col='<font color=black>'
                 btn=""
                 fc62="<td style='text-align: right; nowrap;'>"+fs+"<right>"+col+str(formatted_distance_from_home)+"</td><td><center>"+fs+"<a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Google Map'><font size=3>🌐</a><a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Map of ALL data'><font size=3>🌍</a><a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=3>🗾</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart'><font size=3>"+"📊"+"</a>"+fs+"<a href=/theme/chart_distance_by_serial_by_day/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance per day'><font size=3>📉</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/ALL/ target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart Each Day'><font size=3>"+"📈"+"</a></a>"+fs+"<a href=/theme/heatmap_view/DAY"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for just today'><font size=3>♨️</a><a href=/theme/heatmap_view/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for All data'><font size=3>🔥</a></td>"
                 # changed Dec 20, 2023 for IOS testing
                 fc62mobile="<td style='text-align: right; nowrap;'>"+fs+"<right>"+col+str(formatted_distance_from_home)+"</td><td><center>"+fs+"<a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Google Map'><font size=3>🌐</a><a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=3>🗾</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart'><font size=3>"+"📊"+"</a><br>"+fs+"<a href=/theme/chart_distance_by_serial_by_day/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance per day'><font size=3>📉</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/ALL/ target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart Each Day'><font size=3>"+"📈"+"</a></a>"+fs+"<a href=/theme/heatmap_view/DAY"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for just today'><font size=3>♨️</a><a href=/theme/heatmap_view/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for All data'><font size=3>🔥</a></td>"
                 ###fc62mobile="<td style='text-align: right; nowrap;'>"+fs+"<right>"+col+str(formatted_distance_from_home)+"</td><td><center>"+fs+"<a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Google Map'><font size=3>🌐</a><a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=3>🗾</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart'><font size=3>"+"📊"+"</a><br>"+fs+"<a href=/theme/chart_distance_by_serial_by_day/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance per day'><font size=3>📉</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/ALL/ target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart Each Day'><font size=3>"+"📈"+"</a></a>"+fs+"<a href=/theme/heatmap_view/DAY"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for just today'><font size=3>♨️</a><a href=/theme/heatmap_view/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for All data'><font size=3>🔥</a></td>"
                 #fc62mobile="<td style='text-align: right; nowrap;'>"+fs+"<right>"+col+str(formatted_distance_from_home)+"</td><td><center>"+fs+"<a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Google Map'><font size=3>🌐</a><a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/ALL/ target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Map of ALL data'><font size=3>🌍</a><a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=3>🗾</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart'><font size=3>"+"📊"+"</a><br>"+fs+"<a href=/theme/chart_distance_by_serial_by_day/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance per day'><font size=3>📉</a><a href=/theme/line_chart_distance_from_home/"+SERIAL_NUMBER+"/ALL/ target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Distance From Home Chart Each Day'><font size=3>"+"📈"+"</a></a>"+fs+"<a href=/theme/heatmap_view/DAY"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for just today'><font size=3>♨️</a><a href=/theme/heatmap_view/"+SERIAL_NUMBER+" target=_blank class='btn btn-light btn-sm custom-btn btn-fixed-width20' title='Heat Map for All data'><font size=3>🔥</a></td>"
                 #fc70="<td nowrap>"+fs+alert_string+"</td>"
                 #col_row.append([fc69+fc55+fc68+fc59+fc60+fc61+fc62+fc53+fc57+fc63+fc64+fc65+fc66+fc67+fc52+fc51])
                 #row_num=row_num+1
                 #print("file_contents=",fc49+fc55+fc68+fc59+fc60+fc62+fc57+fc58+fc66)
                 if (category_selected == "ACTIVE" and distance_today > 0 ) or (category_selected != "ACTIVE" and category_selected != "AWAY" and category_selected != "ALERTS") or (category_selected == "AWAY" and ADDRESS != "Home") or (category_selected == "ALERTS" and btn_color == "btn-outline-danger"):
                    item_counter=item_counter+1
                    if platform == "mobile":
                       #file_contents=file_contents+fc49+fc55mobile+"<tr>"
                       file_contents=file_contents+fc49+fc55mobile+fc59+fc60+fc62mobile+fc57+fc58+fc66+"<tr>"
                    else:
                       file_contents=file_contents+fc49+fc55+fc59+fc60+fc62+fc57+fc58+fc66+fc52+fc51+fc70+fc50a+"<tr>"
                 else:
                    continue
               else:
                 continue
              else:
               # Mobile screen format
               if platform == 'mobile' and (category_selected == category or category_selected == "ALL" or category_selected      == "ACTIVE" or category_selected == "AWAY"):
                 fs="<font size=6>"
                 fc01="<tr><td>"+fs+"<b><center><font size=2>#</td>"
                 fc02="<td><center><b>"+fs+"🔌</td>"
                 fc06="<td nowrap><b>"+fs+"Name</td>"
                 fc19="<td nowrap><b>"+fs+"Location</td>"
                 fc08="<td ALIGN=CENTER><font size=2>🚥</td>"
                 file_contents=fc01+fc02+fc06+fc19+fc08
                 heading_once=False
               if platform == 'mobile' and (category_selected == category or category_selected == "ALL" or category_selected      == "ACTIVE" or category_selected == "AWAY"):
                fs="<font size=6>"
                fc50="<tr><td><center>"+fs+"<a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank title='Map it'>"+str(item_counter)+"</a></td>"
                fc51="<td>"+fs+"<center>"+BATTERYSTATUS[0:1]+"</td>"
                fc55="<td nowrap>"+fs+DESCR[1:]+"</td>"
                fc68="<td nowrap>"+fs+ADDRESS[:25]+"</td>"
                fc57="<td>"+fs+STATUS_MARK+"</td>"
                distance_today,total_home,total_non_home,different_updated_dates_ctr,pct_diff=todays_distance_for_serial_number("",SERIAL_NUMBER)
                if (category_selected == "ACTIVE" and distance_today > 0 ) or (category_selected != "ACTIVE" and category_selected != "AWAY") or (category_selected == "AWAY" and ADDRESS != "Home"):
                   item_counter=item_counter+1
                   file_contents=file_contents+fc50+fc51+fc55+fc68+fc57
                #
           #else:
           #   print('username/serial number not for this user..continue..')
    file.close()
    result=file_contents #+"<center><b><font size=2><font color=blue>Main Site: <a href=https://MrRobby.ca>https://MrRobby.ca</a>"
    if found_user == "false":
        result="<font color=red><br>You have not registered any Trackers as yet! Please contact us now!"
    args = {'result': result}
    return render(request, "view_log.html", args)

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def read_file_gps_5min_unit(request,ser):

    #
    # takes way too long to show 22 days so just show last day 1440 entries
    #
    import glob
    import csv
    one_day_ctr=0
    # format  of log files: DATA/20230119_B0P00224515E_gps.TEXT.log
    pattern = "*_"+ser+"_*gps.5min.TEXT.log"
    file_contents=""
    from .paths import CUST_DIR
    DIR = CUST_DIR+'/DATA'
    # Device,Rob’s MacBook Air,2023-01-19_18:15:07,43.83827738551673,-79.30015186037782,2023-01-19 17:58:33,17 Minutes,kWF4MTWIbyJ0,✔️,43°50′17.8″N79°18′0.5″W,'147, Mallory Avenue, Hagerman'
    file_contents="<tr><td><font size=2><b>TYPE</td><td nowrap><font size=2><b>Name</td><td nowrap><font size=2><b>Location</td><td nowrap><font size=2><b>Data Date/Time</td><td ALIGN=CENTER><font size=2>⏳</td><td nowrap><font size=2><b>Last Date/Time</td><td nowrap><font size=2><b>Last Update</td><td><fond size=2>➕</td><td nowrap><font size=2>⏩</td><td><font size=2>⏩</td><td><font size=2><center><b>Distance</b></td><td nowrap><center><font size=2><b>km Home</td>"

    previous_latitude = None
    previous_longitude = None
    for file_name in sorted(glob.glob(DIR+'/'+ pattern), reverse=True):
     with open(file_name, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
         #if one_day_ctr < 289*2:  # 2 days
         if one_day_ctr < 4032:  # about 14 days
          TYPE = row[0]
          TAGNAME = row[1]
          SAMPLE_DATE = row[2][0:16]
          SAMPLE_DATE=SAMPLE_DATE.replace("_", " ")
          LAT = row[3]
          LONG = row[4]
          APPLE_UPDATE_DATE = row[5]
          TIME_SINCE_LAST_UPDATE = row[6]
          SERIAL_NUMBER = row[1]
          STATUS_MARK = row[8]
          DEGREES_LOCATION = row[9]
          ADDRESS = row[10]
          if request.user.is_authenticated:
             logged_in_username = request.user.username
             device_details = get_device_details(logged_in_username, SERIAL_NUMBER)
             if device_details:
              username = device_details['username']
              serial_number = device_details['Serial_Number']
              SERIALN = serial_number
              description = device_details['Description']
              DESCR = description
              X=DESCR[0:1]
              tag_type = device_details['Tag_Type']
              TYPE_OF_TAG = tag_type
              attributes = device_details['Attributes']
              SHOW = attributes
              lat = device_details['Lat']
              HOME_LAT = lat
              longi = device_details['Long']
              HOME_LONG = longi
              if previous_latitude is not None and previous_longitude is not None:
                 distance = haversine(float(previous_latitude), float(previous_longitude), float(LAT), float(LONG))
              else:
                 distance = float(0)
              
              distance_from_home=home_distance_for_serial_number(float(HOME_LAT),float(HOME_LONG),float(LAT),float(LONG))
              previous_latitude = LAT
              previous_longitude = LONG              
              TIME_SINCE_LAST_UPDATE=TIME_SINCE_LAST_UPDATE.replace("Min","Min Ago")                
              TIME_SINCE_LAST_UPDATE=TIME_SINCE_LAST_UPDATE.replace("Agoutes","Ago")                
              rounded_num = round(distance, 2)
              formatted_num = "{:.2f}".format(rounded_num)
              formatted_distance_from_home = "{:.2f}".format(distance_from_home)
              file_contents=file_contents+"<tr><td><font size=2>"+TYPE_OF_TAG+"</td><td nowrap><font size=2>"+DESCR+"</td><td nowrap><font size=2>"+ADDRESS+"</td><td nowrap><font size=2>"+SAMPLE_DATE+"</td><td><font size=2>"+STATUS_MARK+"</td><td nowrap><font size=2>"+APPLE_UPDATE_DATE+"</td><td nowrap><font size=2><center>"+TIME_SINCE_LAST_UPDATE+"</td><td><font size=2><a href=/theme/gps_log_5min_unit/"+SERIAL_NUMBER+">➕</a></td><td nowrap><font size=2><a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank>"+"📍"+"</a></td><td><font size=2><a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" target=_blank>📌</a></td><td nowrap><font size=2><center>"+str(formatted_num)+" km</td><td nowrap><center><font size=2>"+str(formatted_distance_from_home)+" km</td>"
              one_day_ctr=one_day_ctr+1
    result=file_contents
    file.close()         
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

@user_passes_test(lambda u: u.is_superuser)
def read_file_gps_5min_today_airtag(request):
    from .paths import CUST_DIR
    f = open(CUST_DIR+'/gps_current_5min_AIRTAG.log', 'r',encoding="utf-8")
    file_contents = f.read()
    f.close()
    args = {'result': file_contents}
    return render(request, "view_log.html", args)

def get_temp():
    f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
    temperature = f.read()
    f.close()
    return temperature

def get_space():
    import os
    space = os.system('df')
    return space

def get_environment():
    from .paths2 import CUST_DIR2
    f = open(CUST_DIR2+'/Wilkyconsultants.conf', 'r')
    server_status = f.read()
    f.close()
    return server_status

def news(request):
    from gnewsclient import gnewsclient
    client = gnewsclient.NewsClient(language='english',
                                location='canada',
                                topic='sports',
                                max_results=50)
    news_list = client.get_news()
    file_contents = news_list
    #for item in news_list:
    #    print("Title : ", item['title'], "URL : ", item['link'])

    args = {'result': file_contents}
    return render(request, "news.html", args)

def business(request):
    from gnewsclient import gnewsclient
    client = gnewsclient.NewsClient(language='english',
                                location='canada',
                                topic='business',
                                max_results=50)
    news_list = client.get_news()
    file_contents = news_list
    args = {'result': file_contents}
    return render(request, "business.html", args)

def technology(request):
    from gnewsclient import gnewsclient
    client = gnewsclient.NewsClient(language='english',
                                location='canada',
                                topic='technology',
                                max_results=50)
    news_list = client.get_news()
    file_contents = news_list
    args = {'result': file_contents}
    return render(request, "technology.html", args)


#@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_list(request):
    list_contact_form = Contact.objects.all()
    return render(request,'contact_list.html',{'list_contact_form':list_contact_form})

#@user_passes_test(lambda u: u.is_superuser)
class ContactCreate(CreateView):
    model = Contact
    fields = ['name', 'email', 'phone', 'reason', 'message']
    success_url = '/theme/contact_list'

#@user_passes_test(lambda u: u.is_superuser)
class ContactUpdate(UpdateView):
    model = Contact
    fields = ['name', 'email', 'phone', 'reason', 'message']
    success_url = '/theme/contact_list'

#@user_passes_test(lambda u: u.is_superuser)
class ContactDelete(DeleteView):
    model = Contact
    success_url = '/theme/contact_list'

#@login_required
@user_passes_test(lambda u: u.is_superuser)
def Research_Assistant_list(request):
    list_Research_Assistant_form = Research_Assistant.objects.all()
    return render(request,'Research_Assistant_list.html',{'list_Research_Assistant_form':list_Research_Assistant_form})

#@user_passes_test(lambda u: u.is_superuser)
class Research_AssistantCreate(CreateView):
    model = Research_Assistant
    fields = ['user', 'category', 'subcategory', 'keywords', 'url', 'notes']
    success_url = '/theme/Research_Assistant_list'

#@user_passes_test(lambda u: u.is_superuser)
class Research_AssistantUpdate(UpdateView):
    model = Research_Assistant
    fields = ['category', 'subcategory', 'keywords', 'url', 'notes']
    success_url = '/theme/Research_Assistant_list'

#@user_passes_test(lambda u: u.is_superuser)
class Research_AssistantDelete(DeleteView):
    model = Research_Assistant
    success_url = '/theme/Research_Assistant_list'

#@login_required
@user_passes_test(lambda u: u.is_superuser)
def Research_AssistantX(request):
    if request.method == 'POST':
        form = Research_AssistantForm(request.POST)

        if form.is_valid():
            current_user = request.user
            user  = current_user
            category  = request.POST.get('Research_Assistant_category', '')
            subcategory = request.POST.get('Research_Assistant_subcategory', '')
            keywords  = request.POST.get('Research_Assistant_keywords', '')
            #create_date = models.DateTimeField(auto_now_add=True)
            #update_date = models.DateTimeField(auto_now=True)
            url = request.POST.get('Research_Assistant_url', '')
            notes = request.POST.get('Research_Assistant_notes', '')
            p = Research_Assistant(user=user, category=category, subcategory=subcategory, keywords=keywords, url=url, notes=notes)
            p.save()
            return redirect("/theme/Research_Assistant_list")
    else:
        form = Research_AssistantForm()

    return render(request, 'Research_Assistant.html', {'form': form})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def dyn_menu_list(request):
    from .models import menu
    list_menu_form = menu.objects.all().order_by('menu_dropdown','menu_order')
    return render(request,'dyn_menu_list.html',{'list_menu_form':list_menu_form})

#class dyn_menu_update(UpdateView):
#    model = menu
#    fields = ['menu_id','menu_title','menu_notes','menu_fb','menu_link','menu_align','menu_order','menu_status','menu_admin','menu_image','menu_dropdown','menu_new_window','menu_scope']
#    success_url = '/theme/dyn_menu_list'

class dyn_menu_update(UpdateView):
    model = menu
    form_class = dyn_menuForm_udpate
    #clone this template for use as update, update text to reflect that
    template_name = 'dyn_menu_update.html'

    def get_form(self, form_class=None):
        from .models import buttons
        form = super().get_form(form_class)
        current_user = self.request.user 
        if self.request.user.is_superuser:
           form.fields['menu_dropdown'].queryset = buttons.objects.all()
        else:
           form.fields['menu_dropdown'].queryset = buttons.objects.filter(user=current_user)
        return form
    success_url = '/theme/dyn_menu_list'

#@user_passes_test(lambda u: u.is_superuser)
class dyn_menu_delete(DeleteView):
    from .models import menu
    from django.views.generic.edit import CreateView, UpdateView, DeleteView
    model = menu
    success_url = '/theme/dyn_menu_list'


#@login_required
#@user_passes_test(lambda u: u.is_superuser)
def dyn_menu_new(request):
    #
    # importing menu as menuX because I have a conflict with a function named menu
    #
    from .models import menu as menuX
    from .models import buttons
    if request.method == 'POST':
        if request.user.is_superuser:
           super_user = "superuser"
        else:
           super_user = ""
        form = dyn_menuForm(request.POST,name=request.user.username,super_user=super_user)

        if form.is_valid():
            menu_id          = request.POST.get('menu_id', '')
            menu_id          = menu_id.replace(" ", "")
            menu_title       = request.POST.get('menu_title', '')
            menu_notes       = request.POST.get('menu_notes', '')
            menu_fb          = request.POST.get('menu_fb', '')
            menu_link        = request.POST.get('menu_link', '')
            menu_align       = request.POST.get('menu_align', '')
            menu_order       = request.POST.get('menu_order', '')
            menu_status      = request.POST.get('menu_status', '')
            menu_admin       = request.POST.get('menu_admin', '')
            menu_image       = request.POST.get('menu_image', '')
            #
            # example of setting pk : https://groups.google.com/g/django-users/c/PcSDKZhPVmc
            #  - note, this took me a whole day to solve!
            #
            buttons_pk = request.POST.get('menu_dropdown')
            menu_dropdown = buttons.objects.get(pk=buttons_pk)
            #
            menu_new_window  = request.POST.get('menu_new_window', '')
            menu_scope  = request.POST.get('menu_scope', '')
            menu_header  = request.POST.get('menu_header', '')
            current_user = request.user
            menu_user  = current_user

            p = menuX(menu_id=menu_id, menu_title=menu_title, menu_notes=menu_notes, menu_fb=menu_fb, menu_link=menu_link, menu_align=menu_align, menu_order=menu_order, menu_status=menu_status, menu_admin=menu_admin, menu_image=menu_image, menu_dropdown=menu_dropdown, menu_new_window=menu_new_window,menu_scope=menu_scope,menu_user=menu_user,menu_header=menu_header)
            try:
               p.save()
            except:   
               # if form valid but get save error, likely a dup key
               messages.error(request, "Menu ID is not unique. Please specify a different Menu ID.")
               return render(request, 'dyn_menu.html', {'form': form})
            return redirect("/theme/dyn_menu_list")
        else:
            # if invalid form - show error messages and stay on form - difference between get_DROPDOWN_choices  - worksand get _DROPDOWN_choices(name) - does not work
            #
            #
            if request.user.is_superuser:
               super_user = "superuser"
            else:
               super_user = ""
            #form = dyn_menuForm(name=request.user.username,super_user=super_user)
            #
            return render(request, 'dyn_menu.html', {'form': form})
    else:
        if request.user.is_superuser:
           super_user = "superuser"
        else:
           super_user = ""
        form = dyn_menuForm(name=request.user.username,super_user=super_user)
        #form = dyn_menuForm(initial={"username": request.user.username})
        return render(request, 'dyn_menu.html', {'form': form})
    
#@login_required
def menu(request, menu_id):
    from .models import menu
    list_menu_form = menu.objects.all().filter(menu_id=menu_id)
    # django templates lose the value of menu.menu_image when in another loop so I am setting it in another variable(im) that works
    for menu in list_menu_form:
        im = menu.menu_image
        lnk = menu.menu_link
        # newly added Nov 9/22
        menu_admin = menu.menu_admin
        #
        new_window = menu.menu_new_window
    if lnk != "":
        if new_window == "Yes":
            return render(request, 'redirect.html', {'list_menu_form':list_menu_form})
        else:
            return redirect(lnk)
    import os
    import fnmatch
    from .paths import CUST_DIR
    path=CUST_DIR+'/theme/uploads/images'
    image_list = sorted(fnmatch.filter(os.listdir(path), menu_id+"*"))
    return render(request, 'menu.html', {'list_menu_form':list_menu_form, 'image_list':image_list, 'im':im})

#@user_passes_test(lambda u: u.is_superuser)
def buttons_new(request):
    from .models import buttons
    if request.method == 'POST':
        form = buttons_Form(request.POST)

        if form.is_valid():
            button      = request.POST.get('button', '')
            color       = request.POST.get('color', '')
            order       = request.POST.get('order', '')
            #
            # check if user is a superuser, if not then set scope to "USER" 
            #
            if request.user.is_superuser:
               scope       = request.POST.get('scope', '')
            else:
               scope       = "USER"
            current_user = request.user
            user  = current_user
            p = buttons(button=button,color=color,order=order,scope=scope,user=user)
            try:
               p.save()
            except:
               # if form valid but get save error, likely a dup key
               messages.error(request, "Button is not unique. Please specify a different Button Name.")
               return render(request, 'buttons.html', {'form': form})
            return redirect("/theme/buttons_list")
        else:
            # if invalid form - show error messages and stay on form
            return render(request, 'buttons.html', {'form': form})
    else:
        form = buttons_Form()
        return render(request, 'buttons.html', {'form': form})

#@user_passes_test(lambda u: u.is_superuser)
def buttons_list(request):
    from .models import buttons
    list_buttons_form = buttons.objects.all().order_by('order','button','color','user')
    return render(request,'buttons_list.html',{'list_buttons_form':list_buttons_form})

class buttons_update(UpdateView):
    from .models import buttons
    from django import forms
    #from django.views.generic.edit import CreateView, UpdateView, DeleteView
    model = buttons
    #fields = ['button','color','order','scope']
    form_class = buttons_update
    #clone this template for use as update, update text to reflect that
    template_name = 'button_update.html'

    def get_form(self, form_class=None):
        from .models import buttons
        form = super().get_form(form_class)
        #current_user = self.request.user
        if self.request.user.is_superuser:
           SCOPE_CHOICES = (
                ('ALL','ALL'),
                ('USER','USER'),
                           )
        else:
           SCOPE_CHOICES = (
                ('USER','USER'),
                           )
           USER_CHOICES = (
                (self.request.user,self.request.user),
                           )
           form.fields['scope'].choices = SCOPE_CHOICES
        return form
    success_url = '/theme/buttons_list'

class buttons_delete(DeleteView):
    from .models import buttons
    from django.views.generic.edit import CreateView, UpdateView, DeleteView
    model = buttons
    success_url = '/theme/buttons_list'

#
# blog
#

#
# show the list of Published blogs to users
#
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog.html'

#
# show the blog for all users
#
#class PostDetail(generic.DetailView):
#    model = Post
#    template_name = 'post_detail.html'


@user_passes_test(lambda u: u.is_superuser)
def hacker01(request):
    from .models import Post
    list_blog_form = Post.objects.all().order_by('created_on')
    return render(request,'blog_list.html',{'list_blog_form':list_blog_form})

def PostDetail(request, slug):
    from .models import Post
    list_blog_form = Post.objects.filter(slug=slug)
    import os
    import fnmatch
    from .paths import CUST_DIR
    path=CUST_DIR+'/theme/uploads/images'
    for slugs in list_blog_form:
        ps=slugs.slug+"*"
        im=slugs.image
        link=slugs.link
    image_list = sorted(fnmatch.filter(os.listdir(path), ps))
    return render(request,'post_detail.html',{'list_blog_form':list_blog_form, 'image_list':image_list,'ps':ps,'im':im,'link':link})
#
# exposing the Blog update screen
#
#class BlogList(generic.ListView):
#    queryset = Post.objects.filter(status=1).order_by('-created_on')
#    template_name = 'blog_list.html'

@user_passes_test(lambda u: u.is_superuser)
def BlogList(request):
    from .models import Post
    list_blog_form = Post.objects.all().order_by('created_on')
    return render(request,'blog_list.html',{'list_blog_form':list_blog_form})

class blog_update(UpdateView):
    from .models import Post
    model = Post
    form_class = blog_update
    template_name = 'blog_update.html'
    success_url = '/theme/blog_list'

class blog_delete(DeleteView):
    from .models import Post
    from django.views.generic.edit import DeleteView
    model = Post
    success_url = '/theme/blog_list'

def blog_new(request):
    from .models import Post
    if request.method == 'POST':
        form = blog_Form(request.POST)

        if form.is_valid():
            title      = request.POST.get('title', '')
            slug       = request.POST.get('slug', '')
            content    = request.POST.get('content', '')
            status     = request.POST.get('status', '')
            image      =  request.POST.get('image', '')
            link       =  request.POST.get('link', '')
            from django.contrib.auth.models import User
            userList = User.objects.values()
            for user in userList:
                if user["username"] == request.user.username:
                   author_id = user["id"]
            #p = Post(title=title,slug=slug,content=content,status=status,author_id=author_id)
            p = Post(title=title,slug=slug,content=content,status=status,author_id=author_id,image=image,link=link)
            try:
               p.save()
            except:
               messages.error(request, "Error, Save failed - Check that your slug is unique!")
               return render(request, 'blog_new.html', {'form': form})
            return redirect("/theme/blog_list")
        else:
            return render(request, 'blog_new.html', {'form': form})
    else:
        form = blog_Form()
        return render(request, 'blog_new.html', {'form': form})

class HomePageView(generic.ListView):
    from .models import upload
    #model = upload
    #queryset = upload.objects.filter().order_by('-id')[0]
    #queryset = upload.objects.all().last()
    queryset = upload.objects.all()
    template_name = 'home2.html'

class CreatePostView(CreateView): # new
    model = upload
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('home2')    


from urllib.parse import urlparse

def get_last_portion(url):
    path = urlparse(url).path
    if path.endswith('/'):
        path = path.rstrip('/')
    return path.split('/')[-1]

from django.views.generic.edit import FormView
from .forms import FileFieldForm
#
# post2 code
#
class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'post.html'  # Replace with your template.
    #success_url = '/theme/inventory_detail/'+last_portion+'/'
    #success_url = '/theme/inventory_list'  # Replace with your URL or reverse().
    #success_url = '/home2'  # Replace with your URL or reverse().
    def get_success_url(self):
        referring_url = self.request.POST.get('referring_url', '')
        last_portion = get_last_portion(referring_url)
        if last_portion and last_portion[0].isdigit():
           success_url = reverse('theme:inventory_detail', kwargs={'pk': last_portion})
        else:
           success_url = reverse('theme:blog')
        #success_url = reverse('theme:inventory_detail', kwargs={'last_portion': last_portion})
        return success_url

    def post(self, request, *args, **kwargs):
        #referring_url = request.POST.get('referring_url', '')
        #parts = referring_url.split('/')
        #last_portion = parts[-1]
        referring_url = request.POST.get('referring_url', '')
        #referring_url = request.META.get('HTTP_REFERER', '')
        last_portion = get_last_portion(referring_url)
        print("referring_url=",referring_url," last_portion=",last_portion)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            reason = request.POST.get('reason', '')
            for f in files:
                 handle_uploaded_file(f,reason,last_portion)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)    

def handle_uploaded_file(f,reason,last_portion):
    import os
    print("last_portion=",last_portion)
    n='/tmp/'+f.name
    head_tail = os.path.split(n)
    if head_tail[1] != "":
       with open(n, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)        
       import shutil
       from .paths import CUST_DIR
       #new_filename = CUST_DIR+'/theme/uploads/images/'+reason+"_"+head_tail[1]
       new_filename = CUST_DIR+'/theme/uploads/images/'+last_portion+"_"+head_tail[1]
       shutil.move(n, new_filename)            
       #os.rename(filename, new_filename)
            
def bitcoin():
    import requests
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data["bpi"]["USD"]["rate"]            

def FatherAbraham(request):
    return render(request, "FatherAbraham.html")

# test API creation URL - returns disk space on webserver
def get_disk_space(request):
    disk_info = psutil.disk_usage("/")
    return JsonResponse({
        "total": disk_info.total,
        "used": disk_info.used,
        "free": disk_info.free
    })

#def chatbot_new(request):
#    from django.http import HttpResponseRedirect
#    from .forms import chatbot
#    if request.method == "POST":
#        # Redirect the user to a different URL
#        return HttpResponseRedirect('/theme/chatbot/')
#    else:
#        return render(request, 'chatbot_new.html')

#def chatbot_view(request):
#    from django.shortcuts import render
#    #import openai
#    from .forms import chatbot
#    import requests
#    form_class = chatbot
#    # Get the user's message
#    message = request.POST.get('my_input')

    #api_endpoint = "https://api.openai.com/v1/completions"
    #model = "text-davinci-002"
    # Make the API request
    #headers = {
    #    "Content-Type": "application/json",
    #    "Authorization": f"Bearer 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"
    #}

    #response = requests.post(
    #    api_endpoint,
    #    headers=headers,
    #    json={
    #        "model": model,
    #        "prompt": message,
    #        #"max_tokens": 4000,
    #        "max_tokens": 2048,
    #        "temperature": 0.9,
    #    }
    #)

    # Get the chatbot's response
    #response_data = response.json()
    #chatbot_response = response_data['choices'][0]['text']

    #chatbot_response = "testing!"

    # Render the chatbot template
    #return render(request, 'chatbot.html', {'chatbot_response': chatbot_response})



from django.shortcuts import render, redirect

chat_history = []
def message_view(request):
    import requests
    if request.method == 'POST':
        message = request.POST.get('message')
        message_save = request.POST.get('message')
        #chat_history = []
        api_endpoint = "https://api.openai.com/v1/completions"
        model = "text-davinci-003"
        ##model = "text-davinci-002"
        #model = "text-curie-001"
        #model = "text-babbage-001"
        # Make the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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"
        }

        data = requests.post(
            api_endpoint,
            headers=headers,
            json={
                "model": model,
                "prompt": message,
                "max_tokens": 2048,
                "top_p": 1,
                "temperature": 0.9,
            }
        )

        response_text = data.json()["choices"][0]["text"]
        ##response_data = response.json()
        try:
            #message = "Query: \n"+message_save+"\n\n"+"Answer: "+response_data['choices'][0]['text']
            ##message = "Query: \n"+message_save+"\n\n"+"Answer: "+response_text
            message = ""
            chat_history.append("===>\n"+"Query: \n"+message_save+"\n\n"+"Answer: "+response_text)
            chat_history_reversed = chat_history[::-1]
            return render(request, 'message.html', {'message': message, 'chat_history':chat_history_reversed})
        except Exception:   
           message = "** The query received an error **\n"
           return render(request, 'message.html', {'message': message})
        #return render(request, 'message.html', {'message': message})
        #return render(request, 'message.html', {'message': chat_history})

    return render(request, 'message.html')
#
# Calc the distance between 2 sets of lat/long coordinates
# Example use: 
# print(round(haversine(lat1, lon1, lat2, lon2),1)," km")
# example use: haversine(previous_latitude, previous_longitude, latitude, longitude)
#
def haversine(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

import folium
from django.shortcuts import render
#
from .models import Trip_Events
@login_required
def show_map_trips(request,pk):
    # read the pk from Trip_Events
    from django.shortcuts import get_object_or_404
    trip_event = get_object_or_404(Trip_Events, pk=pk)
    start_date_time=trip_event.start_date_time[0:10]
    end_date_time=trip_event.end_date_time[:10]
    start_location_address=trip_event.start_location_address
    end_location_address=trip_event.end_location_address
    start_lat_long=trip_event.start_lat_long
    target_lat_long=trip_event.target_lat_long
    trip_description=trip_event.trip_description
    trip_category=trip_event.trip_category
    trip_user=trip_event.trip_user
    trip_serial=trip_event.trip_serial

    dt=start_date_time
    dt1=start_date_time
    dt2=end_date_time
    if dt2 == "":
       from datetime import datetime
       current_date = datetime.now().date()
       dt2 = current_date.strftime("%Y-%m-%d")
       #dt2="9999-99-99"
    ser=trip_serial

    from datetime import datetime
    import json
    now=datetime.now() # current date and time
    #icon_list = {"icons": ["✅", "🟠",     "🟡",     "🟢",     "🟣",     "🔵",     "🟤",     "🟦",     "🟧",     "🟨",     "🟩",     "🟪",     "🟫",    "🔰",     "🟥",     "🔒",     "🔏",     "🔐",     "🔑",     "🔎",  "🔖",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽",     "📿",     "🔅",     "🔆",     "🔇",     "📍" ]}
    icon_list = {"icons": ["✅", "🚗",     "🚕",     "🚙",     "🚌",     "🚎",     "🏎",     "🚓",     "🚑",     "🚒",     "🚐",     "🛻",     "🚚",    "🚛",     "🚜",     "🛴",     "🚲",     "🛵",     "🏍",     "🛺",  "🚍",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽",     "📿",     "🔅",     "🔆",     "🔇",     "📍", "⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳", "㉑", "㉒", "㉓", "㉔", "㉕", "㉖", "㉗", "㉘", "㉙", "㉚", "㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵", "㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿", "✅", "🚗",     "🚕",     "🚙",     "🚌",     "🚎",     "🏎 ",     "🚓",     "🚑",     "🚒",     "🚐",     "🛻",     "🚚",    "🚛",     "🚜",     "🛴",     "🚲",     "🛵",     "🏍 ",     "🛺",  "🚍",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽 ",     "📿",     "🔅",     "🔆",     "🔇",     "📍", "⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳", "㉑", "㉒", "㉓", "㉔", "㉕", "㉖", ">㉗", "㉘", "㉙", "㉚", "㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵", "㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿"]}
    D="_"
    coords = []
    HOME_coords = []
    TARGET_coords = []
    popup = []
    popup_tooltip = []
    bulb_color = []
    counter = []
    unique_dates = []
    set_icon = []
    addr = []
    full_date = []
    distance = []
    marker_counter=0
    unique_location_ctr=0
    unique_points_ctr=0
    serial_authorized="false"
    check_done="false"
    from .paths import CUST_DIR
    DIR=CUST_DIR
    accum_ser_chk=""
    if request.user.is_authenticated:
       logged_in_username = request.user.username
       device_details = get_device_details(logged_in_username, ser)
       if device_details:       
           serial_authorized="true"
    else:
        map_html="[1]Not authorized, please login to render maps!"
        return render(request, 'route.html', {'map_html': map_html})
    if serial_authorized == "false":
        map_html="[2]Not authorized!"
        return render(request, 'route.html', {'map_html': map_html})
    prev_popup_date=""
    popup_date="                    "
    import csv
    PREV_APPLE_UPDATE_DATE=""
    PREV_ADDRESS=""

    import glob
    import csv
    # format  of log files: DATA/20230119_B0P00224515E_gps.TEXT.log
    print("dt=",dt)
    # will never be ALL because this is a trip with 2 dates dt1 and dt2, fix later
    if dt == "ALL":
       #pattern = "*_"+ser+"_*gps.5min.TEXT.log"
       pattern = "*_"+ser+"_*gps.5min.TEXT.log.SUMMARY"
    else:
       from datetime import datetime
       # Your date strings
       # dt1 = "2023-10-16"
       # dt2 = "2023-11-02"
       # Convert the date strings to datetime objects
       date_format = "%Y-%m-%d"
       date1 = datetime.strptime(dt1, date_format)
       date2 = datetime.strptime(dt2, date_format)
       # Calculate the difference in days
       num_days = (date2 - date1).days

       dt_mod=str(dt[0:4])+str(dt[5:7])+str(dt[8:10])
       print("#days=",num_days)
       if num_days > 7:
          pattern = "*_"+ser+"_*gps.5min.TEXT.log.SUMMARY"
       else:
       #pattern = dt_mod+"_"+str(ser)+'_gps.5min.TEXT.log'
          pattern = "*_"+ser+"_*gps.5min.TEXT.log"
    try: 
     for file_name in sorted(glob.glob(DIR + '/DATA/' + pattern), reverse=True):
      with open(file_name, 'r', encoding="utf-8") as file:
        #reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
         DEVICE_ITEM = row[0]
         TAGNAME = row[1]
         SAMPLE_DATE = row[2]
         LAT = row[3]
         LONG = row[4]
         APPLE_UPDATE_DATE = row[5]
         TIME_SINCE_LAST_UPDATE = row[6]
         SERIAL_NUMBER = row[1]
         STATUS_MARK = row[8]
         DEGREES_LOCATION = row[9]
         ADDRESS = row[10]


         # Replace this with db looked, remove ini file use
         device_details = get_device_details(logged_in_username, ser)
         # Check if the function returned a result
         if device_details:
            serial_authorized="true"         
            #DESCR=device_details['Description']
            DESCR=trip_description
            TYPE_OF_ITEM=device_details['Tag_Type']
            SHOW=device_details['Attributes']
            HOME_LAT=device_details['Lat']
            HOME_LONG=device_details['Long']
            #category=device_details['category']

         from datetime import datetime, timedelta
         now=datetime.now() # current date and time
         date_string = now.strftime("%Y-%m-%d")
         date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
         # changed Oct 31, 2023 as not used
         #new_date_minus_7 = date_object - timedelta(days=365)
         #new_date_minus_7x = str(new_date_minus_7)                       

         if SAMPLE_DATE[0:10] >= dt1 and PREV_APPLE_UPDATE_DATE != APPLE_UPDATE_DATE and SAMPLE_DATE[0:10] <= dt2:
                  if PREV_APPLE_UPDATE_DATE != "":
                     DISTANCE=round(haversine(float(PREV_LAT),float(PREV_LONG), float(LAT), float(LONG)),2)
                  else:   
                     DISTANCE=0
                  unique_points_ctr=unique_points_ctr+1
                  distance.append(DISTANCE)   
                  unique_location_ctr=unique_location_ctr+1
                  PREV_APPLE_UPDATE_DATE=APPLE_UPDATE_DATE
                  popup_appledate=APPLE_UPDATE_DATE
                  PREV_LAT=LAT
                  PREV_LONG=LONG
                  popup_last_time_updated=APPLE_UPDATE_DATE
                  addr.append(ADDRESS)
                  full_date.append(SAMPLE_DATE)
                  # get the time indicator : ✅ means < 5 minutes, ❌ means > 1 hour, other means >5min<1hr
                  popup_last_time_updatedX=STATUS_MARK
                  popup_address=ADDRESS
                  popup_tagname=TAGNAME
                  dt="ALL"
                  if dt != "ALL":
                      serial_number = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ target=_blank><font size=2><font color=red><br>Click to show all data for Tag Name: <font color=blue>"+DESCR+"</a>"
                      #serial_number = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ target=_blank><font size=2><font color=red><br>Click to show all data for Tag Name: <font color=blue>"+TAGNAME+"</a>"
                  else:
                      serial_number = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+"/ target=_blank><font color=red><font size=2>Filter to this date only: <font color=blue>"+SAMPLE_DATE[0:10]+"</a>"
                  serial_number_11=SERIAL_NUMBER
                  # format it with this format
                  # <a href=/theme/show_map2/X9L7criU6EA/2023-01-06/ target=_blank>SERIAL#</a href>
                  prev_popup_date=popup_date
                  popup_date=SAMPLE_DATE[0:10]
                  # set the icon based on relative position of the unique date to the icon_list dictionary
                  if popup_date != prev_popup_date:
                     unique_dates.append(popup_date)
                     last_index = len(unique_dates) - 1
                     # allow access by index to the icon_list with icons variable
                     icons = icon_list['icons']
                     try:
                         set_icon.append(icons[last_index])
                     except:
                         set_icon.append("ERROR(NOT=)")
                  else:
                     last_index = len(unique_dates) - 1
                     icons = icon_list['icons']
                     set_icon.append(icons[last_index])
                  # Format html :
                  popup_lat_long_url="<td nowrap><font size=2><a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank>📍</a>"
                  # check if the user is on a mobile so we can make some text bigger
                  user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
                  if 'mobile' in user_agent or 'android' in user_agent:
                     device = "mobile"
                     FNT="<font size=4>"
                  else:
                     device = "computer"
                     FNT="<font size=1>"
                  
                  popup_text = FNT+"<b><font color=red>Device/item name: <font color=blue>"+TYPE_OF_ITEM+" "+DESCR+"<br><font color=red>Collection date/time: <font color=blue>"+SAMPLE_DATE+"<br><font color=red>Address: <font color=blue>"+ADDRESS+"<br><font color=red>Locate Age at time of collection: <font color=blue>"+STATUS_MARK+" "+TIME_SINCE_LAST_UPDATE+"<br><font color=red>Date/time located: <font color=blue>"+APPLE_UPDATE_DATE+"<br><font color=red>Located at Lat/long: <font color=blue>"+LAT+","+LONG+" :click to open: "+popup_lat_long_url +"<br>"+serial_number +"<br><font color=red>Distance to next point: <font color=blue>"+str(DISTANCE)+"km - "+PREV_ADDRESS
                  popup_tooltip_text = FNT+"<b><font color=red>Device/item name: <font color=blue>"+TYPE_OF_ITEM+" "+DESCR+"<br><font color=red>Collection date/time: <font color=blue>"+SAMPLE_DATE+"<br><font color=red>Address: <font color=blue>"+ADDRESS+"<br><font color=red>Locate Age at time of collection: <font color=blue>"+STATUS_MARK+" "+TIME_SINCE_LAST_UPDATE+"<br><font color=red>Date/time located: <font color=blue>"+APPLE_UPDATE_DATE+"<br><font color=red>Located at Lat/long: <font color=blue>"+LAT+","+LONG  +"<br><font color=red>Distance to next point: <font color=blue>"+str(DISTANCE)+"km - "+PREV_ADDRESS
                  PREV_ADDRESS=ADDRESS
                  popup.append(popup_text)
                  popup_tooltip.append(popup_tooltip_text)
                  marker_counter = marker_counter + 1
                  # once per hour instead of 5 minutes
                  #if marker_counter % 12 == 0: 
                  counter.append(str(marker_counter))
                  elements_num0=float(LAT)
                  elements_num1=float(LONG)
                  coords.append((elements_num0, elements_num1))
         #elif PREV_APPLE_UPDATE_DATE == APPLE_UPDATE_DATE and SAMPLE_DATE[0:10] > '2023-01-23': 
         elif PREV_APPLE_UPDATE_DATE == APPLE_UPDATE_DATE: 
                  unique_points_ctr=unique_points_ctr+1
    except:
       print("Bad date") 
    #FILE.close()
    # https://python.plainenglish.io/django-webapp-for-plotting-route-between-two-points-in-a-map-6f1babfeec59
    # List of coordinates
    # coords = [(43.8383632,-79.3000453), (43.8654045,-79.3129236), (43.8699234,-79.3055358)]

    # Create a Map instance, if the passed date yeilds 0 coordinates then we just fudge some to prevent error
    try:
       m = folium.Map(location=coords[0], zoom_start=12,zoom_control=False,control_scale=True,position='bottomleft')
       ##m = folium.Map(location=coords[0], zoom_start=15,zoom_control=False,control_scale=True,position='bottomleft')
    except:
       coords = [(43.8383632,-79.3000453), (43.8654045,-79.3129236), (43.8699234,-79.3055358)]
       m = folium.Map(location=coords[0], zoom_start=10,zoom_control=False)
    from folium.plugins import AntPath
    data2 = tuple(reversed(coords))
    AntPath(data2, delay=400,weight=3,color="black",dash_array=[60,20]).add_to(m)

    # reverse the counters as they are sorted by last data collected at the top
    counter_reversed = []
    for ele in reversed(counter):
        counter_reversed.append(ele)

    full_date_reversed = []
    for ele in reversed(full_date):
        full_date_reversed.append(ele)

    from folium.map import Popup
    from folium.map import Icon
    from folium.features import DivIcon
    first="true"
    for i, (coord,d,number,tt,set_the_icon,addrs,f_date_r,f_date,dist) in enumerate(zip(coords,popup,counter_reversed,popup_tooltip,set_icon,addr,full_date_reversed,full_date,distance)):
        popup = folium.Popup(d,max_width=1000, style='white-space: nowrap')
        if first == "true":
           #if SHOW == "0": 
           i=trip_description[0:1]
           html='<div style="font-size: 11pt;font-weight: bold;  color : red;white-space: nowrap;"><font size=7>'+i+'<font size=5>📌<font color=black><font size=2>' +addrs+' '+f_date[0:16]+'</div>'
           first="false"
        else:   
            if int(f_date[11:13]) < 12:
               tm="am"
            else:
               tm="pm"
            ratio=0
            if i != 0:
               from fuzzywuzzy import fuzz
               ratio = fuzz.token_sort_ratio(addr[i], addr[i-1])
               #if ratio > 92:
               if dist < 0.05:
                  tm=""
                  print_date=""
               elif ratio < 90:
                  print_date=f_date[11:16]
               else:
                  tm=""
                  print_date=""

            # check if the user is on a mobile so we can make some text bigger
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            if 'mobile' in user_agent or 'android' in user_agent:
                device = "mobile"
                FNT="<font size=4>"
            else:
                device = "computer"                  
                FNT="<font size=2>"
            # This is where it adds the time HH:MM to the trip icon.
            if trip_category == "NOTIME":
               html='<div style="font-size: 6pt;font-weight: bold;  color : blue;">'+set_the_icon ##+' <font color=black><b><font size=1></div>'+FNT+print_date #+'?'+str(DISTANCE)+'km'
            else:
               html='<div style="font-size: 6pt;font-weight: bold;  color : blue;">'+set_the_icon+'<font color=black><b><font size=1></div>'+FNT+print_date #+'?'+str(DISTANCE)+'km'

        #from folium.plugins import MarkerCluster
        #marker_cluster = MarkerCluster().add_to(m)            

        folium.Marker(coord,popup=popup,tooltip=tt,icon=DivIcon(html=html)).add_to(m)

        ####flashing icon
        # Create a MarkerCluster object with the icon_create_function parameter
        #marker_cluster = MarkerCluster(icon_create_function=lambda x: folium.Icon(icon='cloud', color='red'))

        # Add a marker to the MarkerCluster object with the popup and animation parameters
        #marker = folium.Marker(location=[coord], popup='Hello!', animation=True)

        # Add the marker to the MarkerCluster object and then add the MarkerCluster object to the map
        #marker_cluster.add_child(marker)
        #map.add_child(marker_cluster)
        ####flashing icon


        # Add home location from security file
        elements_num0=float(HOME_LAT)
        elements_num1=float(HOME_LONG)
        HOME_coords.append((elements_num0, elements_num1))

        # Create a LayerGroup
        LayerGroup = folium.FeatureGroup("LayerGroup")

        # Add a circle marker
        LayerGroup.add_child(folium.Marker(HOME_coords[0],icon=DivIcon(html='<font size=12>🏠')))
        # Add the LayerGroup to the map
        m.add_child(LayerGroup)                

        # Add target_lat_long finish line 🏁 flag
        try:
          target_lat, target_long = target_lat_long.split(',')
          target_lat = float(target_lat)
          target_long = float(target_long)
          TARGET_coords.append((target_lat, target_long))
          LayerGroup.add_child(folium.Marker(TARGET_coords[0],icon=DivIcon(html='<font size=12>🏁')))
          m.add_child(LayerGroup)
        except:
          print("Could not add the finish line due to invalid coordinates: "+target_lat_long)

    got_error="no"    
    if D == "_":
       last_index = len(unique_dates) - 1
       # get earliest date we have in the data
       try:
          earliest_date = unique_dates[last_index]
          latest_date = unique_dates[0]
          percent_points=round((unique_location_ctr*100)/unique_points_ctr)
          display_date="All Data - <font color=red>"+earliest_date+" : "+latest_date+" "+"<font color=black> - <br>"+str(last_index+1)+" days. <font color=green>Locations: "+str(unique_location_ctr)+"/"+str(unique_points_ctr)+" ["+str(percent_points)+"%]"+" <a href=/theme/trip_edit/"+str(pk)+"/edit/ target=_blank>Edit Trip</a>"
       except:
          got_error="yes"
       title_link_ALL=""
    else:
        # just one date
        try:
           from datetime import date, timedelta
           date_string = D[0:10] # "2022-01-01"
           date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
           new_date_minus_1 = date_object - timedelta(days=1)
           new_date_plus_1 = date_object + timedelta(days=1)

           now=datetime.now() # current date and time
           CHK_D=now.strftime("%Y-%m-%d")
           if CHK_D == D[0:10]: 
              PREV_DAY='<br><a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>['+str(new_date_minus_1)+'] 🔙 </a>[<font color=red>'+D[0:10]+'<font color=black>]' 
           else:   
              PREV_DAY='<br><a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>🗓['+str(new_date_minus_1)+']🔙</a><font color=red>'+D[0:10]+'<a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_plus_1)+'><font color=black>⮕['+str(new_date_plus_1)+'<font color=black>]</a>' 
           total_points=round(int(f_date_r[11:13])*12+int(f_date_r[14:16])/5)+1
           percent_points=round((unique_location_ctr*100)/total_points)
           display_date="<br><font size=3><font color=green> Locations: "+str(unique_location_ctr)+"/"+str(total_points)+" ["+str(percent_points)+"%]"+PREV_DAY
           #display_date=D[0:10]+"<font color=green> - Locations: "+str(unique_location_ctr)+"/"+str(total_points)+" ["+str(percent_points)+"%]"+PREV_DAY
        except Exception as e:
           got_error="yes"    
           total_points=0
        try:     
          title_link_ALL = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ target=_blank><font color=black>[ALL Dates]</a>"
        except Exception as e:
          got_error="yes" 
    if got_error == "no":
     loc = "<font size=3><font color=blue>"+TYPE_OF_ITEM+" - "+DESCR+"<font color=black> - "+display_date+" "+title_link_ALL
     #loc = "<font color=blue>"+popup_tagname+"<font color=black> - "+display_date+" "+title_link_ALL
     title_html = '''
          <h6 align="center" style="font-size:12px"><b>{}</b></h3>
          '''.format(loc)
     m.get_root().html.add_child(folium.Element(title_html))

     # Generate a polyline for the route
     ##folium.PolyLine(coords, color="black", weight=3, opacity=2, dash_array=5).add_to(m)
     #folium.PolyLine(coords, color="red", weight=2.5, opacity=1, dash_array=5).add_to(m)

     # Save the map to an HTML file
     map_html = m.get_root().render()
    else: 
     try:   
         map_html="<font color=red><font size=5>No Data Available - "+e
     except Exception as e:    
         map_html="<font color=red><font size=5>No Data Available "
    return render(request, 'route.html', {'map_html': map_html})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def show_findmy(request):
    import json
    import csv
    from datetime import datetime
    import json    
    from folium.map import Popup
    from folium.map import Icon
    from folium.features import DivIcon    
    icon_list = {"icons": ["🚗", "🚕",     "🚙",     "🚌",     "🚎",     "🏎",     "🚓",     "🚑",     "🚒",     "🚐",     "🛻",     "🚚",     "🚛",    "🚜",     "🛺",     "🛵",     "🏍",     "🔐",     "🔑",     "🔎",  "🔖",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽",     "📿",     "🔅",     "🔆",     "🔇",     "📍" ]}
    coords = []
    HOME_coords = []
    set_icon = []    
    addr = []    
    descr = []    
    counter=0
    from .paths import CUST_DIR
    file = open(CUST_DIR+'/gps_current_TEXT_5min_LAST.log', 'r',encoding="utf-8")
    reader = csv.reader(file, delimiter=',', quotechar="'")
    for row in reader:
        TYPE        = row[0]
        TAGNAME     = row[1]
        SAMPLE_DATE = row[2]
        LAT         = row[3]
        LONG        = row[4]
        APPLE_UPDATE_DATE      = row[5]
        TIME_SINCE_LAST_UPDATE = row[6]
        SERIAL_NUMBER          = row[1]
        STATUS_MARK            = row[8]
        DEGREES_LOCATION       = row[9]
        ADDRESS                = row[10]

        found_user="false"
        #user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        #if 'mobile' in user_agent or 'android' in user_agent:
        #    device = "mobile"
        #else:
        #    device = "computer"

        #if request.user.is_authenticated:
        #   logged_in_username = request.user.username
        #elif device == "mobile":
        #   logged_in_username = "alene"
        #else:
        #   logged_in_username = ""
        #if  logged_in_username != "":
        if request.user.is_authenticated:
           logged_in_username = request.user.username
           device_details = get_device_details(logged_in_username, SERIAL_NUMBER)
           if device_details:
              username = device_details['username']
              serial_number = device_details['Serial_Number']
              SERIALN = serial_number
              description = device_details['Description']
              DESCR = description
              X=DESCR[0:1]
              tag_type = device_details['Tag_Type']
              TYPE_OF_TAG = tag_type
              attributes = device_details['Attributes']
              SHOW = attributes
              lat = device_details['Lat']
              HOME_LAT = lat
              longi = device_details['Long']
              HOME_LONG = longi
              found_user = "true"
              elements_num0=float(LAT)
              elements_num1=float(LONG)
              coords.append((elements_num0, elements_num1))
              elements_num0=float(HOME_LAT)
              elements_num1=float(HOME_LONG)
              HOME_coords.append((elements_num0, elements_num1))
              descr.append(DESCR)
              addr.append(ADDRESS)
              counter=counter+1              
   
    if counter > 0:
       m = folium.Map(location=coords[0], zoom_start=11,zoom_control=False)
       # I need to add the descr of each tag here as a Legend
       title_html='<font size=2><b><font color=blue>Legend: </b></font><br>'
       for coord, icon, addrs, descrs, HOME_coord in zip(coords, icon_list["icons"], addr, descr, HOME_coords):
           addrs=addrs[:25]
           title_html=title_html+"<b>"+descrs+"</b>-"+addrs+"<br>"
           descrs=descrs[:8]
           html = "<div style='white-space:nowrap;'><font size=8>" + '<b><font size=3> ' + ' '.join(map(str, descrs))+"</b></div>"
           #html = "<div style='white-space:nowrap;'><font size=8>" + '<b><font size=3> ' + ' '.join(map(str, descrs))+"</b></div>"
           ##html = "<div style='white-space:nowrap;'><font size=8>" + ' '.join(map(str, icon))+ '<b><font size=3> ' + ' '.join(map(str, descrs))+"</b></div>"
           marker = folium.Marker(location=coord, icon=folium.DivIcon(html=html))
           marker.add_to(m)

           # Create a LayerGroup
           LayerGroup = folium.FeatureGroup("LayerGroup")
           # Add a home marker
           LayerGroup.add_child(folium.Marker(HOME_coord,icon=DivIcon(html='<font size=5>🏠')))
           # Add the LayerGroup to the map
           m.add_child(LayerGroup)
       #m.get_root().html.add_child(folium.Element(title_html))
       map_html = m.get_root().render()
       map_html = '<table>'+title_html+'</table><table>'+map_html+'</table>'
       return render(request, 'route.html', {'map_html': map_html})
    else:
       map_html = "<font color=red><font size=6>No Tags allocated, contact Tag Central!"
       title_html=''
       return render(request, 'route.html', {'map_html': map_html,'title_html': title_html})

def percentage(serial_number_input):
  import csv
  import glob
  from datetime import datetime, timedelta
  # get the current date
  today = datetime.now().date()

  # calculate the date 7 days ago
  seven_days_ago = today - timedelta(days=7)


  # list of input files
  from .paths import CUST_DIR
  input_files = glob.glob(CUST_DIR+"/DATA/*_*_gps.5min.TEXT.log")

  # dictionary to store the results
  results = {}

  for input_file in input_files:
    with open(input_file, "r",encoding="utf-8") as f:
        # use the csv reader to read the file
        reader = csv.reader(f)
        # skip the header row
        next(reader)

        # keep track of the previous record
        prev_record = None

        for record in reader:
            serial_number = record[1]

            sample_date = record[2][:10]

            # check if the sample date is within the past 7 days
            if datetime.strptime(sample_date, "%Y-%m-%d").date() < seven_days_ago:
              continue

            # initialize the record in the dictionary if it doesn't exist
            if serial_number not in results:
                results[serial_number] = {
                    "Tag_name": record[1],
                    "change_counter": 0,
                    "total_counter": 0,
                }

            results[serial_number]["total_counter"] += 1

            # check if the apple_date field has changed
            if prev_record and prev_record[1] == serial_number and prev_record[5] != record[5]:
                results[serial_number]["change_counter"] += 1

            prev_record = record

  # generate the HTML table
  html_output=""
  #html_output = "<table>"
  #html_output += "<tr>"
  #html_output += "<th>Serial Number</th>"
  #html_output += "<th>Tag Name</th>"
  #html_output += "<th>Change Counter</th>"
  #html_output += "<th>Total Counter</th>"
  #html_output += "<th>Percentage Counter</th>"
  #html_output += "</tr>"

  for serial_number, data in results.items():
     if serial_number == serial_number_input:
      percentage_counter = data["change_counter"] / data["total_counter"] * 100
      #html_output += "<tr>"
      #html_output += f"<td><font size=2>{serial_number}</td>"
      #html_output += f"<td>{data['Tag_name']}</td>"
      html_output += f"<td align=right><font size=2>{data['change_counter']}</td>"
      html_output += f"<td align=right><font size=2>{data['total_counter']}</td>"
      html_output += f"<td align=right><font size=2>{percentage_counter:.1f}%</td>"
      #html_output += "</tr>\n"

  #html_output += "</table>"
  return html_output

from django.shortcuts import render
# URL : device_security
def device_ini_show_data(request):
    result = device_ini_json_to_html()
    args = {'result': result}
    return render(request, "view_log.html", args)    


def device_ini_json_to_html():
    import json
    from .paths import CUST_DIR
    json_file=CUST_DIR+'/device_item_security.ini'
    with open(json_file, 'r',encoding="utf-8") as file:
        data = json.load(file)

    html_string = '<table border=1>'
    for user in data['users']:
        html_string += '<tr><td colspan="6"><font color=blue><b>Username:</b><font color=black> {}</td></tr>'.format(user['username'])
        html_string += '<tr><th>ID</th><th>Name</th><th>Tag Type</th><th>Tag Attr</th><th>Home Latitude</th><th>Home Longitude</th><td><b>Home Location</td></tr>'
        for device in user['Device_Item']:
            html_string += '<tr>'
            html_string += '<td><font size=2>{}</td>'.format(device[0])
            html_string += '<td><font size=2>{}</td>'.format(device[1])
            html_string += '<td><font size=2>{}</td>'.format(device[2])
            html_string += '<td><center><font size=2>{}</td>'.format(device[3])
            html_string += '<td><font size=2>{}</td>'.format(device[4])
            html_string += '<td><font size=2>{}</td>'.format(device[5])
            html_string += '<td nowrap><center><font size=2><a href=https://www.google.com/maps/place/'+str(device[4])+','+str(device[5])+' target=_blank>'+'📍'+'</a></td>'
            html_string += '</tr>\n'
    html_string += '</table>'
    return html_string

import csv
from django.db.models import Q

#def export_to_csv():
#        writer = csv.writer(file)
#        writer.writerow(['Username', 'Serial Number', 'Description', 'Tag Type', 'Attributes', 'Latitude', 'Longitude'])
#
#        for device_item in DeviceItemSecurity.objects.all():
#            writer.writerow([device_item.username, device_item.Serial_Number, device_item.Description, device_item.Tag_Type, device_item.Attributes, device_item.Lat, device_item.Long])

# used for exporting the security to json file
#import json
#from django.db.models import Q

#def export_to_json():
#   data = []
#   for device_item in DeviceItemSecurity.objects.all().order_by("username", "Tag_Type", "Serial_Number"):
#      data.append({
#      'Username': device_item.username,
#      'Serial Number': device_item.Serial_Number,
#      'Description': device_item.Description,
#      'Tag Type': device_item.Tag_Type,
#      'Attributes': device_item.Attributes,
#      'Latitude': device_item.Lat,
#      'Longitude': device_item.Long
#      })


#import json
#
#def export_to_json2():
#   data = []
#   for device_item in DeviceItemSecurity.objects.all().order_by("username", "Tag_Type", "Serial_Number"):
#      data.append({
#         'username': device_item.username,
#         'device_item': [
#            device_item.Serial_Number,device_item.Description,device_item.Tag_Type,device_item.Attributes,device_item.Lat,device_item.Long
#         ]
#      })

#      for item in data:
#          file.write(json.dumps(item, ensure_ascii=False, separators=(',', ':')) + '\n')

# How to call: import_from_csv()
#
# Purpose: import the csv data for the serial numbers table in to the db, to be used when I move to prod
#
import csv
from django.core.exceptions import ValidationError

def import_from_csv():
    from .paths import CUST_DIR
    with open(CUST_DIR+'/device_item_security.csv', 'r',encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader) # skip the first row (headers)

        for row in reader:
            try:
                device_item = DeviceItemSecurity(
                    username=row[0],
                    Serial_Number=row[1],
                    Description=row[2],
                    Tag_Type=row[3],
                    Attributes=row[4],
                    Lat=row[5],
                    Long=row[6]
                )
                device_item.full_clean() # validate the model
                device_item.save()
            except ValidationError as e:
                print(f"Validation error: {e}")

from django.shortcuts import render, redirect
from .models import DeviceItemSecurity

# theme/device_list
@login_required
def device_item_security_list(request):
    #export_to_csv()
    #export_to_json2()
    #import_from_csv()  # use to load table from csv
    #device_item_security = DeviceItemSecurity.objects.all().order_by("username", "Tag_Type", "Serial_Number")
    logged_in_username = request.user.username
    if request.user.is_staff:
       device_item_security = DeviceItemSecurity.objects.all().order_by("username", "Tag_Type", "Serial_Number")
    else:   
       device_item_security = DeviceItemSecurity.objects.filter(username=logged_in_username).order_by("username", "Tag_Type", "Serial_Number")
    #device_item_security = DeviceItemSecurity.objects.all()
    context = {'device_item_security': device_item_security}
    return render(request, 'device_item_security_list.html', context)

@login_required
def device_item_security_list_feeder(request, pk):
    logged_in_username = request.user.username
    #device_item_security = DeviceItemSecurity.objects.all().order_by("username", "Tag_Type", "Serial_Number")
    desired_feeder = Feeder.objects.get(pk=pk)
    device_item_security = DeviceItemSecurity.objects.filter(feeder=desired_feeder)
    context = {'device_item_security': device_item_security}
    return render(request, 'device_item_security_list.html', context)

@login_required
def device_item_security_update(request, pk):
    #double chk this user didn't change the url to access unauth record
    logged_in_username = request.user.username
    if request.user.is_staff:
       try:
          device_item_security = DeviceItemSecurity.objects.get(pk=pk)
       except:
          return HttpResponse("Record does not exist, perhaps someone just deleted it?", status=404)           
    else:   
       try:
          device_item_security = DeviceItemSecurity.objects.get(pk=pk,username=logged_in_username)
       except:
          return HttpResponse("No access to that record permitted!", status=404)    
    #device_item_security = DeviceItemSecurity.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeviceItemSecurityForm(request.POST, instance=device_item_security)
        if form.is_valid():
            form.save()
            return redirect('theme:device_item_security_list')
    else:
        form = DeviceItemSecurityForm(instance=device_item_security)
    context = {'form': form}
    return render(request, 'device_item_security_form.html', context)

#@login_required
@user_passes_test(lambda u: u.is_superuser)
def device_item_security_delete(request, pk):
    #double chk this user didn't change the url to access unauth record
    #logged_in_username = request.user.username
    #try:
    #   device_item_security = DeviceItemSecurity.objects.get(pk=pk,username=logged_in_username)
    #except:
    #    return HttpResponse("No access to that record permitted!", status=404)
    device_item_security = DeviceItemSecurity.objects.get(pk=pk)
    if request.method == 'POST':
        device_item_security.delete()
        return redirect('theme:device_item_security_list')
    context = {'device_item_security': device_item_security}
    return render(request, 'device_item_security_confirm_delete.html', context)

#@login_required
@user_passes_test(lambda u: u.is_superuser)
def device_item_security_create(request):
    if request.method == 'POST':
        form = DeviceItemSecurityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('theme:device_item_security_list')
    else:
        form = DeviceItemSecurityForm()
    context = {'form': form}
    return render(request, 'device_item_security_form.html', context)


#@login_required
@user_passes_test(lambda u: u.is_superuser)
def device_item_security_clone(request, pk):
    #logged_in_username = request.user.username
    #try:
    #   existing_instance = DeviceItemSecurity.objects.get(pk=pk,username=logged_in_username)
    #except:
    #    return HttpResponse("No access to that record permitted!", status=404)
    
    existing_instance = DeviceItemSecurity.objects.get(pk=pk)
    instance_dict = {field.name: getattr(existing_instance, field.name) for field in existing_instance._meta.get_fields()}
    if request.method == 'POST':
        form = DeviceItemSecurityForm(request.POST)
        if form.is_valid():
            new_instance = form.save()
            return redirect('theme:device_item_security_list')
    else:
        form = DeviceItemSecurityForm(initial=instance_dict)
    context = {'form': form}
    return render(request, 'device_item_security_form.html', context)

from .models import DeviceItemSecurity

def get_device_details(username, serial_number):
    try:
        device = DeviceItemSecurity.objects.get(username__iexact=username, Serial_Number__iexact=serial_number)
        return {
            'id': device.id,
            'username': device.username,
            'Serial_Number': device.Serial_Number,
            'Description': device.Description,
            'Tag_Type': device.Tag_Type,
            'Attributes': device.Attributes,
            'Lat': device.Lat,
            'Long': device.Long,
            'category': device.category,
            'feeder': device.feeder
        }
    except DeviceItemSecurity.DoesNotExist:
        return None

import re
import glob

def data_get_low_high_count_dates(serial_number):
    # the pattern of the file names
    from .paths import CUST_DIR
    file_pattern = CUST_DIR+'/DATA/*_'+serial_number+'_gps.5min.TEXT.log'

    # the regular expression pattern to extract the date and serial number
    regex_pattern = r'(\d{8})_([\w+]{12})_gps.5min.TEXT.log'

    # a dictionary to keep track of the highest and lowest date for each serial number
    dates = {}

    # get the list of file names that match the pattern
    file_list = glob.glob(file_pattern)

    # loop through the file names and extract the date and serial number
    for file_name in file_list:
        match = re.search(regex_pattern, file_name)
        if match:
            date = match.group(1)
            serial_number = match.group(2)

            # add the serial number to the dictionary if it's not already there
            if serial_number not in dates:
                dates[serial_number] = [date, date, 1]
            else:
                # update the highest and lowest date if necessary
                if date < dates[serial_number][0]:
                    dates[serial_number][0] = date
                elif date > dates[serial_number][1]:
                    dates[serial_number][1] = date
                dates[serial_number][2] += 1

    # return the results in a tuple
    return dates[serial_number][0], dates[serial_number][1], dates[serial_number][2]

import csv
import os
import math

def process_csv_files(user,path, pattern):
    serial_numbers = {}
    return_string="<p><center><font color=blue><b>Tag Analytics - By Day</b></center><table border=1><tr><td><b><font color=black><font size=2>Date</td><td nowrap><b><font size=2>Tag type</td><td><b><font size=2>🛠</td><td><b><font size=2>Description</td><td><b><font size=2>Serial</td><td><b><center><font size=2>Distance</td><td><b><center><font size=2>No Travel</td><td><b><center><font size=2>Travel</td><td><b><center><font size=2>Travel%</td><td><center><font size=2><font color=black><b>✅Ping%</td>"
    files = os.listdir(path)
    files = sorted(files, key=lambda x: (x[8:], x[:8]))
    previous_serial_number = None
    sum_return_string=""
    for filename in files:
        if not filename.endswith(pattern):
            continue
        date, serial_number = filename.split("_")[:2]
        total_distance = 0
        previous_latitude = previous_longitude = None
        with open(os.path.join(path, filename),encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                latitude = float(row[3])
                longitude = float(row[4])
                if previous_latitude is not None and previous_longitude is not None:
                    total_distance += haversine(previous_latitude, previous_longitude, latitude, longitude)
                previous_latitude = latitude
                previous_longitude = longitude
        if previous_serial_number is not None and previous_serial_number != serial_number:
            if tag_type != "Unknown":
               #return_string = return_string + "<tr><td>.</td><td><center>-</td><td><center>-</td>"
               return_string=return_string+"<tr><td><b><font color=black><font size=2>Date</td><td nowrap><b><font size=2>Tag type</td><td><b><font size=2>🛠</td><td><b><font size=2>Description</td><td><b><font size=2>Serial</td><td><b><center><font size=2>Distance</td><td><b><center><font size=2>No Travel</td><td><b><center><font size=2>Travel</td><td><b><center><font size=2>Travel%</td><td><center><font size=2><font color=black><b>Ping%</td>"
        device_details = get_device_details(user, serial_number)
        # Check if the function returned a result
        if device_details:
           description = device_details['Description']
           tag_type = device_details['Tag_Type']
        else:
           description="Unknown"
           tag_type="Unknown"
        if tag_type != "Unknown":   
           # run it
           #serial_number="HGFJP6UFP0GV"
           #date="20230212"
           home_ctr,non_home_ctr,pct_non_home = count_home_nonhome_records(serial_number,date)
           #print(home_ctr,non_home_ctr,pct_non_home)
           #total_distance=day_distance_for_serial_number(date,serial_number)
           # added feb 14, 2023
           distance_today,total_home,total_non_home,different_updated_dates_ctr,pct_diff=todays_distance_for_serial_number(date,serial_number)
           #
           return_string=return_string+"<tr><td nowrap><a href=/theme/show_map2/"+serial_number+"/"+date[0:4]+"-"+date[4:6]+"-"+date[6:8]+" target=_blank><font size=2>"+date+"</a></td><td nowrap><font size=2>"+tag_type+"</td><td nowrap><font size=2>"+description[0:1]+"</td><td nowrap><font size=2>"+description[1:]+"</td><td><font size=2><font color=black>🔒"+serial_number+"</td><td><center><font size=2>"+str(round(total_distance,1))+" km</td><td><center><font size=2>"+str(home_ctr)+"</td><td><center><font size=2>"+str(non_home_ctr)+"</td><td><center><font size=2>"+str(round(pct_non_home))+"%</td><td><center><font size=2>"+str(round(pct_diff))+"%</td>\n"
        previous_serial_number = serial_number
        if serial_number in serial_numbers:
            serial_numbers[serial_number] += total_distance
        else:
            serial_numbers[serial_number] = total_distance
    return_string=return_string+"</table>"
    sum_return_string=sum_return_string+"<center><font color=blue><b>Tag Analytics - Over ALL and Today</center><table border=1><tr>"
    sum_return_string=sum_return_string+"<td colspan=4><center>Tag Information</td><td colspan=7><center>Over ALL</td><td colspan=7><center>Today</td><tr><td nowrap><b><font size=2>Tag type</td><td><font color=blue><b>🛠</td><td><font color=black><b><font size=2>Description</td><td><b><font size=2>Serial</td><td><b><font size=2><font color=black>Date Range</td><td><font size=2><font color=black><b><center>Distance</td><td><b><font size=2><font color=black><center>Days</td><td nowrap><b><font size=2><font color=black><center>/Day</td><td><b><center><font size=2>No Travel</td><td><b><center><font size=2>Travel</td><td><b><center><font size=2>Travel%</td><td><font size=2><font color=black><b><center>Distance</td><td><b><font size=2><font color=black><center>No Travel</td><td nowrap><b><font size=2><font color=black><center>Travel</td><td><b><center><font size=2>Travel%</td><td><b><center><font size=2>#✅Ping</td><td><b><center><font size=2>✅Ping%</td>"
    for serial_number, total_distance in serial_numbers.items():
        # look up tag description from db and add to report
        device_details = get_device_details(user, serial_number)
        # Check if the function returned a result
        if device_details:
           description = device_details['Description']
           tag_type = device_details['Tag_Type']
        else:
           description="Unknown"
           tag_type="Unknown"
        lowest_date,highest_date,count = data_get_low_high_count_dates(serial_number)
        avg=round(float(total_distance/count),1)
        if tag_type != "Unknown":   
           home_ctr_sum,non_home_ctr_sum,pct_non_home_sum = count_home_nonhome_records_sum(serial_number)
           distance_today,total_home,total_non_home,different_updated_dates_ctr,pct_diff=todays_distance_for_serial_number("",serial_number)
           #total_distance=all_distance_for_serial_number(serial_number)
           #avg=round(total_distance/count)
           try:
              percent_out=round(total_non_home/(total_home+total_non_home)*100)
           except:
              percent_out=0
           sum_return_string=sum_return_string+"<tr><td><font size=2>"+tag_type+"</td><td nowrap><font size=2>"+description[0:1]+"</td><td><font size=2>"+description[1:]+"</td><td nowrap><font size=2><font color=black>🔒"+serial_number+"</td><td nowrap><font size=1>"+str(lowest_date)+" to "+str(highest_date)+"</td><td nowrap><center><font size=2>"+str(round(total_distance,1))+" km</td><td><font size=2><a href=/theme/show_map2/"+serial_number+"/ALL/ target=_blank><font size=2><center>"+str(count)+"</a></td><td nowrap><center><font size=2>"+str(avg)+" km</td><td><center><font size=2>"+str(home_ctr_sum)+"</td><td><center><font size=2>"+str(non_home_ctr_sum)+"</td><td><center><font size=2>"+str(pct_non_home_sum)+"%</td><td><font size=2><a href=/theme/gps_log_5min_unit/"+serial_number+" target=_blank><center>"+str(round(distance_today,1))+" km</a></td><td><center><font size=2><font color=black>"+str(total_home)+"</td><td><center><font size=2><font color=black>"+str(total_non_home)+"</td><td><center><font size=2><font color=black>"+str(percent_out)+"%</td><td><center><font size=2><font color=black>"+str(different_updated_dates_ctr)+"</td><td nowrap><a href=/theme/show_map2/"+serial_number+"/"+date[0:4]+"-"+date[4:6]+"-"+date[6:8]+" target=_blank><font size=2><center>"+str(pct_diff)+"%</a></td>\n"
    sum_return_string=sum_return_string+"</table>"
    return(sum_return_string+return_string)

@login_required
def distance_summary_report(request):
    user = request.user.username
    from .paths import CUST_DIR
    # change Oct 14. 2023 - read from RAMDisk for performance
    #CUST_DIR='/Volumes/RAMDisk'
    result=process_csv_files(user,CUST_DIR+"/DATA/", "_gps.5min.TEXT.log")
    args = {'result': result}
    return render(request, "view_log.html", args)

#
# get the lowest, highest dates for a serial number and the # of days
#
import re
import glob

def data_get_low_high_count_dates(serial_number):
    # the pattern of the file names
    from .paths import CUST_DIR
    file_pattern = CUST_DIR+'/DATA/*_'+serial_number+'_gps.5min.TEXT.log'

    # the regular expression pattern to extract the date and serial number
    regex_pattern = r'(\d{8})_([\w+]{12})_gps.5min.TEXT.log'

    # a dictionary to keep track of the highest and lowest date for each serial number
    dates = {}

    # get the list of file names that match the pattern
    file_list = glob.glob(file_pattern)

    # loop through the file names and extract the date and serial number
    for file_name in file_list:
        match = re.search(regex_pattern, file_name)
        if match:
            date = match.group(1)
            serial_number = match.group(2)

            # add the serial number to the dictionary if it's not already there
            if serial_number not in dates:
                dates[serial_number] = [date, date, 1]
            else:
                # update the highest and lowest date if necessary
                if date < dates[serial_number][0]:
                    dates[serial_number][0] = date
                elif date > dates[serial_number][1]:
                    dates[serial_number][1] = date
                dates[serial_number][2] += 1

    # return the results in a tuple
    return dates[serial_number][0], dates[serial_number][1], dates[serial_number][2]
#
# Compute distance between last point and current point
# Add logic so that if we get a apple time less than current we just use distance of 0
#
import csv
import datetime
from math import radians, sin, cos, sqrt, atan2
def todays_distance_for_serial_number(date,serial_number):
    if date == "":
       #today = datetime.datetime.now().strftime("%Y%m%d")
       today = datetime.now().strftime("%Y%m%d")
    else:   
       today=date 
    from .paths import CUST_DIR
    filename = f"{CUST_DIR}/DATA/{today}_{serial_number}_gps.5min.TEXT.log"
    total_distance = 0
    total_non_home = 0
    total_home = 0
    different_updated_dates_ctr=1
    try:
     with open(filename, 'r',encoding="utf-8") as file:
        reader = csv.reader(file)
        #reader = csv.reader(f, delimiter=',', quotechar='"')
        ##header = next(reader) # skip the header row
        previous_latitude = None
        previous_longitude = None
        previous_updated_date_time = None

        for row in reader:
            latitude = float(row[3])
            longitude = float(row[4])
            description = row[10]
            updated_date_time = row[5]
            location=description
            if location == "Home" or "Mallory" in location or "Kimbark" in location or "Goldhawk" in location or "Loganberry" in location or "Wenlock" in location:
            #if description == "Home":
               total_home=total_home+1
            else:
               total_non_home=total_non_home+1
            if previous_latitude is not None and previous_longitude is not None:
                # if the current updated data is less than previous we have some issue with the data so dist=0
                if updated_date_time >= previous_updated_date_time:
                   distance = 0 
                else:   
                   different_updated_dates_ctr=different_updated_dates_ctr+1 
                   distance = haversine(previous_latitude, previous_longitude, latitude, longitude)
                   if distance >= 0.250:
                      total_distance += distance
            previous_latitude = latitude
            previous_longitude = longitude
            previous_updated_date_time = updated_date_time
    except:
       pct_diff=0
        
    # get div by zero error at 00:00 cuz only 1 record        
    try:
       pct_diff=round(different_updated_dates_ctr/(total_home+total_non_home)*100)
    except:
       pct_diff=0 
    #
    return round(total_distance,1),total_home,total_non_home,different_updated_dates_ctr,pct_diff

# Count the # of points at home vs away for a specific date
#
import os
import csv
def count_home_nonhome_records(serial_number, date):
    home_ctr = 0
    non_home_ctr = 0
    from .paths import CUST_DIR
    filename = f"{CUST_DIR}/DATA/{date}_{serial_number}_gps.5min.TEXT.log"
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as f:
            #reader = csv.reader(f)
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for fields in reader:
                if len(fields) >= 11:
                    location = fields[10].strip()
                    #print(location)
                    if location == "Home" or "Mallory" in location or "Kimbark" in location or "Goldhawk" in location or "Loganberry" in location or "Wenlock" in location:
                        home_ctr += 1
                    else:
                        non_home_ctr += 1
    pct_non_home = round(non_home_ctr / (home_ctr + non_home_ctr) * 100, 1)
    return home_ctr, non_home_ctr, pct_non_home

#
# Count the # of points at home vs away for all data
#
import csv
import glob
import os

def count_home_nonhome_records_sum(serial_number):
    home_ctr = 0
    non_home_ctr = 0
    from .paths import CUST_DIR
    file_pattern = f"{CUST_DIR}/DATA/*_{serial_number}_gps.5min.TEXT.log"
    for filename in glob.glob(file_pattern):
        if os.path.exists(filename):
            with open(filename, 'r', encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                for fields in reader:
                    if len(fields) >= 11:
                        location = fields[10].strip()
                        if location == "Home" or "Mallory" in location or "Kimbark" in location or "Goldhawk" in location  or "Wenlock" in location:
                            home_ctr += 1
                        else:
                            non_home_ctr += 1
    pct_non_home = round(non_home_ctr / (home_ctr + non_home_ctr) * 100)
    return home_ctr, non_home_ctr, pct_non_home

def all_distance_for_serial_number(serial_number):
   from .paths import CUST_DIR
   file_pattern = f"{CUST_DIR}/DATA/*_{serial_number}_gps.5min.TEXT.log"
   files = glob.glob(file_pattern)
   files = sorted(glob.glob(file_pattern))
   total_distance = 0

   for file in files:
       with open(file, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        previous_latitude = None
        previous_longitude = None
        previous_updated_date_time = None

        for row in reader:
            latitude = float(row[3])
            longitude = float(row[4])
            description = row[10]
            updated_date_time = row[5]
            if previous_latitude is not None and previous_longitude is not None:
                #if updated_date_time >= previous_updated_date_time:
                #    distance = 0
                #else:
                distance = haversine(previous_latitude, previous_longitude, latitude, longitude)
                total_distance += distance
            previous_latitude = latitude
            previous_longitude = longitude
            previous_updated_date_time = updated_date_time
   return round(total_distance)

def day_distance_for_serial_number(day,serial_number):
   from .paths import CUST_DIR
   file_pattern = f"{CUST_DIR}/DATA/{day}_{serial_number}_gps.5min.TEXT.log"
   files = glob.glob(file_pattern)
   files = sorted(glob.glob(file_pattern))
   total_distance = 0

   for file in files:
       with open(file, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        previous_latitude = None
        previous_longitude = None
        previous_updated_date_time = None

        for row in reader:
            latitude = float(row[3])
            longitude = float(row[4])
            description = row[10]
            updated_date_time = row[5]
            if previous_latitude is not None and previous_longitude is not None:
                #if updated_date_time >= previous_updated_date_time:
                #    distance = 0
                #else:
                distance = haversine(previous_latitude, previous_longitude, latitude, longitude)
                total_distance += distance
            previous_latitude = latitude
            previous_longitude = longitude
            previous_updated_date_time = updated_date_time
   return round(total_distance)
# distance from Home
def home_distance_for_serial_number(Home_lat,Home_long,Lat,Long):
   distance = haversine(Home_lat, Home_long, Lat, Long)
   return round(distance,2)   

from django.shortcuts import render

def handler404(request, slug):
    return render(request, '404.html', {'slug': slug})

from django.shortcuts import render

def custom_404_view(request, exception=None):
    return render(request, 'theme/404.html', status=404)

import os
import glob
import mpld3
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime

def plot_distance_from_home_by_serial_and_date(user, passed_serial, passed_date):
    # URL: /theme/line_chart_distance_from_home/HGFJP6UFP0GV/2023-02-24/
    # 20230225_B0P00224749A_gps.5min.TEXT.log
    filter_date=passed_date.replace("-","") 
    # Define the path pattern to search for files
    device_details = get_device_details(user, passed_serial)
    if device_details:
       desc = device_details['Description']
    from .paths import CUST_DIR
    DATA_DIR=CUST_DIR+'/DATA'
    os.system('cd '+CUST_DIR+'/DATA')
    #debugmsg=user+" "+passed_serial+" "+passed_date
    #  f.write(debugmsg+'\n')
    #f.close
    if passed_date == "ALL":
       path_pattern = f"*_{passed_serial}_gps.5min.TEXT.log"
    else:
       path_pattern = f"{filter_date}_{passed_serial}_gps.5min.TEXT.log"

    # Create a dictionary to store the data for each serial
    data_by_serial = {}

    # Create the plot
    fig, ax = plt.subplots()

    # Search for files that match the pattern
    # f.write('DEBUG begin\n')
    if passed_date == "ALL":
        chart=DATA_DIR+'/chart.tmp'
        os.system('rm '+chart)
        for filename in sorted(glob.glob(DATA_DIR+"/"+path_pattern)):
            c_date=filename[51:60]
            if c_date > '20230220':
               os.system('cat '+filename+' >>' + chart)
        os.system('sort '+chart+'>' + chart+'.srt')
        path_pattern=chart+'.srt'
    #for filename in sorted(glob.glob(path_pattern)):
    if passed_date != "ALL":
     path_pattern=DATA_DIR+'/'+path_pattern
    with open(path_pattern, 'r',encoding="utf-8") as csvfile:
    #with open(chart+'.srt', 'r',encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            #next(reader)  # skip header row
            for i, row in enumerate(reader):
                # Parse the fields
                serial_number = row[1]
                row[2]=row[2].replace("_"," ")
                capture_datetime = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
                try:
                   distance_from_home = round(float(row[7]))  # remove commas from distance field
                except:
                   distance_from_home = round(float(0.0))

                # Add the data to the dictionary for the corresponding serial
                if serial_number not in data_by_serial:
                    data_by_serial[serial_number] = {'x': [], 'y': [], 'label': ""}
                    #data_by_serial[serial_number] = {'x': [], 'y': [], 'label': f"Ser {serial_number}"}
                capture_datetime_str = capture_datetime.strftime('%Y-%m-%d %H:%M:%S')
                data_by_serial[serial_number]['x'].append(capture_datetime)
                data_by_serial[serial_number]['y'].append(distance_from_home)

            # Add the data value to the plot
            ##ax.annotate(str(distance_from_home), xy=(capture_datetime, distance_from_home), fontsize=10)

    # Plot the data
    for serial_data in data_by_serial.values():
        ax.plot(serial_data['x'], serial_data['y'], label=serial_data['label'],color='#008000',linewidth=4)
        ####ax.bar(serial_data['x'], serial_data['y'], label=serial_data['label'])

    ax.legend(fontsize=22)
    ax.set_xlabel('Time ['+passed_date+"]",fontsize=18,color='#FF0000')
    ax.set_ylabel('Distance from home (km)',fontsize=18, color='#FF0000')
    # set the y axis away from the numbers
    ax.yaxis.set_label_coords(-0.10, 0.5)
    ax.set_title(f"Distance from home for  : "+desc,fontsize=22,color='#0000FF')
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    ax.grid(True,linewidth=0.1,color='#AFF000')
    ax.set_ylim(bottom=0)

    # add thr labels to the Distance_from_home points
    #ctr=12
    #for x,y in zip(serial_data['x'],serial_data['y']):
    # if ctr == 12:
    #  label = "{:.0f}".format(y)
    #  plt.annotate(label, # this is the text
    #             (x,y), # these are the coordinates to position the label
    #             textcoords="offset points", # how to position the text
    #             xytext=(-50,10), # distance from text to points (x,y)
    #             ha='center') # horizontal alignment can be left, right or center
    #  ctr=0
    # ctr=ctr+1

    # Generate the HTML code for the plot and return it
    plt.tight_layout()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)
    return html

import glob
import os
import numpy as np
import mpld3
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from datetime import datetime
from geopy.distance import geodesic
from datetime import datetime

# Define a function to calculate the distance between two points using their latitude and longitude values:
def calculate_distance(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).km

def plot_distance_by_day_by_serial(user, ser):
  ctr=0
  device_details = get_device_details(user, ser)
  if device_details:
     desc = device_details['Description']
  else:
     desc=""
  from .paths import CUST_DIR
  path = CUST_DIR+'/DATA'
  os.chdir(path)
  if ser == "ALL": 
    files = glob.glob('????????_????????????_gps.5min.TEXT.log') 
  else:
    files = glob.glob('????????_'+ser+'_gps.5min.TEXT.log') 
  file_list_sorted=sorted(files, key=lambda x: (x[8:], x[:8]))

  prev_lat = None
  prev_lon = None
  prev_serial = None
  prev_dt = None
  prev_dt_full = None
  total_distance = 0
  values = []
  labels = []
  high_value=0
  for filename in file_list_sorted:
    #print(filename)
    date=filename[0:9]
    serial=filename[9:22]

    # Open the file and iterate over each line:
    with open(filename, 'r') as f:
        lines=f.readlines()
        lines.reverse()
        for line in lines:
            # Parse the fields from the line:
            fields = line.strip().split(',')
            lat = float(fields[3])
            lon = float(fields[4])
            serial = fields[1]
            dt = fields[2][0:10]
            dt_full = fields[2]
            if prev_dt is not None and prev_dt != dt:
               values.append(round(total_distance))
               capture_datetime = datetime.strptime(prev_dt, '%Y-%m-%d').date()
               labels.append(capture_datetime)
               ctr=ctr+1
               if total_distance > high_value:
                  high_value=total_distance
               total_distance = 0
            if prev_serial is not None and prev_serial != serial:
               total_distance = 0
            # Calculate the distance between this point and the previous point:
            if prev_lat is not None and prev_lon is not None:
                distance = calculate_distance(lat, lon, prev_lat, prev_lon)
                total_distance += distance
            # Update the previous latitude and longitude:
            prev_lat = lat
            prev_lon = lon
            prev_serial = serial
            prev_dt = dt
            prev_dt_full = dt_full
  values.append(round(total_distance))
  capture_datetime = datetime.strptime(prev_dt, '%Y-%m-%d').date()
  labels.append(capture_datetime)

  ##capture_datetime = [datetime.strptime(prev_dt, '%Y-%m-%d').date() for prev_dt in labels]
  ##date_strings = [str(date) for date in capture_datetime]

  fig, ax = plt.subplots()
  ax.bar(labels, values, label="Distance (km)", color='blue')
  #ax.plot(labels, values, marker='o', linestyle='-', label="Distance (km)", color='blue')

  if high_value < 500:
      ax.set_ylim(bottom=0, top=high_value)
  else:
      ax.set_ylim(bottom=0, top=500)

  #ax.bar(labels, values)
  for i, v in enumerate(values):
      ax.text(i, v, str(v)+'k', ha='center', fontsize=10,fontdict={'weight': 'bold'},color='red')
  ax.legend(loc='upper right')
  #ax.plot(labels, values)

  #ax.bar(labels, values)

  ax.set_xlabel('Days', fontsize=16, labelpad=0, color='green')
  #ax.set_xlabel('Days', fontsize=14, labelpad=10, rotation=45, color='green')
  ax.set_ylabel('Distance (km)', fontsize=16, labelpad=10, color='green')
  ax.set_title('Distance for Serial#{}'.format(ser)+" "+desc+" From ["+str(labels[0])+" : "+str(labels[ctr])+"]", fontsize=16, color='black')
  #ax.set_title('Distance for Serial#{}\n{} From [{} : {}]'.format(ser, desc, labels[0], labels[ctr]), fontsize=16, color='black')
  #ax.set_title('Distance for Serial#{}\n{} From [{} : {}]'.format(ser, desc, labels[0], labels[ctr]), fontsize=16, color='black', fontweight='bold')

  #ax.set_title('Distance for Serial#{}'.format(ser)+" "+desc+" From ["+str(labels[0])+" : "+str(labels[ctr])+"]", fontsize=16, color='black')


  fig.set_size_inches(12, 4)
  fig.tight_layout()
  ##plt.show()
  #ax.grid(True)
  ax.grid(True, linestyle='--')
  #ax.grid(True, linestyle='--', alpha=0.7)

  # Annotate data points that are over 500 with "++"
  ##for i, value in enumerate(values):
  ##  if value > 500:
  ##      ax.annotate("++", (date_strings[i], value), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, color='red')

  html = mpld3.fig_to_html(fig)
  plt.close(fig)
  return html

def chart_distance_by_serial_by_day(request,ser):
    user = request.user.username
    file_contents=plot_distance_by_day_by_serial(user, ser)
    args = {'result': file_contents}
    return render(request, "view_log.html", args)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Trip_Events
from .forms import TripForm

from django.db.models import Q
@login_required
def trip_list(request):
    if request.user.is_superuser: # Check if the user is an admin
        trips = Trip_Events.objects.all().order_by('-trip_serial')
    else:
        trips = Trip_Events.objects.filter(Q(trip_user=request.user.username) | Q(trip_user=None)).order_by('-trip_serial')
    return render(request, 'trip_list.html', {'trips': trips})

#@user_passes_test(lambda u: u.is_superuser)
#def trip_list(request):
#    trips = Trip_Events.objects.all()
#    return render(request, 'trip_list.html', {'trips': trips})


#@login_required
@user_passes_test(lambda u: u.is_superuser)
def trip_detail(request, pk):
    trip = get_object_or_404(Trip_Events, pk=pk)
    return render(request, 'trip_detail.html', {'trip': trip})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def trip_new(request):
    if request.method == "POST":
        form = TripForm(request.POST, user=request.user) 
        ##form = TripForm(request.POST, instance=trip,user=request.user) 
        #form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            #form.fields['trip_inventory_id']=''
            #trip.start_date_time = timezone.now().date().strftime("%Y-%m-%d")
            trip.save()
            return redirect('/theme/trip_list/')
        else:
            print("Error on save of new trip")
            #return redirect('/theme/trip_detail', pk=trip.trip_number)
    else:
        form = TripForm(user=request.user)
        form.fields['start_date_time'].initial = timezone.now().date().strftime("%Y-%m-%d")
        form.fields['trip_user'].initial = request.user.username
        #form.fields['trip_inventory_id'].initial = ''
    return render(request, 'trip_edit.html', {'form': form})

@login_required
def trip_new_init(request,ser):
    if request.method == "POST": 
        form = TripForm(request.POST, user=request.user) 
        if form.is_valid():
            trip = form.save(commit=False)
            trip.save()
            return redirect('/theme/trip_list/')
        else:
            print("Error on save of new trip")
    else:
        form = TripForm(user=request.user,initial={'trip_serial': ser})
        form.fields['trip_user'].initial = request.user.username
        form.fields['start_date_time'].initial = ""
        form.fields['trip_inventory_id'].initial = ""
    return render(request, 'trip_edit.html', {'form': form})


@login_required
def trip_new_init_inventory(request,inv):
    if request.method == "POST": 
        form = TripForm(request.POST, user=request.user) 
        if form.is_valid():
            trip = form.save(commit=False)
            trip.save()
            return redirect('theme:inventory_detail', pk=inv)
        else:    
            print("Error on save of new trip")
    else:        
        form = TripForm(user=request.user,initial={'trip_serial': 'To_Be_Determined', 'inv': inv})
        form.fields['trip_user'].initial = request.user.username
        form.fields['trip_inventory_id'].initial = inv
        form.fields['start_date_time'].initial = datetime.now().strftime('%Y-%m-%d')

    return render(request, 'trip_edit.html', {'form': form})


from django.http import Http404

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def trip_edit(request, pk):
    if request.user.is_superuser:
       trip = get_object_or_404(Trip_Events, pk=pk)
    else:
       trip = get_object_or_404(Trip_Events, pk=pk)
    try:
        if not request.user.is_superuser:
            trip = Trip_Events.objects.get(pk=pk, trip_user=request.user.username)
    except Trip_Events.DoesNotExist:
        raise Http404("Error: Trip not found. Click the back arrow in the browser to continue.")

    if request.method == "POST":
        ##form = TripForm(request.POST, instance=trip) # changed Oct 29, 2023
        form = TripForm(request.POST, instance=trip,user=request.user)
        if not request.user.is_superuser:
            #print("User is not superuser")
            form.fields['trip_user'].initial = request.user.username
        else:
            print("User is superuser")
        if form.is_valid():
            #print("form is valid")
            trip = form.save(commit=False)
            trip.save()
            #print("form is saved")
            return redirect('/theme/trip_list/')
            #return redirect('/theme/trip_detail', pk=trip.trip_number)
        else:
            print("Error saving Trip edit form")
            form_errors = form.errors.as_text()
            return HttpResponse(form_errors, status=400)
    else:
        form = TripForm(instance=trip, user=request.user)
    context = {'form': form, 'trip': trip}  # add 'trip' to the context
    return render(request, 'trip_edit.html', context)
    #return render(request, 'trip_edit.html', {'form': form})

@login_required
def trip_edit_inventory(request, pk, inv):
    if request.user.is_superuser:
       trip = get_object_or_404(Trip_Events, pk=pk)
    else:
       trip = get_object_or_404(Trip_Events, pk=pk)
    try:
        if not request.user.is_superuser:
            trip = Trip_Events.objects.get(pk=pk, trip_user=request.user.username)
    except Trip_Events.DoesNotExist:
        raise Http404("Error: Trip not found. Click the back arrow in the browser to continue.")

    if request.method == "POST":
        ##form = TripForm(request.POST, instance=trip) # changed Oct 29, 2023
        form = TripForm(request.POST, instance=trip,user=request.user)
        if not request.user.is_superuser:
            print("User is not superuser")
            form.fields['trip_user'].initial = request.user.username
        else:
            print("User is superuser")
        if form.is_valid():
            print("form is valid")
            trip = form.save(commit=False)
            trip.save()
            print("form is saved")
            return redirect('theme:inventory_detail', pk=inv)
        else:
            print("Error saving Trip edit form")
    else:
        form = TripForm(instance=trip, user=request.user)
    context = {'form': form, 'trip': trip}  # add 'trip' to the context
    return render(request, 'trip_edit.html', context)


from django.shortcuts import render, get_object_or_404, redirect

#@login_required
#@user_passes_test(lambda u: u.is_superuser)
@login_required
def trip_delete(request, pk):
    trip = get_object_or_404(Trip_Events, pk=pk)
    trip.delete()
    return redirect('/theme/trip_list')

#@login_required
#@user_passes_test(lambda u: u.is_superuser)
@login_required
def trip_delete2(request, pk, inv):
    #trip = trip.objects.get(pk=pk)
    try:
        trip = get_object_or_404(Trip_Events, pk=pk, trip_user=request.user)
    except Http404:
        # If no records are found, raise Http404 to return a 404 response
        raise Http404("Tracking not found for the current user")
    if request.method == 'POST':
        trip.delete()
        return redirect('/theme/inventory_detail/'+str(inv)+'/')
        #return redirect('/theme/trip_list')
    context = {'trip': trip}
    return render(request, 'trip_confirm_delete.html', context)

@login_required
def trip_delete3(request, pk):
    #trip = trip.objects.get(pk=pk) 
    try:
        if not request.user.is_superuser:
           trip = get_object_or_404(Trip_Events, pk=pk, trip_user=request.user)
        else:
           trip = get_object_or_404(Trip_Events, pk=pk)
    except Http404:
        # If no records are found, raise Http404 to return a 404 response
        raise Http404("Tracking not found for the current user")
    if request.method == 'POST':
        trip.delete()
        return redirect('/theme/trip_list')
    context = {'trip': trip}
    return render(request, 'trip_confirm_delete.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Trip_Events
from .forms import TripForm 

@login_required
def trip_shipped(request, pk, inv):
    try:
        if not request.user.is_superuser:
           trip = get_object_or_404(Trip_Events, pk=pk, trip_user=request.user)
        else:
           trip = get_object_or_404(Trip_Events, pk=pk)
    except Http404: 
        # If no records are found, raise Http404 to return a 404 response
        raise Http404("Tracking not found for the current user")
    if request.method == 'POST':
       form = TripForm(request.POST, instance=trip,user=request.user)
       if form.is_valid():
          trip = form.save(commit=False)
          trip.trip_status = 'Shipped'
          trip.save()
     
@login_required
def trip_shipped(request, pk, inv):
    trip = get_object_or_404(Trip_Events, pk=pk, trip_user=request.user)
    if request.method == 'POST':
       form = TripForm(request.POST, instance=trip,user=request.user)
       form.data['start_date_time'] = trip.start_date_time
       form.data['start_lat_long'] = trip.start_lat_long
       form.data['target_lat_long'] = trip.target_lat_long
       form.data['trip_description'] = trip.trip_description
       form.data['trip_category'] = trip.trip_category
       form.data['trip_user'] = trip.trip_user
       form.data['trip_serial'] = trip.trip_serial
       form.data['trip_status'] = 'Shipped'
       if form.is_valid():
          #trip = form.save(commit=False)
          trip.save()
          return redirect('theme:inventory_detail', pk=inv)
       else:
          raise Http404("ERROR on save trips, error=", form.errors)
    else:
      form = TripForm(instance=trip, user=request.user)
      raise Http404("ERROR no POST")
    return redirect('theme:inventory_detail', pk=inv)

#def trip_delete(request, pk):
#    trip = get_object_or_404(Trip_Events, pk=pk)
#
#    # If a POST request is made, delete the trip
#    if request.method == 'POST':
#        trip.delete()
#        return redirect('/theme/trip_list')
#
#    # If a GET request is made, show the confirmation page
#    else:
#        context = {'trip': trip}
#        return render(request, 'confirmation.html', context)

#def trip_delete_confirm(request, pk):
#    trip = get_object_or_404(Trip_Events, pk=pk)
#
#    # If a POST request is made, delete the trip
#    if request.method == 'POST':
#        context = {'trip': trip}
#        return render(request, 'confirmation.html', context)
#    else:
#        form = TripForm(instance=trip)


def get_direction(previous_coords,current_coords):
    # Comparing latitude values 
    if current_coords[0] > previous_coords[0]:
       latitude_direction = "North"
    elif current_coords[0] < previous_coords[0]:
       latitude_direction = "South" 
    else:          
       latitude_direction = "" # no change
           
    # Comparing longitude values
    if current_coords[1] > previous_coords[1]:
        longitude_direction = "East"
    elif current_coords[1] < previous_coords[1]:
        longitude_direction = "West"
    else: 
        longitude_direction = "" # no change
        
    # Mapping the direction strings to corresponding arrow characters
    direction_to_arrow = {
        "North": "↑",
        "South": "↓",
        "East": "→",
        "West": "←",
        "NorthEast": "↗",
        "NorthWest": "↖",
        "SouthEast": "↘",
        "SouthWest": "↙"
    }

    # Retrieving the arrow characters for the latitude and longitude directions
    combined_direction=latitude_direction+longitude_direction
    overall_direction=direction_to_arrow.get(combined_direction, "")
    latitude_arrow = direction_to_arrow.get(latitude_direction, "")
    longitude_arrow = direction_to_arrow.get(longitude_direction, "")
    return overall_direction

#
#-- new 
##
import folium
from django.shortcuts import render
def show_map3(request,ser,dt):
    from datetime import datetime
    #import json
    now=datetime.now() # current date and time

    # keep this until figure out use
    from .paths import CUST_DIR
    DIR=CUST_DIR

    if request.user.is_authenticated:
       logged_in_username = request.user.username
    else:
       logged_in_username = ""

    if logged_in_username != "":
       device_details = get_device_details(logged_in_username, ser)
       if device_details:       
           serial_authorized="true"
    else:
        map_html="[1]Not authorized, please login to render maps!"
        return render(request, 'route_wbase.html', {'map_html': map_html})
    if serial_authorized == "false":
        map_html="[2]Not authorized!"
        return render(request, 'route_wbase.html', {'map_html': map_html})

    lowest_date,highest_date,count = data_get_low_high_count_dates(ser)
    from datetime import datetime, timedelta
    now=datetime.now() # current date and time
    date_string = now.strftime("%Y-%m-%d")
    date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

    device_details = get_device_details(logged_in_username, ser)
    if device_details:
       serial_authorized="true"
       DESCR=device_details['Description']
       TYPE_OF_ITEM=device_details['Tag_Type']
       SHOW=device_details['Attributes']
       HOME_LAT=device_details['Lat']
       HOME_LONG=device_details['Long']
       SERIAL_NUMBER = ser

    #
    # set up to build the maps
    #
    map_html=''

    current_date = datetime.now()
    if dt == "ALL":
       date_object = datetime.strptime(lowest_date, "%Y%m%d")
       formatted_date_start = date_object.strftime("%Y-%m-%d")
       formatted_date_end = current_date.strftime('%Y-%m-%d')
       formatted_date_start_today = current_date.strftime('%Y-%m-%d')
       formatted_date_end_today = current_date.strftime('%Y-%m-%d')
       # last 29 days
       map_html = '<center><table id="map-container"><tr><td>'+heatmap_view_inventory2(SERIAL_NUMBER, DESCR, formatted_date_start, formatted_date_end, str(HOME_LAT)+','+str(HOME_LONG), 'Home', 'Home', str(HOME_LAT)+','+str(HOME_LONG))+'</td></tr></table>'
       # single current day
       #map_html += '<center><table id="map-container"><tr><td>'+heatmap_view_inventory2(SERIAL_NUMBER, DESCR, formatted_date_start_today, formatted_date_end_today, str(HOME_LAT)+','+str(HOME_LONG), 'Home', 'Home', str(HOME_LAT)+','+str(HOME_LONG))+'</td></tr></table>'
       #map_html += '<center><table id="map-container"><tr><td>'+heatmap_view_inventory2(SERIAL_NUMBER, DESCR, formatted_date_start, formatted_date_end, str(HOME_LAT)+','+str(HOME_LONG), 'Home', 'Home', str(HOME_LAT)+','+str(HOME_LONG))+'</td></tr></table>'
       map_html += '<br><center><table id="map-container"><tr><td>'+heatmap_view_inventory(SERIAL_NUMBER, DESCR, formatted_date_start, formatted_date_end )+'</td></tr></table>'
    else:
       date_object_p = datetime.strptime(dt, "%Y-%m-%d")
       date_object = date_object.strftime('%Y-%m-%d')
       formatted_date_start_today = date_object
       formatted_date_end_today = date_object
       formatted_date_start = date_object
       formatted_date_end = date_object
       try:
           map_html = '<center><table id="map-container"><tr><td>'+heatmap_view_inventory2(SERIAL_NUMBER, DESCR, dt, dt, str(HOME_LAT)+','+str(HOME_LONG), 'Home', 'Home', str(HOME_LAT)+','+str(HOME_LONG))+'</td></tr></table>'
       except:
           map_html = "No Data"
       map_html += '<br><center><table id="map-container"><tr><td>'+heatmap_view_inventory(SERIAL_NUMBER, DESCR, dt, dt )+'</td></tr></table>'

    return render(request, 'route_wbase.html', {'map_html': map_html})

from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import SessionSearchForm

def active_users(request):
    # if the request is a POST request, validate the form data and filter sessions accordingly
    if request.method == 'POST':
        form = SessionSearchForm(request.POST)
        if form.is_valid():
            minutes = form.cleaned_data['minutes_since_activity']
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            user_ids = [s.get_decoded().get('_auth_user_id') for s in sessions]
            #active_user_ids = set([uid for uid in user_ids if uid is not None and (timezone.now() - sessions[user_ids.index(uid)].get_decoded().get('_last_activity')).seconds < minutes * 60])
            active_user_ids = set([uid for uid in user_ids if uid is not None and sessions[user_ids.index(uid)].get_decoded().get('_last_activity') is not None and (timezone.now() - sessions[user_ids.index(uid)].get_decoded().get('_last_activity')).seconds < minutes * 60])
            active_users = User.objects.filter(id__in=active_user_ids)
            return render(request, 'active_users.html', {'users': active_users, 'form': form})
    else:
        form = SessionSearchForm()
    return render(request, 'session_search.html', {'form': form})

# views.py
from django.shortcuts import render
from django.http import JsonResponse

@login_required
def heatmap_view(request):
    locations = [
        {'lat': 40.712776, 'lng': -74.005974},
        {'lat': 41.878113, 'lng': -87.629799},
        {'lat': 51.507351, 'lng': -0.127758},
    ]
    return render(request, 'heatmap.html', {'locations': locations})

from django.shortcuts import render, get_object_or_404, redirect
from .models import TagAlert
from .forms import TagAlertForm

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_list(request):
    user = request.user
    tag_alerts = TagAlert.objects.filter(TagAlert_user=user).order_by('TagAlert_serial', 'TagAlert_alert_type')
    return render(request, 'tag_alert_list.html', {'tag_alerts': tag_alerts})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_new2(request):
    if request.method == "POST": 
        form = TagAlertForm(request.POST)
        if form.is_valid():
            print("TagAlertForm is valid")
            form.instance.TagAlert_user = request.user
            TForm = form.save(commit=False)
            TForm.save()
            print("TagAlertForm is saved")
            return redirect('/theme/tagalert_list/')
        else:
            print("TagAlertForm Validation Error")
            messages.error(request, 'There was an error with the form')
            print(form.errors)
    else:
        print("TagAlertForm initial entry")
        form = TagAlertForm(user=request.user)
    return render(request, 'tag_alert_form.html', {'form': form})

@login_required
def tagalert_new(request):
    if request.method == "POST": 
        #form = TagAlertForm(request.POST)
        # ADDED NOV 3, 2023 AT 5:20PM
        form = TagAlertForm(request.POST, user=request.user)  # Pass the user here
        if form.is_valid():
            TForm = form.save(commit=False)
            form.instance.TagAlert_user = request.user
            TForm.save()
            return redirect('/theme/tagalert_list/')
        else:
            messages.error(request, 'There was an error with the form')
            print(form.errors)
    else:
        #form = TagAlertForm()
        form = TagAlertForm(user=request.user)
    return render(request, 'tag_alert_form.html', {'form': form})

#
#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_edit(request, pk):
    try:
       tag_alert = get_object_or_404(TagAlert, pk=pk)
       #form = TagAlertForm(request.POST or None, instance=tag_alert)
       form = TagAlertForm(request.POST or None, instance=tag_alert,  user=request.user)  # Pass the user here
       if form.is_valid():
           form.save()
           return redirect('/theme/tagalert_list')
    except:
           return redirect('/theme/tagalert_list/')
    return render(request, 'tag_alert_form.html', {'form': form})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_delete(request, pk):
    tag_alert = get_object_or_404(TagAlert, pk=pk)
    if request.method == 'POST':
        tag_alert.delete()
        return redirect('/theme/tagalert_list')
    return render(request, 'tag_alert_confirm_delete.html', {'tag_alert': tag_alert})

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_detail(request, pk):
    tag_alert = get_object_or_404(TagAlert, pk=pk)
    form = TagAlertForm(instance=tag_alert)
    return render(request, 'tag_alert_detail.html', {'form': form, 'tag_alert': tag_alert})


#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_clone(request, pk):
    original_tag_alert = TagAlert.objects.get(id=pk)

    cloned_tag_alert = TagAlert(
        TagAlert_user=original_tag_alert.TagAlert_user,
        TagAlert_description=original_tag_alert.TagAlert_description,
        TagAlert_alert_type=original_tag_alert.TagAlert_alert_type,
        TagAlert_message=original_tag_alert.TagAlert_message,
        TagAlert_notify_address=original_tag_alert.TagAlert_notify_address,
        TagAlert_notification_type=original_tag_alert.TagAlert_notification_type,
        TagAlert_status="Inactive",
        #TagAlert_status=original_tag_alert.TagAlert_status,
        TagAlert_proximity_lat=original_tag_alert.TagAlert_proximity_lat,
        TagAlert_proximity_long=original_tag_alert.TagAlert_proximity_long,
        TagAlert_alarm_distance=original_tag_alert.TagAlert_alarm_distance,
        TagAlert_number_of_alerts=original_tag_alert.TagAlert_number_of_alerts,
        TagAlert_time_between_alerts=original_tag_alert.TagAlert_time_between_alerts,
        TagAlert_start_date_time=original_tag_alert.TagAlert_start_date_time,
        TagAlert_end_date_time=original_tag_alert.TagAlert_end_date_time,
        TagAlert_serial=original_tag_alert.TagAlert_serial,
    )

    cloned_tag_alert.save()

    return redirect('/theme/tagalert_list/')

@login_required
def tagalert_clone2(request, pk):
    existing_instance = TagAlert.objects.get(pk=pk)
    instance_dict = {field.name: getattr(existing_instance, field.name) for field in existing_instance._meta.get_fields()}
    if request.method == 'POST':
        #form = TagAlertForm(request.POST)
        form = TagAlertForm(request.POST,  user=request.user)  # Pass the user here
        #form = TagAlertForm(request.POST, TagAlert_user=request.user, user=request.user)
        if form.is_valid():
            # added Nov 3, 2023 at 5:56pm
            new_instance = form.save(commit=False)
            new_instance.TagAlert_user = request.user  # Set the TagAlert_user to the logged-in user
            #--
            new_instance = form.save()
            return redirect('/theme/tagalert_list/')
        else:
            print("tagalert_clone2 Form Error, save failed.")
    else:       
        #form = TagAlertForm(initial=instance_dict,TagAlert_user=request.user)
        form = TagAlertForm(initial=instance_dict,user=request.user)
        #form.fields['TagAlert_user'].initial = request.user.username
        #form.fields['TagAlert_user'].initial = request.user.username
    context = {'form': form}
    return render(request, 'tag_alert_form.html', context)

from .models import Trip_Events

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def trip_clone(request, pk):
    # Get the original Trip_Events record
    original_trip = Trip_Events.objects.get(trip_number=pk)

    # Create a new Trip_Events record with the same fields as the original
    new_trip = Trip_Events(
        start_date_time=original_trip.start_date_time,
        end_date_time=original_trip.end_date_time,
        start_location_address=original_trip.start_location_address,
        end_location_address=original_trip.end_location_address,
        start_lat_long=original_trip.start_lat_long,
        target_lat_long=original_trip.target_lat_long,
        trip_description=original_trip.trip_description,
        trip_category=original_trip.trip_category,
        trip_user=original_trip.trip_user,
        trip_serial=original_trip.trip_serial,
    )

    # Save the new record
    new_trip.save()

    # Return the new trip_number
    return redirect('/theme/trip_list/')
    #return new_trip.trip_number

#-- added
@login_required
def trip_clone2(request, pk):
    #existing_instance = DeviceItemSecurity.objects.get(pk=pk)
    existing_instance = Trip_Events.objects.get(trip_number=pk)
    instance_dict = {field.name: getattr(existing_instance, field.name) for field in existing_instance._meta.get_fields()}
    if request.method == 'POST':
        form = TripForm(request.POST, user=request.user)
        #form = TripForm(request.POST)
        if form.is_valid():
            new_instance = form.save()
            return redirect('theme:trip_list')
    else:       
        #form = TripForm(initial=instance_dict)
        form = TripForm(initial=instance_dict,user=request.user)
        form.fields['trip_user'].initial = request.user.username
    context = {'form': form}
    return render(request, 'trip_edit.html', context)

#--

# In your views.py file:

import csv
from django.shortcuts import render

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def tagalert_history_list(request,type):
    from .paths import CUST_DIR
    with open(CUST_DIR+'/tag_alerts_history.log') as csvfile:
        data = csv.reader(csvfile)

        # Assuming the 8th field is at index 7 (0-indexed)
        alert_serial_index = 7

        # Filter data based on the alert_type
        if type.upper() != 'ALL':
            data = [row for row in data if row[alert_serial_index] == type]

        return render(request, 'tag_alert_history_list.html', {'data': data})

import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render

def border_graph2(request):
    from .paths import CUST_DIR
    filename = CUST_DIR+'/border_waits.log'

    # Step 1: Read and sort the data
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        #next(reader)  # Skip header
        for row in reader:
            data.append(row)
    data.sort(key=lambda row: (row[0], row[1], int(row[4]), row[2]))

    # Step 2: Extract relevant data
    travellers_flow = [int(row[4]) for row in data]
    updated = [row[5] for row in data]
    cbsa_office = [row[2] for row in data]

    # Step 3: Group the data by CBSAOffice's first character
    cbsa_data = defaultdict(list)
    for i in range(len(data)):
        cbsa_data[cbsa_office[i][0]].append((updated[i], travellers_flow[i]))

    # Step 4: Plot the data
    #fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(14, 6)) 
    colors = ['r', 'b', 'g']
    for i, (char, data) in enumerate(cbsa_data.items()):
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        ax.plot(x, y, f"{colors[i % len(colors)]}-o", label=char)

        #for j, (x_val, y_val) in enumerate(data):
        #    ax.annotate(str(y_val), xy=(x_val, y_val), xytext=(-10, 10), textcoords='offset points')
        #    ax.annotate(char, xy=(x_val, y_val), xytext=(10, 0), textcoords='offset points', ha='left', va='center')

    ax.set_xlabel('Updated')
    ax.set_ylabel('TravellersFlow')
    ax.set_title('CBSAOffice TravellersFlow')
    ax.legend()

    # Generate the HTML string using mpld3
    graph_html = mpld3.fig_to_html(fig)

    # Render the template with the context containing the graph
    context = {'graph_html': graph_html}
    return render(request, 'border_graph.html', context)

import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render

def border_graph(request):
    from .paths import CUST_DIR
    filename = CUST_DIR+'/border_waits.log'

    # Step 1: Read and sort the data
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    data.sort(key=lambda row: (row[0], row[1], int(row[4]), row[2]))

    # Step 2: Extract relevant data
    travellers_flow = [int(row[4]) for row in data]
    updated = [row[5] for row in data]
    cbsa_office = [row[2] for row in data]

    # Step 3: Group the data by CBSAOffice's first character
    cbsa_data = defaultdict(list)
    for i in range(len(data)):
        cbsa_data[cbsa_office[i][0]].append((updated[i], travellers_flow[i]))

    # Step 4: Plot the data
    fig, ax = plt.subplots(figsize=(14, 6)) 
    plt.rcParams.update({'font.size': 16}) # increase font size
    colors = ['r', 'b', 'g']
    for i, (char, data) in enumerate(cbsa_data.items()):
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        # Set the legend label to the first 10 characters of the CBSA Office name
        ax.plot(x, y, f"{colors[i % len(colors)]}-o", label=cbsa_office[i][:28])
    
    ax.set_xlabel(' 20 min Updates')
    ax.set_ylabel('Minutes Wait to Cross The Border')
    ax.set_title('')
    #ax.set_title('TravellersFlow - 20 min Intervals')
    ax.grid(True, axis='y')
    #ax.grid(True)
    #ax.legend()
    #ax.legend(loc='top center')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
    
    # Generate the HTML string using mpld3
    graph_html = mpld3.fig_to_html(fig)
    
    # Render the template with the context containing the graph
    context = {'graph_html': graph_html}
    return render(request, 'border_graph.html', context)

from django.shortcuts import render, redirect
from django.urls import reverse

from django.db.models.functions import Lower

def category_selection_view(request):
    # filter by username 
    #if request.user.is_staff:
    user = request.user.username
    # Get a list of distinct categories from DeviceItemSecurity
    #categories = DeviceItemSecurity.objects.order_by('category').values_list('category', flat=True).distinct()

    #categories = DeviceItemSecurity.objects.order_by(Lower('category')).values_list('category', flat=True).distinct()
    categories = DeviceItemSecurity.objects.filter(username=user).order_by(Lower('category')).values_list('category', flat=True).distinct()

    if request.method == 'POST':
        # Retrieve the selected category from the POST data
        selected_category = request.POST.get('category')

        # Redirect to the GPS log view with the selected category as a parameter
        return redirect(reverse('theme:gps_log_5min_today_last', kwargs={'category_selected': selected_category}))

    # Render the category selection template with the list of categories
    return render(request, 'category_selection.html', {'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Feeder
from .forms import FeederForm

from .models import Ticket
from .forms import TicketForm

from django.db.models import Count

@user_passes_test(lambda u: u.is_superuser)
def feeder_list(request):
    #feeders = Feeder.objects.all()
    ##feeders = Feeder.objects.annotate(num_tags=Count('deviceitemsecurity'))
    feeders = Feeder.objects.annotate(num_tags=Count('deviceitemsecurity', filter=Q(deviceitemsecurity__username='tracker')))
    #feeders = Feeder.objects.filter(username='tracker').annotate(num_tags=Count('deviceitemsecurity'))
    from .paths import CUST_DIR
    with open(CUST_DIR+'/transfer_data.log', 'r', encoding="utf-8") as f:
       lines = f.readlines()
    # Keep only the last 500 lines
    #file_contents = ''.join(lines[-100:])
    file_contents = ''.join(lines[-500:][::-1])

    #return render(request, 'feeder_list.html', {'feeders': feeders})
    #return render(request, 'feeder_list.html', {'feeders': feeders}, {'file_contents': file_contents})
    return render(request, 'feeder_list.html', {'feeders': feeders, 'file_contents': file_contents})

@user_passes_test(lambda u: u.is_superuser)
def feeder_detail(request, pk):
    feeder = get_object_or_404(Feeder, pk=pk)
    return render(request, 'feeder_detail.html', {'feeder': feeder})

@user_passes_test(lambda u: u.is_superuser)
def feeder_create(request):
    if request.method == 'POST':
        form = FeederForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/theme/feeder_list')
    else:
        form = FeederForm()
    return render(request, 'feeder_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def feeder_update(request, pk):
    feeder = get_object_or_404(Feeder, pk=pk)
    if request.method == 'POST':
        form = FeederForm(request.POST, instance=feeder)
        if form.is_valid():
            form.save()
            return redirect('/theme/feeder_list')
    else:
        form = FeederForm(instance=feeder)
    return render(request, 'feeder_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def feeder_delete(request, pk):
    feeder = get_object_or_404(Feeder, pk=pk)
    if request.method == 'POST':
        feeder.delete()
        return redirect('/theme/feeder_list')
    return render(request, 'feeder_confirm_delete.html', {'feeder': feeder})

@login_required
def ticket_list(request):

    if request.user.is_superuser:
        all_tickets_q = Ticket.objects.all()
    else:
        all_tickets_q = Ticket.objects.filter(created_by=request.user)

    # Calculate the counts
    all_tickets = all_tickets_q.count()
    open_tickets = all_tickets_q.filter(status__in=['New', 'Open', 'In Progress', 'On Hold', 'Reopened']).count()
    closed_tickets = all_tickets_q.filter(status__in=['Closed', 'Resolved']).count()

    if request.user.is_superuser:
       tickets = Ticket.objects.all()
    else:
       tickets = Ticket.objects.filter(created_by=request.user)
    #return render(request, 'ticket_list.html', {'tickets': tickets, 'status': 'All'})
    return render(request, 'ticket_list.html', {'tickets': tickets, 'status': 'All', 'all_tickets': all_tickets, 'open_tickets': open_tickets, 'closed_tickets': closed_tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    from django.http import HttpResponseForbidden
    if request.user != ticket.created_by and not request.user.is_superuser:
        # Handle unauthorized access here, such as showing an error page or redirecting
        return HttpResponseForbidden("<font color=red><b><font size=5>ERROR: You are not authorized to view this ticket. Click the BACK button on the browser.")
    #return render(request, 'ticket_form.html', {'form': TicketForm(instance=ticket), 'ticket': ticket})
    return render(request, 'ticket_detail.html', {'ticket': ticket})

from django.shortcuts import get_object_or_404

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            #tracker_user, created = User.objects.get_or_create(username='tracker')
            ##ticket.assignee = get_object_or_404(User, username='tracker')
            #print("ticket.assignee=",ticket.assignee)
            #assignee = form.cleaned_data.get('assignee')
            #print("Assignee:", assignee)
            ticket.save()
            return redirect('/theme/ticket_list')
        else:
            # Form is not valid, so display an error message
            messages.error(request, "Form submission has errors. Please correct the errors below.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field '{form.fields[field].label}': {error}")
    else:
        form = TicketForm(user=request.user)
        #tracker_user, created = User.objects.get_or_create(username='tracker')
        #form.assignee = tracker_user
    
    return render(request, 'ticket_form.html', {'form': form})

@login_required
def ticket_update(request, pk):
    from django.http import HttpResponseForbidden
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user != ticket.created_by and not request.user.is_superuser:
        # Handle unauthorized access here, such as showing an error page or redirecting
        return HttpResponseForbidden("<font color=red><b><font size=5>ERROR: You are not authorized to update this ticket. Click the BACK button on the browser.")

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/theme/ticket_list')
    else:
        form = TicketForm(instance=ticket, user=request.user)
    # Retrieve the ticket number
    ticket_number = ticket.ticket_number
    
    context = {
        'form': form,
        'ticket_number': ticket_number,
    }
#
    return render(request, 'ticket_form.html', context)

@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    from django.http import HttpResponseForbidden
    if request.user != ticket.created_by and not request.user.is_superuser:
        # Handle unauthorized access here, such as showing an error page or redirecting
        return HttpResponseForbidden("<font color=red><b><font size=5>ERROR: You are not authorized to update this ticket. Click the BACK button on the browser.")
    if request.method == 'POST':
        ticket.delete()
        return redirect('/theme/ticket_list')
    return render(request, 'ticket_confirm_delete.html', {'ticket': ticket})


from django.http import HttpResponseForbidden
from django.shortcuts import render
from .models import Ticket

@login_required
def open_tickets_list(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(status__in=["New", "Open", "In Progress", "On Hold", "Reopened"])
    else:
        tickets = Ticket.objects.filter(created_by=request.user, status__in=["New", "Open", "In Progress", "On Hold", "Reopened"])
    return render(request, 'ticket_list.html', {'tickets': tickets, 'status': 'Open'})

@login_required
def closed_tickets_list(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(status__in=["Closed", "Resolved"])
    else:
        tickets = Ticket.objects.filter(created_by=request.user, status__in=["Closed", "Resolved"])
    return render(request, 'ticket_list.html', {'tickets': tickets, 'status': 'Closed'})


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def demo_login(request):
    if request.user.is_authenticated:
        # If a user is already logged in, log them out
        logout(request)

    # Perform authentication for the demo user
    user = authenticate(request, username='demo', password='')

    if user is not None:
        # If authentication is successful, log the user in
        login(request, user)
        platform=mobile_check_demo(request)
        return redirect('/theme/home/')
    else:
        return HttpResponse("Sorry the Demo user authentication is currently disabled. PM Rob to enable it!")


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
#
# This will accept username/password from a client and return login success or failure
#
def login_API(request):
    if request.method == 'POST':
        # Get the username and password from the request POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Perform authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            
            # Perform any additional actions, if needed
            platform = mobile_check_demo(request)

            # Return a success response (you might customize this)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})

        # If authentication fails, return an error response
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

    # If the request is not a POST request, return an error response
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


#
# Heat map in folium
#
import folium
import random
from django.shortcuts import render
from django.http import HttpResponse
from folium.plugins import HeatMap

@login_required
def heatmap_view_working_example(request):
    # Replace these with the actual coordinates where you want to center the map
    #latitude = 37.1234
    #longitude = -122.5678

    # Generate some random latitude and longitude data for demonstration
    data = [(random.uniform(37, 38), random.uniform(-122, -121)) for _ in range(500)]

    latitude, longitude = data[0]

    # Create a Folium map centered at the specified location
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Create a HeatMap layer
    folium.plugins.HeatMap(data).add_to(m)

    # Render the Folium map as an HTML string
    map_html = m._repr_html_()

    # Pass the map HTML to the template
    context = {'map_html': map_html}

    # Render a template with the map
    return render(request, 'heatmap_template.html', context)

#      
# Heat map in folium using my live data
#      
import folium
import random
from django.shortcuts import render
from django.http import HttpResponse
from folium.plugins import HeatMap,FloatImage
       
@login_required
def heatmap_view(request,ser):
    # if ser is DAY then provide just a 1 day heat map(today)
    # else it is a serial number so show ALL available data on the heat map
    count=0
    Home_count=0
    from .paths import CUST_DIR
    DIR=CUST_DIR
    
    #print("ser[0:3]=",ser[0:3])
    if ser[0:3] != "DAY":
       pattern = "*_"+ser+"_*gps.5min.TEXT.log"
    else:
       import datetime
       current_date = datetime.date.today()
       formatted_date = current_date.strftime("%Y%m%d")
       ser=ser[3:]
       print("ser=",ser)
       pattern = formatted_date +"_"+ser+"_*gps.5min.TEXT.log"
    data = []
    first=True
    for file_name in sorted(glob.glob(DIR + '/DATA/' + pattern), reverse=True):
      with open(file_name, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
         DEVICE_ITEM = row[0]
         TAGNAME = row[1]
         SAMPLE_DATE = row[2]
         LAT = row[3]
         LONG = row[4]
         APPLE_UPDATE_DATE = row[5]
         TIME_SINCE_LAST_UPDATE = row[6]
         SERIAL_NUMBER = row[1]
         STATUS_MARK = row[8]
         DEGREES_LOCATION = row[9]
         ADDRESS = row[10]
         if first == True:
            end_date=SAMPLE_DATE
            current_latitude=LAT
            current_longitude=LONG
            current_address=ADDRESS
            first=False
         count=count+1
         if ADDRESS == "Home":
            Home_count=Home_count+1
         latitude, longitude = float(row[3]), float(row[4])
         data.append((latitude, longitude))

    if request.user.is_authenticated:
       logged_in_username = request.user.username

    # get the user details to add to map info
    device_details = get_device_details(logged_in_username, ser)
    if device_details:
            serial_authorized="true"
            DESCR=device_details['Description']
            TYPE_OF_ITEM=device_details['Tag_Type']
            SHOW=device_details['Attributes']
            HOME_LAT=device_details['Lat']
            HOME_LONG=device_details['Long']

            latitude=float(device_details['Lat'])
            longitude=float(device_details['Long'])
         
    ##latitude, longitude = data[0]
         
    # Create a Folium map centered at the specified location
    m = folium.Map(location=[current_latitude, current_longitude], zoom_start=12, fullscreen_control=True)
         
    # Create a HeatMap layer
    folium.plugins.HeatMap(data).add_to(m)

# ---- for markers instead of heatmap
    #for location in data:
    #    folium.Marker(location=location, popup='Marker Popup').add_to(m)
    #folium.PolyLine(data, color="blue", weight=2.5, opacity=1).add_to(m)
# ----

    from datetime import datetime

    date_obj1 = datetime.strptime(SAMPLE_DATE[:10], '%Y-%m-%d').date()
    date_obj2 = datetime.strptime(end_date[:10], '%Y-%m-%d').date()

    # Calculate the difference in days
    delta = date_obj2 - date_obj1

    # Get the number of days as an integer
    num_days = delta.days + 1

    # add percentage of time at Home location
    pct_Home=float(Home_count/count*100)
    pct_Home=format(pct_Home, '.1f')
    # Create a custom HTML element with your title text
    title_html = "<p><b><font size=4><center>Heat Map {footprint} for Tag : </b>"+TAGNAME+"-"+DESCR+" <p><b>Start:</b> "+SAMPLE_DATE[:10]+"<b> End: </b>"+end_date[:10]+" - "+str(count)+" Data Points - "+str(num_days)+" Days</b><br>"+str(pct_Home)+"% at Home Location<p></center>"
    m.get_root().html.add_child(folium.Element(title_html))

#   Put a house on the home location
    folium.Marker(
        location=[latitude, longitude],
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 64px;">🏠</div>'
        ),
        popup='Home',
    ).add_to(m)

#   Put a 📌 on the current location
    folium.Marker(
        location=[current_latitude, current_longitude],
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html = '<div style="font-size: 44px; white-space: nowrap;">📌 <font size=2><b>' + current_address + '</font></div>'
        ),
        popup=folium.Popup('Current location: '+current_address, parse_html=True, max_width=400),
    ).add_to(m)

    # Render the Folium map as an HTML string
    map_html = m._repr_html_()

    # Pass the map HTML to the template
    context = {'map_html': map_html}
         
    # Render a template with the map
    return render(request, 'heatmap_template.html', context)

from django.test import RequestFactory

def get_user_info_helper():
    # Create a request using the request factory
    request = RequestFactory().get('/get_user_info/')

    # Call the 'get_user_info' view with the created request
    response = get_user_info(request)

    if response.status_code == 200:
        user_info = response.content.decode('utf-8').split('\n')
        first_name, last_name, email, login_datetime = user_info
        login_date, login_time = login_datetime.split()
        return first_name, last_name, email, login_date, login_time
    else:
        return None

@login_required
def map_chart_explain(request):
    return render(request, 'view_log_explain.html')

import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render
from datetime import datetime

def network_chart(request, YYYYMMDD):
    if YYYYMMDD == "TODAY":
        current_date = datetime.now()
        YYYYMMDD = current_date.strftime('%Y%m%d')
    from .paths import CUST_DIR
    network_file_path = CUST_DIR +'/'+ YYYYMMDD + '_network_stats.out'
    cpu_file_path = CUST_DIR+'/' + YYYYMMDD + '_cpu_stats.out'
    health_file_path = CUST_DIR+'/health.out'
    disk_io_file_path = CUST_DIR+'/' + YYYYMMDD + '_disk_io_stats.out'
    web_log_file_path = CUST_DIR+'/server.log'
#
##-- Health performance --#
#
    health_date_list, health_percent_list = [], []
    try:
          # 2024-01-13 15:45,47,33,4,14,1,70
          with open(health_file_path, 'r') as csv_file:
               csv_reader = csv.reader(csv_file)

               for row in csv_reader:
                  date_str, all_ctr,active_ctr,away_ctr,lost_ctr,battery_weak_ctr,health_percent_str = row
                  date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                  just_date = date_str[:10]
                  #health_chart_html="Compare date="+str(just_date)+" vs "+str(date.today)+" ::"
                  today_str = date.today().strftime('%Y-%m-%d')
                  if just_date == today_str:
                    health_percent = float(health_percent_str)
                    health_date_list.append(date)
                    health_percent_list.append(health_percent)
                    last_health_value=health_percent_str

          # Plot the HEALTH data
          plt.figure(figsize=(10, 4))
          plt.plot(health_date_list, health_percent_list, label='Tag Health Percent', color='blue')
          plt.fill_between(health_date_list, health_percent_list, color='blue', alpha=0.2)
          plt.ylim(0, 100)
          plt.title(f'Tag Health Percentage for {YYYYMMDD} - Current {last_health_value}%', fontsize=26)
          plt.xlabel('Date/Time:',fontsize=26)
          plt.ylabel('Health Utilization (%)',fontsize=26)
          plt.legend(fontsize=26)
          plt.grid(True)
          # Convert the Matplotlib plot to HTML
          health_chart_html = mpld3.fig_to_html(plt.gcf())
          plt.close()
    except Exception as e:
          health_chart_html = f'No Health data for this date: {YYYYMMDD}_health_stats.out\nError: {str(e)}'
    return render(request, 'network_chart.html', {'health_chart_html': health_chart_html})

#
#-- Network performance --#
#
    # Read network CSV file and prepare data for plotting
    network_date_list, network_sent_list, network_received_list = [], [], []

    try:
        with open(network_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            #next(csv_reader)  # Skip header

            for row in csv_reader:
                date_str, bytes_sent_str, bytes_received_str = row
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                received = int(bytes_received_str) / 300
                sent = int(bytes_sent_str) / 300

                network_date_list.append(date)
                network_received_list.append(received)
                network_sent_list.append(sent)

        # Calculate the intervals for each 5-minute increment
        network_received_interval = [network_received_list[i] - network_received_list[i - 1] if i > 0 else
                                      network_received_list[i] for i in range(len(network_received_list))]
        network_sent_interval = [network_sent_list[i] - network_sent_list[i - 1] if i > 0 else network_sent_list[i]
                                 for i in range(len(network_sent_list))]

        # Ensure that the intervals are in 5-minute increments
        interval_length = 1  # in minutes
        network_date_list, network_received_interval, network_sent_interval = zip(*[
            (date, received, sent)
            for date, received, sent in zip(network_date_list, network_received_interval, network_sent_interval)
            if (date.minute % interval_length == 0 and date.second == 0)
        ])

        # Skip the first n data points to avoid distortion
        skip_initial_points = 1  # Adjust the number of points to skip
        network_date_list = network_date_list[skip_initial_points:]
        network_received_interval = network_received_interval[skip_initial_points:]
        network_sent_interval = network_sent_interval[skip_initial_points:]

        # Plot the network data
        plt.figure(figsize=(12, 2))
        #plt.figure(figsize=(8, 4))
        #plt.figure(figsize=(10, 6))
        plt.plot(network_date_list, network_received_interval, label='Bytes Received/s', color='blue')
        plt.plot(network_date_list, network_sent_interval, label='Bytes Sent/s', color='green')

        plt.fill_between(network_date_list, network_received_interval, color='blue', alpha=0.2)
        plt.fill_between(network_date_list, network_sent_interval, color='green', alpha=0.2)

        plt.title(f'Network Bytes/s Transmitted for {YYYYMMDD}', fontsize=20)
        plt.xlabel('Date/Time:')
        plt.ylabel('Bytes/s')
        plt.legend()
        plt.grid(True)

        # Convert the Matplotlib plot to HTML
        network_chart_html = mpld3.fig_to_html(plt.gcf())
        plt.close()
    except:
        network_chart_html = 'No Network data for this date: ' + YYYYMMDD + '_network_stats.out'
#
#-- CPU performance --#
#
    # Read CPU CSV file and prepare data for plotting
    cpu_date_list, cpu_percent_list = [], []

    try:
        with open(cpu_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            #next(csv_reader)  # Skip header

            for row in csv_reader:
                date_str, cpu_percent_str = row
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                cpu_percent = float(cpu_percent_str)

                cpu_date_list.append(date)
                cpu_percent_list.append(cpu_percent)

        # Plot the CPU data
        #plt.figure(figsize=(8, 4))
        plt.figure(figsize=(12, 2))
        #plt.figure(figsize=(10, 6))
        plt.plot(cpu_date_list, cpu_percent_list, label='CPU Utilization', color='blue')
        plt.fill_between(cpu_date_list, cpu_percent_list, color='blue', alpha=0.2)

        plt.ylim(0, 100)

        plt.title(f'CPU Utilization for {YYYYMMDD}', fontsize=20)
        plt.xlabel('Date/Time:')
        plt.ylabel('CPU Utilization (%)')
        plt.legend()
        plt.grid(True)

        # Convert the Matplotlib plot to HTML
        cpu_chart_html = mpld3.fig_to_html(plt.gcf())
        plt.close()
    except:
        cpu_chart_html = 'No CPU data for this date: ' + YYYYMMDD + '_cpu_stats.out'

#--
    # Read disk_io CSV file and prepare data for plotting
    disk_io_date_list, disk_io_sent_list, disk_io_received_list = [], [], []

    try:
        with open(disk_io_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            #next(csv_reader)  # Skip header

            for row in csv_reader:
                date_str, bytes_sent_str, bytes_received_str = row
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                received = int(bytes_received_str) / 300
                sent = int(bytes_sent_str) / 300

                disk_io_date_list.append(date)
                disk_io_received_list.append(received)
                disk_io_sent_list.append(sent)

        # Calculate the intervals for each 5-minute increment
        disk_io_received_interval = [disk_io_received_list[i] - disk_io_received_list[i - 1] if i > 0 else
                                      disk_io_received_list[i] for i in range(len(disk_io_received_list))]
        disk_io_sent_interval = [disk_io_sent_list[i] - disk_io_sent_list[i - 1] if i > 0 else disk_io_sent_list[i]
                                 for i in range(len(disk_io_sent_list))]

        # Ensure that the intervals are in 5-minute increments
        interval_length = 1  # in minutes
        disk_io_date_list, disk_io_received_interval, disk_io_sent_interval = zip(*[
            (date, received, sent)
            for date, received, sent in zip(disk_io_date_list, disk_io_received_interval, disk_io_sent_interval)
            if (date.minute % interval_length == 0 and date.second == 0)
        ])

        # Skip the first n data points to avoid distortion
        skip_initial_points = 1  # Adjust the number of points to skip
        disk_io_date_list = disk_io_date_list[skip_initial_points:]
        disk_io_received_interval = disk_io_received_interval[skip_initial_points:]
        disk_io_sent_interval = disk_io_sent_interval[skip_initial_points:]

        # Plot the disk_io data
        #plt.figure(figsize=(8, 4))
        plt.figure(figsize=(12, 2))
        #plt.figure(figsize=(10, 6))
        plt.plot(disk_io_date_list, disk_io_received_interval, label='KBytes Read/s', color='blue')
        plt.plot(disk_io_date_list, disk_io_sent_interval, label='KBytes Written/s', color='green')

        plt.fill_between(disk_io_date_list, disk_io_received_interval, color='blue', alpha=0.2)
        plt.fill_between(disk_io_date_list, disk_io_sent_interval, color='green', alpha=0.2)

        plt.title(f'DISK I/O KBytes/s Read+Written for {YYYYMMDD}', fontsize=20)
        plt.xlabel('Date/Time:')
        plt.ylabel('KBytes/s')
        plt.legend()
        plt.grid(True)

        # Convert the Matplotlib plot to HTML
        disk_io_chart_html = mpld3.fig_to_html(plt.gcf())
        plt.close()
    except Exception as e:
        disk_io_chart_html = 'No disk io data for this date: ' + YYYYMMDD + '_disk_io_stats.out'+' : '+str(e)
    except ValueError as ve:
        disk_io_chart_html = 'No disk io data for this date: ' + YYYYMMDD + '_disk_io_stats.out'+' : '+str(ve)
#--
#-- Web hits chart --#
    hits_per_hour_list = {}
    ip_address_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    web_log_chart_html=''

    #if 1 == 1:
    try:
        web_log_chart_html=web_log_chart_html+"Open file: "+web_log_file_path
        with open(web_log_file_path, 'r') as log_file:
            for line in log_file:
                web_log_chart_html=web_log_chart_html+line
                # Filter out log entries that don't contain an IP address
                if not ip_address_pattern.search(line):
                    continue

                # Parse the log entry to extract the timestamp
                try:
                  timestamp_str = line.split('[')[1].split(']')[0]
                  timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y %H:%M:%S')
                
                  # Aggregate hits per hour
                  hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
                  if hour_key in hits_per_hour_list:
                      hits_per_hour_list[hour_key] += 1
                  else:
                      hits_per_hour_list[hour_key] = 1
                except:
                      continue
                      #print("issue with index")

    except Exception as e:
        web_log_chart_html = 'Error reading webserver log file: '+str(e)

    if not hits_per_hour_list:
        web_log_chart_html = web_log_chart_html + 'No data in webserver log file'
    else:
        # Convert hits per hour dictionary to lists for plotting
        web_date_list, hits_list = zip(*sorted(hits_per_hour_list.items()))

        # Plot the web hits data
        #plt.figure(figsize=(10, 6))
        plt.figure(figsize=(12, 2))
        plt.plot(web_date_list, hits_list, label='Hits per Hour', color='green')
        plt.fill_between(web_date_list, hits_list, color='green', alpha=0.2)

        plt.title('Web Hits per Hour', fontsize=20)
        plt.xlabel('Date/Time')
        plt.ylabel('Number of Hits')
        plt.legend()
        plt.grid(True)

        # Convert the Matplotlib plot to HTML
        web_log_chart_html = mpld3.fig_to_html(plt.gcf())
        plt.close()
#--
#-- hits by ip address
#--
    hits_per_ip = {}

    # Regular expression pattern to match IP addresses
    ip_address_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    # Read the web server log file
    try:
        with open(web_log_file_path, 'r') as log_file:
            for line in log_file:
                # Filter out log entries that don't contain an IP address
                if not ip_address_pattern.search(line):
                    continue

                # Parse the log entry to extract the timestamp and IP address
                try:
                    timestamp_str = line.split('[')[1].split(']')[0]
                    timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y %H:%M:%S')
                    ip_address = ip_address_pattern.search(line).group()

                    # Aggregate hits per unique IP address
                    if ip_address in hits_per_ip:
                        hits_per_ip[ip_address] += 1
                    else:
                        hits_per_ip[ip_address] = 1
                except (IndexError, ValueError) as e:
                    # Handle parsing errors
                    a=1
                    #print('Issue parsing log entry:', str(e))

    except Exception as e:
        # Handle file reading errors
        print('Error reading webserver log file:', str(e))

    # Generate HTML table
    html_table = "<table border=1 class='bordered-table'><tr><th>IP Address</th><th>Number of Hits</th></tr>"

    # Sort IP addresses by the number of hits in reverse order
    sorted_hits_per_ip = sorted(hits_per_ip.items(), key=lambda x: x[1], reverse=True)

    for ip, hits in sorted_hits_per_ip:
        html_table += f"<tr><td>{ip}</td><td>{hits}</td></tr>"

    html_table += "</table>"

    # Assign the HTML table to the ip_log_chart_html variable
    ip_log_chart_html = html_table
#--
#-- Transfer log chart success vs failure
#--
    # File path
    from .paths import CUST_DIR
    log_file_path = CUST_DIR+'/transfer_data.log'
    
    # Dictionary to store counts per day for records with "Starting" and "Errno"
    counts_per_day = defaultdict(lambda: {'Starting': 0, 'Errno': 0})
    
    # Flag to check if the first date is encountered
    first_date_encountered = False
    
    # Read the log file
    try:
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                # Split the line into fields
                fields = line.split()
    
                # Check if the line starts with '20'
                if fields and fields[0].startswith('20'):
                    # Join fields from the 2nd position onward to get the message
                    message = ' '.join(fields[1:])
    
                    # Extract the date from the first field
                    date_str = fields[0]
                    date = datetime.strptime(date_str, '%Y-%m-%d')
    
                    # If it's the first date encountered, skip all records with this date
                    if not first_date_encountered:
                        first_date_encountered = True
                        continue
    
                    # Count records with "Starting" and "Errno" per day
                    if 'Starting' in message:
                        counts_per_day[date]['Starting'] += 1
                    if 'Errno' in message:
                        counts_per_day[date]['Errno'] += 1
    
    except Exception as e:
        print(f"Error reading log file: {e}")
    
    # Calculate percentages
    dates = list(counts_per_day.keys())
    #starting_percentages = [min(count_dict['Starting'] / 1440 * 100, 100) for count_dict in counts_per_day.values()]
    #errno_percentages = [min(count_dict['Errno'] / 1440 * 100, 100) for count_dict in counts_per_day.values()]
    starting_percentages = [min(count_dict['Starting'] / len(range(0, datetime.now().hour * 12 + datetime.now().minute // 5)) * 100, 100) for count_dict in counts_per_day.values()]
    errno_percentages = [min(count_dict['Errno'] / len(range(0, datetime.now().hour * 12 + datetime.now().minute // 5)) * 100, 100) for count_dict in counts_per_day.values()]

    # Create a line chart with larger font sizes
    #plt.figure(figsize=(12, 8))
    plt.figure(figsize=(12, 2))
    plt.plot(dates, starting_percentages, label='Success', color='blue', linewidth=2)
    plt.plot(dates, errno_percentages, label='Error', color='red', linewidth=2)
    
    # Increase font size for titles and axis labels
    plt.title('Transfer % Success vs Failure per Day', fontsize=20)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Percentage (%)', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=16)
    plt.grid(True)
    
    # Convert the Matplotlib plot to HTML
    transfer_chart_html = mpld3.fig_to_html(plt.gcf())
    plt.close()

#--

    # Render the template with the HTML charts
    return render(request, 'network_chart.html', {'health_chart_html': health_chart_html, 'network_chart_html': network_chart_html, 'cpu_chart_html': cpu_chart_html, 'disk_io_chart_html': disk_io_chart_html, 'web_log_chart_html': web_log_chart_html,'ip_log_chart_html': ip_log_chart_html,'transfer_chart_html': transfer_chart_html})

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Inventory
from .forms import InventoryForm

@login_required
def inventory_list(request,category):
    if request.user.is_superuser:
      if category == 'ALL':
        #inventory_items = Inventory.objects.all()
        inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username))
      else:
        inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username,inventory_category=category))
    else:
      if category == 'ALL':
        inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username))
      else:
        inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username,inventory_category=category))

    import os
    import fnmatch
    from .paths import CUST_DIR
    path=CUST_DIR+'/theme/static/images'
    for inventory_item in inventory_items:
        images_dir = f'{path}/{inventory_item.id}_*'
        inventory_item.image_list = sorted(fnmatch.filter(os.listdir(path), str(inventory_item.id)+"_"+"*"))
    total_paid_price = inventory_items.aggregate(Sum('inventory_paid_price'))['inventory_paid_price__sum']
    total_value = inventory_items.aggregate(Sum('inventory_value'))['inventory_value__sum']
    total_sales_price = inventory_items.aggregate(Sum('inventory_sales_price'))['inventory_sales_price__sum']
    return render(
        request,
        'inventory_list.html',
        {
            'inventory_items': inventory_items,
            'total_paid_price': total_paid_price,
            'total_value': total_value,
            'total_sales_price': total_sales_price,
        }
    )


from django.db.models import Sum

@login_required
def inventory_listXX(request, category):
    if request.user.is_superuser:
        if category == 'ALL':
            inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username))
        else:
            inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username, inventory_category=category))
    else:
        if category == 'ALL':
            inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username))
        else:
            inventory_items = Inventory.objects.filter(Q(inventory_user=request.user.username, inventory_category=category))

    # Calculate totals
    total_paid_price = inventory_items.aggregate(Sum('inventory_paid_price'))['inventory_paid_price__sum']
    total_value = inventory_items.aggregate(Sum('inventory_value'))['inventory_value__sum']
    total_sales_price = inventory_items.aggregate(Sum('inventory_sales_price'))['inventory_sales_price__sum']

    return render(
        request,
        'inventory_list.html',
        {
            'inventory_items': inventory_items,
            'total_paid_price': total_paid_price,
            'total_value': total_value,
            'total_sales_price': total_sales_price,
        }
    )

from .models import Inventory, Auction, Trip_Events

#@user_passes_test(lambda u: u.is_superuser)
@login_required
def inventory_detail(request, pk):
    #inventory_item = get_object_or_404(Inventory, pk=pk)
    try:
       inventory_item = get_object_or_404(Inventory, pk=pk, inventory_user=request.user)
    except Http404:
       # If no records are found, raise Http404 to return a 404 response
       raise Http404("Inventory not found for the current user")

    # Get the pk of the current inventory_item
    inventory_item_pk = inventory_item.pk

    # Query Auction records based on auction_inventory_id
    related_auctions = Auction.objects.filter(auction_inventory_id=inventory_item_pk)
    related_trips = Trip_Events.objects.filter(trip_inventory_id=inventory_item_pk)

    # Extract trip_serial values in a loop
    trip_serials = [trip.trip_serial for trip in related_trips]

    # generate all maps for tracking this inventory item, usually 1 map but flexible for as many packages as required.
    map=''
    #for trip_serial in trip_serials:
    #    map = map + heatmap_view_inventory(trip_serial,pk)

    for trip in related_trips:
        # Fetch trip_serial and trip_description
        trip_serial = trip.trip_serial
        trip_description = trip.trip_description
        start_date_time = trip.start_date_time
        end_date_time = trip.end_date_time
        trip_status = trip.trip_status
        target_lat_long = trip.target_lat_long
        end_location_address = trip.end_location_address
        start_location_address = trip.start_location_address
        start_lat_long = trip.start_lat_long

        # Pass trip_serial, target lat,long and trip_description to heatmap_view_inventory
        if trip_status == "Delivered" or trip_status == "Shipped" or trip_status == "Out-For-Delivery":
           map += heatmap_view_inventory2(trip_serial, trip_description, start_date_time, end_date_time, target_lat_long, end_location_address, start_location_address, start_lat_long)
           map += heatmap_view_inventory(trip_serial, trip_description, start_date_time, end_date_time )
        else:
           map += "<center><font color=black>NOTE: <font color=green>"+trip_description+"<font color=black> is not qualified Shipped,Out-For-Delivery or Delivered items only."

    import os
    import fnmatch
    from .paths import CUST_DIR
    path=CUST_DIR+'/theme/uploads/images'
    image_list = sorted(fnmatch.filter(os.listdir(path), str(inventory_item_pk)+"_"+"*"))
    #return render(request, 'menu.html', {'list_menu_form':list_menu_form, 'image_list':image_list, 'im':im})

    return render(request, 'inventory_detail.html', {
        'inventory_item': inventory_item,
        'related_auctions': related_auctions,
        'related_trips': related_trips,
        'map': map,
        'image_list':image_list,
    })

@login_required
def inventory_new(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        #form = InventoryForm(request.POST, user=request.user)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.inventory_user = request.user.username
            inventory_item.save()
            return redirect('/theme/inventory_list/ALL')
        else:
            print("Error on save of new inventory item")
    else:
        #form = InventoryForm()
        #form = InventoryForm(initial={'inventory_date_added': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))})
        form = InventoryForm(initial={
            'inventory_date_added': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            'inventory_user': request.user.username,  # Initial value for inventory_user,
            'inventory_paid_price': 0.00, 
            'inventory_value': 0.00, 
            'inventory_sales_price': 0.00, 
        })
        #form = InventoryForm(user=request.user)
    return render(request, 'inventory_edit.html', {'form': form})

@login_required
def inventory_new_init(request, ser):
    if request.method == "POST":
        form = InventoryForm(request.POST, user=request.user)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            
            # Set inventory_date_added to the current date and time
            inventory_item.inventory_date_added = datetime.now()

            inventory_item.save()
            return redirect('/theme/inventory_list/ALL')
        else:
            print("Error on save of new inventory item")
    else:
        form = InventoryForm(user=request.user, initial={'inventory_date_added': str(datetime.now())})
        #form = InventoryForm(user=request.user, initial={'inventory_serial': ser})
    return render(request, 'inventory_edit.html', {'form': form})


@login_required
def inventory_edit(request, pk):
    if request.user.is_superuser:
        inventory_item = get_object_or_404(Inventory, pk=pk)
    else:
        inventory_item = get_object_or_404(Inventory, pk=pk, inventory_user=request.user.username)

    if request.method == "POST":
        form = InventoryForm(request.POST, instance=inventory_item)
        #form = InventoryForm(request.POST, instance=inventory_item, user=request.user)
        if not request.user.is_superuser:
            print("User is not superuser")
            form.fields['inventory_user'].initial = request.user.username
        else:
            print("User is superuser")
        if form.is_valid():
            print("form is valid")
            inventory_item = form.save(commit=False)
            inventory_item.save()
            print("form is saved")
            return redirect('/theme/inventory_list/ALL')
        else:
            print("Error saving Inventory edit form")
    else:
        form = InventoryForm(instance=inventory_item)
    context = {'form': form, 'inventory_item': inventory_item}
    return render(request, 'inventory_edit.html', context)

@login_required
def inventory_delete2(request, pk):
    try:
        inventory_item = get_object_or_404(Inventory, pk=pk, inventory_user=request.user)
    except Http404:
        # If no records are found, raise Http404 to return a 404 response
        raise Http404("Inventory not found for the current user")
    if request.method == 'POST':
        inventory_item.delete()
        return redirect('/theme/inventory_list/ALL')
    context = {'inventory_item': inventory_item}
    return render(request, 'inventory_confirm_delete.html', context)

from .models import Auct_group

@login_required
def auct_group_new(request):
    if request.method == "POST":
        form = AuctGroupForm(request.POST)
        if form.is_valid():
            auct_group = form.save(commit=False)
            auct_group.auct_group_user = request.user.username
            auct_group.save()
            return redirect('/theme/auct_group_list/')
        else:
            print("Error on save of new auct_group")
    else:
        form = AuctGroupForm(initial={
            'auct_group_user': request.user.username,
        })  
    return render(request, 'auct_group_edit.html', {'form': form})

@login_required
def auct_group_list(request):
    if request.user.is_superuser:
        auct_group = Auct_group.objects.all()
    else:
        auct_group = Auct_group.objects.filter(Q(auct_group_user=request.user.username))
    return render(request, 'auct_group_list.html', {'auct_group': auct_group})

@login_required
def auct_group_detail(request, pk):
    auct_group = get_object_or_404(Auct_group, pk=pk)
    return render(request, 'auct_group_detail.html', {'auct_group': auct_group})

@login_required
def auct_group_edit(request, pk):
    if request.user.is_superuser:
        auct_group = get_object_or_404(Auct_group, pk=pk)
    else:
        auct_group = get_object_or_404(Auct_group, pk=pk, auct_group_user=request.user.username)

    if request.method == "POST":
        form = AuctGroupForm(request.POST, instance=auct_group)
        if not request.user.is_superuser:
            print("User is not superuser")
            form.fields['auct_group_user'].initial = request.user.username
        else:
            print("User is superuser")
        if form.is_valid():
            print("form is valid")
            auct_group = form.save(commit=False)
            auct_group.save()
            print("form is saved")
            return redirect('/theme/auct_group_list/')
        else:
            print("Error saving auct_group edit form")
    else:
        form = AuctGroupForm(instance=auct_group)
    context = {'form': form, 'auct_group': auct_group}
    return render(request, 'auct_group_edit.html', context)

@login_required
def auct_group_delete2(request, pk):
    auct_group = get_object_or_404(Auct_group, pk=pk)
    if request.method == 'POST':
        auct_group.delete()
        return redirect('/theme/auct_group_list')
    context = {'auct_group': auct_group}
    return render(request, 'auct_group_confirm_delete.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Auction
from .forms import AuctionForm

@login_required
def auction_new(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.auction_userid = request.user.username
            auction.save()
            return redirect('/theme/auction_list/')
        else:
            print("Error on save of new auction")
    else:
        form = AuctionForm()
    return render(request, 'auction_edit.html', {'form': form})

@login_required
def auction_list(request):
    if request.user.is_superuser:
        #auctions = Auction.objects.all()
        auctions = Auction.objects.filter(auction_userid=request.user.username)
    else:
        auctions = Auction.objects.filter(auction_userid=request.user.username)
    return render(request, 'auction_list.html', {'auctions': auctions})


@login_required
#
# change this to pre fill in the details from the inventory record passed as pk
#
def auction_new_inventory(request, pk):
    inventory_instance = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST": 
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.auction_userid = request.user.username
            auction.save()
            ##return redirect('theme:inventory_list/ALL')
            return redirect(reverse('theme:inventory_list', args=['ALL']))
            #return redirect('theme/auction_list/')
        else:
            print("Error on save of new auction")
    else:
        #form = AuctionForm()
        form = AuctionForm(initial={
            'auction_description': inventory_instance.inventory_item_description,
            'auction_details': inventory_instance.inventory_item_description,
            'auction_userid': inventory_instance.inventory_user,
            'auction_our_cost': inventory_instance.inventory_paid_price,
            'auction_bin_price': inventory_instance.inventory_sales_price,
            'auction_inventory_id': pk,
        })
    return render(request, 'auction_edit.html', {'form': form})

#@login_required
#def auction_list(request):
#    if request.user.is_superuser:
#        auctions = Auction.objects.filter(auction_userid=request.user.username)
#        #auctions = Auction.objects.all()
#    else:
#        auctions = Auction.objects.filter(auction_userid=request.user.username)
#    return render(request, 'auction_list.html', {'auctions': auctions})

@login_required
def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    return render(request, 'auction_detail.html', {'auction': auction})

@login_required
def auction_edit(request, pk):
    if request.user.is_superuser:
        auction = get_object_or_404(Auction, pk=pk)
    else:
        auction = get_object_or_404(Auction, pk=pk, auction_userid=request.user.username)

    if request.method == "POST":
        form = AuctionForm(request.POST, instance=auction)
        if not request.user.is_superuser:
            form.fields['auction_userid'].initial = request.user.username
        if form.is_valid():
            auction = form.save(commit=False)
            auction.save()
            return redirect('/theme/auction_list/')
        else:
            print("Error saving auction edit form")
    else:
        form = AuctionForm(instance=auction)
    context = {'form': form, 'auction': auction}
    return render(request, 'auction_edit.html', context)

@login_required
def auction_edit_inventory(request, pk, inv):
    if request.user.is_superuser:
        auction = get_object_or_404(Auction, pk=pk)
    else:
        auction = get_object_or_404(Auction, pk=pk, auction_userid=request.user.username)

    if request.method == "POST":
        form = AuctionForm(request.POST, instance=auction)
        if not request.user.is_superuser:
            form.fields['auction_userid'].initial = request.user.username
        if form.is_valid():
            auction = form.save(commit=False)
            auction.save()
            return redirect('theme:inventory_detail', pk=inv)
        else:
            print("Error saving auction edit form")
    else:
        form = AuctionForm(instance=auction)
    context = {'form': form, 'auction': auction}
    return render(request, 'auction_edit.html', context)


@login_required
def auction_delete(request, pk, inv):
    try:
        auction = get_object_or_404(Auction, pk=pk, auction_userid=request.user)
    except Http404:
        # If no records are found, raise Http404 to return a 404 response
        raise Http404("Inventory not found for the current user")
    if request.method == 'POST':
        auction.delete()
        #return redirect('theme:inventory_list')
        return redirect('theme:inventory_detail', pk=inv)
        #return redirect('/theme/auction_list/')
    context = {'auction': auction}
    return render(request, 'auction_confirm_delete.html', context)

@login_required
def auction_delete2(request, pk):
    try:
        auction = get_object_or_404(Auction, pk=pk, auction_userid=request.user)
    except Http404:
        # If no records are found, raise Http404 to return a 404 response
        raise Http404("Inventory not found for the current user")
    if request.method == 'POST':
        auction.delete()
        #return redirect('theme:inventory_list')
        #return redirect('theme:inventory_detail', pk=inv)
        return redirect('/theme/auction_list/')
    context = {'auction': auction}
    return render(request, 'auction_confirm_delete.html', context)

#      
# Heat map in folium using my live data
#      
import folium
import random
from django.shortcuts import render
from django.http import HttpResponse
from folium.plugins import HeatMap,FloatImage
       
def heatmap_view_inventory(ser,trip_description, start_date_time, end_date_time):
    import datetime
    # if ser is DAY then provide just a 1 day heat map(today)
    # else it is a serial number so show ALL available data on the heat map
    if end_date_time == '':
       current_date = datetime.date.today()
       no_end_date = current_date.strftime("%Y-%m-%d")
       end_date_time = no_end_date
    count=0
    Home_count=0
    from .paths import CUST_DIR
    DIR=CUST_DIR
    
    #print("ser[0:3]=",ser[0:3])
    if ser[0:3] != "DAY":
       pattern = "*_"+ser+"_*gps.5min.TEXT.log"
    else:
       current_date = datetime.date.today()
       formatted_date = current_date.strftime("%Y%m%d")
       ser=ser[3:]
       print("ser=",ser)
       pattern = formatted_date +"_"+ser+"_*gps.5min.TEXT.log"
    data = []
    first=True
    for file_name in sorted(glob.glob(DIR + '/DATA/' + pattern), reverse=True):
      with open(file_name, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
         DEVICE_ITEM = row[0]
         TAGNAME = row[1]
         SAMPLE_DATE = row[2]
         #-- filter to just the trip date range
         # Check if SAMPLE_DATE is within the specified range
         from datetime import datetime
         sample_date_obj = datetime.strptime(SAMPLE_DATE[:10], '%Y-%m-%d').date()
         start_date_obj = datetime.strptime(start_date_time, '%Y-%m-%d').date()
         end_date_obj = datetime.strptime(end_date_time, '%Y-%m-%d').date()

         if start_date_obj <= sample_date_obj <= end_date_obj:
            LAT = row[3]
            LONG = row[4]
            APPLE_UPDATE_DATE = row[5]
            TIME_SINCE_LAST_UPDATE = row[6]
            SERIAL_NUMBER = row[1]
            STATUS_MARK = row[8]
            DEGREES_LOCATION = row[9]
            ADDRESS = row[10]
            if first == True:
               end_date=SAMPLE_DATE
               current_latitude=LAT
               current_longitude=LONG
               current_address=ADDRESS
               first=False
            count=count+1
            if ADDRESS == "Home":
               Home_count=Home_count+1
            latitude, longitude = float(row[3]), float(row[4])
            data.append((latitude, longitude))

    #if request.user.is_authenticated:
    #   logged_in_username = request.user.username
    logged_in_username="tracker"
    # get the user details to add to map info
    device_details = get_device_details(logged_in_username, ser)
    if device_details:
            serial_authorized="true"
            DESCR=device_details['Description']
            TYPE_OF_ITEM=device_details['Tag_Type']
            SHOW=device_details['Attributes']
            HOME_LAT=device_details['Lat']
            HOME_LONG=device_details['Long']
            latitude=float(device_details['Lat'])
            longitude=float(device_details['Long'])
         
    # Create a Folium map centered at the specified location
    try:
       m = folium.Map(location=[current_latitude, current_longitude], zoom_start=12, fullscreen_control=False,zoom_control=False)

       # Create a HeatMap layer
       folium.plugins.HeatMap(data).add_to(m)

       from datetime import datetime

       date_obj1 = start_date_obj 
       date_obj2 = end_date_obj 

       # Calculate the difference in days
       delta = date_obj2 - date_obj1

       # Get the number of days as an integer
       num_days = delta.days + 1

       # add percentage of time at Home location
       pct_Home=float(Home_count/count*100)
       pct_Home=format(pct_Home, '.1f')
       # Create a custom HTML element with your title text
       title_html = "<p><p><b><font size=4><center>Heat Map for : </b>"+TAGNAME+"-"+trip_description+"<br><b>Trip Start:</b> " +start_date_time+" <b>End:</b> "+end_date_time+" -<b> #Days: </b>"+str(num_days)+"<b>   Data Points:</b> "+str(count)+"<br><b>Current location:</b> "+current_address+"</center><p>"
       m.get_root().html.add_child(folium.Element(title_html))

#   Put a house on the home location
       folium.Marker(
        location=[latitude, longitude],
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 64px;">🏠</div>'
        ),
        popup='Home',
       ).add_to(m)

#   Put a 📌 on the current location
       folium.Marker(
        location=[current_latitude, current_longitude],
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html = '<div style="font-size: 44px; white-space: nowrap;">📌 <font size=2><b>' + current_address + '</font></div>'
        ),
        popup=folium.Popup('Current location: '+current_address, parse_html=True, max_width=400),
       ).add_to(m)

       # Render the Folium map as an HTML string
       map_html = m._repr_html_()

       # Pass the map HTML to the template
       context = {'map_html': map_html}
    except:
       map_html="<br<br><center>Heat Map - Issue with tracking device: "+ser 
         
    # Render a template with the map
    return map_html

import folium
import random
import glob
import csv
from django.shortcuts import render
from django.http import HttpResponse
from folium.plugins import FloatImage
from datetime import datetime

def heatmap_view_inventory2(ser, trip_description, start_date_time, end_date_time, target_lat_long, end_location_address, start_location_address, start_lat_long):

    import datetime as dt_tm

    # DEMO : Gerry Asia Cruise trip
    if ser == 'FF3B36B5DEMO':
       end_date_time =  '2023-12-01'
    # DEMO : jayco BC trip
    if ser == 'FF3B36B5DEM2':
       end_date_time =  '2023-10-04'
    # DEMO : Cyrillia Solovenia Trip
    if ser == 'FF3B36B5DEM3':
       end_date_time =  '2023-05-27'
    # DEMO : Cyrillia Solovenia Trip
    if ser == 'FF3B36B5DEM4':
       end_date_time =  '2023-06-21'
    # DEMO : Sarah USA Trip
    if ser == 'FF3B36B5DEM5':
       end_date_time =  '2023-05-13'
#    if ser == 'FF3BRANDDEMO':
#       end_date_time =  '2023-12-19'

    # if ser is DAY then provide just a 1 day heat map(today)
    # else it is a serial number so show ALL available data on the heat map
    if end_date_time == '':
       current_date = dt_tm.date.today()
       no_end_date = current_date.strftime("%Y-%m-%d")
       end_date_time = no_end_date
    from datetime import datetime
    count=0
    Home_count=0
    from .paths import CUST_DIR
    DIR=CUST_DIR
    
    #if ser[0:3] != "DAY":
    if start_date_time == end_date_time:
       #current_date = dt_tm.date.today()
       date_object = datetime.strptime(start_date_time, "%Y-%m-%d")
       formatted_date = date_object.strftime("%Y%m%d")
       #formatted_date = current_date.strftime("%Y%m%d")
       pattern = formatted_date +"_"+ser+"_*gps.5min.TEXT.log"
    else:
       pattern = "*_"+ser+"_*gps.5min.TEXT.log"
    #else:
    #   current_date = datetime.date.today()
    #   formatted_date = current_date.strftime("%Y%m%d")
    #   ser=ser[3:]
    #   print("ser=",ser)
    #   pattern = formatted_date +"_"+ser+"_*gps.5min.TEXT.log"

    data = []
    data_time = []
    data_location = []
    data_sample_date = []
    data_time_part = []
    data_ADDRESS = []
    data_APPLE_UDPDATE_DATE = []

    first=True

    from datetime import datetime
    APPLE_UPDATE_DATE_PREV=''
    start_date_obj = datetime.strptime(start_date_time, '%Y-%m-%d')
    start_date_obj_YYYYMMDD = start_date_obj.strftime('%Y%m%d')
    end_date_obj = datetime.strptime(end_date_time, '%Y-%m-%d')
    end_date_obj_YYYYMMDD = end_date_obj.strftime('%Y%m%d')

    #print("start_date_time=",str(start_date_time), " end_date_time=",end_date_time)
    days_difference = (end_date_obj - start_date_obj).days
    if trip_description[0] == "〽":
       plot_days=999 # 4 weeks
       max=''
       icon_list = {"icons": ["🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘","🟤","🔵","🟢","🟠","🔴","🟣","⛔","🔘"]}
    else:
       plot_days=28 # 4 weeks
       icon_list = {"icons": ["✅", "🚘", "🚗", "🚕",     "🚙",     "🚌",     "🚎",     "🏎 ",     "🚓",     "🚑",     "🚒",     "🚐",     "🛻",     "🚚",     "🚛",    "🚜",     "🛺",     "🛵",     "🏍 ",     "🔐",     "🔑",     "🔎",  "🔖",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽 ",     "📿",     "🔅",     "🔆",     "🔇",     "📍" ]}
       max='-Max 4 weeks'
    if days_difference > plot_days:
       new_start_date_obj = datetime.now() - timedelta(days=plot_days)
       start_date_obj_YYYY_MM_DD = new_start_date_obj.strftime('%Y-%m-%d')
       start_date_obj_YYYYMMDD = new_start_date_obj.strftime('%Y%m%d')
       start_date_time = str(start_date_obj_YYYY_MM_DD)

       #start_date_obj = datetime.strptime(start_date_time, "%Y%m%d")
       #start_date_obj = start_date_obj.strftime("%Y-%m-%d")
       start_date_obj = datetime.strptime(start_date_time, '%Y-%m-%d')

    for file_name in sorted(glob.glob(DIR + '/DATA/' + pattern), reverse=True):
     #print("file_name=",file_name)
     match = re.search(r'(\d{8})', file_name)
     if match:
        date_substring = match.group(1)
        date_object = datetime.strptime(date_substring, '%Y%m%d')
        compare_date_YYYYMMDD = date_object.strftime('%Y%m%d')
     if start_date_obj_YYYYMMDD <=  compare_date_YYYYMMDD <= end_date_obj_YYYYMMDD:
      #print("Passed filename=",file_name)
      with open(file_name, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
         APPLE_UPDATE_DATE = row[5]
         if APPLE_UPDATE_DATE_PREV != APPLE_UPDATE_DATE:
           DEVICE_ITEM = row[0]
           TAGNAME = row[1]
           SAMPLE_DATE = row[2]
           LAT = row[3]
           LONG = row[4]
           TIME_SINCE_LAST_UPDATE = row[6]
           SERIAL_NUMBER = row[1]
           STATUS_MARK = row[8]
           DEGREES_LOCATION = row[9]
           ADDRESS = row[10]
           # adding 360 to negative longitudes to fix mapping issue
           if float(LONG) < 0:
              LONG=str(float(LONG)+360)
           # the first record is the latest location due to the file is reverse sort order
           if first == True:
              end_date=SAMPLE_DATE
              current_latitude=LAT
              current_longitude=LONG
              current_address=ADDRESS
              first=False
           count=count+1
           if ADDRESS == "Home":
              Home_count=Home_count+1
           #latitude, longitude = float(row[3]), float(row[4])
           latitude, longitude = float(LAT), float(LONG)
           data.append((latitude, longitude))
           data_time.append((APPLE_UPDATE_DATE))
           data_location.append((ADDRESS))
           data_sample_date.append((SAMPLE_DATE))
           data_time_part.append((SAMPLE_DATE[11:16]))
           data_ADDRESS.append((ADDRESS))
           data_APPLE_UDPDATE_DATE.append((APPLE_UPDATE_DATE))
           APPLE_UPDATE_DATE_PREV = APPLE_UPDATE_DATE

    logged_in_username="tracker"
    # get the user details to add to map info
    device_details = get_device_details(logged_in_username, ser)
    if device_details:
            serial_authorized="true"
            DESCR=device_details['Description']
            TYPE_OF_ITEM=device_details['Tag_Type']
            SHOW=device_details['Attributes']
            HOME_LAT=device_details['Lat']
            HOME_LONG=device_details['Long']
            latitude=float(device_details['Lat'])
            longitude=float(device_details['Long'])
            if longitude < 0:
               longitude = longitude + 360

    zoom_level = 13
    if TAGNAME == 'FF3B36B5DEMO' or TAGNAME == 'FF3B36B5DEM2':
       zoom_level = 5 
    elif TAGNAME == 'FF3B36B5DEM3': 
       zoom_level = 10
    elif TAGNAME == 'FF3B36B5DEM4':
       zoom_level = 6 
    elif TAGNAME == 'FF3B36B5DEM5':
       zoom_level = 9 
    elif TAGNAME == 'FF3BRANDDEMO':
       zoom_level = 5 
    else:
       zoom_level = 13

    try:
       #m = folium.Map(location=[current_latitude, current_longitude], zoom_start=13, fullscreen_control=False, zoom_control=False)
       m = folium.Map(location=[current_latitude, current_longitude], zoom_start=zoom_level, fullscreen_control=False, zoom_control=False)

    except:
       current_latitude=43.8382
       current_longitude=-79.3001+360
       m = folium.Map(location=[current_latitude, current_longitude], zoom_start=20, fullscreen_control=False, zoom_control=False)
    from folium.plugins import AntPath
    data2 = tuple(reversed(data))
    AntPath(data2, delay=400,weight=5,color="black",dash_array=[60,20]).add_to(m)
    try:
       start_lat, start_long = start_lat_long.split(',')
    except:
       start_lat = "0"
       start_long = "0"
    try:
       target_lat, target_long = target_lat_long.split(',')
    except:
       target_lat = "0"
       target_long = "0"
    distance_start_to_target = haversine(float(target_lat), float(target_long), float(start_lat), float(start_long))
    distance_start_to_target_formatted = f"{distance_start_to_target:.1f}"
    # distance from current to target pct completed
    distance_to_target = haversine(float(target_lat), float(target_long), float(data[0][0]), float(data[0][1]))
    try:
        pct_distance = ((distance_start_to_target - distance_to_target) / distance_start_to_target)*100
        if pct_distance > 99.5:
           pct_distance = 100
        elif pct_distance < 0.37:
           pct_distance = 0
        pct_distance_formatted = f"{pct_distance:.1f}"
    except:
        pct_distance_formatted = 0
    locations_html = '<center>'
    if start_location_address != end_location_address:
       locations_html = '<br><table><tr><td nowrap><b>Starting Location: </b><font color=blue>'+start_location_address+'</td></tr>'
       locations_html += '<tr><td nowrap><font color=black><b>Target Location: </b><font color=blue>'+end_location_address+'</td></tr>'
       locations_html += '<tr><td nowrap><b><font color=black>Distance between Start and Target: </b><font color=blue>'+str(distance_start_to_target_formatted)+'km<font color=black> - '+str(pct_distance_formatted)+'% Completed</td></tr></table><p><br>'

    locations_html=locations_html+'<br><b>Locations detected by Apple icloud Network<table border=1 class="bordered-table" style="padding: 8px;"><tr><td><b>Update Date/Time</td><td><b>Location</td><td><b>Distance(km)</td><td><b>Target(km)</td></tr>'

    total_distance=0
    day_number=0
    prev_day=''
    for i in range(0, len(data)-1, 1):
        distance_to_target = haversine(float(target_lat), float(target_long), float(data[i][0]), float(data[i][1]))
        distance_to_target_formatted = f"{distance_to_target:.1f}"
        distance = haversine(float(data[i+1][0]), float(data[i+1][1]), float(data[i][0]), float(data[i][1]))
        total_distance=total_distance+distance
        distance_formatted = f"{distance:.2f}"
        if distance > 0.1:
           c='<font color=red>'
           data_fixed=str(data[i])
           data_fixed=data_fixed.replace(" ","")

           full_datetime_string = data_sample_date[i]
           date_part = full_datetime_string[:10]

           locations_html=locations_html+'<tr><td nowrap>'+data_APPLE_UDPDATE_DATE[i]+'</td><td nowrap><a href=https://www.google.com/maps/place/'+str(data_fixed)+' target=_blank>📍'+'<a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+date_part+'/ target=_default>'+icon_list["icons"][day_number-1]+'</a>⬆'+data_ADDRESS[i][:50]+'</td><td><center>'+c+str(distance_formatted)+'</td><td><center>'+str(distance_to_target_formatted)+'</td></tr>'
        #else:
        #   c='<font color=black>'
        #locations_html=locations_html+'<tr><td nowrap>'+data_APPLE_UDPDATE_DATE[i]+'</td><td nowrap>'+data_ADDRESS[i]+'</td><td><center>'+c+str(distance_formatted)+'</td></tr>'
        #distance = haversine(float(data[i+1][0]), float(data[i+1][1]), float(data[i][0]), float(data[i][1]))
        if distance > .5 and data_ADDRESS[i] != 'Home':
           # if trip start date and trip end date are the same then add the time of the point otherwise it's too messy
           if start_date_time == end_date_time:
              set_direction_icon = '<font size=2><b>'+data_time_part[i]
           else:
              set_direction_icon = ''
           #set_direction_icon = get_direction(data[i+1],data[i])+'<font size=2><b>'+data_time_part[i]
        else:
           set_direction_icon = ''

        full_datetime_string = data_sample_date[i]
        date_part = full_datetime_string[:10]
        if prev_day != date_part:
           day_number = day_number + 1 
           prev_day = date_part

        if trip_description[0] == "〽":
           html = "<div style='white-space:nowrap;'><font size=1>o"+"</div>"
        else:
           html = "<div style='white-space:nowrap;'><font size=1>"+icon_list["icons"][day_number-1]+"</div>"

        #html = "<div style='white-space:nowrap;'><font size=3>✅"+set_direction_icon+"</div>"
        data_fixed=str(data[i])
        data_fixed=data_fixed.replace(" ","")

        folium.Marker(
            location=[data[i][0], data[i][1]],
            icon=folium.DivIcon(html=html),
            popup="<div style='white-space: nowrap;'><font size=2><a href=https://www.google.com/maps/place/"+str(data_fixed)+" target=_blank>📍google Map</a></div><br><div style='white-space: nowrap;'><a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+date_part+"/ target=_default>Show map for just: "+date_part+"</a>",
            #popup="<div style='white-space: nowrap;'><font size=2><a href=https://www.google.com/maps/place/"+str(data_fixed)+" target=_blank>📍google Map</a></div>",
            tooltip="<font size=3><font color=blue><b>Sample Time: </b>"+data_sample_date[i]+"<br><b>Updated: </b>"+data_time[i]+"<b><br>Location:</b> "+data_location[i]
        ).add_to(m)
    
        # Add dashed line between markers 
        #if i+1 < len(data):
        #    folium.PolyLine([data[i], data[i+1]], color="black", weight=2.5, opacity=1, dash_array=5).add_to(m)
    total_distance_formatted = f"{total_distance:.1f}"
    locations_html=locations_html+'<tr><td><b>Total</td><td></td><td><b><center>'+total_distance_formatted+'km</td></tr>'
    locations_html=locations_html+'</table><br>'
    # Add the last marker
    try:
     folium.Marker(
        location=[data[-1][0], data[-1][1]],
        #icon=custom_icon,
        icon=folium.DivIcon(html=html)
     ).add_to(m)
    except:
     a=1

    from datetime import datetime


    date_obj1 = start_date_obj
    date_obj2 = end_date_obj

    # Calculate the difference in days
    delta = date_obj2 - date_obj1

    # Get the number of days as an integer
    num_days = delta.days + 1

    # add percentage of time at Home location
    try:
      pct_Home=float(Home_count/count*100)
      pct_Home=format(pct_Home, '.1f')
    except:
      pct_Home=0
    try:
     title_html = "<p><p><b><font size=4><center>Tracking for : </b>"+TAGNAME+"-"+trip_description
     if trip_description != DESCR:
         title_html = title_html +"<br><font size=2>["+DESCR+"]"

     title_html = title_html +"<br><b><font size=4>Trip Start:</b> " +start_date_time+" <b>End:</b> "+end_date_time+" -<b> #Days: </b>"+str(num_days)+"<b>   Data Points:</b> "+str(count)+"<font size=2> "+max+"<font size=4></br>"

     title_html = title_html +"<b>Current location:</b> "+current_address+"</center>"

     if start_date_time == end_date_time:
        # add to get next and prev days
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d')
        current_date_p = datetime.strptime(current_date, "%Y-%m-%d").date()
        formatted_date = start_date_time
        date_object = datetime.strptime(formatted_date, "%Y-%m-%d").date()
        new_date_minus_1 = date_object - timedelta(days=1)
        new_date_plus_1 = date_object + timedelta(days=1)
        if new_date_plus_1 > current_date_p:
           title_html = title_html +'<center><a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+' target=_blank><font size=3><font color=black><font size=4>['+str(new_date_minus_1)+']🔙</a><font color=red>'+start_date_time+'<a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_plus_1)+'  target=_blank></a><font color=black>  <a href=/theme/show_map2/'+SERIAL_NUMBER+'/ALL target=_blank>⮕[ALL]</a></a><font size=2> *4 weeks max<font size=4></center>'
        else:
           title_html = title_html +'<center><a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'  target=_blank><font size=3><font color=black><font size=4>['+str(new_date_minus_1)+']🔙</a><font color=red>'+start_date_time+'<a href=/theme/show_map2/'+SERIAL_NUMBER+'/'+str(new_date_plus_1)+'  target=_blank><font color=black>⮕['+str(new_date_plus_1)+'<font color=black>]</a><br><font color=black>  <a href=/theme/show_map2/'+SERIAL_NUMBER+'/ALL target=_blank>⮕[ALL]</a><font size=2> *4 weeks max<font size=4></center>'
     #

     m.get_root().html.add_child(folium.Element(title_html))

     # Add a house on the home location
     if float(longitude) < 0:
        longitude = float(longitude) + 360
     folium.Marker(
        location=[latitude, longitude],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 64px;">🏠</div>'
        ),
        popup='Home',
     ).add_to(m)

     # Add a finish flag on the target location
     if float(target_long) < 0:
        target_long = float(target_long) + 360
     ##folium.Marker(
     ##   location=[target_lat, target_long],
     ##   icon=folium.DivIcon(
     ##       icon_size=(150, 36),
     ##       icon_anchor=(0, 0),
     ##       html='<div style="font-size: 64px;">🏁</div>'
     ##   ),
     ##   popup='Target Address',
     ##).add_to(m)

     # Add a 📌 on the current location

     folium.Marker(
        location=[current_latitude, current_longitude],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 44px; white-space: nowrap;">📌 <font size=2><b>' + current_address + '</font></div>'
        ),
        popup=folium.Popup('Current location: ' + current_address, parse_html=True, max_width=400),
     ).add_to(m)

     # Render the Folium map as an HTML string
     map_html = m._repr_html_()
     ###map_html = map_html.replace('width: 100%;height: 100%', 'width: 100%').replace('height: 100.0%;', 'height: 609px;', 1)

     # Pass the map HTML to the template
     context = {'map_html': map_html}

    except:
     title_html=""
     map_html="<br><br><p><center> -- Map - Issue with tracking device: "+ser+" ---- "

    map_html=map_html+locations_html
    # Render a template with the map
    return map_html


import os
from django.http import HttpResponse
from django.shortcuts import render

def delete_imageX(request, image_name):
    try:
        # Assuming the images are stored in the /theme/static/images/ directory
        image_path = os.path.join('theme', 'static', 'images', image_name)

        # Check if the file exists before attempting to delete
        if os.path.exists(image_path):
            os.remove(image_path)
            return HttpResponse(f"Image '{image_name}' deleted successfully.")
        else:
            return HttpResponse(f"Image '{image_name}' does not exist.")
    except Exception as e:
        return HttpResponse(f"Error deleting image '{image_name}': {e}")

from django.shortcuts import render, redirect

def delete_image(request, image_name, pk):
    try:
        # Assuming the images are stored in the /theme/static/images/ directory
        image_path = os.path.join('theme', 'static', 'images', image_name)

        # Check if the file exists before showing the confirmation page
        if os.path.exists(image_path):
            return render(request, 'delete_confirmation.html', {'image_name': image_name, 'pk': pk})
        else:
            return HttpResponse(f"Image '{image_name}' does not exist.")
    except Exception as e:
        return HttpResponse(f"delete_image: Error deleting image '{image_name}': {e}")

def delete_confirmation(request, image_name, pk):
    if request.method == 'POST':
        # User confirmed the deletion, perform the actual deletion
        try:
            image_path = os.path.join('theme', 'static', 'images', image_name)
            os.remove(image_path)
            #return HttpResponse(f"Image '{image_name}' deleted successfully.")
            #return redirect('/theme/inventory_detail/') 
            return redirect('theme:inventory_detail', pk=pk)
        except Exception as e:
            return HttpResponse(f"delete_confirmation: Error deleting image '{image_name}': {e}")
    else:
        # User accessed the confirmation page without confirming, redirect back to the original view
        # issue here, staying on delete confirm screen??
        return redirect('/theme/delete_confirmation/', image_name=image_name, pk=pk) 
        #return redirect('/theme/delete_image/', image_name=image_name) 

#
#- OLD - use for mobile
#
import folium
from django.shortcuts import render
##@login_required
def show_map3_mobile(request,ser,dt):
    from datetime import datetime
    import json
    now=datetime.now() # current date and time
    if dt == "ALL":
       icon_list = {"icons": ["✅", "🚗",     "🚕",     "🚙",     "🚌",     "🚎",     "🏎",     "🚓",     "🚑",     "🚒",     "🚐",     "🛻",     "🚚",    "🚛",     "🚜",     "🛴",     "🚲",     "🛵",     "🏍",     "🛺",  "🚍",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽",     "📿",     "🔅",     "🔆",     "🔇",     "📍", "⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳", "㉑", "㉒", "㉓", "㉔", "㉕", "㉖", "㉗", "㉘", "㉙", "㉚", "㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵", "㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿", "✅", "🚗",     "🚕",     "🚙",     "🚌",     "🚎",     "🏎 ",     "🚓",     "🚑",     "🚒",     "🚐",     "🛻",     "🚚",    "🚛",     "🚜",     "🛴",     "🚲",     "🛵",     "🏍 ",     "🛺",  "🚍",     "🔗",     "🔘",     "🔙",     "🔛",     "🔜",     "🔝",     "🔞",     "🔥",     "🔦",     "🔧",     "🔨",     "🔩",     "🔪",     "🔫",     "🔮",     "🔱",     "🔲",     "🔳",     "🔵",     "🔶",     "🔷",     "🔸",     "🔹",     "🔺",     "🔻",     "💠",     "💡",     "💢",     "💣",     "💤",     "💥",     "💦",     "💧",     "💨",     "💩",     "💪",     "💫",     "💬",     "💭",     "💮",     "💯",     "💰",     "💱",     "💲",     "💳",     "💴",     "💵",     "💶",     "💷",     "💸",     "💹",     "💺",     "💻",     "💼",     "💽",     "💾",     "💿",     "📀",     "📂",     "📃",     "📄",     "📅",     "📇",     "📈",     "📉",     "📊",     "📋",     "+",     "📎",     "📏",     "📐",     "📑",     "📒",     "📓",     "📔",     "📕",     "📖",     "📗",     "📘",     "📙",     "📚",     "📛",     "📜",     "📝",     "📞",     "📟",     "📠",     "📡",     "📢",     "📣",     "📤",     "📦",     "📧",     "📨",     "📩",     "📪",     "📫",     "📬",     "📭",     "📮",     "📯",     "📰",     "📱",     "📳",     "📴",     "📵",     "📶",     "📷",     "📸",     "📹",     "📺",     "📻",     "📼",     "📽 ",     "📿",     "🔅",     "🔆",     "🔇",     "📍", "⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳", "㉑", "㉒", "㉓", "㉔", "㉕", "㉖", ">㉗", "㉘", "㉙", "㉚", "㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵", "㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿"]}
       D="_"
    else:
       icon_list = {"icons": ["✅"]}
       D=dt+"_"
    coords = []
    HOME_coords = []
    popup = []
    popup_tooltip = []
    bulb_color = []
    counter = []
    unique_dates = []
    set_icon = []
    addr = []
    full_date = []
    distance = []
    marker_counter=0
    unique_location_ctr=0
    unique_points_ctr=0
    serial_authorized="false"
    check_done="false"
    from .paths import CUST_DIR
    DIR=CUST_DIR
    accum_ser_chk=""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    if 'mobile' in user_agent or 'android' in user_agent:
        device = "mobile"
    else:
        device = "computer"
    if request.user.is_authenticated:
       logged_in_username = request.user.username
    elif device == "mobile":
    # changed to tracker from "" for  IOS testing - need to change back once we get auth code added for api
       #logged_in_username = "demo"
       # for IOS testing - change back to nothing after testing as we will provide an auth token once code is done
       logged_in_username = "tracker"
    else:
       logged_in_username = ""
    if logged_in_username != "":
       device_details = get_device_details(logged_in_username, ser)
       if device_details:       
           serial_authorized="true"
    else:
        map_html="[1]Not authorized, please login to render maps!"
        return render(request, 'route.html', {'map_html': map_html})
    # add back in IOS testing
    #if serial_authorized == "false":
    #    map_html="[2]Not authorized!"
    #    return render(request, 'route.html', {'map_html': map_html})
    prev_popup_date=""
    popup_date="                    "
    import csv
    PREV_APPLE_UPDATE_DATE=""
    PREV_ADDRESS=""

    import glob
    import csv
    # format  of log files: DATA/20230119_B0P00224515E_gps.TEXT.log
    if dt == "ALL":
       lowest_date,highest_date,count = data_get_low_high_count_dates(ser)
       if count > 21:
          pattern = "*_"+ser+"_*gps.5min.TEXT.log.SUMMARY"
       else:
          pattern = "*_"+ser+"_*gps.5min.TEXT.log"
    else:
       dt_mod=str(dt[0:4])+str(dt[5:7])+str(dt[8:10])
       pattern = dt_mod+"_"+str(ser)+'_gps.5min.TEXT.log'
    try: 
     for file_name in sorted(glob.glob(DIR + '/DATA/' + pattern), reverse=True):
      #print("file_name=",file_name)
      with open(file_name, 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
         DEVICE_ITEM = row[0]
         TAGNAME = row[1]
         SAMPLE_DATE = row[2]
         LAT = row[3]
         LONG = row[4]
         APPLE_UPDATE_DATE = row[5]
         TIME_SINCE_LAST_UPDATE = row[6]
         SERIAL_NUMBER = row[1]
         STATUS_MARK = row[8]
         DEGREES_LOCATION = row[9]
         ADDRESS = row[10]


         # Replace this with db looked, remove ini file use
         device_details = get_device_details(logged_in_username, ser)
         # Check if the function returned a result
         if device_details:
            serial_authorized="true"         
            DESCR=device_details['Description']
            TYPE_OF_ITEM=device_details['Tag_Type']
            SHOW=device_details['Attributes']
            HOME_LAT=device_details['Lat']
            HOME_LONG=device_details['Long']
                       
         from datetime import datetime, timedelta
         now=datetime.now() # current date and time
         date_string = now.strftime("%Y-%m-%d")
         date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
         #new_date_minus_7 = date_object - timedelta(days=365)
         #new_date_minus_7x = str(new_date_minus_7)                       
         # changed Oct 31, 2023 to stop limitting the data to 141 days.
         #print("TIME=[",SAMPLE_DATE[11:16],"]")
         # if ALL dates, limit it to 7am - midnight, Oct 31, 2023  - reduces data by 25%
         if ((dt == "ALL" and (SAMPLE_DATE[11:16] == "00:00" or SAMPLE_DATE[11:16] > "06:00")) or dt == SAMPLE_DATE[0:10]) and PREV_APPLE_UPDATE_DATE != APPLE_UPDATE_DATE:
         #if (dt == "ALL" or dt == SAMPLE_DATE[0:10]) and PREV_APPLE_UPDATE_DATE != APPLE_UPDATE_DATE:
         ##if (dt == "ALL" or dt == SAMPLE_DATE[0:10]) and PREV_APPLE_UPDATE_DATE != APPLE_UPDATE_DATE and SAMPLE_DATE[0:10] > new_date_minus_7x:
                  #print("PASSED TIME=[",SAMPLE_DATE[11:16],"]")
                  if PREV_APPLE_UPDATE_DATE != "":
                     DISTANCE=round(haversine(float(PREV_LAT),float(PREV_LONG), float(LAT), float(LONG)),2)
                  else:   
                     DISTANCE=0
                  unique_points_ctr=unique_points_ctr+1
                  distance.append(DISTANCE)   
                  unique_location_ctr=unique_location_ctr+1
                  PREV_APPLE_UPDATE_DATE=APPLE_UPDATE_DATE
                  popup_appledate=APPLE_UPDATE_DATE
                  PREV_LAT=LAT
                  PREV_LONG=LONG
                  popup_last_time_updated=APPLE_UPDATE_DATE
                  addr.append(ADDRESS)
                  full_date.append(SAMPLE_DATE)
                  # get the time indicator : ✅ means < 5 minutes, ❌ means > 1 hour, other means >5min<1hr
                  popup_last_time_updatedX=STATUS_MARK
                  popup_address=ADDRESS
                  popup_tagname=TAGNAME
                  if dt != "ALL":
                      serial_number = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ target=_blank><font size=2><font color=red><br>Click to show all data for Tag Name: <font color=blue>"+DESCR+"</a>"
                  else:
                      serial_number = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+"/ target=_blank><font color=red><font size=2>Filter to this date only: <font color=blue>"+SAMPLE_DATE[0:10]+"</a>"
                  serial_number_11=SERIAL_NUMBER
                  # format it with this format
                  # <a href=/theme/show_map2/X9L7criU6EA/2023-01-06/ target=_blank>SERIAL#</a href>
                  prev_popup_date=popup_date
                  popup_date=SAMPLE_DATE[0:10]
                  # set the icon based on relative position of the unique date to the icon_list dictionary
                  if popup_date != prev_popup_date:
                     #print("popup_date=",popup_date)
                     unique_dates.append(popup_date)
                     last_index = len(unique_dates) - 1
                     # allow access by index to the icon_list with icons variable
                     icons = icon_list['icons']
                     try:
                         set_icon.append(icons[last_index])
                     except:
                         set_icon.append("ERROR(NOT=)")
                  else:
                     last_index = len(unique_dates) - 1
                     icons = icon_list['icons']
                     set_icon.append(icons[last_index])
                  # Format html :
                  popup_lat_long_url="<td nowrap><font size=2><a href=https://www.google.com/maps/place/"+str(LAT)+","+str(LONG)+" target=_blank>📍</a>"
                  # check if the user is on a mobile so we can make some text bigger
                  user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
                  if 'mobile' in user_agent or 'android' in user_agent:
                     device = "mobile"
                     FNT="<font size=4>"
                  else:
                     device = "computer"
                     FNT="<font size=1>"
                  
                  popup_text = FNT+"<b><font color=red>Device/item name: <font color=blue>"+TYPE_OF_ITEM+" "+DESCR+"<br><font color=red>Collection date/time: <font color=blue>"+SAMPLE_DATE+"<br><font color=red>Address: <font color=blue>"+ADDRESS+"<br><font color=red>Locate Age at time of collection: <font color=blue>"+STATUS_MARK+" "+TIME_SINCE_LAST_UPDATE+"<br><font color=red>Date/time located: <font color=blue>"+APPLE_UPDATE_DATE+"<br><font color=red>Located at Lat/long: <font color=blue>"+LAT+","+LONG+" :click to open: "+popup_lat_long_url +"<br>"+serial_number +"<br><font color=red>Distance to next point: <font color=blue>"+str(DISTANCE)+"km - "+PREV_ADDRESS
                  popup_tooltip_text = FNT+"<b><font color=red>Device/item name: <font color=blue>"+TYPE_OF_ITEM+" "+DESCR+"<br><font color=red>Collection date/time: <font color=blue>"+SAMPLE_DATE+"<br><font color=red>Address: <font color=blue>"+ADDRESS+"<br><font color=red>Locate Age at time of collection: <font color=blue>"+STATUS_MARK+" "+TIME_SINCE_LAST_UPDATE+"<br><font color=red>Date/time located: <font color=blue>"+APPLE_UPDATE_DATE+"<br><font color=red>Located at Lat/long: <font color=blue>"+LAT+","+LONG  +"<br><font color=red>Distance to next point: <font color=blue>"+str(DISTANCE)+"km - "+PREV_ADDRESS
                  PREV_ADDRESS=ADDRESS
                  popup.append(popup_text)
                  popup_tooltip.append(popup_tooltip_text)
                  marker_counter = marker_counter + 1
                  counter.append(str(marker_counter))
                  elements_num0=float(LAT)
                  elements_num1=float(LONG)
                  coords.append((elements_num0, elements_num1))
         elif PREV_APPLE_UPDATE_DATE == APPLE_UPDATE_DATE: 
                  unique_points_ctr=unique_points_ctr+1
    except:
       print("Bad date") 
    # Create a Map instance, if the passed date yeilds 0 coordinates then we just fudge some to prevent error
    try:
       m = folium.Map(location=coords[0], zoom_start=13,zoom_control=True,control_scale=True)
       from folium.plugins import AntPath
       data2 = tuple(reversed(coords))
       AntPath(data2, delay=400,weight=3,color="black",dash_array=[60,20]).add_to(m)
       #m = folium.Map(location=coords[0], zoom_start=13,zoom_control=True,control_scale=True,position='bottomleft')
       #zoom_control = folium.ZoomControl(position='bottomright')
       #zoom_control.add_to(m)

    except:
       coords = [(43.8383632,-79.3000453), (43.8654045,-79.3129236), (43.8699234,-79.3055358)]
       m = folium.Map(location=coords[0], zoom_start=10,zoom_control=False)
    # reverse the counters as they are sorted by last data collected at the top
    counter_reversed = []
    for ele in reversed(counter):
        counter_reversed.append(ele)

    full_date_reversed = []
    for ele in reversed(full_date):
        full_date_reversed.append(ele)

    from folium.map import Popup
    from folium.map import Icon
    from folium.features import DivIcon
    first="true"
    previous_coords = None
    for i, (coord,d,number,tt,set_the_icon,addrs,f_date_r,f_date,dist) in enumerate(zip(coords,popup,counter_reversed,popup_tooltip,set_icon,addr,full_date_reversed,full_date,distance)):
        popup = folium.Popup(d,max_width=1000, style='white-space: nowrap')
        if first == "true":
           #if SHOW == "0": 
           DESCR2=DESCR[:2]
           DESCR2=DESCR2.replace(" ","")
           html='<div style="font-size: 11pt;font-weight: bold;  color : red;white-space: nowrap;"><font size=7>'+DESCR2[:1]+'<font size=5>📌<font color=black><font size=2>' +addrs+' '+f_date[0:16]+'</div>'
           first="false"
        else:   
            if int(f_date[11:13]) < 12:
               tm="am"
            else:
               tm="pm"
            ratio=0
            if i != 0:
               from fuzzywuzzy import fuzz
               ratio = fuzz.token_sort_ratio(addr[i], addr[i-1])
               #if ratio > 92:
               if dist < 0.05 or dt == "ALL":
                  tm=""
                  print_date=""
               elif ratio < 90:
                  print_date=f_date[11:16]
               else:
                  tm=""
                  print_date=""

            # check if the user is on a mobile so we can make some text bigger
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            if 'mobile' in user_agent or 'android' in user_agent:
                device = "mobile"
                FNT="<font size=3>"
                FNT_arrow="<font size=6>"
            else:
                device = "computer"
                FNT="<font size=2>"
                FNT_arrow="<font size=6>"
                FNT_arrow="<font size=3>"
            #check coord[0] and coord[1] to see direction and change the set_the_icon based on that
            if previous_coords != None:
                distance = haversine(float(previous_coords[0]), float(previous_coords[1]), float(coord[0]), float(coord[1]))
                if distance > .20:
                   current_coords = coord
                   #set_the_icon = set_the_icon+FNT_arrow+get_direction(previous_coords,coord)
                   # only show the direction arrows on non mobile devices as it clutters the screen
                   #if 'mobile' in user_agent: # or trip_category == "NOTIME":
                   # no time or arrows if it's ALL dates or mobile
                   if 'mobile' in user_agent or dt == "ALL": # or trip_category == "NOTIME":
                   # default to NOTIME, Oct 31, 2023
                       set_the_icon = ""
                       #set_the_icon = get_direction(coord,previous_coords)
                   else:
                       set_the_icon = set_the_icon+FNT_arrow # +get_direction(coord,previous_coords)
           
            # change this to modify the HH:MM that is on each marker
            if dt == "ALL":
               html='<div style="font-size: 9pt;font-weight: bold;  color : blue;"><font color=black><b></div>'+FNT+set_the_icon
            else:
               html='<div style="font-size: 9pt;font-weight: bold;  color : blue;"><font color=black><b></div>'+FNT+print_date +set_the_icon
            previous_coords = coord

        folium.Marker(coord,popup=popup,tooltip=tt,icon=DivIcon(html=html)).add_to(m)

        # Add home location from security file
        elements_num0=float(HOME_LAT)
        elements_num1=float(HOME_LONG)
        HOME_coords.append((elements_num0, elements_num1))

        # Create a LayerGroup
        LayerGroup = folium.FeatureGroup("LayerGroup")

        # Add a circle marker
        LayerGroup.add_child(folium.Marker(HOME_coords[0],icon=DivIcon(html='<font size=12>🏠')))
        # Add the LayerGroup to the map
        m.add_child(LayerGroup)                

    got_error="no"    
    if D == "_":
       last_index = len(unique_dates) - 1
       # get earliest date we have in the data
       earliest_date = unique_dates[last_index]
       latest_date = unique_dates[0]
       percent_points=round((unique_location_ctr*100)/unique_points_ctr)
       display_date="All Data - <font color=red>"+earliest_date+" : "+latest_date+" "+"<font color=black> - <br>"+str(last_index+1)+" days. <font color=green>Locations: "+str(unique_location_ctr)+"/"+str(unique_points_ctr)+" ["+str(percent_points)+"%]"
       title_link_ALL=""
    else:
        # just one date
        try:
           from datetime import date, timedelta
           date_string = D[0:10] # "2022-01-01"
           date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
           new_date_minus_1 = date_object - timedelta(days=1)
           new_date_plus_1 = date_object + timedelta(days=1)

           now=datetime.now() # current date and time
           CHK_D=now.strftime("%Y-%m-%d")
           if CHK_D == D[0:10]: 
              PREV_DAY='<br><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>['+str(new_date_minus_1)+'] 🔙 </a>[<a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+D[0:10]+'><font color=green>'+D[0:10]+'</a><font color=black>]' 
              ##PREV_DAY='<br><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>['+str(new_date_minus_1)+'] 🔙 </a>[<font color=red>'+D[0:10]+'<font color=black>]' 
           else:   
              # change Dec 23, 2023 remove the target=_default to handle IOS app
              PREV_DAY='<br><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>['+str(new_date_minus_1)+']🔙</a><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+D[0:10]+'><font color=green>'+D[0:10]+'</a><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_plus_1)+'><font color=black>⮕['+str(new_date_plus_1)+'<font color=black>]</a>' 
              #PREV_DAY='<br><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>['+str(new_date_minus_1)+']🔙</a><font color=red>'+D[0:10]+'<a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_plus_1)+'><font color=black>⮕['+str(new_date_plus_1)+'<font color=black>]</a>' 
              ##PREV_DAY='<br><a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_minus_1)+'><font size=3><font color=black>['+str(new_date_minus_1)+']🔙</a><font color=red>'+D[0:10]+'<a href=/theme/show_map2_mobile/'+SERIAL_NUMBER+'/'+str(new_date_plus_1)+'  target=_blank><font color=black>⮕['+str(new_date_plus_1)+'<font color=black>]</a>' 
           total_points=round(int(f_date_r[11:13])*12+int(f_date_r[14:16])/5)+1
           percent_points=round((unique_location_ctr*100)/total_points)
           display_date="<br><font size=3><font color=green> Locations: "+str(unique_location_ctr)+"/"+str(total_points)+" ["+str(percent_points)+"%]"+PREV_DAY
           #display_date=D[0:10]+"<font color=green> - Locations: "+str(unique_location_ctr)+"/"+str(total_points)+" ["+str(percent_points)+"%]"+PREV_DAY
        except Exception as e:
           got_error="yes"    
           total_points=0
        try:     
          # dec 23, 2023 change target
          title_link_ALL = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/><font color=black>[ALL]</a>"
          #title_link_ALL = "<a href=/theme/show_map2/"+SERIAL_NUMBER+"/ALL/ target=_blank><font color=black>[ALL Dates]</a>"
        except Exception as e:
          got_error="yes" 
    if got_error == "no":
     loc = "<font size=5><font color=blue>"+"<a href=/theme/gps_log_5min_today_last_IOS_Only/ALL/> 🪐 </a><font size=3>"+DESCR[:31]+"<font color=black> "+display_date+" "+title_link_ALL
     ##loc = "<font size=7><font color=blue>"+"<a href=/theme/gps_log_5min_today_last_IOS_Only/ALL/> ↞🏠 </a><font size=3>"+TYPE_OF_ITEM+" - "+DESCR[:20]+"<font color=black> "+display_date+" "+title_link_ALL
     title_html = '''
          <h6 align="center" style="font-size:12px"><b>{}</b></h3>
          '''.format(loc)
     m.get_root().html.add_child(folium.Element(title_html))

     # Generate a polyline for the route
     #folium.PolyLine(coords, color="black", weight=3, opacity=2, dash_array=5).add_to(m)
     #folium.PolyLine(coords, color="red", weight=2.5, opacity=1, dash_array=5).add_to(m)

     # Save the map to an HTML file
     map_html = m.get_root().render()
    else: 
     try:   
         map_html="<font color=red><font size=5>No Data Available - "+e
     except Exception as e:    
         map_html="<font color=red><font size=5>No Data Available"
    return render(request, 'route2.html', {'map_html': map_html})
#
# new show_map_trips
#
import folium
from django.shortcuts import render
#
from .models import Trip_Events
@login_required
def show_map_trips_new(request,pk):
    # read the pk from Trip_Events
    from django.shortcuts import get_object_or_404
    trip_event = get_object_or_404(Trip_Events, pk=pk)
    start_date_time=trip_event.start_date_time[0:10]
    end_date_time=trip_event.end_date_time[:10]
    start_location_address=trip_event.start_location_address
    end_location_address=trip_event.end_location_address
    start_lat_long=trip_event.start_lat_long
    target_lat_long=trip_event.target_lat_long
    trip_description=trip_event.trip_description
    trip_category=trip_event.trip_category
    trip_user=trip_event.trip_user
    trip_serial=trip_event.trip_serial

    if end_date_time == "":
       from datetime import datetime
       current_date = datetime.now().date()
       end_date_time = current_date.strftime("%Y-%m-%d")
    logged_in_username=request.user.username
    device_details = get_device_details(logged_in_username, trip_serial)
    if device_details:
       DESCR=trip_description
       TYPE_OF_ITEM=device_details['Tag_Type']
       HOME_LAT=device_details['Lat']
       HOME_LONG=device_details['Long']

    DESCR='〽'+DESCR
    #map_html = '<center><table id="map-container"><tr><td>+heatmap_view_inventory2('+trip_serial+','+ DESCR+','+ start_date_time+','+ end_date_time+','+ str(HOME_LAT)+','+str(HOME_LONG)+', Home, Home,'+ str(HOME_LAT)+','+str(HOME_LONG)+')</td></tr></table>'

#heatmap_view_inventory2(ser, trip_description, start_date_time, end_date_time, target_lat_long, end_location_address, sta     rt_location_address, start_lat_long)

    map_html = '<center><table id="map-container"><tr><td>'+heatmap_view_inventory2(trip_serial, DESCR, start_date_time, end_date_time, str(target_lat_long), end_location_address, start_location_address, start_lat_long)+'</td></tr></table>'

    ##map_html = '<center><table id="map-container"><tr><td>'+heatmap_view_inventory2(trip_serial, DESCR, start_date_time, end_date_time, str(HOME_LAT)+','+str(HOME_LONG), 'Home', 'Home', str(HOME_LAT)+','+str(HOME_LONG))+'</td></tr></table>'

    return render(request, 'route.html', {'map_html': map_html})

from django.shortcuts import render
from .models import Inventory

def inventory_for_sale_display(request):
    from .paths import CUST_DIR
    file_path = CUST_DIR+'/platform2.log'
    record="From inventory_for_sale_display, Request method:"+str(request.method)+" - Request headers:"+str(request.headers)
    try:
        # Open file for append
        with open(file_path, "a") as file:
           file.write(record)
    except Exception as e:
        print(f"Error writing to file: {e}")

    cart_log(request)
    inventory_items = Inventory.objects.filter(
        inventory_status='in-stock',
        inventory_sales_price__gt=0
    ).exclude(inventory_sales_price=None)

    import os
    import fnmatch
    from .paths import CUST_DIR
    path=CUST_DIR+'/theme/static/images'
    for inventory_item in inventory_items:
        images_dir = f'{path}/{inventory_item.id}_*'
        inventory_item.image_list = sorted(fnmatch.filter(os.listdir(path), str(inventory_item.id)+"_"+"*"))

    # Calculate the number of items in the cart
    num_items = len(request.session.get('cart', []))

    # Calculate the total value in the cart
    #total_value = sum(item.inventory_sales_price for item in request.session.get('cart', []))

    cart_item_ids = request.session.get('cart', [])
    cart_items = Inventory.objects.filter(id__in=cart_item_ids)
    total_value = sum(item.inventory_sales_price for item in cart_items)

    return render(
        request,
        'inventory_for_sale_display.html',
        {
            'inventory_items': inventory_items,
            'num_items_in_cart': num_items,
            'total_value_in_cart': total_value,
        }
    )

from django.shortcuts import render, redirect
from .models import Inventory

def add_to_cart(request):

    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        # Check if the item is already in the cart
        cart = request.session.get('cart', [])
        if item_id in cart:
            # Item is in the cart, remove it
            cart.remove(item_id)
        else:
            # Item is not in the cart, add it
            cart.append(item_id)

        # Update the session variable
        request.session['cart'] = cart

    return redirect('theme:inventory_for_sale_display')


from django.shortcuts import render
from .models import Inventory

def view_cart(request):
    # Get the list of item IDs from the session
    cart_item_ids = request.session.get('cart', [])

    # Query the Inventory model to get details of items in the cart
    cart_items = Inventory.objects.filter(id__in=cart_item_ids)

    import os
    import fnmatch
    from .paths import CUST_DIR
    path=CUST_DIR+'/theme/static/images'
    for item in cart_items:
        images_dir = f'{path}/{item.id}_*'
        item.image_list = sorted(fnmatch.filter(os.listdir(path), str(item.id)+"_"+"*"))

    total = sum(item.inventory_sales_price for item in cart_items)
    context = {'cart_items': cart_items, 'total': total }

    return render(request, 'view_cart.html', context)


from django.shortcuts import redirect

def remove_from_cart(request):
    if request.method == 'POST':
        cart_item_ids = request.session.get('cart', [])
        for key in request.POST:
            if key.startswith('remove_item_'):
                item_id = key.replace('remove_item_', '')
                if item_id in cart_item_ids:
                    cart_item_ids.remove(item_id)
        request.session['cart'] = cart_item_ids
    return redirect('theme:view_cart')

def cart_log(request): 
    user_agent = get_user_agent(request)
    from datetime import datetime
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'AnonymousUser'
    if user_agent.is_mobile or user_agent.is_tablet: 
        logging.info(f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | mobile | User: {username} | cart")
        platform = 'mobile'
    else: 
        logging.info(f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | computer | User: {username} | cart")  
        platform = 'computer'
    #record=f"{datetime.now()} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | computer  | User: {username}\n"
    record = f"{formatted_timestamp} | IP: {get_client_ip(request)} | Platform: {user_agent.device.family} | {platform} | User: {username} | cart\n"
    from .paths import CUST_DIR
    file_path = CUST_DIR+'/platform2.log'
    try:
        # Open file for append
        with open(file_path, "a") as file:
            # Write the record
            file.write(record)
        # File automatically closed when exiting the 'with' block
    except Exception as e:
        print(f"Error writing to file: {e}")
    return platform

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class hello_API(APIView): 

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user  # Get the current logged-in user
        content = {'message': f'Hello, {user.username}!', 'user_id': user.id}
        return Response(content)

import os
import math
from rest_framework.permissions import AllowAny
from .serializers import ChartSerializer
           
class chart_api(APIView):
    permission_classes = [AllowAny]

    @staticmethod       
    def todays_distance_for_serial_number_IOS(date,serial_number):
        import csv           
        import datetime    
        from math import radians, sin, cos, sqrt, atan2
        from datetime import datetime
        if date == "":   
           today = datetime.now().strftime("%Y%m%d")
        else:       
           today=date
        from .paths import CUST_DIR
        filename = f"{CUST_DIR}/DATA/{today}_{serial_number}_gps.5min.TEXT.log"
        total_distance = 0
        total_non_home = 0
        total_home = 0
        different_updated_dates_ctr=1
        try:
         with open(filename, 'r',encoding="utf-8") as file:
            reader = csv.reader(file)
            previous_latitude = None
            previous_longitude = None
            previous_updated_date_time = None

            for row in reader:
                latitude = float(row[3])
                longitude = float(row[4])
                description = row[10]
                updated_date_time = row[5]
                location=description
                if location == "Home":
                   total_home=total_home+1
                else:
                   total_non_home=total_non_home+1
                if previous_latitude is not None and previous_longitude is not None:
                    # if the current updated data is less than previous we have some issue with the data so dist=0
                    if updated_date_time >= previous_updated_date_time:
                       distance = 0
                    else:
                       different_updated_dates_ctr=different_updated_dates_ctr+1
                       distance = haversine(previous_latitude, previous_longitude, latitude, longitude)
                       if distance >= 0.250:
                          total_distance += distance
                previous_latitude = latitude
                previous_longitude = longitude
                previous_updated_date_time = updated_date_time
        except:
           pct_diff=0

        # get div by zero error at 00:00 cuz only 1 record
        try:
           pct_diff=round(different_updated_dates_ctr/(total_home+total_non_home)*100)
        except:
           pct_diff=0
        #
        return round(total_distance,0),total_home,total_non_home,different_updated_dates_ctr,pct_diff
    def get(self, request):
        logger = logging.getLogger(__name__)
        #logger.info("header="+str(request.META))
        #try:
        #   token = request.META['HTTP_HTTP_MR_TRACKER_TOKEN']
        #except:
        #   token = "Not provided"
        #   return Response("Tokenization Error")
        serializer = ChartSerializer(data=request.query_params)
        if serializer.is_valid():
            serialNumber = serializer.validated_data.get('serialNumber')
            username = serializer.validated_data.get('username')
            logger.info("in serializer, serialNumber="+serialNumber)
        from .paths import CUST_DIR
        path=CUST_DIR+"/DATA/"
        pattern = "*_"+serialNumber+"_gps.5min.TEXT.log"
        json_data = []
        files = glob.glob(CUST_DIR+'/DATA/*_'+serialNumber+'_gps.5min.TEXT.log')
        files.sort()  # Sort the files sequentially
        last_7_files = files[-45:]
        for filename in last_7_files:
           #logger.info("filename="+filename)
           fn = os.path.basename(filename)
           date = fn[:8]
           distance_today, total_home, total_non_home, different_updated_dates_ctr, pct_diff = self.todays_distance_for_serial_number_IOS(date,serialNumber)
           id_counter = 0 
           report_dict = {
            "id": id_counter,
             "name": date,
             #"name": date[:2],
             "sales": distance_today,
            }
           id_counter += 1
           json_data.append(report_dict)
           logger.info("date="+date[-2:]+" distance="+str(distance_today))
        return Response(json_data)

from rest_framework.permissions import AllowAny
from .serializers import ChartSerializer
        
class chart_api2(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
           json_data = []
           id_counter = 0
           report_dict = {
            "id": id_counter,
             "name": "Jan",
             "sales": 28,
            }
           id_counter += 1
           json_data.append(report_dict)
           report_dict = {
            "id": id_counter,
             "name": "Feb",
             "sales": 18,
            }
           id_counter += 1
           json_data.append(report_dict)
           return Response(json_data)

#
# to be used to pass info to my IOS app
#
from rest_framework.permissions import AllowAny
from .serializers import TagListSerializer

class tag_health_api(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]
#
# Function get is where all the action happens
#
    def get(self, request):
               import csv
               import json
               from .paths import CUST_DIR
               from datetime import datetime

               # Path to your CSV file
               csv_file_path = CUST_DIR+'/health.out'

               # List to store JSON data
               json_data = []

               # Counter for id field
               id_counter = 1

               current_date = datetime.now().strftime('%Y-%m-%d')

               # Open CSV file and read data
               with open(csv_file_path, 'r') as csv_file:
                   # Create a CSV reader
                   csv_reader = csv.reader(csv_file)

                   # Iterate through rows
                   for row in csv_reader:
                       row_date = row[0][:10].strip()
                       # Create a dictionary for each row
                       if row_date == current_date:
                         report_dict = {
                           "id": id_counter,
                           "Date_time": row[0].strip(),
                           #"Date_time": row[0][10:16].strip(),
                           "all_ctr": row[1].strip(),
                           "active_ctr": row[2].strip(),
                           "away_ctr": row[3].strip(),
                           "lost_ctr": row[4].strip(),
                           "battery_weak_ctr": row[5].strip(),
                           "healthy_ctr": row[6].strip(),
                       }

                         # Increment id counter
                         id_counter += 1

                         # Append the dictionary to the list
                         json_data.append(report_dict)

               # Convert the list to JSON
               #json_output = json.dumps(json_data, indent=2)
               json_data_sorted = sorted(json_data, key=lambda x: x["Date_time"], reverse=True)
               return Response(json_data_sorted) 

#
# to be used to pass info to my IOS app
#
class tag_list_api(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]
    @staticmethod       
    def todays_distance_for_serial_number_IOS(date,serial_number):
        import csv           
        import datetime     
        from math import radians, sin, cos, sqrt, atan2
        from datetime import datetime
        if date == "":  
           today = datetime.now().strftime("%Y%m%d")
        else:       
           today=date
        from .paths import CUST_DIR
        filename = f"{CUST_DIR}/DATA/{today}_{serial_number}_gps.5min.TEXT.log"
        total_distance = 0
        total_non_home = 0
        total_home = 0
        different_updated_dates_ctr=1
        try:      
         with open(filename, 'r',encoding="utf-8") as file:
            reader = csv.reader(file)
            previous_latitude = None
            previous_longitude = None
            previous_updated_date_time = None

            for row in reader:
                latitude = float(row[3])
                longitude = float(row[4])
                description = row[10]
                updated_date_time = row[5]
                location=description
                if location == "Home":
                   total_home=total_home+1
                else:
                   total_non_home=total_non_home+1
                if previous_latitude is not None and previous_longitude is not None:
                    # if the current updated data is less than previous we have some issue with the data so dist=0
                    if updated_date_time >= previous_updated_date_time:
                       distance = 0
                    else:
                       different_updated_dates_ctr=different_updated_dates_ctr+1
                       distance = haversine(previous_latitude, previous_longitude, latitude, longitude)
                       if distance >= 0.250:
                          total_distance += distance
                previous_latitude = latitude
                previous_longitude = longitude
                previous_updated_date_time = updated_date_time
        except:
           pct_diff=0

        # get div by zero error at 00:00 cuz only 1 record
        try:
           pct_diff=round(different_updated_dates_ctr/(total_home+total_non_home)*100)
        except:
           pct_diff=0
        #
        return round(total_distance,0),total_home,total_non_home,different_updated_dates_ctr,pct_diff

    @staticmethod
    def get_device_details_IOS(username, serial_number):
        from .models import DeviceItemSecurity
        #username='tracker'
        try:   
            device = DeviceItemSecurity.objects.get(username__iexact=username, Serial_Number__iexact=serial_number)
            return {
                'id': device.id,
                'username': device.username,
                'Serial_Number': device.Serial_Number,
                'Description': device.Description,
                'Tag_Type': device.Tag_Type,
                'Attributes': device.Attributes,
                'Lat': device.Lat,
                'Long': device.Long,
                'category': device.category,
                'feeder': device.feeder
            }     
        except DeviceItemSecurity.DoesNotExist:
            return None
#
# Function get is where all the action happens
#
    def get(self, request):
        #from django.db.models import F
        logger = logging.getLogger(__name__)
        #logger.info("header="+str(request.META))
        try:
           token = request.META['HTTP_HTTP_MR_TRACKER_TOKEN']
        except:
           token = "Not provided"
           return Response("Tokenization Error")
        serializer = TagListSerializer(data=request.query_params)
        if serializer.is_valid():
            option = serializer.validated_data.get('option')
            user_id = serializer.validated_data.get('user_id')
            #token = serializer.validated_data.get('token')
        from django.apps import apps
        from django.db import connection
        Token = apps.get_model('authtoken', 'Token')
        token_count = Token.objects.filter(key=token).count() 
        token_user_id = list(Token.objects.filter(key=token).values_list('user_id', flat=True))
        token_user_id = token_user_id[0] 
        token_user_id = int(token_user_id)
        if token_count > 0:
           with connection.cursor() as cursor:
             cursor.execute("SELECT COUNT(*) FROM auth_user WHERE id = %s", (token_user_id,))
             row = cursor.fetchone()
             record_count = row[0]
             if record_count == 0:
                return Response("Special2 Auth failed")
                logger.info("2-token lookup was unsuccessful, access denied")
             else:
                from django.contrib.auth.models import User
                user_data = User.objects.filter(id=token_user_id).values_list('first_name', 'last_name', 'username')
                first_name = user_data.first()[0]
                last_name = user_data.first()[1] 
                looked_up_username = user_data.first()[2]  
                if user_id != looked_up_username:
                   logger.info("FAILED: user_id passed="+user_id+" looked up username="+looked_up_username)
                   return Response("Unauthorized hacking attempt")
        else:
           logger.info("1-token lookup was unsuccessful, access denied")
           return Response("Special1 Auth failed")
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        from .paths import CUST_DIR
        LOG=CUST_DIR+'/server.log'
        DATA = CUST_DIR+'/gps_current_TEXT_5min_LAST_1min.log'
        with open(DATA, 'r', encoding="utf-8") as DATA_log:
            csv_reader_DATAlog = csv.reader(DATA_log, delimiter=',', quotechar="'")
            DATAlog_content = list(csv_reader_DATAlog)
        #final_output='<!DOCTYPE html><table border=1>'
        html='<!DOCTYPE html><html><body><font size=10>Tag List<br><br><table border=1>'
        text=''
        import json
        json_records = []
        # for option="REPORT"
        away_ctr = 0
        active_ctr = 0
        lost_ctr = 0
        all_ctr = 0
        healthy_ctr = 0
        battery_weak_ctr = 0
        for record in DATAlog_content:
           # lookup the serial to see if the user is allowed to view this tag
           device_details = self.get_device_details_IOS(user_id, record[1])  
           if device_details:
              # the only thing I need from the Device record is the Description and home_lat,home_lon
              description = device_details['Description'][:30]
              #description = device_details['Description'][:24]
              lat2 = float(device_details['Lat'])
              lon2 = float(device_details['Long'])
              # These fields all come from the 1min file
              serialNumber = record[1]
              lat1 = float(record[3])
              lon1 = float(record[4])
              ago = record[6]
              ago = ago.replace("Hours","hr")
              marker = record[8]
              address = record[10]
              battery_status = record[11]
              # calculated fields
              distance,total_home,total_non_home,different_updated_dates_ctr,pct_diff=self.todays_distance_for_serial_number_IOS("",str(record[1]))
              # Create a dictionary for each record
              link='https://MrRobby.ca/theme/show_map2_mobile/'+serialNumber+'/'+str(today)+'/'
              id=1
              BATTERYSTATUS=''
              B=int(battery_status.replace("%",""))
              if B == 100:
                 BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
              elif B > 79:
                 BATTERYSTATUS="🔋"+str(BATTERYSTATUS) 
              elif B > 59:
                 BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
              elif B > 39:
                 BATTERYSTATUS="⚡"+str(BATTERYSTATUS)
              elif B > 19:
                 BATTERYSTATUS="🪫"+str(BATTERYSTATUS)
              elif B >0:   
                 BATTERYSTATUS="🪫" +str(BATTERYSTATUS)
              else:   
                 BATTERYSTATUS="💤" +str(BATTERYSTATUS)

              # calculate the distance fron home for AWAY option
              # example use: haversine(previous_latitude, previous_longitude, latitude, longitude)
              #def haversine(lat1, lon1, lat2, lon2):
              from math import radians, sin, cos, sqrt, atan2
              R = 6371  # radius of Earth in km
              lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
              dlat = lat2 - lat1
              dlon = lon2 - lon1
              a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
              c = 2 * atan2(sqrt(a), sqrt(1-a))
              distance_from_home = int(R * c)

              record_dict = {
                  "id": id,
                  "description": description,
                  "battery_status": BATTERYSTATUS,
                  "marker": marker,
                  "distance": str(int(distance))+"km/"+str(distance_from_home),
                  "address": address,
                  "serialNumber": serialNumber,
                  "link": link,
                  "distance_from_home": str(distance_from_home),
                  "ago": ago,
              }
              id=id+1
              # Append the dictionary to the list
              if (option == "HEALTHY" and marker != "❌") or (option == "BATTERY_WEAK" and BATTERYSTATUS == "🪫") or option == "ALL" or (option == "AWAY" and address != "Home") or (option == "ACTIVE" and distance > 0) or (option == "LOST" and marker == "❌"):
                 json_records.append(record_dict)
                 html=html+'<tr><td nowrap><font size=9>'+marker+str(battery_status)+':'+description+':'+str(distance)+'<br>..<a href=https://MrRobby.ca/theme/show_map2_mobile/'+serialNumber+'/'+str(today)+'/>'+address+'</td></a>'
                 text=text+marker+','+str(battery_status)+','+description+','+str(distance)+',https://MrRobby.ca/theme/show_map2_mobile/'+','+serialNumber+','+str(today)+',"'+address+'"\n'
              if option == "REPORT":
                  if marker == "❌": 
                     lost_ctr = lost_ctr + 1
                     if distance > 0:
                        active_ctr = active_ctr + 1
                     if address != "Home":
                        away_ctr = away_ctr + 1
                  elif distance > 0:
                     active_ctr = active_ctr + 1
                     if address != "Home":
                        away_ctr = away_ctr + 1
                  elif address != "Home":
                     away_ctr = away_ctr + 1
                  if BATTERYSTATUS == "🪫":
                     battery_weak_ctr = battery_weak_ctr + 1
                  all_ctr = all_ctr + 1
        html=html+'</table></body>'
        #json_string = json.dumps({"result": json_records})
        healthy_ctr = all_ctr - lost_ctr
        if option == "REPORT":
              id=1
              json_report = []
              report_dict = {
                  "id": id,
                  "all_ctr":          str(all_ctr),
                  "active_ctr":       str(active_ctr),
                  "away_ctr":         str(away_ctr),
                  "lost_ctr":         str(lost_ctr),
                  "healthy_ctr":      str(healthy_ctr),
                  "battery_weak_ctr": str(battery_weak_ctr),
                  "type": "REPORT",
              }
              json_report.append(report_dict)
       
        if option == "REPORT":
           return Response(json_report)
        else:
           return Response(json_records)
#
# URL Mapping: /theme/gps_log_5min_today_last_IOS_Only/ALL/
#
from .models import DeviceItemSecurity

@login_required
def read_file_gps_5min_today_last_IOS_Only(request,category_selected):
    from .paths import CUST_DIR
    file_path = CUST_DIR+'/platform2.log'
    record="From read_file_gps_5min_today_last_IOS_Only, Request method:"+str(request.method)+" - Request headers:"+str(request.headers)
    try:
        # Open file for append
        with open(file_path, "a") as file:
           file.write(record)
    except Exception as e:
        print(f"Error writing to file: {e}")
    platform='mobile'
    import csv
    item_counter=1
    from .paths import CUST_DIR
    file = open(CUST_DIR+'/gps_current_TEXT_5min_LAST_1min.log', 'r',encoding="utf-8")
    reader = csv.reader(file, delimiter=',', quotechar="'")
    # sort by category and Tag type
    reader = sorted(reader, key=lambda x: (x[12].upper(), x[0]),reverse=False)
    found_user="false"
    heading_once=True
    # store elements in array so we can sort them
    col_row = []
    row_num=0
    file_contents=""
    #
    for row in reader:
        TYPE        = row[0]
        TAGNAME     = row[1]
        SAMPLE_DATE = row[2][0:16]
        SAMPLE_DATE=SAMPLE_DATE.replace("_", " ")
        LAT         = row[3]
        LONG        = row[4]
        APPLE_UPDATE_DATE      = row[5]
        TIME_SINCE_LAST_UPDATE = row[6]
        SERIAL_NUMBER          = row[1]
        STATUS_MARK            = row[8]
        DEGREES_LOCATION       = row[9]
        ADDRESS                = row[10][0:40]
        ADDRESS=ADDRESS.replace(","," ")
        BATTERYSTATUS          = row[11]
        B=int(BATTERYSTATUS.replace("%",""))
        if B == 100:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
        elif B > 79:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS) 
        elif B > 59:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
        elif B > 39:
           BATTERYSTATUS="🔋"+str(BATTERYSTATUS)
        elif B > 19:
           BATTERYSTATUS="🪫"+str(BATTERYSTATUS)
        elif B >0:   
           BATTERYSTATUS="🪫" +str(BATTERYSTATUS)
        else:   
           BATTERYSTATUS="💤" +str(BATTERYSTATUS)
        if TYPE == "Device":
           BOLD="<b>"
        else:
           BOLD=""
        #
        # Load up the security file in to a list to check if the user should have access to the device_item
        #
        from .paths import CUST_DIR
        DIR = CUST_DIR
        SHOW="0"
        if request.user.is_authenticated:
           logged_in_username = request.user.username
           # Call the function with the desired username and serial_number
           device_details = get_device_details(logged_in_username, SERIAL_NUMBER)
           # Check if the function returned a result
           if device_details:
              found_user = "true" 
              # Reference the values in the returned dictionary
              device_ID = str(device_details['id'])
              username = device_details['username']
              serial_number = device_details['Serial_Number']
              SERIALN = serial_number
              description = device_details['Description']
              DESCR = description
              X=DESCR[0:1]
              tag_type = device_details['Tag_Type']
              TYPE_OF_TAG = tag_type
              attributes = device_details['Attributes']
              SHOW = attributes
              lat = device_details['Lat']
              HOME_LAT = lat
              longi = device_details['Long']
              HOME_LONG = longi
              category=device_details['category']

              try:
                  device_item_security_instance = DeviceItemSecurity.objects.get(
                       username__iexact=logged_in_username,
                       Serial_Number__iexact=SERIAL_NUMBER
                  )

                  if device_item_security_instance.feeder:
                     feeder_instance = device_item_security_instance.feeder
                     ip_address = feeder_instance.ip_address
                     iphone = feeder_instance.iphone.replace("iphone","")
                     #print("IP Address:", ip_address)
                  else:
                     ip_address = ""
                     iphone = ""
                     #print("Feeder is not set for this DeviceItemSecurity instance.")

              except DeviceItemSecurity.DoesNotExist:
                  ip_address = ""
                  iphone = ""
                  print("DeviceItemSecurity instance not found.")

              if platform == 'computer' or platform =='mobile' and (category_selected == category or category_selected == "ALL" or category_selected == "ACTIVE" or category_selected == "AWAY" or category_selected == "ALERTS"):
               if heading_once == True:
                  if category_selected == "ACTIVE": 
                     head="<tr><td><font size=9><center>{Tag Selection: Only <b>Active</b> Tags}</center></td>"
                  elif category_selected == "AWAY":
                     head="<tr><td><font size=9><center>{Tag Selection: Only <b>Away</b> Tags}</center></td>"
                  else:
                     head="<tr><td><font size=9><center>{Tag Selection: <b>"+category_selected+"}</b></center></td>"
                  fs="<font size=9>"
                  fc06mobile="<tr>"
                  #fc06mobile="<table class='bordered-table'><tr>"
                  #fc06mobile="<table class='bordered-table'><tr><td nowrap>"+"<font size=12><font color=grey><b><center>---- Tag Name/Location ----</td>"
                  # set the output for headings
                  file_contents=head+fc06mobile+"<tr>"
                  heading_once=False
               fs="<font size=9>"
               if SHOW == "0":
               #if SHOW == "0" and (category_selected == category or category_selected == "ALL" or category_selected == "ACTIVE" or category_selected == "AWAY" or category_selected == "ALERTS"):
                 fc49="<td nowrap><center>"+fs+"<font size=9>"+str(item_counter)+"</td>"
                 if int(BATTERYSTATUS[1:].replace("%","")) < 21: 
                    col="red"
                 else:
                    col="black"

                 if ADDRESS == 'Home':
                    br = '<br>'
                    c = '<font color=blue>'
                 else:
                    br = '<br>'
                    c = '<font color=blue>'
                 distance_today,total_home,total_non_home,different_updated_dates_ctr,pct_diff=todays_distance_for_serial_number("",SERIAL_NUMBER)
                 if distance_today > 0:
                    dist=str(distance_today)+'km'
                 else:
                    dist=''
                 if (category_selected == "ACTIVE" and distance_today > 0) or (category_selected == "AWAY" and ADDRESS != "Home") or  category_selected == "ALL": 
                    fc55mobile="<tr><td nowrap>"+fs+"<font size=8>"+BATTERYSTATUS[0:1]+STATUS_MARK+"|<font size=8>"+DESCR+":<font size=6>("+iphone+")"+":"+dist+"</font>"+br+"&nbsp;&nbsp;&nbsp;<a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=9>"+"🌎"+c+"</b>"+ADDRESS+"</a></td>"
                    ##fc55mobile="<tr><td nowrap>"+fs+DESCR+"<font size=8>("+iphone+")"+BATTERYSTATUS[0:1]+STATUS_MARK+" "+dist+"</font>"+br+"&nbsp;&nbsp;&nbsp;<a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=9>"+"📌"+c+"</b>"+ADDRESS+"</a></td>"
                    #fc55mobile=fc68="<td nowrap><b>"+fs+DESCR+"<font size=6>("+iphone+")"+BATTERYSTATUS[0:1]+STATUS_MARK+" "+str(distance_today)+'km '+"</font>"+br+"&nbsp;&nbsp;&nbsp;<a href=/theme/show_map2_mobile/"+SERIAL_NUMBER+"/"+SAMPLE_DATE[0:10]+" class='btn btn-sm custom-btn btn-fixed-width20' title='Map of Today'><font size=9>"+"📌"+c+"</b>"+ADDRESS+"</a></td>"
                 # set output for data
                    file_contents=file_contents+fc55mobile+"<tr>"
               else:
                 continue
    file.close()
    result=file_contents 
    if found_user == "false":
        result="<font color=red><br>You have not registered any Trackers as yet! Please contact us now!"
    args = {'result': result}
    return render(request, "view_log_IOS_Only.html", args)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from .serializers import LoginSerializer

class api_login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        from .paths import CUST_DIR
        file_path = CUST_DIR+'/platform2.log'
        record="Request method:"+str(request.method)+" - Request data:"+str(request.data)
        try:
            # Open file for append
            with open(file_path, "a") as file:
               file.write(record)
        except Exception as e:
            print(f"Error writing to file: {e}")

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                # Authentication successful, generate a token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # Authentication failed
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid data
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class hello_API2(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the current logged-in user
        content = {'message': f'Hello, {user.username}!', 'user_id': user.id}
        return Response(content)

# https://mrrobby.ca/theme/show_map_api?serial=HGCJPLQ9P0GV&username=xxxxx
#
#- OLD - use for mobile API
#
#from django.shortcuts import render
from rest_framework import serializers
from .serializers import TagMapSerializer
class show_map_api(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]
#
# Function get is where all the action happens
#
    def get_device_details(username, serial_number):
        try:   
            device = DeviceItemSecurity.objects.get(username__iexact=username, Serial_Number__iexact=serial_number)
            return {
            'id': device.id,
            'username': device.username,
            'Serial_Number': device.Serial_Number,
            'Description': device.Description,
            'Tag_Type': device.Tag_Type,
            'Attributes': device.Attributes,
            'Lat': device.Lat,
            'Long': device.Long,
            'category': device.category,
            'feeder': device.feeder
            }     
        except DeviceItemSecurity.DoesNotExist:
            return None

    def get(self, request):
     serializer = TagMapSerializer(data=request.query_params)
     if serializer.is_valid():
         ser = serializer.validated_data.get('ser')
         username = serializer.validated_data.get('username')
         date = serializer.validated_data.get('date')
         days = serializer.validated_data.get('days')
     logged_in_username=username # passed

     import logging
     logger = logging.getLogger(__name__)
     #logger.info("date passed ="+str(date))
     # request_META is the request headers
     #logger.info("header="+str(request.META))
     #
     # Authorization for MT Tracker had to be customized on the fact that the Authorization Header is not passed from Swift
     # As a result I had to create my own header called HTTP_HTTP_MR_TRACKER_TOKEN
     # When the swift app passes the Token through that header we check it against the authtoken_token table which has all tokens
     # We get the user_id # back that matches the token and we compare that against the QUERY_STRING username
     # To ensure the user is not hacking us
     #
     try:
        token = request.META['HTTP_HTTP_MR_TRACKER_TOKEN']
     except:
        token = "Not provided"
        return Response("Tokenization Error")
     from django.apps import apps
     from django.db import connection
     Token = apps.get_model('authtoken', 'Token')
     token_count = Token.objects.filter(key=token).count()
     token_user_id = list(Token.objects.filter(key=token).values_list('user_id', flat=True))
     token_user_id = token_user_id[0]
     token_user_id = int(token_user_id)
     if token_count > 0:
        with connection.cursor() as cursor:
          cursor.execute("SELECT COUNT(*) FROM auth_user WHERE id = %s", (token_user_id,))
          row = cursor.fetchone()
          record_count = row[0]
          if record_count == 0:
             return Response("Special2 Auth failed")
             logger.info("2-token lookup was unsuccessful, access denied")
          else:
             from django.contrib.auth.models import User
             user_data = User.objects.filter(id=token_user_id).values_list('first_name', 'last_name', 'username')
             first_name = user_data.first()[0]
             last_name = user_data.first()[1]
             looked_up_username = user_data.first()[2]
             if username != looked_up_username:
                #logger.info("PASSED: token lookup was successful and matched username. first_name="+first_name+" last_name="+last_name)
                logger.info("FAILED: user_id passed="+username+" looked up username="+looked_up_username)
                return Response("Unauthorized hacking attempt")
     else:
        logger.info("1-token lookup was unsuccessful, access denied")
        return Response("Special1 Auth failed")


     from datetime import datetime
     current_date = datetime.now().strftime('%Y%m%d')
     from .paths import CUST_DIR
     DIR=CUST_DIR
     # needed for api
     report_dict = []
     json_data = []
     id_counter=0

     # only return last 1 day of a tag
     #days=1
     from datetime import datetime, timedelta
     current_date = datetime.now()
     current_date_str = current_date.strftime('%Y%m%d')

     # only get 1 min data if today's date
     # pull off the latest 1 min record to show on map to be current
     #logger.info("date="+date+" current_date_str="+current_date_str)
     if date == current_date_str:
      one_min_data = 'gps_current_TEXT_5min_LAST_1min.log'
      with open(DIR+'/'+one_min_data, 'r', encoding="utf-8") as one_min_file:
         #logger.info("getting 1min data as it is current date!")
         one_min_reader = csv.reader(one_min_file, delimiter=',', quotechar="'")
         for row in one_min_reader:
          SERIAL_NUMBER = row[1]
          if SERIAL_NUMBER == ser:
           DEVICE_ITEM = row[0]
           SAMPLE_DATE = row[2]
           LAT = row[3]
           LONG = row[4]
           APPLE_UPDATE_DATE = row[5]
           #TIME_SINCE_LAST_UPDATE = row[6]
           #STATUS_MARK = row[8]
           #DEGREES_LOCATION = row[9] 
           address1 = row[10]
           address2 = address1.replace(","," ")
           address = address2.replace("'","")
           device_details = get_device_details(logged_in_username, ser)
           if device_details:
              description=device_details['Description']
              #TYPE_OF_ITEM=device_details['Tag_Type']
              #SHOW=device_details['Attributes']
              home_lat=str(device_details['Lat'])
              home_long=str(device_details['Long'])
              #if longitude < 0:
              #   longitude = longitude + 360
              # Create a dictionary for each row
              #logger.info("1min: Returned, SAMPLE_DATE="+SAMPLE_DATE.strip()+" APPLE_UPDATE_DATE=["+APPLE_UPDATE_DATE+"} ")
              report_dict = {
                           "id": id_counter,
                           "Sample_Date_Time": SAMPLE_DATE.strip(),
                           "iCloud_Date_Time": APPLE_UPDATE_DATE.strip(),
                           "description": description.strip(),
                           "address":address.strip(),
                           "home_latitude": float(home_lat),
                           "home_longitude": float(home_long),
                           "latitude": float(LAT),
                           "longitude": float(LONG),
                       }
              id_counter += 1
              json_data.append(report_dict)

     #from datetime import datetime
     #pattern = current_date+"_"+ser+"_*gps.5min.TEXT.log"
     #for file_name in sorted(glob.glob(DIR + '/DATA/' + pattern), reverse=True):

     # over ride the date for passed date
     current_date_str = date
     passed_date = datetime.strptime(date, "%Y%m%d")
     passed_date_d = passed_date.strftime('%Y%m%d') 
     #formatted_date = date

     # calc the new date based on passed date minute (days - 1)
     result_date = passed_date - timedelta(days=days-1)
     formatted_date = result_date.strftime('%Y%m%d')

     if days == 1:
        pattern = current_date_str+"_"+ser+"_*gps.5min.TEXT.log"
     else:
        pattern = "*"+ser+"_*gps.5min.TEXT.log"

     file_list = glob.glob(DIR + '/DATA/' + pattern)
     file_list = sorted(file_list, reverse=True)
     #file_list.sort(key=lambda x: datetime.strptime(re.search(r'(\d{8})', x).group(1), '%Y%m%d'), reverse=False)
     import logging
     logger = logging.getLogger(__name__)
     APPLE_UPDATE_DATE_PREV=""
     ADDRESS_PREV=""
     #logger.info("file_list="+str(file_list))
     for file_name in file_list:
       first_8_characters = file_name.split('/')[-1][:8]
       #logger.info("in loop, current file_list="+str(file_name))
       #match = re.search(r'(\d{8})', file_name)
       #if match:
       #logger.info("Compare first_8_characters >= formatted_date - "+str(first_8_characters)+" vs "+str(formatted_date))
       #logger.info("Compare first_8_characters <= passed_date_d - "+str(first_8_characters)+" vs "+str(passed_date_d))
       if first_8_characters >= formatted_date and first_8_characters <= passed_date_d:
        with open(file_name, 'r', encoding="utf-8") as file:
         #logger.info("in loop, current file_list="+str(file_name))
         reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
         for row in reader:
          APPLE_UPDATE_DATE = row[5]
          if APPLE_UPDATE_DATE_PREV != APPLE_UPDATE_DATE:
           #logger.info("PASS: just compared PREV to CURRENT, SAMPLE_DATE="+SAMPLE_DATE.strip()+" APPLE_UPDATE_DATE=["+APPLE_UPDATE_DATE+"} APPLE_UPDATE_DATE_PREV=["+APPLE_UPDATE_DATE_PREV+"]")
           DEVICE_ITEM = row[0]
           SERIAL_NUMBER = row[1]
           #TAGNAME = row[1]
           SAMPLE_DATE = row[2]
           LAT = row[3]
           LONG = row[4]
           #TIME_SINCE_LAST_UPDATE = row[6]
           #STATUS_MARK = row[8]
           #DEGREES_LOCATION = row[9]
           full_address = row[10]
           address = row[10] #[:25]  # limit to 25 chars to reduce memory
           # adding 360 to negative longitudes to fix mapping issue
           #if float(LONG) < 0:
           #   LONG=str(float(LONG)+360)
           #latitude, longitude = float(LAT), float(LONG)
           #APPLE_UPDATE_DATE_PREV = APPLE_UPDATE_DATE
           #logged_in_username=username # passed
           # get the user details to add to map info
           device_details = get_device_details(logged_in_username, ser)
           if device_details:
              description=device_details['Description']
              #TYPE_OF_ITEM=device_details['Tag_Type']
              #SHOW=device_details['Attributes']
              home_lat=str(device_details['Lat'])
              home_long=str(device_details['Long'])
              #if longitude < 0:
              #   longitude = longitude + 360
              # Create a dictionary for each row
              #logger.info("Selected, SAMPLE_DATE="+SAMPLE_DATE.strip()+" APPLE_UPDATE_DATE=["+APPLE_UPDATE_DATE+"} APPLE_UPDATE_DATE_PREV=["+APPLE_UPDATE_DATE_PREV+"]")
              APPLE_UPDATE_DATE_PREV = APPLE_UPDATE_DATE
              #if 1 == 1: $4277 Paul 31 days - crash, too much memory used
              #if address != "Home": #1019 Paul 31 days
              #if (address == "Home" and ADDRESS_PREV != "Home") or address != "Home": 
              # least # of points with this filter
              if (address == "Home" and ADDRESS_PREV != "Home") or (address != "Home" and ADDRESS_PREV != address): 
               #logger.info("Selected, SAMPLE_DATE="+SAMPLE_DATE.strip()+" address=["+address+"] ADDRESS_PREV=["+ADDRESS_PREV+"]")
               report_dict = {
                           "id": id_counter,
                           "Sample_Date_Time": SAMPLE_DATE.strip(),
                           "iCloud_Date_Time": APPLE_UPDATE_DATE.strip(),
                           "description": description.strip(),
                           "address":address.strip(),
                           "home_latitude": float(home_lat),
                           "home_longitude": float(home_long),
                           "latitude": float(LAT),
                           "longitude": float(LONG),
                       }
               id_counter += 1
               json_data.append(report_dict)
               ADDRESS_PREV = address
               #json_data_sorted = sorted(json_data, key=lambda x: x["Sample_Date_Time"], reverse=True)
               #json_data=json_data_sorted
     logger.info("Total points returned: "+str(id_counter))
     return Response(json_data)
