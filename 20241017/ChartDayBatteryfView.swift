//
//  ChartDayBatteryfView.swift
//  MRTRACKER
//
//  Created by Robert A Wilkinson on 2024-01-30.
//
//
//  work in progress, need to clone api chartDayDistance_api to chartDayBattery_api in django
//


import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187

class ChartsViewModel9: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

//struct ChartData9: Codable, Identifiable {
//    var id: UUID {
//        return UUID()
//    }
//    let date: String   // name
//    let distance: Double
//    let serialNumber: String
//    //let response: Int       // sales
//    let seq: String
//}

struct ChartData9: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let name: String   // name
    let sales: Double //distance
    let serialNumber: String
}

struct GraphType9: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartDayBatteryView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    let date: String
    
    private let pdays = Array(1...365)
    @State private var days = 7  // default is 7 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel9()
    @State private var chartData9: [ChartData9] = []
    
    @State private var totalDistance: Double = 0
    
    var updateTotalDistance: Double {
        chartData9.reduce(0, { $0 + $1.sales })
    }


   // let totalDistance = chartData9.reduce(0, { $0 + $1.distance })
    var averageResponseTime: Double {
        guard !chartData9.isEmpty else { return 0 }
        let totalResponseTime = chartData9.reduce(0) { $0 + $1.sales }
        return Double(totalResponseTime) / Double(chartData9.count)
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
        chartData9.first?.name
    }

    var lastElementName: String? {
        chartData9.last?.name
    }
    
    var body: some View {
        VStack {
            Text("\(description)")
                .bold()
                .foregroundColor(Color.green)
                .font(.custom("Arial", size: 22))
            Text("For Date: \(date)")
                .bold()
                .foregroundColor(Color.blue)
                .font(.custom("Arial", size: 18))
            Text("Battery %")
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
                Chart(chartData9, id: \.name) { element in
                    // we use this one only
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.name),
                            y: .value("Battery%", element.sales)
                        )
                    }
                }
                // this is the chart title
                .frame(height: viewModel.graphType.isProgressChart ? 150 : 150)
                .padding()
                .chartYScale(domain: 0...100)
                .chartLegend(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
            //}
            //Text("Average distance: \(String(format: "%.1f", averageResponseTime)) km")
            //    .font(.custom("Arial", size: 16))
            //    .foregroundColor(Color.red) // You can customize the color
            List {
                ForEach(chartData9, id: \.name) { data in
                        VStack(alignment: .leading) {
                            Text("\(data.name) - \(String(format: "%.0f", data.sales))% battery")
                                .foregroundColor(.blue)
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
        guard let url = URL(string: "https://\(server)/theme/chartDayBattery_api?serialNumber=\(serialNumber)&username=\(username)&date=\(date)") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData9].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData9 = decodedData
                        // print("chartData9=\(chartData9)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}

