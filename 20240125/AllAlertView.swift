//
//  AllAlertView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-28.
//

import SwiftUI

struct AlertData: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    var date: String
    var alert: String
    var action: String
    var description: String
    var serialNumber: String
}


struct AllAlertView: View {
    let server: String
    @State private var alertData: [AlertData] = []
    @State private var searchText = ""

    var body: some View {
        NavigationView {
            List {
                ForEach(alertData.filter {
                    searchText.isEmpty ? true :
                    $0.description.localizedCaseInsensitiveContains(searchText) ||
                    $0.date.localizedCaseInsensitiveContains(searchText) ||
                    $0.alert.localizedCaseInsensitiveContains(searchText) ||
                    $0.action.localizedCaseInsensitiveContains(searchText) ||
                    $0.serialNumber.localizedCaseInsensitiveContains(searchText)
                }) { alert in
                    HStack {
                        VStack(alignment: .leading) {
                            let updatedDate = alert.date.replacingOccurrences(of: "_", with: " ")
                            Text("\(alert.description)")
                                .fontWeight(.bold)
                                .foregroundColor(.green)
                                .font(.system(size: 16))
                                .textSelection(.enabled) // Add this line to left-align the text
                            Text("\(updatedDate), \(alert.alert) -> \(alert.action)")
                                .foregroundColor(.blue)
                                .font(.system(size: 14))
                            //Text("Alert: \(alert.alert) - \(alert.action)")
                            //    .foregroundColor(.red)
                            //    .font(.system(size: 14))
                            Text("")
                        }
                        Spacer()
                    }
                }
                .navigationTitle("All Alerts")
                .searchable(text: $searchText)
                .onAppear {
                    fetchData()
                }
            }
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/Alerts_api") else {
            return
        }

        URLSession.shared.dataTask(with: url) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([AlertData].self, from: data)
                    DispatchQueue.main.async {
                        self.alertData = decodedData
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}

