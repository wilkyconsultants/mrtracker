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
    2024-01-18 -Version 1.1 - add lines on routes
    2024-01-19 -Version 1.2 - add toolbar
    2024-01-20 -Version 1.3 - date selection
    2024-01-21 -Version 1.4 - add coloured routes
    2024-01-23 -Version 1.5 - add distance chart
    2024-01-24 -Version 1.6 - add search bar
    
    The Ultimate Solution for Tracking Anything, Anywhere in the World.

    MR🌐Tracker is a cutting-edge tracking solution, meticulously engineered to monitor the location of a diverse range of assets. From vacation cruises, letters and packages to luggage, vehicles, keys, backpacks, bicycles, and construction equipment – we've got you covered. Whether you're a traveler, a professional, or simply looking to safeguard your belongings, our advanced technology offers comprehensive oversight, providing the peace of mind you deserve.
    
    Simply decide what you want to track, attach a tag, and you're good to go – it's that simple. The tags record locations worldwide with no data charges.

    Your typical setup includes a MacBook computer, iPhone, and tracking tags. Run as a franchise at your site. We handle all the necessary software installation, network setup, and offer remote support for a nominal charge. Rest assured about data privacy – all data uses SSL encryption, ensuring your information remains secure. Reports are accessible only to you as an admin, and you can grant access to additional users with user IDs chosen by you as the admin.
    
    To get started send an email to MrTracker.416@gmail.com and we will walk you throigh teh set up required.

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
