//
//  ChartBatteryView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-25.
//

import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187
class ChartsViewModel2: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData2: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let name: String
    let sales: Double
}

struct GraphType2: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartBatteryView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    
    private let pdays = Array(1...365)
    @State private var days = 365  // default is 365 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel2()
    @State private var chartData2: [ChartData2] = []

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
        chartData2.first?.name
    }

    var lastElementName: String? {
        chartData2.last?.name
    }
    
    var body: some View {
        VStack {
            // can't use firstElement or lastElement here, get error??
            //Text("Daily Distance(km) : \(serialNumber):\(description)")
            Text("\(description)")
                //.font(.title3)
                .bold()
                .foregroundColor(Color.green)
                .font(.custom("Arial", size: 22))
            //Text(" Date Range: \(firstElementName ?? "") -  \(lastElementName ?? "")")
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
                Chart(chartData2, id: \.name) { element in


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
                            y: .value("Battery %", element.sales)
                        )
                        // this sets color in each bar
                       // .foregroundStyle(by: .value("Type", element.name))
                        
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
                    Text("Battery% - last \(dateDifference ?? 0) days")
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
                //
                // this is deprecated in ios 17 but when I comment it out it doesn't seem to make any difference
                // so I will just remove it
                //
                //.AxisValueLabel(
                //.chartBackground { chartProxy in
                //    GeometryReader { geometry in
                //        let frame = geometry[chartProxy.plotAreaFrame]
                //        VStack {
                //            //Text("Distance by Day")
                //            Text("")
                //                .font (.callout)
                //                .foregroundStyle(.secondary)
                //            Text("")
                //                .font(.title2.bold ())
                //                .foregroundColor (.primary)
                //        }
                 //       .position(x: frame.midX, y: frame.midY)
                  //  }
                //}
                //.padding()
                .chartYScale(domain: 0...100)
            }
        }
        .padding()
        .onAppear {
            fetchData()
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/chart_Battery_api?serialNumber=\(serialNumber)&username=\(username)&days=\(days)") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData2].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData2 = decodedData
                        print("chartData2=\(chartData2)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}

