//
//  InfoView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

struct InfoView: View {
    let InfoText = """
    MR🌐Tracker Change History:
    2024-01-17 -Version 1.0 - Initial
    2024-01-18 -Version 1.1 - lines on routes
    2024-01-19 -Version 1.2 - toolbar
    2024-01-20 -Version 1.3 - date selection
    2024-01-21 -Version 1.4 - colour routes
    2024-01-23 -Version 1.5 - distance chart
    2024-01-24 -Version 1.6 - search bar
    
    The Ultimate Solution for Tracking Anything, Anywhere in the World.

    MR🌐Tracker is a cutting-edge tracking solution, meticulously engineered to monitor the location of a diverse range of assets. From vacation cruises, letters and packages to luggage, vehicles, keys, backpacks, bicycles, and construction equipment – we've got you covered. Whether you're a traveler, a professional, or simply looking to safeguard your belongings, our advanced technology offers comprehensive oversight, providing the peace of mind you deserve.
    
    Simply decide what you want to track, attach a tag, and you're good to go – it's that simple. The tags record locations worldwide, usually with no data charges depending on your set up.

    Your typical setup includes a computer, to be used as a webserver, and tracking tags. You generally run the application as a franchise at your site. We handle all the necessary software installation, network setup, and offer remote support for a nominal charge. Rest assured about data privacy – all data uses SSL encryption, ensuring your information remains secure. Reports are accessible only to you as an admin, and you can grant access to additional users with user IDs chosen by you as the admin. There is no cost for the IOS iphone application as it is provided via App Store free of charge to make it easier to access your maps and reports.
    
    To get started send an email to MrTracker.416@gmail.com and we will walk you through the set up required.

    If you have any questions or concerns regarding Mr Tracker functionality please contact us by using email address MrTracker.416@gmail.com, we would love to hear from you!
    
    """

    var body: some View {
        ScrollView {
            Text(InfoText)
                .padding()
        }
        .navigationBarTitle("Product Information", displayMode: .inline)
    }
}
