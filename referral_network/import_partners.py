"""Import original and five-county referral prospects into SQLite without overwriting outreach decisions."""
import argparse
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ("referral_partner_prospects.csv", "metro_five_county_additions.csv")
COUNTIES = {"Hennepin", "Ramsey", "Dakota", "Anoka", "Washington"}

def import_partners(db_path: Path, source_dir: Path = ROOT):
    with sqlite3.connect(db_path) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript((source_dir / "schema.sql").read_text(encoding="utf-8"))
        for filename in SOURCES:
            with (source_dir / filename).open(newline="", encoding="utf-8-sig") as file:
                for row in csv.DictReader(file):
                    name = row["organization_name"].strip()
                    if not name:
                        continue
                    # source_identified is evidence of a candidate source, not completed verification.
                    status = row.get("verification_status", "needs_verification")
                    if status not in ("needs_verification", "official_site_identified", "verified"):
                        status = "needs_verification"
                    counties = "; ".join(
                        c for c in (v.strip() for v in row.get("service_counties", "").split(";"))
                        if c in COUNTIES
                    )
                    db.execute("""
                        INSERT INTO referral_partners
                        (organization_name, verification_status, partnership_status, priority,
                         website, phone, email, service_area, notes)
                        VALUES (?, ?, 'not_contacted', ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(organization_name) DO UPDATE SET
                            website=COALESCE(NULLIF(referral_partners.website,''), excluded.website),
                            phone=COALESCE(NULLIF(referral_partners.phone,''), excluded.phone),
                            email=COALESCE(NULLIF(referral_partners.email,''), excluded.email),
                            service_area=COALESCE(NULLIF(referral_partners.service_area,''), excluded.service_area),
                            notes=COALESCE(NULLIF(referral_partners.notes,''), excluded.notes)
                    """, (name, status, row.get("priority", "review"),
                          row.get("source_url") or None, row.get("public_phone") or None,
                          row.get("public_email") or None, counties or None,
                          row.get("referral_category") or None))
        return db.execute("SELECT COUNT(*) FROM referral_partners").fetchone()[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True,
                        help="SQLite database path; use a test database first")
    args = parser.parse_args()
    print(f"Total referral prospects: {import_partners(args.db)}")
