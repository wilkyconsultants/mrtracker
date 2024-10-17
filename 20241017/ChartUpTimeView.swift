//
//  ChartUpTime.swift
//  MRTRACKER
//
//  Created by Robert A Wilkinson on 2024-02-07.
import SwiftUI
import Charts

class ChartsViewModel10: ObservableObject {
    @Published var graphType: GraphType = GraphType()
}

struct ChartData10: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let date: String
    let hour: String   // name
    let pct_up_time: Int //sales
}

struct GraphType10: Equatable {
    var isBarChart: Bool = true
    var isProgressChart: Bool = false
    var isPieChart: Bool = false
    var isLineChart: Bool = false
}

struct ChartUpTimeView: View {
    let server: String
    
    @StateObject var viewModel = ChartsViewModel10()
    @State private var chartData10: [ChartData10] = []
    @State private var averageUpTime: Double = 0.0
    @State private var firstDate: String = ""
    @State private var lastDate: String = ""
    
    var body: some View {
        VStack {
            Text("Back-End Server Up-Time % By Hour")
                .bold()
                .foregroundColor(Color.brown)
                .font(.custom("Arial", size: 18))
            Text("Date Range: \(firstDate) - \(lastDate)")
                .font(.custom("Arial", size: 16))
                .foregroundColor(.gray)
            Text("24 hr Average Up-Time: \(String(format: "%.2f", averageUpTime))%")

            Spacer()

            Chart(chartData10, id: \.hour) { element in
                if viewModel.graphType.isBarChart {
                    BarMark(
                        x: .value("Date", "\(element.date) \(element.hour)"),
                        y: .value("Up-Time%", element.pct_up_time)
                    )
                }
            }
            // this is the chart title
            .frame(height: viewModel.graphType.isProgressChart ? 200 : 200)
            .padding()
            .chartYScale(domain: 0...100)

            Spacer()
            List {
                ForEach(chartData10, id: \.id) { data in
                    VStack(alignment: .leading) {
                        Text("\(data.date)-\(data.hour):00 - \(data.pct_up_time)%")
                            .foregroundColor(data.pct_up_time == 100 ? .green : .red)
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

    func calculateAverageUpTime() {
        let relevantData = chartData10.prefix(24) // Get the last 24 hours of data
        let totalUpTime = relevantData.reduce(0.0) { $0 + Double($1.pct_up_time) }
        averageUpTime = totalUpTime / Double(relevantData.count)
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/UpTime_api") else {
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let data = data {
                do {
                    let decodedData = try JSONDecoder().decode([ChartData10].self, from: data)
                    DispatchQueue.main.async {
                        self.chartData10 = decodedData
                        if let first = chartData10.first?.date, let last = chartData10.last?.date {
                            self.firstDate = first
                            self.lastDate = last
                        }
                        calculateAverageUpTime()
                    }
                } catch {
                    print("Error decoding data: \(error.localizedDescription)")
                }
            }
        }.resume()
    }
}
