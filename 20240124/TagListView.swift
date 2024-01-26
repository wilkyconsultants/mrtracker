
//
//  TermsView.swift
//  20240111 Example login, switch to tag type list with counts
//
//  Created by Robert A Wilkinson on 2024-01-24.
//
import SwiftUI

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
