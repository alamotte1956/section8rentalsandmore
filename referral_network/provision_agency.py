"""Provision an invited agency account offline. Do not expose as a public HTTP route."""
import argparse
import getpass
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

def provision(db_path, partner_id, email, password, role="caseworker"):
    if role not in ("caseworker","agency_manager") or len(password)<16:
        raise ValueError("Role invalid or password shorter than 16 characters")
    with sqlite3.connect(db_path) as db:
        db.execute("PRAGMA foreign_keys=ON")
        partner=db.execute("""SELECT id FROM referral_partners WHERE id=? AND
           verification_status='verified' AND partnership_status='approved'""",(partner_id,)).fetchone()
        if not partner:
            raise ValueError("Partner must be verified and approved")
        db.execute("""INSERT INTO agency_users(partner_id,email,password_hash,role)
          VALUES(?,?,?,?)""",(partner_id,email.strip().lower(),generate_password_hash(password),role))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--db",type=Path,required=True)
    p.add_argument("--partner-id",type=int,required=True)
    p.add_argument("--email",required=True)
    p.add_argument("--role",choices=("caseworker","agency_manager"),default="caseworker")
    a=p.parse_args()
    provision(a.db,a.partner_id,a.email,getpass.getpass("Temporary password (16+ chars): "),a.role)
    print("Agency account provisioned; distribute credentials through an approved secure channel.")
