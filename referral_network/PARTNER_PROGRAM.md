# Referral-source preferred-provider program

## Important distinction
These organizations are **prospects**, not contracted referral partners. Do not advertise an organization as endorsing, recommending, approving, or preferring Section 8 Rentals and More without a written, authorized agreement. Do not offer referral fees, gifts, or benefits to public employees or caseworkers. Do not imply exclusive placement rights or government affiliation.

## Partner outreach sequence
1. Verify the agency's current website, public referral contact, geography, and authority to enter partnerships. Preserve dated evidence in the audit log.
2. Ask whether it accepts external housing resource providers, and obtain its referral/vendor onboarding rules.
3. Demonstrate the matching workflow with synthetic cases and listings; identify limitations and tenant privacy controls.
4. Request a nonexclusive written collaboration or resource-listing agreement. If the agency uses a formal procurement or preferred-provider process, follow it rather than claiming preferential access.
5. Document the agency's exact permitted designation, effective date, renewal date, referral workflow, data sharing terms, and termination conditions.
6. Only after approvals and security review, enable named agency users, consent-based referrals, and limited access to their own cases.
7. Track service-level performance: time to acknowledge, candidate listings reviewed, placements confirmed, and referrals closed; never promise guaranteed placement.

## Initial outreach email
Subject: Housing referral resource for your clients in the Twin Cities

Hello,

I founded Section 8 Rentals and More to help housing navigators identify potentially suitable rental opportunities for households seeking housing in the Twin Cities.

We are developing a structured referral and rental-matching workflow that considers location, bedrooms, rent limits, and accessibility needs. Any results are preliminary and require verification of availability and applicable program requirements.

Could you direct me to the person who evaluates housing resource providers or community referral partnerships? I would welcome a brief demonstration and an opportunity to learn your organization's onboarding and privacy requirements.

We are not seeking to represent ourselves as affiliated with your organization without its authorization.

Thank you,
Section 8 Rentals and More

## Tracking
Use partnership statuses `not_contacted`, `contacted`, `interested`, `approved`, `declined`, `inactive`. The `approved` status is an internal workflow marker, not proof of an agency endorsement or preferential designation. A separate written agreement record and approved language are required before any public preferred-provider claim.

## Matching limitations
The development matching engine only uses records deliberately entered into `rental_inventory`. HCV rent caps do not by themselves establish eligibility. Payment standards, utility allowances, rent reasonableness, landlord participation, inspection and PHA approval require separate verification. The matching engine does not rank by protected characteristics or make tenancy decisions.
