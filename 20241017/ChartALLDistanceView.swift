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
    
    //@State private var SelectedDate = "20240127"
    @State private var selectedDate = Date()

    var filteredChartData: [ChartData6] {
        if searchText.isEmpty {
            return chartData6
        } else {
            return chartData6.filter { data in
                return data.description.localizedCaseInsensitiveContains(searchText)
            }
        }
    }
    
    var nonZeroDistanceCount: Int {
        return filteredChartData.filter { $0.distance > 0 }.count
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

        //}
            
            TextField("Selected Date", text: Binding(
                get: { "Distance Chart for date: " + DateFormatter.yyyyMMdd.string(from: selectedDate) },
                set: {
                    if let date = DateFormatter.yyyyMMdd.date(from: $0) {
                        selectedDate = date
                        // print("selectedDate=\(selectedDate)")
                    }
                }
            ))
            .multilineTextAlignment(.center)
            .padding()
            .textFieldStyle(RoundedBorderTextFieldStyle())
            .disabled(true)
            
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

                   // Text("Distance by Tag for \(formattedDate)")
                    Text("Distance by Device: (\(nonZeroDistanceCount)/\(chartData6.count))")
                        .font(.custom("Arial", size: 16))
                        .foregroundColor(Color.brown)
                }
                .frame(height: viewModel.graphType.isProgressChart ? 125 : 125)
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
        
            DatePicker("Select a Date", selection: $selectedDate, displayedComponents: .date)
            .datePickerStyle(.compact)
            .padding()
        
        HStack {
            SearchBar(text: $searchText)
            Button("Cancel") {
                hideKeyboard()
            }
        }
        .padding(.horizontal, 20) 
            List {
                ForEach(filteredChartData, id: \.serialNumber) { data in
               //     NavigationLink(destination: ChartDistanceView(server: server,username: username,serialNumber: data.serialNumber, description: data.description, newdays: calculateDaysDifference)) {
                    NavigationLink(destination: ChartDistanceView(server: server,username: username,serialNumber: data.serialNumber, description: data.description)) {
                        VStack(alignment: .leading) {
                            Text("\(String(format: "%.1f", data.distance))km \(data.description)")
                                .foregroundColor(.blue)
                        }
                    }
                }
        }
        .padding()
        .onAppear {
            fetchData()
        }
        .onChange(of: selectedDate) {
            fetchData()
        }
    }
    func hideKeyboard() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
    var formattedDate: String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyyMMdd"
        return dateFormatter.string(from: selectedDate)
    }
    
    // calculate how many days the selectedDate is from todays date and pass 30+ that # to the ChartDistanceView
    func calculateDaysDifference(selectedDate: Date) -> Int? {
        let calendar = Calendar.current
        let currentDate = Date()
        let dateDifference = calendar.dateComponents([.day], from: selectedDate, to: currentDate).day

        if let daysDifference = dateDifference {
            return 30 - daysDifference
        } else {
            return nil
        }
    }


    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/chartAllDistance_api?username=\(username)&date=\(formattedDate)") else {
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
                        //print("chartData5=\(chartData6)")
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}
extension DateFormatter {
    static let yyyyMMdd: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyyMMdd"
        return formatter
    }()
}
