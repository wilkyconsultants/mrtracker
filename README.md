
MR🌐Tracker, The Ultimate Solution for Tracking Anything, Anywhere in the World.

This is a cutting-edge tracking solution, meticulously engineered to monitor the location of a diverse range of assets. From cruises, letters and packages to luggage, vehicles, keys, backpacks, bicycles, and construction equipment – we've got you covered. 

Whether you're a traveler, a professional, or simply looking to safeguard your belongings, our advanced technology offers comprehensive oversight, providing the peace of mind you deserve. Simply decide what you want to track, attach a tag, and you're good to go – it's that simple.

The solution is made up of a back end django website, pthyon data collectors and a front end IOS application. Location data can be collected on any type of tag that can provide GPS location data (Lat/Long).

The IOS app works by connection to URL's on any back end with specific API HSON data returned.

API's comprise of the following:

ContentView.swift:
https://\(server)/theme/api_login/

TagListView.swift:
https://\(server)/theme/tag_list_api?option=REPORT&user_id=\(username)

TagDetailView.swift
https://\(server)/theme/tag_list_api?option=\(option)&user_id=\(username)

CommentDetailView.swift
https://\(server)/theme/show_map_api?ser=\(comment.serialNumber)&username=\(username)&date=\(formattedDate)&days=\(days)

ChartView.swift
https://\(server)/theme/chart_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)

ChartBatteryView.swift
https://\(server)/theme/chart_Battery_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)

ChartTagPerfView.swift
https://\(server)/theme/chartTagPerf_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)

Most of the API's rely on Token authentication to the django back end so you must have a userid on the back end server. This is set up either by the system admin or through the django website.



