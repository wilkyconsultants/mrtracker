//
//  CommentDetailView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
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
    

    @State private var route: MKRoute?
    @State private var travelTime: String?
    @State private var home_lat: Double?
    @State private var home_long: Double?
    
    //@State private var selectedDate = Date()
    @State private var selectedDate: Date = Date()
    @State private var isDatePickerVisible = false
    
    @State private var fetchDataIsComplete = true
    
    @State private var selectedDay = 1
    @State private var isDropdownVisible = false
    private let days = Array(1...365)
    
    @State private var isLoading = false

    @State private var isChecked: Bool = true // set the marker on if checked, default is on

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
                // the marker is only value for current data ie. todays date
                if currentDate == formattedSelectedDate {
                    
                        Text("\(marker)\(ago): Travelled \(distance)km to home")
                    
                //}
            }
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
            let colors: [Color] = [
                Color(red: 0.0, green: 0.0, blue: 1.0),
                Color(red: 0.0, green: 1.0, blue: 0.0),
                Color(red: 1.0, green: 0.0, blue: 0.0),
                Color(red: 0.0, green: 1.0, blue: 1.0),
                Color(red: 1.0, green: 0.0, blue: 1.0),
                Color(red: 1.0, green: 1.0, blue: 0.0),
                Color(red: 0.5, green: 0.0, blue: 0.5),
                Color(red: 0.5, green: 0.5, blue: 0.0),
                Color(red: 0.0, green: 0.5, blue: 0.5),
                Color(red: 0.7, green: 0.3, blue: 0.0),
                Color(red: 0.0, green: 0.7, blue: 0.3),
                Color(red: 0.3, green: 0.0, blue: 0.7),
                Color(red: 0.7, green: 0.7, blue: 0.0),
                Color(red: 0.0, green: 0.7, blue: 0.7),
                Color(red: 0.7, green: 0.0, blue: 0.7),
                Color(red: 0.2, green: 0.5, blue: 0.8),
                Color(red: 0.8, green: 0.2, blue: 0.5),
                Color(red: 0.5, green: 0.8, blue: 0.2),
                Color(red: 0.9, green: 0.6, blue: 0.2),
                Color(red: 0.2, green: 0.9, blue: 0.6),
                Color(red: 0.6, green: 0.2, blue: 0.9),
                Color(red: 0.8, green: 0.8, blue: 0.5),
                Color(red: 0.5, green: 0.8, blue: 0.8),
                Color(red: 0.8, green: 0.5, blue: 0.8),
                Color(red: 0.3, green: 0.7, blue: 0.5),
                Color(red: 0.5, green: 0.3, blue: 0.7),
                Color(red: 0.7, green: 0.5, blue: 0.3),
                Color(red: 0.6, green: 0.4, blue: 0.8),
                Color(red: 0.8, green: 0.6, blue: 0.4),
                Color(red: 0.4, green: 0.8, blue: 0.6),
                Color(red: 0.2, green: 0.2, blue: 0.2)
            ]

            Map() {
                // Add the polyline to connect points with lines
                //if locations.count > 1 {
                //    MapPolyline(coordinates: locations.map { CLLocationCoordinate2D(latitude: $0.latitude, longitude: $0.longitude) })
                 //       .stroke(Color.red, style: StrokeStyle(lineWidth: 1, dash: [3]))
                //}

                if locations.count > 1 {
                    ForEach(Array(locations.indices.dropLast()), id: \.self) { index in
                        
                        let angle = atan2(locations[index].latitude - locations[index + 1].latitude, locations[index].longitude - locations[index + 1].longitude)
                        
                        
                        // Convert radians to degrees
                        let degrees = angle * 180 / .pi
                        
                        let SAMPLE_DATE_TIME = locations[index].Sample_Date_Time
                        let SAMPLE_DATE_TIME_PREV = locations[index + 1].Sample_Date_Time
                        let ADDRESS = locations[index].address

                        // Select an appropriate image based on the direction
                        let image = getImageForDirection(degrees,SAMPLE_DATE_TIME,SAMPLE_DATE_TIME_PREV, ADDRESS)
     
                         //Annotation("\(locations[index].address) : \(getSubString(locations[index].Sample_Date_Time, start: 0, length: 16))",
                         //           coordinate: CLLocationCoordinate2D(latitude: locations[index + 1].latitude, longitude: locations[index + 1].longitude),
                         //           anchor: .topLeading) {
                         //    Image(systemName: image)
                         //        .padding(2)
                         //        .foregroundStyle(.white)
                         //        .background(.black)
                         //}
                        let day = getSubString(locations[index].Sample_Date_Time, start: 8, length: 2)
                        let dayNumber = Int(day) ?? 1
                        let color = dayNumber >= 1 && dayNumber <= 31 ? colors[dayNumber - 1] : .black
                        
                        MapPolyline(coordinates: [
                            CLLocationCoordinate2D(latitude: locations[index].latitude, longitude: locations[index].longitude),
                            CLLocationCoordinate2D(latitude: locations[index + 1].latitude, longitude: locations[index + 1].longitude)
                        ])
                        .stroke(color, style: StrokeStyle(lineWidth: 2, dash: [2]))
  

                    }
                }
                ForEach(locations) { location in
                    // name the Image based on the first Day (offfset 8-9) in the Sample_Date_Time 2024-01-21_00:00:04
                    // use Image ##.circle - getSubString(location.Sample_Date_Time, start: 8, length: 2))
                    
                    
                    var Image_Name: String {
                        isChecked ? "\(getSubString(location.Sample_Date_Time, start: 8, length: 2)).square" : ""
                    }
                    //var Image_Name = "\(getSubString(location.Sample_Date_Time, start: 8, length: 2)).square"
                    
                    //let location = CLLocation(latitude: location.latitude, longitude: location.longitude)

                    
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
                    // set up for the region to set focus when refresh map
                    //let latitude = firstLocation.latitude
                    //let longitude = firstLocation.longitude
                    //let focuscoordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
                    //let region = MKCoordinateRegion(center: focuscoordinate, latitudinalMeters: 1000, longitudinalMeters: 1000) // Adjust the values for the desired zoom level

                    //Mapview.setRegion(region, animated: true)
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
            .onAppear(perform: {
                fetchDataForToday()
                reportMemoryUsage()
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
    //
    // Save this for use later when we want to gen arrows for direction indicator
    //
    func getImageForDirection(_ degrees: Double, _ SAMPLE_DATE_TIME: String, _ SAMPLE_DATE_TIME_PREV: String, _ ADDRESS: String) -> String {
        var direction = ""
        var symbol = ""
        
        var degrees_360: Double = 0
        if degrees < 0 {
            degrees_360 = degrees + 360
        } else {
            degrees_360 = degrees
        }
        
        if degrees_360 >= 337.5 || degrees_360 < 22.5 {
            direction = "North"
            symbol = "arrow.up"
        } else if degrees_360 >= 22.5 && degrees_360 < 67.5 {
            direction = "North-East"
            symbol = "arrow.up.right"
        } else if degrees_360 >= 67.5 && degrees_360 < 112.5 {
            direction = "East"
            symbol = "arrow.right"
        } else if degrees_360 >= 112.5 && degrees_360 < 157.5 {
            direction = "South-East"
            symbol = "arrow.down.left"
        } else if degrees_360 >= 157.5 && degrees_360 < 202.5 {
            direction = "South"
            symbol = "arrow.down"
        } else if degrees_360 >= 202.5 && degrees_360 < 247.5 {
            direction = "South-West"
            symbol = "arrow.down.right"  // This value seems incorrect, please provide the correct symbol
        } else if degrees_360 >= 247.5 && degrees_360 < 292.5 {
            direction = "West"
            symbol = "arrow.left"
        } else if degrees_360 >= 292.5 && degrees_360 < 337.5 {
            direction = "North-West"
            symbol = "arrow.up.backward"
        }
        if ADDRESS == "Home" {
            symbol = ""
        }
        //print("Passed degrees: \(degrees_360) SAMPLE_DATE_TIME: \(SAMPLE_DATE_TIME) SAMPLE_DATE_TIME_PREV: \(SAMPLE_DATE_TIME_PREV)  Symbol: \(symbol)")

        return symbol
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
    private func fetchDataForToday() {
        fetchData(with: Date(), days: selectedDay)
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
        request.addValue("\(token)", forHTTPHeaderField: "HTTP_MR_TRACKER_TOKEN")
        request.httpMethod = "GET"
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            //if response == response {
            //    print("response=\(String(describing: response))")
            //}
        
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
