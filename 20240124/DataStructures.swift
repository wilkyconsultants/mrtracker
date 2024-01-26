
//
//  DataStructures.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//

import SwiftUI

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
