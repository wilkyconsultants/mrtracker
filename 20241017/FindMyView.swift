//
//  FindMyView.swift
//  MRTRACKER
//
//  Created by Robert A Wilkinson on 2024-02-04.
//

import SwiftUI
import MapKit

struct FindMyView: View {
    let username: String
    let server: String
    
    @State private var locations: [LocationModel] = []
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 0, longitude: 0),
        span: MKCoordinateSpan(latitudeDelta: 5, longitudeDelta: 5)
        
    )
    @State private var showList = false

    @State private var navigateToDetailView = false
    
    var body: some View {
        Text("MR🌐Tracker Device Map")
            .font(.system(size: 24))
            .foregroundColor(.brown)
        NavigationView {
           Map() {
                        ForEach(locations) { location in

                            Annotation("\(location.description)\n[\(location.address)]\n \(location.marker)\(location.update_date_time) EST TZ",
                               coordinate: CLLocationCoordinate2D(latitude: location.latitude, longitude: location.longitude),
                               anchor: .topLeading) {
                                Image(systemName: "mappin.and.ellipse")
                                    .padding(2)
                                    .foregroundStyle(.black)
                                    .background(.white)
                                    .navigationTitle("")
                                    .font(.system(size: 32))
                                    .onTapGesture {
                                        let latitude = location.latitude
                                        let longitude = location.longitude
                                        if let url = URL(string: "https://www.google.com/maps/search/?api=1&query=\(latitude),\(longitude)") {
                                            UIApplication.shared.open(url, options: [:], completionHandler:    nil)
                                        }
                                    }
                            }
                        }
               
                }
                .onAppear {
                    fetchData()
                    
            }
            
        }
        Toggle(isOn: $showList, label: {
            Text("Toggle For Device List")  // Add a Toggle at the top of the screen
        })
        .padding()

        if showList {
           // VStack(alignment: .leading) {
            let sortedLocations = locations.sorted { $0.address < $1.address }
            List(sortedLocations) { location in
                let emptyComment = Comments(description: "", battery_status: "", marker: "", distance: "", address: "", serialNumber: "\(location.serialNumber)", link: "", distance_from_home: "", ago: "")
                NavigationLink(destination: CommentDetailView(comment: emptyComment, server: server, username: username, distance: "", marker: location.marker, ago: location.ago, token: "",date: "-")) {
                    VStack(alignment: .leading) {
                        Text("\(location.description)")
                            .foregroundColor(.green)
                            .font(.system(size: 18))
                            .bold()
                        Text("📍\(location.address)")
                            .font(.system(size: 16))
                            .foregroundColor(.blue)
                        Text("Updated: \(location.marker)\(location.update_date_time) EST")
                            .font(.system(size: 16))
                            .foregroundColor(.blue)
                      //  let emptyComment = Comments(description: "", battery_status: "", marker: "", distance: "", address: "", serialNumber: "\(location.serialNumber)", link: "", distance_from_home: "", ago: "")
                        
                      //  NavigationLink(destination: CommentDetailView(comment: emptyComment, server: server, username: username, distance: "", marker: "", ago: "", token: "", date: location.date_time), isActive: $navigateToDetailView) {
                       //     EmptyView()
                      //  }
                        //.hidden()
                    }
                    .padding(.vertical, 0)
                }
            }
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
    
    func fetchData() {
        if let url = URL(string: "https://\(server)/theme/findmy_api?username=\(username)") {
            URLSession.shared.dataTask(with: url) { data, response, error in
                if let data = data {
                    do {
                        //print("data=\(data)")
                        let locations = try JSONDecoder().decode([LocationModel].self, from: data)
                        // Update the region based on the fetched locations
                        if let firstLocation = locations.first {
                            let center = CLLocationCoordinate2D(latitude: firstLocation.latitude, longitude: firstLocation.longitude)
                            let span = MKCoordinateSpan(latitudeDelta: 0.5, longitudeDelta: 0.5)
                          //  let span = MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
                            region = MKCoordinateRegion(center: center, span: span)
                        }
                        self.locations = locations
                        //print("locations count=\(locations.count)")
                    } catch {
                        print("Error decoding JSON: \(error)")
                    }
                }
            }.resume()
        }
    }
}

struct LocationModel: Identifiable, Decodable {
    let id: Int
    let description: String
    let date_time: String
    let update_date_time: String
    let battery_status: String
    let marker: String
    let address: String
    let serialNumber: String
    let ago: String
    let latitude: Double
    let longitude: Double
}

