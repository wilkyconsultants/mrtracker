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
        Version     (2024-01-18) - lines on routes
        Version     (2024-01-19) - toolbar
        Version     (2024-01-20) - date selection
        Version     (2024-01-21) - coloured routes
        Version     (2024-01-23) - distance chart
        Version     (2024-01-24) - search bar
        Version     (2024-01-25) - battery chart
        Version     (2024-01-29) - perf chart
        Version     (2024-02-01) - auto login
        Version     (2024-02-03) - Clean up
        Version     (2024-02-04) - map color red
        Version     (2024-02-04) - device map
        Version     (2024-02-05) - revamp menu
        Version     (2024-02-07) - back-end perf
        Version     (2024-02-15) - fix tokens

        ❓ Questions or Concerns:
        If you have any questions or concerns about MR🌐Tracker, contact us at MrTracker.416@gmail.com. We value your feedback!
    """

    var body: some View {
        ScrollView {
            Text(InfoText)
                .padding()
        }
        .navigationBarTitle("MR🌐Tracker IOS App Information", displayMode: .inline)
    }
}
