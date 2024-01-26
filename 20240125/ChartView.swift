//
//  ChartView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187
class ChartsViewModel: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let name: String
    let sales: Double
}

struct GraphType: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    
    private let pdays = Array(1...365)
    @State private var days = 30  // default is 30 days of distance data
    
    @StateObject var viewModel = ChartsViewModel()
    @State private var chartData: [ChartData] = []

    var totalSalesPerDay: Double {
        guard let dateDifference = dateDifference, dateDifference > 0 else {
            return 0
        }

        return totalSales / Double(dateDifference)
    }
    
    var totalSales: Double {
        chartData.reduce(0) { $0 + $1.sales }
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
        chartData.first?.name
    }

    var lastElementName: String? {
        chartData.last?.name
    }
    
    var body: some View {
        VStack {
            Text("\(description)")
                .bold()
                .foregroundColor(Color.green)
                .font(.custom("Arial", size: 22))
            Text(" Date Range: \(firstElementName ?? "") - \(lastElementName ?? "") (\(dateDifference ?? 0) days)")
                //.font(.title3)
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
                Chart(chartData, id: \.name) { element in
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.name),
                            y: .value("Distance", element.sales)
                        )
                    }
                }
                // this is the chart title
                .chartXAxisLabel(position: .bottom, alignment: .center, spacing: 26) {
                    Text("km / day - last \(dateDifference ?? 0) days")
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
            }
            Text("Total Distance: \(String(format: "%.0f", totalSales)) km")
                .font(.custom("Arial", size: 16))
                .foregroundColor(Color.red)
            Text("Average Distance per Day: \(String(format: "%.1f", totalSalesPerDay)) km")
                .font(.custom("Arial", size: 16))
                .foregroundColor(Color.brown)
        }
        .padding()
        .onAppear {
            fetchData()
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/chart_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData = decodedData
                        print("chartData=\(chartData)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}


