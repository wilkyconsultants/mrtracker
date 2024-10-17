//
//  ChartALLTagPerfView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-26.
//


import SwiftUI
import Charts
import Combine

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187
class ChartsViewModel4: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData4: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let date: String
    let description: String //name
    let Response_time: Double  //sales was perfMin
    //let UpdateCount: Double
    //let ping_count: Double
    let serialNumber: String
}

struct GraphType4: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartALLTagPerfView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    
    private let pdays = Array(1...365)
    @State private var days = 7  // default is 7 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel4()
    @State private var chartData4: [ChartData4] = []
    
    @State private var isFiltering: Bool = true
    @State private var isRefresh: Bool = false
    
    @State private var searchText: String = ""

    var filteredChartData: [ChartData4] {
        if searchText.isEmpty {
            return chartData4
        } else {
            return chartData4.filter { data in
                data.description.localizedCaseInsensitiveContains(searchText)
            }
        }
    }
    var averageResponseTime: Double {
        guard !chartData4.isEmpty else { return 0 }
        let totalResponseTime = chartData4.reduce(0) { $0 + $1.Response_time }
        return totalResponseTime / Double(chartData4.count)
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
        chartData4.first?.serialNumber
    }

    var lastElementName: String? {
        chartData4.last?.serialNumber
    }
    
    var body: some View {
        VStack {
                Chart(chartData4, id: \.serialNumber) { element in
                    // we use this one only
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.serialNumber),
                            y: .value("Tag Perf In Minutes", element.Response_time)
                        )
                    }
                }
                .padding(EdgeInsets(top: 10, leading: 10, bottom: 10, trailing: 10)) // Adjust values as needed
                // this is the chart title
                .chartXAxisLabel(position: .bottom, alignment: .center, spacing: 4) {

                }
                .frame(height: viewModel.graphType.isProgressChart ? 150 : 150)

                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                .chartXAxis(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                //.chartYScale(domain: 0...100)
                
            }

            Text("Avg Response Time: \(String(format: "%.1f", averageResponseTime)) mins (/\(chartData4.count))")
                .font(.custom("Arial", size: 20))
                .foregroundColor(Color.brown)
        HStack {
            Spacer()
            Toggle("Filter on Healthy Items Only", isOn: $isFiltering)
        }
        .padding(.horizontal, 20) 
        HStack {
            SearchBar(text: $searchText)
            Button("Cancel") {
                hideKeyboard()
            }
        }
        .padding(.horizontal, 20) 
           // SearchBar(text: $searchText)
            List {
                ForEach(filteredChartData, id: \.serialNumber) { data in
                    NavigationLink(destination: ChartTagPerfView(server: server,username: username,serialNumber: data.serialNumber, description: data.description)) {
                        VStack(alignment: .leading) {
                            Text("\(String(format: "%.1f", data.Response_time)) min \(data.description)")
                                .foregroundColor(.blue)
                        }
                    }
                }
        }
        .padding()
        .onAppear {
            fetchData()
        }
        
        .onReceive(Just(isFiltering)) { filtering in
            if filtering {
                if isRefresh {
                    fetchData()
                }
            } else {
                if !isRefresh {
                    fetchData()
                }
            }
        }
    }
    func hideKeyboard() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }

    func fetchData() {
        
        let filter = isFiltering ? "Items" : "All"
        guard let url = URL(string: "https://\(server)/theme/chartALLTagPerf_api?username=\(username)&filter=\(filter)") else {
            return
        }
        
        isRefresh.toggle()
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData4].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData4 = decodedData
                        // print("chartData4=\(chartData4)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}
