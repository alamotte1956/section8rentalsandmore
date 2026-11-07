-- Prospect records are not approved partners. No tenant personal data is stored here.
CREATE TABLE IF NOT EXISTS referral_partners (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 organization_name TEXT NOT NULL UNIQUE,
 verification_status TEXT NOT NULL DEFAULT 'needs_verification',
 partnership_status TEXT NOT NULL DEFAULT 'not_contacted',
 priority TEXT NOT NULL DEFAULT 'review',
 website TEXT, phone TEXT, email TEXT, service_area TEXT,
 referral_contact TEXT, notes TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CHECK (verification_status IN ('needs_verification','official_site_identified','verified')),
 CHECK (partnership_status IN ('not_contacted','contacted','interested','approved','declined','inactive')),
 CHECK (priority IN ('high','review','low'))
);
CREATE TABLE IF NOT EXISTS referral_partner_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 partner_id INTEGER NOT NULL REFERENCES referral_partners(id),
 event_type TEXT NOT NULL,
 note TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
