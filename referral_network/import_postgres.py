"""Safe additive PostgreSQL prospect import. No tenant information. Dry run by default.

Requires: pip install "psycopg[binary]>=3.2,<4"
Use an existing DATABASE_URL in the runtime; never print it.
"""
import argparse
import csv
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCES=("referral_partner_prospects.csv","metro_five_county_additions.csv","greater_minnesota_prospects.csv")
COUNTIES={"Hennepin","Ramsey","Dakota","Anoka","Washington","Renville","Redwood","Lyon"}

DDL="""CREATE TABLE IF NOT EXISTS section8_referral_partner_prospects (
 id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 organization_name TEXT NOT NULL UNIQUE,
 service_counties TEXT,
 referral_category TEXT,
 priority TEXT NOT NULL DEFAULT 'review',
 source_url TEXT,
 public_phone TEXT,
 public_email TEXT,
 verification_status TEXT NOT NULL DEFAULT 'needs_verification',
 partnership_status TEXT NOT NULL DEFAULT 'not_contacted',
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 CONSTRAINT prospect_verification_check CHECK (verification_status IN ('needs_verification','official_site_identified','verified')),
 CONSTRAINT prospect_partnership_check CHECK (partnership_status IN ('not_contacted','contacted','interested','approved','declined','inactive'))
)"""

def load():
    rows={}
    for source in SOURCES:
        with (ROOT/source).open(encoding="utf-8-sig",newline="") as f:
            for item in csv.DictReader(f):
                name=item["organization_name"].strip()
                if not name: continue
                if name in rows: continue
                counties="; ".join(c for c in (v.strip() for v in item.get("service_counties","").split(";")) if c in COUNTIES)
                verification=item.get("verification_status","needs_verification")
                if verification not in ("needs_verification","official_site_identified"): verification="needs_verification"
                rows[name]=(name,counties,item.get("referral_category") or None,
                    item.get("priority") if item.get("priority") in ("high","review","low") else "review",
                    item.get("source_url") or None,item.get("public_phone") or None,
                    item.get("public_email") or None,verification)
    return list(rows.values())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--execute",action="store_true",help="Commit new prospects (default: rollback preview)")
    args=p.parse_args()
    url=os.environ.get("DATABASE_URL")
    if not url: raise SystemExit("DATABASE_URL must be set securely in the environment")
    import psycopg
    rows=load()
    with psycopg.connect(url,connect_timeout=10,sslmode="require") as db:
        with db.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(78191208)")
            cur.execute(DDL)
            new=0
            for row in rows:
                cur.execute("""INSERT INTO section8_referral_partner_prospects
                 (organization_name,service_counties,referral_category,priority,source_url,public_phone,public_email,verification_status)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (organization_name) DO NOTHING RETURNING id""",row)
                if cur.fetchone(): new+=1
            print(f"Prospects in input: {len(rows)}; newly inserted: {new}; existing preserved: {len(rows)-new}")
            if args.execute:
                db.commit()
                print("Committed. No existing records updated.")
            else:
                db.rollback()
                print("Preview only; transaction rolled back.")

if __name__=="__main__":main()
