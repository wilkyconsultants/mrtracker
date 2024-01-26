
//
//  TagDetailView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

struct TagDetailView: View {
    let username: String
    let server: String
    let token: String
    let option: String
    let chartList: String

    @State private var comments: [Comments]?
    @State private var searchText = ""

    var filteredComments: [Comments] {
        comments?.filter {
            $0.description.localizedCaseInsensitiveContains(searchText)
        } ?? []
    }

    var body: some View {
        VStack {
            SearchBar(text: $searchText)

            // Fetch and display filtered data
            if let comments = comments {
                List {
                    ForEach(searchText.isEmpty ? comments : filteredComments) { comment in

                    // Your existing code for displaying comments
                    if chartList == "CHART" {
                        NavigationLink(destination: ChartView(server: server,username: username,serialNumber: comment.serialNumber, description: comment.description)) {
                            VStack(alignment: .leading) {
                                Text("\(comment.description)")
                                //.padding()
                                    //.background(Color.blue.opacity(0.2)) // Set background color here
                                    .cornerRadius(8) // Add corner radius for a rounded look
                                //Divider()
                                //Text("  ► \(comment.battery_status)\(comment.marker)\(comment.ago): //🏃\(comment.distance)km ")
                                //Text("📍\(comment.address)")
                            }
                        }
                        } else {
                            NavigationLink(destination: CommentDetailView(comment: comment,server: server, username: username, distance: comment.distance, marker: comment.marker, ago: comment.ago, token: token)) {
                                VStack(alignment: .leading) {
                                    Text("\(comment.description)")
                                    //.padding()
                                        .background(Color.blue.opacity(0.2)) // Set background color here
                                        .cornerRadius(8) // Add corner radius for a rounded look
                                    //Divider()
                                    Text("  ► \(comment.battery_status)\(comment.marker)\(comment.ago): 🏃\(comment.distance)km ")
                                    Text("📍\(comment.address)")
                                //}
                        }
                       }
                    }
                }
                }
            } else {
                ProgressView("Loading...")
                    .progressViewStyle(CircularProgressViewStyle())
            }
        }
        .onAppear {
            fetchComments()
        }
        .navigationTitle("🏷️ [\(String(option.prefix(7)))]")
    }
    

    func fetchComments() {
        guard let url = URL(string: "https://\(server)/theme/tag_list_api?option=\(option)&user_id=\(username)") else {
            return
        }

        var request = URLRequest(url: url)
        request.addValue("\(token)", forHTTPHeaderField: "HTTP_MR_TRACKER_TOKEN")

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            do {
                let decodedData = try JSONDecoder().decode([Comments].self, from: data)
                DispatchQueue.main.async {
                    self.comments = decodedData
                }
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
            }
        }.resume()
    }
}
struct SearchBar: View {
    @Binding var text: String

    var body: some View {
        HStack {
            TextField("Search", text: $text)
                .padding(8)
                .background(Color(.systemGray6))
                .cornerRadius(8)
                .padding(.horizontal, 10)
            Button(action: {
                text = ""
            }) {
                Image(systemName: "xmark.circle.fill")
                    .foregroundColor(.gray)
                    .padding(8)
            }
            .padding(.trailing, 10)
            .opacity(text.isEmpty ? 0 : 1)
            .animation(.default)
        }
    }
}
