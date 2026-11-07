"""Matching tests use synthetic properties only."""
import sqlite3
import unittest
from pathlib import Path
from matching import find_candidates

class MatchingTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(":memory:")
        self.db.row_factory=sqlite3.Row
        root=Path(__file__).parent
        self.db.executescript((root/"schema.sql").read_text())
        self.db.executescript((root/"referral_schema.sql").read_text())
        self.db.executescript((root/"matching_schema.sql").read_text())
        self.db.execute("INSERT INTO referral_partners(organization_name) VALUES('Synthetic Partner')")
        self.db.execute("""INSERT INTO housing_referrals(partner_id,external_case_reference,county,bedrooms_needed,
          maximum_rent,housing_program,accessibility_requested,consent_attested)
          VALUES(1,'SYNTH0001','Dakota',2,1600,'HCV',1,1)""")
        records=[("good","Dakota",2,1500,1,1,"available"),
                 ("too-expensive","Dakota",2,1800,1,1,"available"),
                 ("wrong-county","Ramsey",2,1400,1,1,"available"),
                 ("not-accessible","Dakota",2,1400,0,1,"available"),
                 ("not-hcv","Dakota",2,1400,1,0,"available"),
                 ("unverified","Dakota",2,1400,1,1,"unverified"),
                 ("too-small","Dakota",1,1400,1,1,"available")]
        self.db.executemany("""INSERT INTO rental_inventory
          (listing_reference,county,bedrooms,monthly_rent,accessible,accepts_hcv,availability)
          VALUES(?,?,?,?,?,?,?)""",records)
    def tearDown(self):self.db.close()
    def test_only_eligible_confirmed_listings(self):
        self.assertEqual([x["listing_reference"] for x in find_candidates(self.db,1)],["good"])
    def test_missing_rent_cap_does_not_claim_match(self):
        self.db.execute("UPDATE housing_referrals SET maximum_rent=NULL WHERE id=1")
        self.assertEqual(find_candidates(self.db,1),[])
    def test_missing_referral_rejected(self):
        with self.assertRaises(ValueError):find_candidates(self.db,999)

if __name__=="__main__":unittest.main()
