-- Organization-scoped accounts, no public registration.
CREATE TABLE IF NOT EXISTS agency_users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 partner_id INTEGER NOT NULL REFERENCES referral_partners(id),
 email TEXT NOT NULL COLLATE NOCASE UNIQUE,
 password_hash TEXT NOT NULL,
 role TEXT NOT NULL CHECK(role IN ('caseworker','agency_manager')),
 active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_agency_users_partner ON agency_users(partner_id,active);
