
MR🌐Tracker, Is the Ultimate Solution for Tracking almost Anything, Anywhere in the World.

This is a cutting-edge tracking solution, meticulously engineered to monitor the location of a diverse range of assets. From cruises, letters and packages to luggage, vehicles, keys, backpacks, bicycles, and construction equipment – we've got you covered. This solution is not intended to be used to pin point assets, rather track the general location data on an ongoing basis for that asset. There are better solutions for tracking the exact location of items but these can work handin hand with this solution if desired.

Whether you're a traveler, a professional, or simply looking to safeguard your belongings, our advanced technology offers comprehensive oversight, providing the peace of mind you deserve. Simply decide what you want to track, attach a tag, and you're good to go – it's that simple.

The solution is made up of a back end django website, pthyon data collectors and a front end IOS application. Location data can be collected on any type of tag that can provide GPS location data (Lat/Long).

The IOS app works by connection to URL's on any back end with specific API HSON data returned.

API's comprise of the following:

ContentView.swift:
https://\(server)/theme/api_login/

TagListView.swift:
https://\(server)/theme/tag_list_api?option=REPORT&user_id=\(username)

TagDetailView.swift:
https://\(server)/theme/tag_list_api?option=\(option)&user_id=\(username)

CommentDetailView.swift:
https://\(server)/theme/show_map_api?ser=\(comment.serialNumber)&username=\(username)&date=\(formattedDate)&days=\(days)

ChartView.swift:
https://\(server)/theme/chart_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)

ChartBatteryView.swift:
https://\(server)/theme/chart_Battery_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)

ChartTagPerfView.swift:
https://\(server)/theme/chartTagPerf_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)

Most of the API's rely on Token authentication to the django back end so you must have a userid on the back end server. This is set up either by the system admin or through the django website.

You can run this as a service, renting out tags (GPS or other) or as a franchise, use for tracking company or personal assets.

The system will scale to fit your needs with as many tracking tags support based on "feeders". We typically use a MacBook computer or Mac Mini as a webserver and install feeder systems as needed and register these feeders to the website which will connect to each feeder and collect the location data on any interval decided upon. Typically 5 minute intervals are sufficient to reduce total data collection and m=allow it to be more managable.

The base back end software currently runs on Macbook feeders as it collects location coorinates using Apple features but with some custimization can be expanded to support many types of location devices as they become available in the market. This can be added and customized for a small development fee, just ask!

