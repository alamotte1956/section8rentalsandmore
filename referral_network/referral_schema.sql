-- Privacy-minimized referral workflow. Never store tenant names, DOB, SSN, voucher numbers, or health data.
CREATE TABLE IF NOT EXISTS housing_referrals (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 partner_id INTEGER NOT NULL REFERENCES referral_partners(id),
 external_case_reference TEXT NOT NULL,
 county TEXT NOT NULL CHECK(county IN ('Hennepin','Ramsey','Dakota','Anoka','Washington','Renville','Redwood','Lyon')),
 bedrooms_needed INTEGER NOT NULL CHECK(bedrooms_needed BETWEEN 0 AND 10),
 maximum_rent INTEGER CHECK(maximum_rent IS NULL OR maximum_rent BETWEEN 0 AND 20000),
 housing_program TEXT NOT NULL CHECK(housing_program IN ('HCV','other_subsidy','market_rate','unknown')),
 accessibility_requested INTEGER NOT NULL DEFAULT 0 CHECK(accessibility_requested IN (0,1)),
 consent_attested INTEGER NOT NULL CHECK(consent_attested = 1),
 status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new','reviewing','matched','closed')),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(partner_id,external_case_reference)
);
CREATE INDEX IF NOT EXISTS idx_housing_referrals_county_status ON housing_referrals(county,status);
CREATE TABLE IF NOT EXISTS housing_referral_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 referral_id INTEGER NOT NULL REFERENCES housing_referrals(id),
 event_type TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
