"""Run with python -m unittest discover -s referral_network -p 'test_*.py'."""
import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path
from import_partners import import_partners, ROOT

class ImportTests(unittest.TestCase):
    def test_import_all_and_preserve_outreach_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.sqlite3"
            first = import_partners(db_path)
            with sqlite3.connect(db_path) as db:
                db.execute("UPDATE referral_partners SET partnership_status='contacted' WHERE organization_name='Solid Ground'")
                db.commit()
            second = import_partners(db_path)
            self.assertEqual(first, 73)
            self.assertEqual(second, first)
            with sqlite3.connect(db_path) as db:
                self.assertEqual(db.execute("SELECT service_area FROM referral_partners WHERE organization_name='Southwest Health and Human Services'").fetchone()[0], "Redwood; Lyon")
            with sqlite3.connect(db_path) as db:
                status = db.execute("SELECT partnership_status FROM referral_partners WHERE organization_name='Solid Ground'").fetchone()[0]
                self.assertEqual(status, "contacted")
                self.assertEqual(db.execute("SELECT COUNT(*) FROM referral_partners WHERE partnership_status='approved'").fetchone()[0], 0)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM referral_partners WHERE verification_status='verified'").fetchone()[0], 0)
                self.assertEqual(db.execute("SELECT service_area FROM referral_partners WHERE organization_name='360 Communities'").fetchone()[0], "Dakota")
                self.assertEqual(db.execute("SELECT COUNT(*) FROM referral_partners WHERE phone IS NOT NULL").fetchone()[0] > 0, True)

if __name__ == "__main__":
    unittest.main()
