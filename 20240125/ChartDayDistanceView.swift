//
//  ChartDayDistanceView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-28.
//

import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187

class ChartsViewModel8: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}


//
struct ChartData8: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let date: String   // name
    let distance: Double
    let serialNumber: String
    //let response: Int       // sales
    let seq: String
}

struct GraphType8: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartDayDistanceView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    let date: String
    
    private let pdays = Array(1...365)
    @State private var days = 7  // default is 7 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel8()
    @State private var chartData8: [ChartData8] = []
    
    @State private var totalDistance: Double = 0
    
    @State private var navigateToDetailView = false
    
    var updateTotalDistance: Double {
        chartData8.reduce(0, { $0 + $1.distance })
    }
    
    var StringupdateTotalDistance: String {
        return String(updateTotalDistance)
    }


   // let totalDistance = chartData8.reduce(0, { $0 + $1.distance })
    var averageResponseTime: Double {
        guard !chartData8.isEmpty else { return 0 }
        let totalResponseTime = chartData8.reduce(0) { $0 + $1.distance }
        return Double(totalResponseTime) / Double(chartData8.count)
    }
    
   // var averageSales: Double {
   //     guard !chartData7.isEmpty else { return 0 }

   //     _ = chartData7.reduce(0) { $0 + $1.sales }
   //     let totalCounts = chartData7.reduce(0) { $0 + $1.UpdateCount }
   //     let pingCounts = chartData7.reduce(0) { $0 + $1.ping_count }
        
        //print("Double(100 / ping_counts \(pingCounts) / totalCounts \(totalCounts)*100) * 5)")
   //     return Double(100 / ((Double(pingCounts) / Double(totalCounts)*100)))*5
        
        //return totalSales / Double(chartData7.count)
    //}
    
    //var minutesPerICloudUpdate: Double {
    //        let minutesPerICloudUpdate = (100 / averageSales) * 5
    //        return minutesPerICloudUpdate.isNaN ? 0 : minutesPerICloudUpdate
    //    }
    
    //var dateDifference: Int? {
    //    guard let firstDate = firstElementName, let lastDate = lastElementName else {
    //        return nil
    //    }

    //    let dateFormatter = DateFormatter()
    //    dateFormatter.dateFormat = "yyyyMMdd"

    //    if let startDate = dateFormatter.date(from: firstDate), let endDate = dateFormatter.date(from: lastDate) {
    //        let calendar = Calendar.current
    //        let components = calendar.dateComponents([.day], from: startDate, to: endDate)
    //        return components.day.map { $0 + 1 }
    //    }

    //    return nil
   // }
    
    
    var firstElementName: String? {
        chartData8.first?.date
    }

    var lastElementName: String? {
        chartData8.last?.date
    }
    
    var body: some View {
        VStack {
            Text("Tag: \(description)")
                .bold()
                .foregroundColor(Color.green)
                .font(.custom("Arial", size: 22))
            let emptyComment = Comments(description: "", battery_status: "", marker: "", distance: "", address: "", serialNumber: "\(serialNumber)", link: "", distance_from_home: "", ago: "")
            
            NavigationLink(destination: CommentDetailView(comment: emptyComment, server: server, username: username, distance: StringupdateTotalDistance, marker: "", ago: "", token: "", date: date), isActive: $navigateToDetailView) {
                EmptyView()
            }
            .hidden()

                Button("Generate Map") {
                    navigateToDetailView = true
                }
                .buttonStyle(.bordered)
                .controlSize(.large)
                .foregroundColor(.white)
                .background(Color.blue)
                .cornerRadius(10)
                .padding()

            
            
            Text("For Date: \(date)")
                .bold()
                .foregroundColor(Color.blue)
                .font(.custom("Arial", size: 18))
            Text("Total Distance is \(String(format: "%.1f", updateTotalDistance)) km")
                .bold()
                .foregroundColor(Color.brown)
                .font(.custom("Arial", size: 18))
            //Text(" Date Range: \(firstElementName ?? "") -  \(lastElementName ?? "")")
            //Text(" Date Range: \(firstElementName ?? "") - \(lastElementName ?? "") (\(dateDifference ?? 0) days)")
             //   .bold()
             //   .foregroundColor(Color.blue)
             //   .font(.custom("Arial", size: 16))
            HStack {
            }

            // Use a ScrollView to allow scrolling if there are many data points
            //ScrollView {
                Chart(chartData8, id: \.date) { element in
                    // we use this one only
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.seq),
                            y: .value("Distance", element.distance)
                        )
                    }
                }
                // this is the chart title
                .frame(height: viewModel.graphType.isProgressChart ? 150 : 150)
                .padding()
                .chartLegend(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
            //}
            //Text("Average distance: \(String(format: "%.1f", averageResponseTime)) km")
            //    .font(.custom("Arial", size: 16))
            //    .foregroundColor(Color.red) // You can customize the color
            List {
                ForEach(chartData8, id: \.date) { data in
                        VStack(alignment: .leading) {
                            Text("\(data.date) - \(String(format: "%.1f", data.distance)) km")
                                .foregroundColor(.brown)
                                .bold()
                                .font(.custom("Arial", size: 16))
                            
                        }
                    }
                }
        }
        .padding()
        .onAppear {
            fetchData()
        }
    }
    

    
    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/chartDayDistance_api?serialNumber=\(serialNumber)&username=\(username)&date=\(date)") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData8].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData8 = decodedData
                        print("chartData8=\(chartData8)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}


