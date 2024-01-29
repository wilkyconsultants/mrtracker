//
//  InfoView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

struct InfoView: View {

    
    let InfoText = """
        MR🌐Tracker Change Highlights:
        Version 1.0 (2024-01-17) - Initial Release
        Version 1.1 (2024-01-18) - lines on routes
        Version 1.2 (2024-01-19) - toolbar
        Version 1.3 (2024-01-20) - date selection
        Version 1.4 (2024-01-21) - coloured routes
        Version 1.5 (2024-01-23) - distance chart
        Version 1.6 (2024-01-24) - search bar
        Version 1.7 (2024-01-25) - battery chart
        Version 1.8 (2024-01-29) - perfo chart

        🌐 The Ultimate Solution for GPS Device Tracking Anywhere in the World!

        MR🌐Tracker is a state-of-the-art GPS monitoring solution designed to keep track of the location of various assets. Whether it is tracking vacation cruises, packages, luggage, vehicles, backpacks, bicycles, or construction equipment, MR🌐Tracker provides comprehensive oversight to meet your needs.

        🚀 Key Features:
        - Simple setup: Include a tracking tag with your asset and you are ready to go.
        - Global tracking: Tags record locations worldwide, often with very low data charges, check with your carrier.
        - Versatile use: Ideal for travelers, professionals, and over-all asset protection.

        💻 Setup Process:
        Setting up MR🌐Tracker is easy. You will need a computer as a web server and some kind of location tags. We handle software installation, network setup, and provide remote support for a nominal charge. Your own data can be secured with SSL encryption, ensuring privacy. Reports are accessible only to you as an admin, and you have control over user access. This is a free service that runs securely at your site with limited access to who you need to be able to see the items being monitored. You choose if this is intranet only or internet by firewall ports.

        📲 iOS App:
        The iOS app is free on the App Store, making it convenient to access maps and reports. The front end is able to interact with a set APIs from a back end rest framework. You can use any webserver to store the data as long as it supports rest APIs. We provide a demo set up for exploration only with test data. The idea is you have your own server and we can help you with the set up.

        📧 Get Started:
        To begin, send an email to MrTracker.416@gmail.com. We will guide you through the setup process.

        ❓ Questions or Concerns:
        If you have any questions or concerns about MR🌐Tracker, contact us at MrTracker.416@gmail.com. We value your feedback!
    
    """

    var body: some View {
        ScrollView {
            Text(InfoText)
                .padding()
        }
        .navigationBarTitle("Product Information", displayMode: .inline)
    }
}

