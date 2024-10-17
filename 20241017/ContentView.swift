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
// 2024-01-23 -Version 1.5 - distance chart
// 2024-01-24 -Version 1.6 - search bar
// 2024-01-25 -Version 1.7 - battery chart
// 2024-01-25              - perf chart
// 2024-01-27 -Version 1.8 - drill down
// 2024-02-01 -Version 1.9 - auto login
// 2024-02-03 -Version 2.0 - Clean up a bit
// 2024-02-04 -Version 2.1 - map color red + only show action of alert if not disabled
// 2024-02-04 -Version 2.2 - add a device map
// 2024-02-05 -Version 2.3 - revamp look
// 2024-02-07 -Version 2.4 - back-end perf+
// 2024-02-15 -Version 2.5 - fix tokens
// 2024-02-15 -Version 2.5 - dist>0, green color otherwise blue
// 2024-05-15 -Version 2.6 - default saved for days to map
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
    
    @State private var flash = false

    
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
                                            Text("Terms of Use")
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
                                //        NavigationLink(destination: TermsView()) {
                                //            VStack(alignment: .center) {
                                //                Image(systemName: "person.crop.circle.badge.questionmark")
                                //                    .resizable()
                                //                    .frame(width: 20, height: 20)
                                //                    .aspectRatio(contentMode: .fit)
                                //                Text("Terms & Conditions")
                                //                    .font(.body)
                                //                    .foregroundColor(.blue)
                                //            }
                                //    } //
                                  }
                                }
                            }
                    }

                    //Map()
                    VStack {
                  //  Map()
                  //      .ignoresSafeArea(.all, edges: .bottom)
                    Spacer()
                    Text("Welcome to")
                            .font(.system(size: 40))
                            .foregroundColor(.green)
                    Text("MR🌐Tracker")
                            .font(.system(size: 40))
                            .foregroundColor(.green)

                    Spacer()
                    HStack {
                            Spacer()
                        Image(systemName: "car.fill")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(width: 60, height: 60) // Adjust size as needed
                            .foregroundColor(.pink)
                            .padding(.vertical, 5)
                            .opacity(flash ? 1.5 : 0.5) // Use a ternary operator to alternate between 1.0 and 0.5 opacity
                            .onAppear {
                                withAnimation(Animation.easeInOut(duration: 1).repeatForever()) {
                                    flash.toggle()
                                }
                            }
                            Spacer()
                        }
                    Spacer()
                    Text("This iOS application enables you to track the movements of your vital assets. It comprises a backend database server that gathers location data from various devices and communicates with the iOS frontend through REST APIs. To fully utilize this application, a dedicated server is essential to serve as a data repository and API service engine. While we provide the application and server software at no cost, you are responsible for providing the server component.")
                        .font(.system(size: 18))
                        .foregroundColor(.blue)
                        .padding(10)

                    Text("For further information, please reach out to us or refer to the Information button located at the top of the screen.")
                            .font(.system(size: 18))
                            .foregroundColor(.blue)
                            .padding(10)

                            .toolbar {

                    ToolbarItem(placement: .bottomBar) {
                        HStack {
                            NavigationLink(destination: TagListView(username: username, server: server, token: token ?? "", chartList: "")) {
                                VStack(alignment: .center) {
                                    Image(systemName: "house")
                                        .resizable()
                                        .frame(width: 20, height: 20)
                                        .aspectRatio(contentMode: .fit)
                                        .foregroundColor(.green)
                                    Text("Start Here")
                                        .font(.body)
                                        .foregroundColor(.green)
                                }
                            }

                        }
                        }
                    }
                }.padding(.horizontal, 20) 
            }
                    
                    VStack(alignment: .center) {
                            Form {
                                if authenticated == false {

                                    Text("     👨🏻‍💼 MR🌐Tracker")
                                        .font(.title)

                                    Button("Click here to Login") {
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
                                    .frame(height: 15)
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
                                            .frame(height: 40)
                                            .padding()
                                            .background(Color(.systemGray5))
                                            .cornerRadius(8)
                                        HStack {
                                                Spacer()
                                            Image(systemName: "car.fill")
                                                .resizable()
                                                .aspectRatio(contentMode: .fit)
                                                .frame(width: 60, height: 60) // Adjust size as needed
                                                .foregroundColor(.blue)
                                                .padding(.vertical, 5)
                                                .opacity(flash ? 1.5 : 0.5) // Use a ternary operator to alternate between 1.0 and 0.5 opacity
                                                .onAppear {
                                                    withAnimation(Animation.easeInOut(duration: 1).repeatForever()) {
                                                        flash.toggle()
                                                    }
                                                }
                                                Spacer()
                                            }
                                        VStack {

                                            
                                        }
                                       // Text("For Demo:")
                                       //     .foregroundColor(.brown)
                                       // Text("username: demo")
                                       //     .foregroundColor(.green)
                                       // Text("password: ")
                                       //     .foregroundColor(.green)
                                        
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
        
        if username == "demo" {
            password = "Bluetooth!!"
        }
        if server == "" {
            server = "mrrobby.ca"
        }
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
