//
//  CircleLink.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

struct CircleLink: View {
    let text: String
    let count: String
    let fillColor: Color
    let fontSize: CGFloat

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 10)
                .fill(fillColor)
                .frame(width: 110, height: 60)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.black, lineWidth: 4)
                        .blur(radius: 4)
                        .offset(x: 2, y: 2)
                        .mask(RoundedRectangle(cornerRadius: 10).fill(LinearGradient(gradient: Gradient(colors: [.black, .clear]), startPoint: .top, endPoint: .bottom)))
                )
                .clipShape(RoundedRectangle(cornerRadius: 10))
                .shadow(color: Color.black.opacity(0.3), radius: 5, x: 2, y: 2)

            VStack {
                Text(text)
                    .foregroundColor(.black)
                    .font(.system(size: fontSize))
                Text(count)
                    .foregroundColor(.white)
                    .font(.title3)
            }
        }
    }
}

