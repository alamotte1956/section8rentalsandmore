"""Greater Minnesota geography and matching tests."""
import sqlite3
import unittest
from pathlib import Path
from matching import find_candidates
from referral_routes import COUNTIES

class GreaterMinnesotaTests(unittest.TestCase):
    def test_counties_and_walnut_grove_taunton_mapping(self):
        self.assertTrue({"Renville","Redwood","Lyon"}.issubset(set(COUNTIES)))
        self.assertEqual(CITY_TO_COUNTY["Walnut Grove"],"Redwood")
        self.assertEqual(CITY_TO_COUNTY["Taunton"],"Lyon")

    def test_matching_in_each_added_county(self):
        root=Path(__file__).parent
        db=sqlite3.connect(":memory:")
        db.row_factory=sqlite3.Row
        for filename in ("schema.sql","referral_schema.sql","matching_schema.sql"):
            db.executescript((root/filename).read_text())
        db.execute("INSERT INTO referral_partners(organization_name) VALUES('Synthetic')")
        for county in ("Renville","Redwood","Lyon"):
            ref="TEST_"+county.upper()
            db.execute("""INSERT INTO housing_referrals(partner_id,external_case_reference,county,
                bedrooms_needed,maximum_rent,housing_program,consent_attested)
                VALUES(1,?,?,2,1600,'HCV',1)""",(ref,county))
            db.execute("""INSERT INTO rental_inventory(listing_reference,county,bedrooms,
                monthly_rent,accepts_hcv,availability) VALUES(?,?,2,1500,1,'available')""",
                (ref,county))
            rid=db.execute("SELECT id FROM housing_referrals WHERE external_case_reference=?",(ref,)).fetchone()[0]
            self.assertEqual([m["listing_reference"] for m in find_candidates(db,rid)],[ref])
        db.close()

from greater_minnesota import CITY_TO_COUNTY
if __name__=="__main__":unittest.main()
