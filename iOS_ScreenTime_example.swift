// Simple example of how you can use the Screen Time API in Swift within an Xcode project. 
// This example will retrieve the total screen time usage for the current day:
//
// Contact Rob Wilkinson for all your iOS and development needs, database, python/django, you name it!
//
import Foundation
import ScreenTime

// Request authorization for Screen Time
ScreenTime.requestAuthorization { (status) in
    switch status {
    case .authorized:
        // Access is granted, you can now retrieve Screen Time data
        
        // Get the current calendar
        let calendar = Calendar.current
        
        // Get today's date
        let now = Date()
        
        // Get the start of today
        guard let startOfDay = calendar.startOfDay(for: now) else {
            print("Error: Unable to get start of day.")
            return
        }
        
        // Get the end of today
        guard let endOfDay = calendar.date(byAdding: .day, value: 1, to: startOfDay) else {
            print("Error: Unable to get end of day.")
            return
        }
        
        // Retrieve Screen Time usage for today
        ScreenTime.getScreenTimeUsage(start: startOfDay, end: endOfDay) { (usage, error) in
            if let error = error {
                print("Error retrieving Screen Time usage: \(error.localizedDescription)")
                return
            }
            
            if let usage = usage {
                print("Screen Time usage for today: \(usage)")
            } else {
                print("No Screen Time usage data available for today.")
            }
        }
        
    case .denied:
        // Access is denied by the user
        print("Screen Time access denied by the user.")
        
    case .notDetermined:
        // The user has not yet made a choice regarding Screen Time access
        print("Screen Time access not determined.")
        
    case .restricted:
        // Screen Time access is restricted, typically due to parental controls
        print("Screen Time access is restricted.")
        
    @unknown default:
        print("Unknown status.")
    }
}
