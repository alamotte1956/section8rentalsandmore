import sqlite3
import unittest
from datetime import datetime,timezone
from pathlib import Path
from retention import purge

class RetentionTests(unittest.TestCase):
    def test_preview_and_closed_only_deletion(self):
        db=sqlite3.connect(":memory:")
        root=Path(__file__).parent
        for name in ("schema.sql","referral_schema.sql","matching_schema.sql"):
            db.executescript((root/name).read_text())
        db.execute("INSERT INTO referral_partners(organization_name) VALUES('Synthetic')")
        for ref,status in (("CLOSED0001","closed"),("OPEN000001","new")):
            db.execute("""INSERT INTO housing_referrals(partner_id,external_case_reference,county,bedrooms_needed,
              housing_program,consent_attested,status,updated_at)
              VALUES(1,?,'Dakota',2,'HCV',1,?,'2025-01-01 00:00:00')""",(ref,status))
        self.assertEqual(purge(db,days=180,dry_run=True,now=datetime(2026,11,7,tzinfo=timezone.utc)),1)
        self.assertEqual(db.execute("SELECT COUNT(*) FROM housing_referrals").fetchone()[0],2)
        self.assertEqual(purge(db,days=180,dry_run=False,now=datetime(2026,11,7,tzinfo=timezone.utc)),1)
        self.assertEqual(db.execute("SELECT external_case_reference FROM housing_referrals").fetchone()[0],"OPEN000001")
        db.close()

if __name__=="__main__":unittest.main()
