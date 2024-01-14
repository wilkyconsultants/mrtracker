//
//  ContentView.swift
//  20240111 login, switch to tag type list with counts
//
//  Created by Rob Wilkinson on 2024-01-13.
//

import SwiftUI

struct ContentView: View {
    @AppStorage("username") var username: String = ""
    @AppStorage("password") var password: String = ""
    @AppStorage("server") var server: String = ""
    @State private var token: String? = nil
    @State private var showAlert = false
    @State private var errorMessage = ""
    @State private var authenticated = false
    @State private var showWebView = false
    @State private var isLoading = false

    var body: some View {
        NavigationView {
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
                }
                .multilineTextAlignment(TextAlignment .center)

                if authenticated {
                    NavigationLink(destination: TagListView(username: username,server: server, token: token ?? ""), isActive: $authenticated) {
                        EmptyView()
                    }
                    .hidden()
                } else {
                    EmptyView()
                }
            }
            .padding()
            .navigationTitle("👨🏻‍💼 MR🌐Tracker")
            .overlay(
                loadingOverlay,
                alignment: .center
            )
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
            //Circle()
            //    .fill(fillColor) // Customize the color as needed
            //    .frame(width: 90, height: 90) // Adjust the size as needed
            //Ellipse()
            //    .fill(fillColor)
            //    .frame(width: 110, height: 70)
            RoundedRectangle(cornerRadius: 10)
                .fill(fillColor)
                .frame(width: 110, height: 70)
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
    @State private var showWebView = false
    @State private var isLoading = false

    var body: some View {
        VStack {
            // Display current date and time
            Text("As of \(formattedCurrentDateTime())")
                .font(.subheadline)
                .foregroundColor(.green)
                .padding()

            if let reports = reports {
                ForEach(reports) { report in
                    VStack {
                        HStack(alignment: .center) {
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ALL")) {
                                CircleLink(text: "All", count: report.all_ctr, fillColor: Color.teal, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "ACTIVE")) {
                                CircleLink(text: "Active Today", count: report.active_ctr, fillColor: Color.blue, fontSize: 16)
                            }
                        }
                        HStack(alignment: .center) {
                            Spacer()
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "AWAY")) {
                                CircleLink(text: "Away", count: report.away_ctr, fillColor: Color.yellow, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "BATTERY_WEAK")) {
                                CircleLink(text: "Battery 🪫", count: report.battery_weak_ctr, fillColor: Color.cyan, fontSize: 18)
                            }
                            NavigationLink(destination: TagDetailView(username: username,server: server, token: token, option: "LOST")) {
                                CircleLink(text: "Lost", count: report.lost_ctr, fillColor: Color.red, fontSize: 18)
                            }

                            Spacer()
                        }
                        .padding()

                        HStack(spacing: 15) {
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
                                        showWebView.toggle()
                                    }) {
                                        ZStack {
                                            Circle()
                                                .fill(circleFillColor(for: percentage))
                                            Text("Over-All Health \(percentage)%")
                                                .font(.system(size: 25))
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
                        exit(0)
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
                .sheet(isPresented: $showWebView) {
                    NavigationView {
                        if isLoading {
                            ProgressView("Loading...")
                                .progressViewStyle(CircularProgressViewStyle(tint: .blue))
                                .scaleEffect(2.0)
                                .padding()
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 0) {
                                        isLoading = false
                                    }
                                }
                        } else {
                            WebView(urlString: "https://\(server)/theme/network-chart/TODAY")
                                .navigationTitle("📊 Tag Health")
                                .navigationBarItems(trailing:
                                    Button("Done") {
                                        showWebView = false
                                    }
                                )
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
        case 0..<30:
            return .red
        case 30..<60:
            return .yellow
        case 60..<74:
            return .orange
        default:
            return .green
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/tag_list_api?option=REPORT&user_id=\(username)") else {
            return
        }

        var request = URLRequest(url: url)
        request.addValue("Token \(token)", forHTTPHeaderField: "Authorization")

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
        dateFormatter.dateStyle = .long
        dateFormatter.timeStyle = .medium
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
                    NavigationLink(destination: CommentDetailView(comment: comment,server: server)) {
                        VStack(alignment: .leading) {
                            Text("\(comment.description)")
                                //.padding()
                                .background(Color.blue.opacity(0.2)) // Set background color here
                                .cornerRadius(8) // Add corner radius for a rounded look
                            //Divider()
                            Text("  ► \(comment.battery_status):\(comment.marker)/ \(comment.ago) : \(comment.distance)km ")
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
        request.addValue("Token \(token)", forHTTPHeaderField: "Authorization")

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
    let comment: Comments
    let server: String

    var body: some View {
        VStack {
            //Text("Description: \(comment.description)")
            //Text("Address: \(comment.address)")

            WebView(urlString: "https://\(server)/theme/show_map2_mobile/\(comment.serialNumber)/\(currentDate())")
        }
        //.navigationTitle("Comment Detail")
    }

    private func currentDate() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"  // Corrected date format
        return formatter.string(from: Date())
    }
}

struct WebView: UIViewRepresentable {
    let urlString: String

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.navigationDelegate = context.coordinator
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        if let url = URL(string: urlString) {
            let request = URLRequest(url: url)
            uiView.load(request)
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, WKNavigationDelegate {
        var parent: WebView

        init(_ parent: WebView) {
            self.parent = parent
        }
    }
}
import WebKit
struct MapView: UIViewRepresentable {
    let serialNumber: String
    let server: String

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.navigationDelegate = context.coordinator
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        let currentDate = DateFormatter.localizedString(from: Date(), dateStyle: .short, timeStyle: .none)
        let mapURLString = "https://\(server)/theme/show_map2_mobile/\(serialNumber)/\(currentDate)"
        if let mapURL = URL(string: mapURLString) {
            let request = URLRequest(url: mapURL)
            uiView.load(request)
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, WKNavigationDelegate {
        var parent: MapView

        init(_ parent: MapView) {
            self.parent = parent
        }
    }
}

struct MapViewBG: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        if let url = URL(string: "https://www.google.com/maps") {
            let request = URLRequest(url: url)
            webView.load(request)
        }
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
struct HealthReportView: View {
    @State private var healths: [Healths] = []
    let server: String

    var body: some View {
        NavigationView {
            List {
                // Table Headers
                HStack {
                    Text("Time").frame(maxWidth: .infinity)
                    Text("All").frame(maxWidth: .infinity)
                    Text("Act").frame(maxWidth: .infinity)
                    Text("Away").frame(maxWidth: .infinity)
                    Text("Lost").frame(maxWidth: .infinity)
                    Text("🪫").frame(maxWidth: .infinity)
                    Text("%").frame(maxWidth: .infinity)
                }
                .padding()
                .background(Color.gray.opacity(0.2))

                // Table Rows
                ForEach(healths) { health in
                    HStack {
                        Text(health.Date_time).frame(maxWidth: .infinity)
                            .frame(maxWidth: .infinity)
                            .lineLimit(1)  // Set line limit to 1
                            .truncationMode(.tail)  // Truncate with ellipsis if needed

                        Text(health.all_ctr).frame(maxWidth: .infinity)
                        Text(health.active_ctr).frame(maxWidth: .infinity)
                        Text(health.away_ctr).frame(maxWidth: .infinity)
                        Text(health.lost_ctr).frame(maxWidth: .infinity)
                        Text(health.battery_weak_ctr).frame(maxWidth: .infinity)
                        Text(health.healthy_ctr).frame(maxWidth: .infinity)
                    }
                    .padding()
                    .background(Color.green)
                }
            }
            .navigationBarTitle("Health Report")
            .onAppear {
                fetchData()
            }
        }
    }

    func fetchData() {
        guard let url = URL(string: "https://\(server)/theme/tag_health_api/") else {
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data, error == nil else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            do {
                let decodedData = try JSONDecoder().decode([Healths].self, from: data)
                DispatchQueue.main.async {
                    self.healths = decodedData
                }
            } catch {
                print("Error decoding data: \(error.localizedDescription)")
            }
        }.resume()
    }
}

// id has to be UUID() type or the data is all the same for all rows
struct Comments: Codable, Identifiable {
    let id = UUID()
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
    let id = UUID()
    let all_ctr: String
    let active_ctr: String
    let away_ctr: String
    let lost_ctr: String
    let healthy_ctr: String
    let battery_weak_ctr: String
    let type: String
}

struct Healths: Codable, Identifiable {
    let id = UUID()
    let Date_time: String
    let all_ctr: String
    let active_ctr: String
    let away_ctr: String
    let lost_ctr: String
    let battery_weak_ctr: String
    let healthy_ctr: String
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
