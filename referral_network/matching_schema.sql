-- Candidate listings for development matching; no real listing inventory is imported.
CREATE TABLE IF NOT EXISTS rental_inventory (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 listing_reference TEXT NOT NULL UNIQUE,
 county TEXT NOT NULL CHECK(county IN ('Hennepin','Ramsey','Dakota','Anoka','Washington')),
 bedrooms INTEGER NOT NULL CHECK(bedrooms BETWEEN 0 AND 10),
 monthly_rent INTEGER NOT NULL CHECK(monthly_rent BETWEEN 0 AND 20000),
 accessible INTEGER NOT NULL DEFAULT 0 CHECK(accessible IN (0,1)),
 accepts_hcv INTEGER NOT NULL DEFAULT 0 CHECK(accepts_hcv IN (0,1)),
 availability TEXT NOT NULL DEFAULT 'unverified' CHECK(availability IN ('unverified','available','unavailable')),
 last_confirmed_at TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_inventory_matching ON rental_inventory(county,availability,bedrooms,monthly_rent);
CREATE TABLE IF NOT EXISTS rental_match_reviews (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 referral_id INTEGER NOT NULL REFERENCES housing_referrals(id),
 listing_id INTEGER NOT NULL REFERENCES rental_inventory(id),
 review_status TEXT NOT NULL DEFAULT 'candidate' CHECK(review_status IN ('candidate','reviewed','rejected')),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(referral_id,listing_id)
);
