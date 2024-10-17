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
    @State private var flash = false
    
    @State private var isDeviceMapExpanded = true
    @State private var isDeviceRoutesExpanded = true
    @State private var isStatusChartsExpanded = false
    @State private var isAlertingExpanded = false

    var body: some View {
        NavigationView {
            VStack {
                Text("MR🌐Tracker Main Menu")
                    .bold()
                List {
                    if let reports = reports {
                       // Section(header: Text("Device Map").font(.custom("Arial", size: 16)).bold()) {
                        DisclosureGroup("Device Map", isExpanded: $isDeviceMapExpanded) {
                        NavigationLink(destination: FindMyView(username: username, server: server)) {
                            Label("Locate All Devices", systemImage: "mappin.and.ellipse")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(10)
                                .background(Color.clear)
                                .cornerRadius(8)
                                .opacity(flash ? 1.5 : 0.4) // Use a ternary operator to alternate between 1.0 and 0.5 opacity
                                .onAppear {
                                    withAnimation(Animation.easeInOut(duration: 1).repeatForever()) {
                                        flash.toggle()
                                    }
                                }
                        }
                        }.bold()

                       // Section(header: Text("Device Routes").font(.custom("Arial", size: 16)).bold()) {
                            DisclosureGroup("Device Routes", isExpanded: $isDeviceRoutesExpanded) {

                                NavigationLink(destination: TagDetailView(username: username, server: server, token: token, option: "ALL", chartList: "")) {
                                    Label("All (\(reports[0].all_ctr))", systemImage: "circle")
                                }
                                NavigationLink(destination: TagDetailView(username: username, server: server, token: token, option: "HEALTHY", chartList: "")) {
                                    Label("Healthy (\(reports[0].healthy_ctr))", systemImage: "checkmark.circle.fill")
                                }
                                // ... other NavigationLinks
                                NavigationLink(destination: TagDetailView(username: username, server: server, token: token, option: "ACTIVE", chartList: "")) {
                                    Label("Active Today (\(reports[0].active_ctr))", systemImage: "bolt.fill")
                                }
                                NavigationLink(destination: TagDetailView(username: username, server: server, token: token, option: "AWAY", chartList: "")) {
                                    Label("Travelling (\(reports[0].away_ctr))", systemImage: "car.fill")
                                }
                                NavigationLink(destination: TagDetailView(username: username, server: server, token: token, option: "BATTERY_WEAK", chartList: "")) {
                                    Label("Low Battery (\(reports[0].battery_weak_ctr))", systemImage: "battery.25percent")
                                }
                                NavigationLink(destination: TagDetailView(username: username, server: server, token: token, option: "LOST", chartList: "")) {
                                    Label("Lost > 1 hour (\(reports[0].lost_ctr))", systemImage: "exclamationmark.triangle.fill")
                                }
                           // }
                        }.bold()

                       // Section(header: Text("Status Charts").font(.custom("Arial", size: 16)).bold()) {
                            DisclosureGroup("Status Charts", isExpanded: $isStatusChartsExpanded) {
                            NavigationLink(destination: ChartALLBatteryView(server: server, username: username, serialNumber: "", description: "")) {
                                Label("Battery", systemImage: "battery.100percent.bolt")
                            }
                            // ... other NavigationLinks
                            NavigationLink(destination: ChartALLTagPerfView(server: server, username: username, serialNumber: "", description: "")) {
                                Label("Performance", systemImage: "flame.fill")
                            }
                            NavigationLink(destination: ChartALLDistanceView(server: server, username: username, serialNumber: "", description: "")) {
                                Label("Distance", systemImage: "map.fill")
                            }
                            NavigationLink(destination: ChartUpTimeView(server: server)) {
                                Label("Server Up-Time", systemImage: "play.display")
                            }
                        }.bold()

                       // Section(header: Text("Alerting").font(.custom("Arial", size: 16)).bold()) {
                            DisclosureGroup("Alerting", isExpanded: $isAlertingExpanded) {
                            NavigationLink(destination: AllAlertView(server: server)) {
                                Label("Notifications", systemImage: "bell.fill")
                            }
                        }.bold()
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
                .listStyle(InsetGroupedListStyle())
            }.padding(.bottom, 20)
            .onAppear {
                fetchData()
            }
            .navigationBarTitleDisplayMode(.inline)

        }
        .navigationBarBackButtonHidden(true)
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
        guard let url = URL(string: "https://\(server)/theme/tag_list_api?option=REPORT&user_id=\(username)&filter=") else {
            return
        }

        var request = URLRequest(url: url)
        request.addValue("\(token)", forHTTPHeaderField: "HTTPMRTRACKERTOKEN")

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            // if let response = response {
            //    print("response=\(response)")
           // }
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
