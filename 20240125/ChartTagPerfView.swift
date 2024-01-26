//
//  ChartTagPerfView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-25.
//


import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187
class ChartsViewModel3: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData3: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let name: String
    let sales: Double
}

struct GraphType3: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartTagPerfView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    
    private let pdays = Array(1...365)
    @State private var days = 365  // default is 365 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel3()
    @State private var chartData3: [ChartData3] = []

    var averageSales: Double {
        guard !chartData3.isEmpty else { return 0 }

        let totalSales = chartData3.reduce(0) { $0 + $1.sales }
        return totalSales / Double(chartData3.count)
    }
    
    var dateDifference: Int? {
        guard let firstDate = firstElementName, let lastDate = lastElementName else {
            return nil
        }

        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyyMMdd"

        if let startDate = dateFormatter.date(from: firstDate), let endDate = dateFormatter.date(from: lastDate) {
            let calendar = Calendar.current
            let components = calendar.dateComponents([.day], from: startDate, to: endDate)
            return components.day.map { $0 + 1 }
        }

        return nil
    }
    
    
    var firstElementName: String? {
        chartData3.first?.name
    }

    var lastElementName: String? {
        chartData3.last?.name
    }
    
    var body: some View {
        VStack {
            Text("\(description)")
                .bold()
                .foregroundColor(Color.green)
                .font(.custom("Arial", size: 22))
            //Text(" Date Range: \(firstElementName ?? "") -  \(lastElementName ?? "")")
            Text(" Date Range: \(firstElementName ?? "") - \(lastElementName ?? "") (\(dateDifference ?? 0) days)")
                .bold()
                .foregroundColor(Color.blue)
                .font(.custom("Arial", size: 16))
            HStack {
                Picker("", selection: $days) {
                    ForEach(pdays, id: \.self) { pday in
                        Text("\(pday) days")
                    }
                }
                .pickerStyle(MenuPickerStyle())
                .font(.custom("Arial", size: 22))
                .onChange(of: days, initial: true) { oldCount, newCount in
                    fetchData()
                }
                Text("Selected")
            }

            // Use a ScrollView to allow scrolling if there are many data points
            ScrollView {
                Chart(chartData3, id: \.name) { element in


                    if viewModel.graphType.isPieChart {
                        SectorMark(
                            angle: .value("Distance", element.sales),
                            innerRadius: .ratio(0.618), angularInset: 1.5
                        )
                        .cornerRadius (5)
                        .foregroundStyle(by: .value ("Date", element.name))
                    }
                    // we use this one only
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.name),
                            //y: .value("Tag Perf %", element.sales)
                            y: .value("Tag Perf %", element.sales)
                        )
                    }

                    if viewModel.graphType.isProgressChart {
                        BarMark(
                            x: .value("Distance", element.sales),
                            stacking: .normalized
                        )
                        .foregroundStyle(by: .value("Date", element.name))
                        
                    }

                    if viewModel.graphType.isLineChart {

                        LineMark(
                        //    x: .value("Date", element.name),
                        //    y: .value("Distance", element.sales)

                            x: .value("Battery%", element.sales),
                            y: .value("Date", element.name)
                        )
                        
                        PointMark(
                            x: .value("Date", element.name),
                            y: .value("Distance", element.sales)
                        )
                    }
                    
                }
                // this is the chart title
                .chartXAxisLabel(position: .bottom, alignment: .center, spacing: 26) {
                    //Text("Tag Perf% - last \(days) days (\(dateDifference ?? 0)")
                    Text("Tag Perf% - last \(dateDifference ?? 0) days")
                        .font(.custom("Arial", size: 16))
                        .foregroundColor(Color.brown)
                }
                .frame(height: viewModel.graphType.isProgressChart ? 500 : 380)
                .padding()
                .chartLegend(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                .chartXAxis(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                .chartYScale(domain: 0...100)
            }
            Text("Average Tag Perf %: \(String(format: "%.0f", averageSales))")
                .font(.custom("Arial", size: 16))
                .foregroundColor(Color.red) // You can customize the color
        }
        .padding()
        .onAppear {
            fetchData()
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/chartTagPerf_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData3].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData3 = decodedData
                        print("chartData3=\(chartData3)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}
