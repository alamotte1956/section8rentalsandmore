"""Import prospect organizations into a local SQLite database. Safe to rerun."""
import argparse
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def import_partners(db_path: Path, csv_path: Path):
    with sqlite3.connect(db_path) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
        with csv_path.open(newline="", encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                db.execute("""
                    INSERT INTO referral_partners
                    (organization_name, verification_status, partnership_status, priority)
                    VALUES (:organization_name,:verification_status,:partnership_status,:priority)
                    ON CONFLICT(organization_name) DO NOTHING
                """, row)
        return db.execute("SELECT COUNT(*) FROM referral_partners").fetchone()[0]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", type=Path, required=True, help="SQLite database path; use a test database first")
    args = p.parse_args()
    print(f"Total partners: {import_partners(args.db, ROOT / 'referral_partner_prospects.csv')}")
