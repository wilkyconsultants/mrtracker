//
//  TagListView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

struct TagListView: View {
    let username: String
    let server: String
    let token: String
    let chartList: String

    @State private var reports: [Reports]?
    @State private var isLoading = false
    @State private var datadate = Date()

    var body: some View {
        
        VStack {
            Text("Refreshed: \(formattedCurrentDateTime())")
                .foregroundColor(.green)
                .bold()
                .font(.title3)
                .padding()

            if let reports = reports {
                ForEach(reports) { report in
                    VStack {
                        HStack(alignment: .center) {
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL", chartList: "")) {
                                CircleLink(text: "All", count: report.all_ctr, fillColor: Color.teal, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "HEALTHY", chartList: "")) {
                                CircleLink(text: "Healthy", count: report.healthy_ctr, fillColor: Color.green, fontSize: 16)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ACTIVE", chartList: "")) {
                                CircleLink(text: "Active Today", count: report.active_ctr, fillColor: Color.blue, fontSize: 16)
                            }
                            //}
                        }
                        HStack(alignment: .center) {
                            //Spacer()
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "AWAY", chartList: "")) {
                                CircleLink(text: "Travelling", count: report.away_ctr, fillColor: Color.cyan, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "BATTERY_WEAK", chartList: "")) {
                                CircleLink(text: "Low 🪫", count: report.battery_weak_ctr, fillColor: Color.yellow, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "LOST", chartList: "")) {
                                CircleLink(text: "Lost > 1 hour", count: report.lost_ctr, fillColor: Color.red, fontSize: 18)
                            }
                        }
                        Divider()
                        HStack(alignment: .center) {
                            //Spacer()
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL", chartList: "CHART")) {
                                CircleLink(text: "Distance ", count: "Chart", fillColor: Color.orange, fontSize: 18)
                            }
                        //}
                        NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL", chartList: "CHART_BATTERY")) {
                            CircleLink(text: "Battery🪫 ", count: "Chart", fillColor: Color.brown, fontSize: 18)
                        }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL", chartList: "CHART_TAGPERF")) {
                                CircleLink(text: "Tag Perf ", count: "Chart", fillColor: Color.purple, fontSize: 18)
                            }
                    }
                        
                        //Spacer(minLength: 30)
                        HStack(spacing: 5) {
                            Text("Tags: \(report.all_ctr)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.primary)
                            Divider().background(Color.primary)
                            VStack {
                                if let healthyCtr = Double(report.healthy_ctr), let allCtr = Double(report.all_ctr), allCtr > 0 {
                                    let ratio = healthyCtr / allCtr
                                    let percentage = Int(round(ratio * 100))
                                    Button(action: {
                                        isLoading = true
                                    }) {
                                        //Spacer()
                                        ZStack {
                                            // Outer circle representing the entire pie chart
                                            Circle()
                                                .fill(circleFillColor(for: percentage).opacity(0.5))
                                                .frame(width: 140, height: 140)

                                            // Pie chart segment based on the percentage
                                            Circle()
                                                .trim(from: 0.0, to: CGFloat(percentage) / 100.0)
                                                .stroke(circleFillColor(for: percentage), lineWidth: 40)
                                                .frame(width: 100, height: 100)
                                                .rotationEffect(.degrees(-90)) // Start from the top

                                            Text("Tag Health: \(percentage)%")
                                                .font(.system(size: 18))
                                                .bold()
                                                .foregroundColor(.black)
                                        }
                                    }
                                    .padding()
                                }
                            }
                        }
                        .padding()
                    }
                }
                //Divider()
                // This needs to turn in to a tab bar
                VStack(alignment: .center) {
                    //Text("👨🏻‍💼 MR🌐Tracker")
                    Text("")
                        .font(.title)
                        .toolbar {
                            ToolbarItemGroup(placement: .automatic) {
                                HStack {
                                    Button(action: {
                                        fetchData()
                                        
                                    }) {
                                        VStack(alignment: .center) {
                                            Image(systemName: "arrow.clockwise")
                                                .resizable()
                                                .frame(width: 20, height: 20)
                                                .aspectRatio(contentMode: .fit)
                                            Text("Refresh")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                        }
                                    }

                                }
                            }
                        }
                }

            } else {
                if isLoading {
                    ProgressView("Loading...")
                        .progressViewStyle(CircularProgressViewStyle(tint: .blue))
                        .scaleEffect(2.0)
                        .padding()
                } else {
                    Text("Loading...")
                }
            }
        }
        .onAppear {
            fetchData()
        }
        .navigationTitle("👨🏻‍💼 MR🌐Tracker")
    }
    
    func circleFillColor(for percentage: Int) -> Color {
        switch percentage {
        case 0..<50:
            return .red
        case 50..<70:
            return .yellow
        default:
            return .green
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/tag_list_api?option=REPORT&user_id=\(username)") else {
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
                let decodedData = try JSONDecoder().decode([Reports].self, from: data)
                DispatchQueue.main.async {
                    self.reports = decodedData
                    isLoading = false
                }
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
            }
        }.resume()
    }

    func formattedCurrentDateTime() -> String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MMM d, y h:mm a" // Use the desired format

        return dateFormatter.string(from: Date())
    }
}

