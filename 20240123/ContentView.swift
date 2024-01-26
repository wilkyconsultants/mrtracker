//
//  ContentView.swift
//  MR Tracker - IOS front end
//
//  Created by Rob Wilkinson on 2024-01-17
//
// MR🌐Tracker Change History:
// 2024-01-17 -Version 1.0 - Initial
// 2024-01-18 -Version 1.1 - lines on routes
// 2024-01-19 -Version 1.2 - toolbar
// 2024-01-20 -Version 1.3 - date selection
// 2024-01-21 -Version 1.4 - coloured routes
// 2024-01-23 -Version 1.5 - add distance chart
// 2024-01-24 -Version 1.6 - add search bar
//
//

import SwiftUI
import MapKit
import Charts

struct ContentView: View {
    @AppStorage("username") var username: String = ""
    @AppStorage("password") var password: String = ""
    @AppStorage("server") var server: String = ""
    @State private var token: String? = nil
    @State private var showAlert = false
    @State private var errorMessage = ""
    @State private var authenticated = false
    @State private var isLoading = false
    @State private var navigateToTagList = false
    

    var body: some View {


        NavigationView {

            ZStack {
                if authenticated == false {
                    Text("")
                        .font(.title)
                        .toolbar {
                            ToolbarItem(placement: .bottomBar) {
                                HStack {
                                    NavigationLink(destination: InfoView()) {
                                        VStack(alignment: .center) {
                                            Image(systemName: "info.square")
                                                .resizable()
                                                .frame(width: 20, height: 20)
                                                .aspectRatio(contentMode: .fit)
                                            Text("Information")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                        }
                                    }
                                    NavigationLink(destination: TermsView()) {
                                        VStack(alignment: .center) {
                                            Image(systemName: "person.crop.circle.badge.questionmark")
                                                .resizable()
                                                .frame(width: 20, height: 20)
                                                .aspectRatio(contentMode: .fit)
                                            Text("Terms & Conditions")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                        }
                                    }
                                }
                            }
                        }
                }
                if authenticated {
                    VStack(alignment: .center) {
                        Text("")
                            .font(.title)
                            .toolbar {
                                ToolbarItemGroup(placement: .primaryAction) {
                                    HStack {
                                        Button(action: {
                                            UIApplication.shared.perform(NSSelectorFromString("suspend"))
                                        }) {
                                            VStack(alignment: .center) {
                                                Image(systemName: "power.circle")
                                                    .resizable()
                                                    .frame(width: 20, height: 20)
                                                    .aspectRatio(contentMode: .fit)
                                                Text("Minimize")
                                                    .font(.body)
                                                    .foregroundColor(.blue)
                                            }
                                        }
                                        NavigationLink(destination: InfoView()) {
                                            VStack(alignment: .center) {
                                                Image(systemName: "info.square")
                                                    .resizable()
                                                    .frame(width: 20, height: 20)
                                                    .aspectRatio(contentMode: .fit)
                                                Text("Information")
                                                    .font(.body)
                                                    .foregroundColor(.blue)
                                            }
                                        }
                                        NavigationLink(destination: TermsView()) {
                                            VStack(alignment: .center) {
                                                Image(systemName: "person.crop.circle.badge.questionmark")
                                                    .resizable()
                                                    .frame(width: 20, height: 20)
                                                    .aspectRatio(contentMode: .fit)
                                                Text("Terms & Conditions")
                                                    .font(.body)
                                                    .foregroundColor(.blue)
                                            }
                                    }
                                  }
                                }
                            }
                    }


                    Text("Welcome to MR🌐Tracker")
                        .font(.system(size: 22))
                        .toolbar {
                    ToolbarItem(placement: .bottomBar) {
                        HStack {
                            NavigationLink(destination: TagListView(username: username, server: server, token: token ?? "", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "house")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                            Text("Main")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                }
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token ?? "", option: "ALL", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "tag.fill")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                            Text("All")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                }
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token ?? "", option: "ACTIVE", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "car")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                            Text("Active")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                }
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token ?? "", option: "AWAY", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "mappin.and.ellipse")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                            Text("Away")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                }
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token ?? "", option: "LOST", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "exclamationmark.triangle")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                            Text("Lost")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                }
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token ?? "", option: "BATTERY_WEAK", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "minus.plus.batteryblock.exclamationmark.fill")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                            Text("Battery")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                }
                            }
                        }
                    }
                }
            }
                    
                    VStack {
                            Form {
                                if authenticated == false {
                                    Text("👨🏻‍💼 MR🌐Tracker")
                                        .font(.title)
                                    Section(header: Text("🗝 Enter Credentials")) {
                                        TextField("Username", text: $username)
                                            .disabled(authenticated)
                                            .autocapitalization(.none)
                                            .frame(height: 40)
                                            .padding()
                                            .background(Color(.systemGray5))
                                            .cornerRadius(8)
                                        
                                        SecureField("Password", text: $password)
                                            .disabled(authenticated)
                                            .frame(height: 40)
                                            .padding()
                                            .background(Color(.systemGray5))
                                            .cornerRadius(8)
                                        
                                        TextField("Server", text: $server)
                                            .disabled(authenticated)
                                            .autocapitalization(.none)
                                            .padding()
                                            .frame(height: 40)
                                            .cornerRadius(8)
                                        
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
                                        .frame(minWidth: 0, maxWidth: .infinity)
                                        .foregroundColor(.white)
                                        .clipShape(RoundedRectangle(cornerRadius: 6))
                                        .shadow(color: Color.gray.opacity(0.5), radius: 3, x: 0, y: 1)
                                        .font(.headline)
                                        
                                    }
                                } else {

                                }
                            }
                            .padding()
                            //.navigationTitle("👨🏻‍💼 MR🌐Tracker")
                            .navigationBarBackButtonHidden(false)
                    }
                }
                .alert(isPresented: $showAlert) {
                    Alert(title: Text(""), message: Text(errorMessage), dismissButton: .default(Text("OK")))
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
                    errorMessage = "Login Failed"
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
                            //errorMessage = "Login Successful, welcome \(username)!"
                            //showAlert = true
                        }
                    } else {
                        errorMessage = "Login Failed"
                        showAlert = true
                    }
                } catch {
                    errorMessage = "Login Failed"
                    showAlert = true
                }
            }.resume()
        } catch {
            errorMessage = "Login Failed"
            showAlert = true
        }
    }
}




struct TermsView: View {
    let termsAndConditionsText = """
    Terms and Conditions of Use

    1. Acceptance of Terms

    By using this product and associated services (hereinafter referred to as "the Product"), you agree to abide by these Terms and Conditions of Use. If you do not agree with any part of these terms, please do not use the Product.

    2. Prohibition of Unauthorized Tracking

    You expressly acknowledge and agree that the Product shall not, under any circumstances, be used for tracking any individual without their explicit and written consent. Tracking an individual without their direct and written consent is strictly prohibited.

    3. Consent Requirement

    Before utilizing the tracking features of the Product to monitor or trace any individual, you are obligated to obtain their express, informed, and written consent, specifying the extent and purpose of tracking. Failure to do so constitutes a breach of these Terms and Conditions.

    4. Legal Responsibility

    You understand and accept that by violating these Terms and Conditions and engaging in unauthorized tracking, you may be subject to legal actions, including but not limited to civil and criminal proceedings, as permitted by applicable laws. You agree to assume full legal responsibility for any consequences arising from such actions.

    5. Compliance with Applicable Laws

    You are required to comply with all local, state, federal, and international laws and regulations governing tracking and monitoring activities. The Product is not intended to be used for unlawful purposes.

    6. Liability and Indemnification

    By using the Product, you agree to hold harmless the product provider, its affiliates, employees, and agents from any liability, claims, losses, or damages arising from your use of the Product in violation of these Terms and Conditions.

    7. Termination of Use

    The product provider reserves the right to terminate your access to the Product or its services without notice if you engage in unauthorized tracking activities or otherwise violate these Terms and Conditions.

    8. Amendments to Terms

    These Terms and Conditions of Use may be amended by the product provider at any time. It is your responsibility to review them periodically for updates and changes.

    9. Contact Information

    If you have any questions or concerns regarding these Terms and Conditions or anything else, please contact us by using email address MrTracker.416@gmail.com, we would love to hear from you!
    """

    var body: some View {
        ScrollView {
            Text(termsAndConditionsText)
                .padding()
        }
        .navigationBarTitle("Terms and Conditions", displayMode: .inline)
    }
}

struct InfoView: View {
    let InfoText = """
    MR🌐Tracker Change History:
    2024-01-17 -Version 1.0 - Initial
    2024-01-18 -Version 1.1 - lines on routes
    2024-01-19 -Version 1.2 - toolbar
    2024-01-20 -Version 1.3 - date selection
    2024-01-21 -Version 1.4 - coloured routes
    
    The Ultimate Solution for Tracking Anything, Anywhere in the World.

    MR🌐Tracker is a cutting-edge tracking solution, meticulously engineered to monitor the location of a diverse range of assets. From vacation cruises, letters and packages to luggage, vehicles, keys, backpacks, bicycles, and construction equipment – we've got you covered. Whether you're a traveler, a professional, or simply looking to safeguard your belongings, our advanced technology offers comprehensive oversight, providing the peace of mind you deserve.
    
    Simply decide what you want to track, attach a tag, and you're good to go – it's that simple. The tags record locations worldwide with no data charges.

    Your typical setup includes a MacBook computer, iPhone, and tracking tags. Run as a franchise at your site. We handle all the necessary software installation, network setup, and offer remote support for a nominal charge. Rest assured about data privacy – all data uses SSL encryption, ensuring your information remains secure. Reports are accessible only to you as an admin, and you can grant access to additional users with user IDs chosen by you as the admin.
    
    To get started send an email to MrTracker.416@gmail.com and we will walk you throigh teh set up required.

    If you have any questions or concerns regarding Mr Tracker functionality please contact us by using email address MrTracker.416@gmail.com, we would love to hear from you!
    """

    var body: some View {
        ScrollView {
            Text(InfoText)
                .padding()
        }
        .navigationBarTitle("Product Information", displayMode: .inline)
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
    let chartList: String

    @State private var reports: [Reports]?
    @State private var isLoading = false
    @State private var datadate = Date()

    var body: some View {
        
        VStack {
            Text("Refreshed: \(formattedCurrentDateTime())")
                .foregroundColor(.green)
                .bold()
                .font(.title3)
                .padding()

            if let reports = reports {
                ForEach(reports) { report in
                    VStack {
                        HStack(alignment: .center) {
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL", chartList: "")) {
                                CircleLink(text: "All", count: report.all_ctr, fillColor: Color.teal, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "HEALTHY", chartList: "")) {
                                CircleLink(text: "Healthy", count: report.healthy_ctr, fillColor: Color.green, fontSize: 16)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ACTIVE", chartList: "")) {
                                CircleLink(text: "Active Today", count: report.active_ctr, fillColor: Color.blue, fontSize: 16)
                            }
                            //}
                        }
                        HStack(alignment: .center) {
                            //Spacer()
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "AWAY", chartList: "")) {
                                CircleLink(text: "Travelling", count: report.away_ctr, fillColor: Color.cyan, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "BATTERY_WEAK", chartList: "")) {
                                CircleLink(text: "Low 🪫", count: report.battery_weak_ctr, fillColor: Color.yellow, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "LOST", chartList: "")) {
                                CircleLink(text: "Lost > 1 hour", count: report.lost_ctr, fillColor: Color.red, fontSize: 18)
                            }
                        }
                        HStack(alignment: .center) {
                            //Spacer()
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL", chartList: "CHART")) {
                                CircleLink(text: "Distance ", count: "Chart", fillColor: Color.orange, fontSize: 18)
                            }
                        }
                        
                        //Spacer(minLength: 30)
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
                                                .foregroundColor(.black)
                                        }
                                    }
                                    .padding()
                                }
                            }
                        }
                        .padding()
                    }
                }
                //Divider()
                // This needs to turn in to a tab bar
                VStack(alignment: .center) {
                    //Text("👨🏻‍💼 MR🌐Tracker")
                    Text("")
                        .font(.title)
                        .toolbar {
                            ToolbarItemGroup(placement: .automatic) {
                                HStack {
                                    Button(action: {
                                        fetchData()
                                        
                                    }) {
                                        VStack(alignment: .center) {
                                            Image(systemName: "arrow.clockwise")
                                                .resizable()
                                                .frame(width: 20, height: 20)
                                                .aspectRatio(contentMode: .fit)
                                            Text("Refresh")
                                                .font(.body)
                                                .foregroundColor(.blue)
                                        }
                                    }

                                }
                            }
                        }
                }

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
        case 50..<70:
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
    let chartList: String

    @State private var comments: [Comments]?

    var body: some View {
        VStack {
            // Fetch and display data from the third API
            if let comments = comments {
                List(comments) { comment in
                    if chartList == "CHART" {
                        NavigationLink(destination: ChartView(server: server,username: username,serialNumber: comment.serialNumber, description: comment.description)) {
                            VStack(alignment: .leading) {
                                Text("\(comment.description)")
                                //.padding()
                                    //.background(Color.blue.opacity(0.2)) // Set background color here
                                    .cornerRadius(8) // Add corner radius for a rounded look
                                //Divider()
                                //Text("  ► \(comment.battery_status)\(comment.marker)\(comment.ago): //🏃\(comment.distance)km ")
                                //Text("📍\(comment.address)")
                            }
                        }
                        } else {
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
                       // }
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
                .foregroundColor(Color.black)
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

struct Distances: Codable, Identifiable {
    var id: UUID {
        return UUID()
    }
    let TagDescription: String
    let TagSerial: String
    let TagDate: String
    let TagKm: Int
}

var id: UUID {
    return UUID()
}

struct Locations: Codable, Identifiable {
    var id: UUID = UUID()
    let Sample_Date_Time: String
    let iCloud_Date_Time: String
    let description: String
    let address: String
    let home_latitude: Double
    let home_longitude: Double
    let latitude: Double
    let longitude: Double

    private enum CodingKeys: String, CodingKey {
        case Sample_Date_Time
        case iCloud_Date_Time
        case description
        case address
        case home_latitude
        case home_longitude
        case latitude
        case longitude
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
