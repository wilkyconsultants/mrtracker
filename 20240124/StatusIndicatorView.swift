//
//  StatusIndicatorView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

struct StatusIndicatorView: View {
    let title: String
    let value: String
    let color: Color

    var body: some View {
        
        VStack(alignment: .leading) {
            Text("\(title): \(value)")
                .font(.title3)
                .multilineTextAlignment(.leading)
                .foregroundColor(color)
        }
    }
}
