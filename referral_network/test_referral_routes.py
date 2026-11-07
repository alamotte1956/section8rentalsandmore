"""Admin-only referral intake security regression tests."""
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

class ReferralTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.previous={k:os.environ.get(k) for k in ("FLASK_SECRET_KEY","REFERRAL_ADMIN_PASSWORD","REFERRAL_DB_PATH")}
        os.environ.update(FLASK_SECRET_KEY="test-secret-only",REFERRAL_ADMIN_PASSWORD="test-password",
                          REFERRAL_DB_PATH=str(Path(self.tmp.name)/"test.sqlite3"))
        from import_partners import import_partners
        from referral_routes import init_referral_schema
        import_partners(Path(os.environ["REFERRAL_DB_PATH"]))
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            init_referral_schema(db,Path(__file__).with_name("referral_schema.sql"))
            self.partner_id=db.execute("SELECT id FROM referral_partners WHERE organization_name='360 Communities'").fetchone()[0]
        from admin_app import app
        app.config.update(TESTING=True,SESSION_COOKIE_SECURE=False)
        self.client=app.test_client()

    def tearDown(self):
        for k,v in self.previous.items():
            if v is None:os.environ.pop(k,None)
            else:os.environ[k]=v
        self.tmp.cleanup()

    def test_approval_consent_and_intake(self):
        self.assertEqual(self.client.get("/referrals/").status_code,403)
        self.client.post("/login",data={"password":"test-password"})
        with self.client.session_transaction() as s: csrf=s["csrf"]
        payload={"csrf":csrf,"partner_id":self.partner_id,"external_case_reference":"CASE_0001",
                 "county":"Dakota","bedrooms_needed":"2","maximum_rent":"1500","housing_program":"HCV"}
        self.assertEqual(self.client.post("/referrals/",data=payload).status_code,400)
        payload["consent_attested"]="1"
        self.assertEqual(self.client.post("/referrals/",data=payload).status_code,403)
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            db.execute("UPDATE referral_partners SET verification_status='verified',partnership_status='approved' WHERE id=?",(self.partner_id,))
        self.assertEqual(self.client.post("/referrals/",data=payload).status_code,302)
        self.assertEqual(self.client.post("/referrals/",data=payload).status_code,409)
        self.assertIn(b"CASE_0001",self.client.get("/referrals/").data)
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM housing_referrals").fetchone()[0],1)

if __name__=="__main__":unittest.main()
