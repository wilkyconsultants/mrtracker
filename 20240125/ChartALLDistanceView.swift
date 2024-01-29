//
//  ChartALLTDistanceView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-26.
//

import SwiftUI
import Charts

//
// Chart example
// https://lyvennithasasikumar.medium.com/ios-17-updates-enhancing-swift-charts-dca213155187

class ChartsViewModel6: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData6: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let date: String
    let description: String //name
    let serialNumber: String
    let distance: Double  //sales
}

struct GraphType6: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartALLDistanceView: View {
    let server: String
    let username: String
    let serialNumber: String
    let description: String
    
    private let pdays = Array(1...365)
    @State private var days = 7  // default is 7 days of battery % data
    
    @StateObject var viewModel = ChartsViewModel6()
    @State private var chartData6: [ChartData6] = []

    @State private var searchText = ""

    var filteredChartData: [ChartData6] {
        if searchText.isEmpty {
            return chartData6
        } else {
            return chartData6.filter { data in
                return data.description.localizedCaseInsensitiveContains(searchText)
            }
        }
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
        chartData6.first?.serialNumber
    }

    var lastElementName: String? {
        chartData6.last?.serialNumber
    }
    
    var body: some View {
        VStack {
            //Text("\(description)")
            //    .bold()
            //    .foregroundColor(Color.green)
            //    .font(.custom("Arial", size: 22))
            //Text(" Date Range: \(firstElementName ?? "") -  \(lastElementName ?? "")")
            //Text(" Date Range: \(firstElementName ?? "") - \(lastElementName ?? "") (\(dateDifference ?? 0) days)")
               // .bold()
               // .foregroundColor(Color.blue)
               // .font(.custom("Arial", size: 16))
            //HStack {
              //  Picker("", selection: $days) {
              //      ForEach(pdays, id: \.self) { pday in
               //         Text("\(pday) days")
              //      }
              //  }
              //  .pickerStyle(MenuPickerStyle())
              //  .font(.custom("Arial", size: 22))
              //  .onChange(of: days, initial: true) { oldCount, newCount in
              //      fetchData()
              //  }
              //  Text("Selected")
            //}

            // Use a ScrollView to allow scrolling if there are many data points
           // ScrollView {
                Chart(chartData6, id: \.serialNumber) { element in


                    // we use this one only
                    if viewModel.graphType.isBarChart {
                        BarMark(
                            x: .value("Date", element.serialNumber),
                            y: .value("Distance(km)", element.distance)
                        )
                    }
                }
                // this is the chart title
                .chartXAxisLabel(position: .bottom, alignment: .center, spacing: 4) {
                    Text("Distance by Tag for today")
                        .font(.custom("Arial", size: 16))
                        .foregroundColor(Color.brown)
               //     Text("")
               //         .font(.custom("Arial", size: 16))
               //         .foregroundColor(Color.brown)
                }
                .frame(height: viewModel.graphType.isProgressChart ? 150 : 150)
                //.padding()
                //.chartLegend(.hidden)

                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                .chartXAxis(.hidden)
                .chartYAxis {
                    AxisMarks(position: .leading)
                }
                //.chartYScale(domain: 0...100)
                
            }
            //Text("Average Tag Perf %: \(String(format: "%.0f", averageSales))")
            //    .font(.custom("Arial", size: 16))
            //    .foregroundColor(Color.red) // You can customize the color
            //Text("Tag Response: \(String(format: "%.1f", averageSales)) Min/update")
            //    .font(.custom("Arial", size: 18))
            //    .foregroundColor(Color.green) // You can customize the color
            //Text("Guidelines: 5 min/update is perfect")
            //    .font(.custom("Arial", size: 14))
            //Text("< 20 min/update is ideal")
            //    .font(.custom("Arial", size: 14))
            //    .foregroundColor(Color.brown) // You can customize the color
           // HStack {
            //if let chartData4.data = chartData5.data {
            SearchBar(text: $searchText)
            List {
                ForEach(filteredChartData, id: \.serialNumber) { data in
                    NavigationLink(destination: ChartDistanceView(server: server,username: username,serialNumber: data.serialNumber, description: data.description)) {
                        VStack(alignment: .leading) {
                            Text("\(String(format: "%.1f", data.distance))km \(data.description)")
                                .foregroundColor(.blue)
                        }
                    }
                }
            //}
            //}
            //}
            //.padding(.bottom, 10)
            //Text("Avg Minutes per iCloud Update: \(String(format: "%.0f", minutesPerICloudUpdate))")
            //    .font(.custom("Arial", size: 16))
            //    .foregroundColor(Color.blue) // You can customize the color
            

        }
        .padding()
        .onAppear {
            fetchData()
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/chartAllDistance_api?username=\(username)&filter=''") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData6].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData6 = decodedData
                        print("chartData5=\(chartData6)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}


