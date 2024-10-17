//
//  UpTimeView.swift
//  MRTRACKER
//
//  Created by Robert A Wilkinson on 2024-02-07.
//
import SwiftUI
import Charts

// Model to represent the data
struct UpTimeData: Codable {
    let id: Int
    let date: String
    let hour: String
    let pct_up_time: Double
}

struct UpTimeView: View {
    @State private var upTimeData: [UpTimeData] = []
    let server: String

    var body: some View {
        VStack {
            if upTimeData.isEmpty {
                Text("Loading...")
                    .padding()
            } else {
                BarChartView(data: upTimeData)
                    .padding()
            }
        }
        .onAppear {
            fetchData()
        }
    }

    // Function to fetch data from the URL
    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/UpTime_api") else {
            print("Invalid URL")
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data else {
                print("No data received: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            do {
                // Parse JSON data into array of UpTimeData objects
                upTimeData = try JSONDecoder().decode([UpTimeData].self, from: data)
            } catch {
                print("Error decoding JSON: \(error.localizedDescription)")
            }
        }.resume()
    }
}

// SwiftUI Bar Chart View
struct BarChartView: View {
    let data: [UpTimeData]

    var body: some View {
        VStack {
            Text("Up-Time Percentage")
                .font(.headline)
                .padding()



            // List showing each date, time, and pct_up_time
            let sortedData = data.sorted {
                if $0.date != $1.date {
                    return $0.date > $1.date
                } else {
                    return $0.hour > $1.hour
                }
            }
            List(sortedData, id: \.id) { entry in
                HStack {
                    VStack(alignment: .leading) {
                        Text("Date: \(entry.date) \(entry.hour):00 Pct: \(String(format: "%.2f", entry.pct_up_time))")
                            .font(.footnote)
                            .foregroundColor(entry.pct_up_time == 100 ? .blue : .red)

                    }
                }
               // .padding(.horizontal)
            }
            //.frame(maxHeight: .infinity)
        }
    }
}
