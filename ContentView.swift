//
//  ContentView.swift
//  MR Tracker - IOS front end
//
//  Created by Rob Wilkinson on 2024-01-19.
//

import SwiftUI
import MapKit
struct ContentView: View {
    @AppStorage("username") var username: String = ""
    @AppStorage("password") var password: String = ""
    @AppStorage("server") var server: String = ""
    @State private var token: String? = nil
    @State private var showAlert = false
    @State private var errorMessage = ""
    @State private var authenticated = false
  
    @State private var isLoading = false

    var body: some View {
        NavigationView {
            ZStack {
                VStack {
                    Form {
                        Section(header: Text("🗝 User Credentials")) {
                            TextField("Username", text: $username)
                                .disabled(authenticated)
                                .autocapitalization(.none)
                                .frame(height: 40)

                            SecureField("Password", text: $password)
                                .disabled(authenticated)
                                .frame(height: 40)

                            TextField("Server", text: $server)
                                .disabled(authenticated)
                                .autocapitalization(.none)
                                .frame(height: 40)
                        }

                        HStack {
                            if authenticated == false {
                                Button("Login") {
                                    authenticate()
                                }
                                
                                .disabled(authenticated)
                                .padding()
                                .background(
                                    LinearGradient(
                                        gradient: Gradient(colors: [Color(.systemBlue), Color(.systemTeal)]),
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .foregroundColor(.white)
                                .clipShape(RoundedRectangle(cornerRadius: 6))
                                .shadow(color: Color.gray.opacity(0.5), radius: 3, x: 0, y: 1)
                                .font(.headline)
                                
                                Spacer()
                                
                            }}
                        .multilineTextAlignment(TextAlignment .center)
                        //if token == token {
                        Spacer()
                        if authenticated {
                            Text("Login Successful, welcome \(username)")
                                .foregroundColor(.green)
                                
                                
                            NavigationLink("👩🏻‍💻 Tag Central", destination: TagListView(username: username,server: server, token: token ?? ""))
                                .foregroundColor(.blue)
                            
                            NavigationLink("🏷️ Tag Inventory", destination: TagDetailView(username: username,server: server, token: token ?? "", option: "ALL"))
                                .foregroundColor(.blue)
                        
                            NavigationLink("⚠️ Tag Alerts", destination: TagDetailView(username: username,server: server, token: token ?? "", option: "LOST"))
                                .foregroundColor(.blue)
                        }
                    }
                    .padding()
                    .navigationTitle("👨🏻‍💼 MR🌐Tracker")
                }
            }
        }
    }

    var loadingOverlay: some View {
        Group {
            if isLoading {
                ZStack {
                    Color(UIColor.systemBackground)
                        .opacity(0.7)
                        .edgesIgnoringSafeArea(.all)

                    VStack {
                        ProgressView("Loading...")
                            .progressViewStyle(CircularProgressViewStyle(tint: .blue))
                            .scaleEffect(2.0)

                        Text("Please wait...")
                            .foregroundColor(.white)
                            .padding(.top, 8)
                    }
                }
                .transition(.opacity)
            }
        }
    }

    func authenticate() {
        guard let url = URL(string: "https://\(server)/theme/api_login/") else {
            return
        }

        let credentials = ["username": username, "password": password]

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: credentials)

            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.httpBody = jsonData
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")

            isLoading = true

            URLSession.shared.dataTask(with: request) { data, response, error in
                isLoading = false

                guard let data = data, error == nil else {
                    errorMessage = "Invalid username or password"
                    showAlert = true
                    return
                }

                do {
                    let json = try JSONSerialization.jsonObject(with: data, options: [])
                    if let jsonDict = json as? [String: String],
                       let token = jsonDict["token"] {
                        DispatchQueue.main.async {
                            self.token = token
                            self.authenticated = true
                        }
                    } else {
                        errorMessage = "Invalid response from server"
                        showAlert = true
                    }
                } catch {
                    errorMessage = "Failed to parse JSON response"
                    showAlert = true
                }
            }.resume()
        } catch {
            errorMessage = "Failed to create JSON data"
            showAlert = true
        }
    }
}
struct CircleLink: View {
    let text: String
    let count: String
    let fillColor: Color
    let fontSize: CGFloat

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 10)
                .fill(fillColor)
                .frame(width: 110, height: 70)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.white, lineWidth: 2)
                        .blur(radius: 4)
                        .offset(x: 2, y: 2)
                        .mask(RoundedRectangle(cornerRadius: 10).fill(LinearGradient(gradient: Gradient(colors: [.black, .clear]), startPoint: .top, endPoint: .bottom)))
                )
                .clipShape(RoundedRectangle(cornerRadius: 10))
                .shadow(color: Color.black.opacity(0.3), radius: 5, x: 0, y: 2)

            VStack {
                Text(text)
                    .foregroundColor(.black)
                    .font(.system(size: fontSize))
                Text(count)
                    .foregroundColor(.white)
                    .font(.title3)
            }
        }
    }
}

struct TagListView: View {
    let username: String
    let server: String
    let token: String

    @State private var reports: [Reports]?
    @State private var isLoading = false
    @State private var datadate = Date()

    var body: some View {
        VStack {
            Text("Refreshed: \(formattedCurrentDateTime())")
                .foregroundColor(.blue)
                .bold()
                .font(.title3)
                .padding()

            if let reports = reports {
                ForEach(reports) { report in
                    VStack {
                        HStack(alignment: .center) {
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL")) {
                                CircleLink(text: "All", count: report.all_ctr, fillColor: Color.teal, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "HEALTHY")) {
                                CircleLink(text: "Healthy", count: report.healthy_ctr, fillColor: Color.green, fontSize: 16)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ACTIVE")) {
                                CircleLink(text: "Active Today", count: report.active_ctr, fillColor: Color.blue, fontSize: 16)
                            }
                            //}
                        }
                        HStack(alignment: .center) {
                            //Spacer()
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "AWAY")) {
                                CircleLink(text: "Travelling", count: report.away_ctr, fillColor: Color.cyan, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "BATTERY_WEAK")) {
                                CircleLink(text: "Low 🪫", count: report.battery_weak_ctr, fillColor: Color.yellow, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "LOST")) {
                                CircleLink(text: "Lost > 1 hour", count: report.lost_ctr, fillColor: Color.red, fontSize: 18)
                            }
                        }
                        Spacer(minLength: 30)
                        HStack(spacing: 5) {
                            Text("Tags: \(report.all_ctr)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.primary)
                            Divider().background(Color.primary)
                            VStack {
                                if let healthyCtr = Double(report.healthy_ctr), let allCtr = Double(report.all_ctr), allCtr > 0 {
                                    let ratio = healthyCtr / allCtr
                                    let percentage = Int(round(ratio * 100))
                                    Button(action: {
                                        isLoading = true
                                    }) {
                                        //Spacer()
                                        ZStack {
                                            // Outer circle representing the entire pie chart
                                            Circle()
                                                .fill(circleFillColor(for: percentage).opacity(0.5))
                                                .frame(width: 140, height: 140)

                                            // Pie chart segment based on the percentage
                                            Circle()
                                                .trim(from: 0.0, to: CGFloat(percentage) / 100.0)
                                                .stroke(circleFillColor(for: percentage), lineWidth: 40)
                                                .frame(width: 100, height: 100)
                                                .rotationEffect(.degrees(-90)) // Start from the top

                                            Text("Tag Health: \(percentage)%")
                                                .font(.system(size: 18))
                                                .bold()
                                                .foregroundColor(.white)
                                        }
                                    }
                                    .padding()
                                }
                            }
                        }
                        .padding()
                    }
                }
                Divider()
                HStack {
                    Button("⏻") {
                        UIApplication.shared.perform(#selector(NSXPCConnection.suspend))
                    }
                    .padding()
                    .background(Color.clear)
                    .foregroundColor(.red)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                    .shadow(color: Color.gray.opacity(0.5), radius: 3, x: 0, y: 1)
                    .font(.largeTitle)

                    Button("↻") {
                        fetchData()
                    }
                    .padding()
                    .background(Color.clear)
                    .foregroundColor(.green)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                    .shadow(color: Color.gray.opacity(0.5), radius: 3, x: 0, y: 1)
                    .font(.largeTitle)
                }
                .navigationBarBackButtonHidden(true)

            } else {
                if isLoading {
                    ProgressView("Loading...")
                        .progressViewStyle(CircularProgressViewStyle(tint: .blue))
                        .scaleEffect(2.0)
                        .padding()
                } else {
                    Text("Loading...")
                }
            }
        }
        .onAppear {
            fetchData()
        }
        .navigationTitle("👨🏻‍💼 MR🌐Tracker")
    }
    
    func circleFillColor(for percentage: Int) -> Color {
        switch percentage {
        case 0..<50:
            return .red
        case 50..<79:
            return .yellow
        default:
            return .green
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/tag_list_api?option=REPORT&user_id=\(username)") else {
            return
        }

        var request = URLRequest(url: url)
        request.addValue("\(token)", forHTTPHeaderField: "HTTP_MR_TRACKER_TOKEN")

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            do {
                let decodedData = try JSONDecoder().decode([Reports].self, from: data)
                DispatchQueue.main.async {
                    self.reports = decodedData
                    isLoading = false
                }
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
            }
        }.resume()
    }

    func formattedCurrentDateTime() -> String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MMM d, y h:mm a" // Use the desired format

        return dateFormatter.string(from: Date())
    }
}

struct StatusIndicatorView: View {
    let title: String
    let value: String
    let color: Color

    var body: some View {
        
        VStack(alignment: .leading) {
            Text("\(title): \(value)")
                .font(.title3)
                .multilineTextAlignment(.leading)
                .foregroundColor(color)
        }
    }
}

struct TagDetailView: View {
    let username: String
    let server: String
    let token: String
    let option: String

    @State private var comments: [Comments]?

    var body: some View {
        VStack {
            // Fetch and display data from the third API
            if let comments = comments {
                List(comments) { comment in
                    NavigationLink(destination: CommentDetailView(comment: comment,server: server, username: username, distance: comment.distance, marker: comment.marker, ago: comment.ago, token: token)) {
                        VStack(alignment: .leading) {
                            Text("\(comment.description)")
                                //.padding()
                                .background(Color.blue.opacity(0.2)) // Set background color here
                                .cornerRadius(8) // Add corner radius for a rounded look
                            //Divider() 
                            Text("  ► \(comment.battery_status)\(comment.marker)\(comment.ago): 🏃\(comment.distance)km ")
                            Text("📍\(comment.address)")
                        }
                    }
                }
            } else {
                Text("Loading...")
            }
        }
        .onAppear {
            fetchComments()
        }
        .navigationTitle("🏷️ [\(String(option.prefix(7)))]")
    }
    

    func fetchComments() {
        guard let url = URL(string: "https://\(server)/theme/tag_list_api?option=\(option)&user_id=\(username)") else {
            return
        }

        var request = URLRequest(url: url)
        request.addValue("\(token)", forHTTPHeaderField: "HTTP_MR_TRACKER_TOKEN")

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            do {
                let decodedData = try JSONDecoder().decode([Comments].self, from: data)
                DispatchQueue.main.async {
                    self.comments = decodedData
                }
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
            }
        }.resume()
    }
}

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

    private let gradient = LinearGradient(colors: [.red, .orange], startPoint: .leading, endPoint: .trailing)
    private let stroke = StrokeStyle(lineWidth: 5, lineCap: .round, lineJoin: .round, dash: [8, 8])

    var home: CLLocationCoordinate2D { CLLocationCoordinate2D(latitude: 43.8382, longitude: -79.3001) }

    var body: some View {
        VStack {
            Text("As of: \(formattedCurrentDate)")
            if let firstLocation = locations.first {
                Text("📍\(firstLocation.address)")
                Text("\(marker)\(ago): Travelled \(distance)km to home")
            }
            Spacer()

            Map() {
                // Add the polyline to connect points with lines
                if locations.count > 1 {
                    MapPolyline(coordinates: locations.map { CLLocationCoordinate2D(latitude: $0.latitude, longitude: $0.longitude) })
                        .stroke(Color.red, style: StrokeStyle(lineWidth: 2, dash: [5]))

                    
                }
                ForEach(locations) { location in
                    Annotation("\(location.address) : \(getSubString(location.Sample_Date_Time, start: 0, length: 16))",
                               coordinate: CLLocationCoordinate2D(latitude: location.latitude, longitude: location.longitude),
                               anchor: .topLeading) {
                        Image(systemName: "car")
                            .padding(3)
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
                fetchData()
            })
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
    private func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/show_map_api?ser=\(comment.serialNumber)&username=\(username)") else {
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
            if response == response {
                print("response=\(String(describing: response))")
            }
        
            do {
                let decodedData = try JSONDecoder().decode([Locations].self, from: data)
                DispatchQueue.main.async {
                    self.locations = decodedData
                    connectLocationsOnMap()
                }
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
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

struct Comments: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let description: String
    let battery_status: String
    let marker: String
    let distance: String
    let address: String
    let serialNumber: String
    let link: String
    let distance_from_home: String
    let ago: String
}

struct Reports: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let all_ctr: String
    let active_ctr: String
    let away_ctr: String
    let lost_ctr: String
    let healthy_ctr: String
    let battery_weak_ctr: String
    let type: String
}

struct Healths: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let Date_time: String
    let all_ctr: String
    let active_ctr: String
    let away_ctr: String
    let lost_ctr: String
    let battery_weak_ctr: String
    let healthy_ctr: String
}

struct Locations: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let Sample_Date_Time: String
    let iCloud_Date_Time: String
    let description: String
    let address: String
    let home_latitude: Double
    let home_longitude: Double
    let latitude: Double
    let longitude: Double
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

