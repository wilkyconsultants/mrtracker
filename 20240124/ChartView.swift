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
    
    
    //@State private var firstElementName: String
    //@State private var lastElementName: String
    
    @StateObject var viewModel = ChartsViewModel()
    @State private var chartData: [ChartData] = []

    var firstElementName: String? {
        chartData.first?.name
    }

    var lastElementName: String? {
        chartData.last?.name
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
            Text(" Date Range: \(firstElementName ?? "") -  \(lastElementName ?? "")")
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

            HStack {
                VStack {
                   // Toggle(isOn: $viewModel.graphType.isBarChart) {
                   //     Text("Bars")
                   //         .foregroundColor(Color.black)
                   // }
                   // .onChange(of: viewModel.graphType.isBarChart) { newValue in
                   //     if newValue {
                   //         viewModel.graphType.isPieChart = false
                   //         viewModel.graphType.isLineChart = false
                   //         viewModel.graphType.isProgressChart = false
                   //     }
                   // }
                    //Toggle(isOn: $viewModel.graphType.isPieChart) {
                    //    Text("Pie")
                    //        .foregroundColor(Color.black)
                    //}
                    //.onChange(of: viewModel.graphType.isPieChart) { newValue in
                    //    if newValue {
                    //        viewModel.graphType.isBarChart = false
                    //        viewModel.graphType.isLineChart = false
                    //        viewModel.graphType.isProgressChart = false
                    //    }
                   // }
                }
                VStack {
                    //Toggle(isOn: $viewModel.graphType.isProgressChart) {
                     //   Text("Progress")
                     //       .foregroundColor(Color.black)
                   // }
                   // .onChange(of: viewModel.graphType.isProgressChart) { newValue in
                   //     if newValue {
                     //       viewModel.graphType.isBarChart = false
                       //     viewModel.graphType.isLineChart = false
                        //    viewModel.graphType.isPieChart = false
                      //  }
                   // }
                    //Toggle(isOn: $viewModel.graphType.isLineChart) {
                    //    Text("Line")
                    //        .foregroundColor(Color.black)
                    //        //.modifier(RotatedXAxisLabels())
                   // }
                    //.onChange(of: viewModel.graphType.isLineChart) { newValue in
                     //   if newValue {
                     //       viewModel.graphType.isBarChart = false
                      //      viewModel.graphType.isPieChart = false
                      //      viewModel.graphType.isProgressChart = false
                      //  }
                    //}
                }
            }
            .padding()

            // Use a ScrollView to allow scrolling if there are many data points
            ScrollView {
                Chart(chartData, id: \.name) { element in


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
                            y: .value("Distance", element.sales)
                            //x: .value("Distance", element.sales),
                            //y: .value("Date", element.name)
                        )
                        // this sets color in each bar
                        .foregroundStyle(by: .value("Type", element.name))
                        
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

                            x: .value("Distance", element.sales),
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
                    Text("km / day - last \(days) days")
                        .font(.custom("Arial", size: 24))
                        .foregroundColor(Color.black)
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
            }
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
struct RotatedXAxisLabels: ViewModifier {
    func body(content: Content) -> some View {
        content
            .rotationEffect(Angle(degrees: -45))
    }
}
