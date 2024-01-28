//
//  ChartDayTagPerfView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-27.
//


import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187

class ChartsViewModel7: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData7: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let date: String   // name
    let response: Int       // sales
    let serialNumber: String
    let seq: String
}

struct GraphType7: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartDayTagPerfView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    let date: String
    
    private let pdays = Array(1...365)
    @State private var days = 7  // default is 7 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel7()
    @State private var chartData7: [ChartData7] = []

    var averageResponseTime: Double {
        guard !chartData7.isEmpty else { return 0 }
        let totalResponseTime = chartData7.reduce(0) { $0 + $1.response }
        return Double(totalResponseTime) / Double(chartData7.count)
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
        chartData7.first?.date
    }

    var lastElementName: String? {
        chartData7.last?.date
    }
    
    var body: some View {
        VStack {
            Text("Tag: \(description)")
                .bold()
                .foregroundColor(Color.green)
                .font(.custom("Arial", size: 18))
            Text("For Date: \(date)")
                .bold()
                .foregroundColor(Color.blue)
                .font(.custom("Arial", size: 16))
            Text("Tag Response in minutes")
                .bold()
                .foregroundColor(Color.brown)
                .font(.custom("Arial", size: 16))
            //Text(" Date Range: \(firstElementName ?? "") -  \(lastElementName ?? "")")
            //Text(" Date Range: \(firstElementName ?? "") - \(lastElementName ?? "") (\(dateDifference ?? 0) days)")
             //   .bold()
             //   .foregroundColor(Color.blue)
             //   .font(.custom("Arial", size: 16))
            HStack {
               // Picker("", selection: $days) {
               //     ForEach(pdays, id: \.self) { pday in
               //         Text("\(pday) days")
               //     }
               // }
               // .pickerStyle(MenuPickerStyle())
               // .font(.custom("Arial", size: 22))
               // .onChange(of: days, initial: true) { oldCount, newCount in
               //     fetchData()
               // }
               // Text("Selected")
            }

            // Use a ScrollView to allow scrolling if there are many data points
            ScrollView {
                Chart(chartData7, id: \.date) { element in
                    // we use this one only
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.seq),
                            y: .value("Tag Perf Minutes", element.response)
                        )
                    }
                }
                // this is the chart title
                .frame(height: viewModel.graphType.isProgressChart ? 200 : 280)
                .padding()
                .chartLegend(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                //.chartXAxis(.hidden)
                //.chartYAxis {
                //    AxisMarks(position: .leading)
                //}
                //.chartYScale(domain: 0...100)
            }
            Text("Average Response: \(String(format: "%.1f", averageResponseTime)) minutes")
                .font(.custom("Arial", size: 16))
                .foregroundColor(Color.red) // You can customize the color
            List {
                ForEach(chartData7, id: \.date) { data in

                        VStack(alignment: .leading) {
                            Text("\(data.date) - \(data.response) mins")
                                .foregroundColor(.blue)
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
        guard let url = URL(string: "https://\(server)/theme/chartDayTagPerf_api?serialNumber=\(serialNumber)&username=\(username)&date=\(date)") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData7].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData7 = decodedData
                        print("chartData7=\(chartData7)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}
