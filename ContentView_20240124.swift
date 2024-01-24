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

struct ContentView: View {
    //UserDefaults variables - universaly shared with the entire application
    @AppStorage("username") var username: String = ""
    @AppStorage("password") var password: String = ""
    @AppStorage("server") var server: String = ""
    //
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
                                                .foregroundColor(.green)
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
                                                .foregroundColor(.green)
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

                    //Map()
                    VStack {
                    Map()
                        .ignoresSafeArea(.all, edges: .bottom)
                    Spacer()
                    Text("Welcome to  MR🌐Tracker")
                        .font(.system(size: 60))
                        .foregroundColor(.green)
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


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
