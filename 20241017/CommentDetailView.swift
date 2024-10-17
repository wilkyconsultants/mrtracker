//
//  CommentDetailView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//
// This view generates a road map of the locations the tag went for a date or range of dates
//

import SwiftUI
import MapKit

struct CommentDetailView: View {
    @State private var locations: [Locations] = []
    
    let comment: Comments
    let server: String
    let username: String
    let distance: String
    let marker: String
    let ago: String
    let token: String
    let date: String
    
    // 20240515 - make the # days to map as saved for next request
    //@State private var selectedDate = Date()
    @AppStorage("selectedDay") var selectedDay: Int = 3
    
    @State private var route: MKRoute?
    @State private var travelTime: String?
    @State private var home_lat: Double?
    @State private var home_long: Double?
    
 
    @State private var selectedDate: Date = Date()
    @State private var isDatePickerVisible = false
    
    @State private var fetchDataIsComplete = true
    
    //@State private var selectedDay = 3 // changed from 1
    @State private var isDropdownVisible = false
    private let days = Array(1...365)
    
    @State private var isLoading = false

    @State private var isChecked: Bool = true // set the marker on if checked, default is on
    
    @State private var goButtonClicked = false

    private let gradient = LinearGradient(colors: [.red, .orange], startPoint: .leading, endPoint: .trailing)
    private let stroke = StrokeStyle(lineWidth: 5, lineCap: .round, lineJoin: .round, dash: [8, 8])
    
    //@State private var region: MKCoordinateRegion?
    
    var home: CLLocationCoordinate2D { CLLocationCoordinate2D(latitude: 43.8382, longitude: -79.3001) }

    var body: some View {
        var currentDate: String {
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "yyyy-MM-dd"
            return dateFormatter.string(from: Date())
        }
        VStack {
            HStack {
                //Text("As of: \(formattedCurrentDate)")
                Button("Go") {
                    fetchData(with: selectedDate, days: selectedDay)
                    if isDatePickerVisible {
                        isDatePickerVisible.toggle()
                    }
                    goButtonClicked = true
                }
                //.padding()
                .background(fetchDataIsComplete ? .green : .yellow)
                .foregroundColor(.black)
                .cornerRadius(8)
                .padding(.horizontal, 20)
                .frame(height: 20)
                .font(.system(size: 35))
                Picker("", selection: $selectedDay) {
                    ForEach(days, id: \.self) { day in
                        Text("\(day) days")
                    }
                }
                .pickerStyle(MenuPickerStyle())
                Button("◀") {
                    selectedDate = Calendar.current.date(byAdding: .day, value: -1, to: selectedDate) ?? selectedDate
                    fetchData(with: selectedDate, days: selectedDay)
                    goButtonClicked = true
                }
                .padding(8)
                .background(Color.teal

                )
                .foregroundColor(.white)
                .cornerRadius(8)
                .font(.system(size: 18))
                Text("\(formattedSelectedDate)")
                    .bold()
                    .foregroundColor(Color.blue)
                if !isSelectedDateToday {
                    Button("▶") {
                        selectedDate = Calendar.current.date(byAdding: .day, value: 1, to: selectedDate) ?? selectedDate
                        fetchData(with: selectedDate,days: selectedDay)
                        goButtonClicked = true
                    }
                    .padding(8)
                    .background(Color.teal)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                    .font(.system(size: 18))
                    //.disabled(isSelectedDateToday)
                }
            }
            if isLoading {
                ProgressView("Fetching Data...")
                    .progressViewStyle(CircularProgressViewStyle(tint: .blue))
                    .scaleEffect(1.5, anchor: .center)
                    .bold()
                    .foregroundColor(.red)
            }
                if let firstLocation = locations.first {
                    Text("📍\(firstLocation.address)")
                }
            if !goButtonClicked  && date != "-" {
                Text("Map Date: \(date)")
            }
                // the marker is only value for current data ie. todays date
                //if currentDate == formattedSelectedDate {
                    
                       // Text("\(marker)\(ago): Travelled \(distance)km to home")
                    
                //}
            //}
            //Text("\(currentDate) vs \(formattedSelectedDate)")
            HStack {

                Toggle(isOn: $isChecked) {
                    Text("Marker")
                }
                .toggleStyle(CheckboxToggleStyle())
                
                Button("Toggle Date Select") {
                    isDatePickerVisible.toggle()
                }
                //.padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
                .padding(.horizontal, 20)
                .frame(height: 18)
                
                Text(" (Pts:\(locations.count)/\(ago))")
                //Button("Fetch Data") {
                //    fetchData(with: selectedDate, days: selectedDay)
                //    if isDatePickerVisible {
                //        isDatePickerVisible.toggle()
                //    }
               // }
                //.padding()
                //.background(Color.blue)
                //.foregroundColor(.white)
                //.cornerRadius(8)
                //.padding(.horizontal, 20)
                //.frame(height: 10)
            }
            if isDatePickerVisible {
                DatePicker("", selection: $selectedDate, in: ...Date(), displayedComponents: .date)
                    .datePickerStyle(GraphicalDatePickerStyle())
                    .labelsHidden()
                    //.padding()
            }
            Spacer()
            // Define a table of colors for the 31 days
         //   let colors: [Color] = [
         //       Color(red: 0.0, green: 0.0, blue: 1.0),
         //       Color(red: 0.0, green: 1.0, blue: 0.0),
         //       Color(red: 1.0, green: 0.0, blue: 0.0),
         //       Color(red: 0.0, green: 1.0, blue: 1.0),
         //       Color(red: 1.0, green: 0.0, blue: 1.0),
         //       Color(red: 1.0, green: 1.0, blue: 0.0),
         //       Color(red: 0.5, green: 0.0, blue: 0.5),
         //       Color(red: 0.5, green: 0.5, blue: 0.0),
         //       Color(red: 0.0, green: 0.5, blue: 0.5),
         //       Color(red: 0.7, green: 0.3, blue: 0.0),
         //       Color(red: 0.0, green: 0.7, blue: 0.3),
         //       Color(red: 0.3, green: 0.0, blue: 0.7),
         //       Color(red: 0.7, green: 0.7, blue: 0.0),
         //       Color(red: 0.0, green: 0.7, blue: 0.7),
         //       Color(red: 0.7, green: 0.0, blue: 0.7),
         //       Color(red: 0.2, green: 0.5, blue: 0.8),
         //       Color(red: 0.8, green: 0.2, blue: 0.5),
         //       Color(red: 0.5, green: 0.8, blue: 0.2),
         //       Color(red: 0.9, green: 0.6, blue: 0.2),
         //       Color(red: 0.2, green: 0.9, blue: 0.6),
         //       Color(red: 0.6, green: 0.2, blue: 0.9),
         //       Color(red: 0.8, green: 0.8, blue: 0.5),
         //       Color(red: 0.5, green: 0.8, blue: 0.8),
         //       Color(red: 0.8, green: 0.5, blue: 0.8),
         //       Color(red: 0.3, green: 0.7, blue: 0.5),
         //       Color(red: 0.5, green: 0.3, blue: 0.7),
          //      Color(red: 0.7, green: 0.5, blue: 0.3),
          //      Color(red: 0.6, green: 0.4, blue: 0.8),
          //      Color(red: 0.8, green: 0.6, blue: 0.4),
          //      Color(red: 0.4, green: 0.8, blue: 0.6),
          //      Color(red: 0.2, green: 0.2, blue: 0.2)
          //  ]

            Map() {

                if locations.count > 1 {
                    ForEach(Array(locations.indices.dropLast()), id: \.self) { index in

                  //      let day = getSubString(locations[index].Sample_Date_Time, start: 8, length: 2)
                  //      let dayNumber = Int(day) ?? 1
                 //       let color = dayNumber >= 1 && dayNumber <= 31 ? colors[dayNumber - 1] : .black
                        
                        MapPolyline(coordinates: [
                            CLLocationCoordinate2D(latitude: locations[index].latitude, longitude: locations[index].longitude),
                            CLLocationCoordinate2D(latitude: locations[index + 1].latitude, longitude: locations[index + 1].longitude)
                        ])
                        .stroke(.red, style: StrokeStyle(lineWidth: 1, dash: [2]))
                        // change this back to color if not what i want
                        //.stroke(color, style: StrokeStyle(lineWidth: 2, dash: [2]))
                    }
                }
                ForEach(locations) { location in
                    // name the Image based on the first Day (offfset 8-9) in the Sample_Date_Time 2024-01-21_00:00:04
                    // use Image ##.circle - getSubString(location.Sample_Date_Time, start: 8, length: 2))
                    
                    
                    var Image_Name: String {
                        isChecked ? "\(getSubString(location.Sample_Date_Time, start: 8, length: 2)).square" : ""
                    }

                   Annotation("\(location.address) : \(getSubString(location.Sample_Date_Time, start: 0, length: 16))",
                               coordinate: CLLocationCoordinate2D(latitude: location.latitude, longitude: location.longitude),
                               anchor: .topLeading) {
                        Image(systemName: Image_Name)
                            .padding(2)
                            .foregroundStyle(.white)
                            .background(.black)
                            .navigationTitle("\(location.description)")
                            .onTapGesture {
                                let latitude = location.latitude
                                let longitude = location.longitude
                                if let url = URL(string: "https://www.google.com/maps/search/?api=1&query=\(latitude),\(longitude)") {
                                    UIApplication.shared.open(url, options: [:], completionHandler: nil)
                                }
                            }
                    }
                }
                if locations.count > 2 {
                if let firstLocation = locations.first {
                    Annotation("HOME",
                               coordinate: CLLocationCoordinate2D(latitude: firstLocation.home_latitude, longitude: firstLocation.home_longitude),
                               anchor: .topLeading) {
                        Image(systemName: "house.and.flag.fill")
                            .padding(3)
                            .font(.title)
                            .foregroundStyle(.white)
                            .background(.green)
                    }

                    Annotation("📍\(firstLocation.address) : \(getSubString(firstLocation.Sample_Date_Time, start: 0, length: 16))",
                               coordinate: CLLocationCoordinate2D(latitude: firstLocation.latitude, longitude: firstLocation.longitude),
                               anchor: .topLeading) {
                        Image(systemName: "flag.checkered")
                            .padding(3)
                            .font(.title)
                            .foregroundStyle(.white)
                            .background(.red)
                            .onTapGesture {
                                let latitude = firstLocation.latitude
                                let longitude = firstLocation.longitude
                                if let url = URL(string: "https://www.google.com/maps/search/?api=1&query=\(latitude),\(longitude)") {
                                    UIApplication.shared.open(url, options: [:], completionHandler: nil)
                                }
                            }
                    }
                   }
                }
            } //Map()
            .onAppear(perform: {
                fetchDataForToday()
                //reportMemoryUsage()
            })
        }
    }

    func reportMemoryUsage() {
        var info = task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<task_basic_info>.size / MemoryLayout<integer_t>.size)
        let kerr: kern_return_t = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_, task_flavor_t(TASK_BASIC_INFO), $0, &count)
            }
        }
        if kerr == KERN_SUCCESS {
            print("Memory in use (in bytes): \(info.resident_size)")
        } else {
            print("Error with task_info(): \(kerr)")
        }
    }
    struct CheckboxToggleStyle: ToggleStyle {
    func makeBody(configuration: Configuration) -> some View {
        Button {
            withAnimation {
                configuration.isOn.toggle()
            }
        } label: {
            Image(systemName: configuration.isOn ? "checkmark.square" : "square")
        }
    }
    }

    private var getAddress: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: selectedDate)
    }
    private var isSelectedDateToday: Bool {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        let selectedDateString = formatter.string(from: selectedDate)
        let currentDateString = formatter.string(from: Date())
        return selectedDateString == currentDateString
    }
    private var formattedSelectedDate: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: selectedDate)
    }
    
   // private func fetchDataForToday() {
   //     fetchData(with: Date(), days: selectedDay)
   // }
    

    
    private func fetchDataForToday() {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyyMMdd"

        if let selectedDate = dateFormatter.date(from: date) {
            fetchData(with: selectedDate, days: selectedDay)
        } else {
            fetchData(with: Date(), days: selectedDay)
        }
    }
    
    func getSubString(_ input: String, start: Int, length: Int) -> String {
        guard start >= 0, start < input.count, length > 0 else {
            return ""
        }

        let startIndex = input.index(input.startIndex, offsetBy: start)
        let endIndex = input.index(startIndex, offsetBy: length)

        return String(input[startIndex..<endIndex])
    }
    var formattedCurrentDate: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm"
        return formatter.string(from: Date())
    }
    private func currentDate() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: Date())
    }
    
    
    //
    // fetch map data
    //
    
    private func fetchData(with date: Date, days: Int) {
        isLoading = true
        fetchDataIsComplete = false
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyyMMdd"
        let formattedDate = formatter.string(from: date)
        guard let url = URL(string: "https://\(server)/theme/show_map_api?ser=\(comment.serialNumber)&username=\(username)&date=\(formattedDate)&days=\(days)") else {
            return
        }
        var request = URLRequest(url: url)
        request.addValue("\(token)", forHTTPHeaderField: "HTTPMRTRACKERTOKEN")
        request.httpMethod = "GET"
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
        
            do {
                let decodedData = try JSONDecoder().decode([Locations].self, from: data)
                DispatchQueue.main.async {
                    self.locations = decodedData
                    connectLocationsOnMap()
                }
                fetchDataIsComplete = true
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
            }
            DispatchQueue.main.async {
                isLoading = false
            }

        }.resume()
    }

    private func connectLocationsOnMap() {
        guard locations.count > 1 else {
            return
        }

        let sourceCoordinate = CLLocationCoordinate2D(latitude: locations[0].latitude, longitude: locations[0].longitude)
        let destinationCoordinate = CLLocationCoordinate2D(latitude: locations.last!.latitude, longitude: locations.last!.longitude)

        fetchRouteFrom(sourceCoordinate, to: destinationCoordinate)
    }

}
extension CommentDetailView {
    
    private func fetchRouteFrom(_ source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) {
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile
        
        Task {
            let result = try? await MKDirections(request: request).calculate()
            route = result?.routes.first
            getTravelTime()
        }
    }
    // Function to calculate the rotation angle of the arrow
    private func getArrowRotation(start: Locations, end: Locations) -> Angle {
        let deltaLat = end.latitude - start.latitude
        let deltaLon = end.longitude - start.longitude
        let angle = atan2(deltaLon, deltaLat)
        return Angle(radians: Double(angle))
    }

    // Function to calculate the position of the arrow
    private func getArrowPosition(start: Locations, end: Locations) -> CGPoint {
        let midpoint = CLLocationCoordinate2D(
            latitude: (start.latitude + end.latitude) / 2,
            longitude: (start.longitude + end.longitude) / 2
        )
        return MKMapView().convert(midpoint, toPointTo: nil)
    }
    private func getTravelTime() {
        guard let route = route else { return }
        let formatter = DateComponentsFormatter()
        formatter.unitsStyle = .abbreviated
        formatter.allowedUnits = [.hour, .minute]
        travelTime = formatter.string(from: route.expectedTravelTime)
    }
}
