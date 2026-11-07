"""Agency isolation and consent tests using synthetic organizations."""
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from werkzeug.security import generate_password_hash

class AgencyPortalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.previous={k:os.environ.get(k) for k in ("FLASK_SECRET_KEY","REFERRAL_ADMIN_PASSWORD","REFERRAL_DB_PATH")}
        os.environ.update(FLASK_SECRET_KEY="test-secret",REFERRAL_ADMIN_PASSWORD="test-admin",
                          REFERRAL_DB_PATH=str(Path(self.tmp.name)/"db.sqlite3"))
        from import_partners import import_partners
        from referral_routes import init_referral_schema
        import_partners(Path(os.environ["REFERRAL_DB_PATH"]))
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            init_referral_schema(db,Path(__file__).with_name("referral_schema.sql"))
            db.executescript(Path(__file__).with_name("agency_schema.sql").read_text())
            ids=[r[0] for r in db.execute("SELECT id FROM referral_partners ORDER BY id LIMIT 2")]
            self.ids=ids
            for i,pid in enumerate(ids):
                db.execute("UPDATE referral_partners SET verification_status='verified',partnership_status='approved' WHERE id=?",(pid,))
                db.execute("INSERT INTO agency_users(partner_id,email,password_hash,role) VALUES(?,?,?,'caseworker')",
                           (pid,f"worker{i}@example.test",generate_password_hash("test-password-long-123")))
            db.execute("""INSERT INTO housing_referrals(partner_id,external_case_reference,county,bedrooms_needed,
              maximum_rent,housing_program,consent_attested) VALUES(?, 'OTHERCASE1','Dakota',2,1500,'HCV',1)""",(ids[1],))
        from admin_app import app
        app.config.update(TESTING=True,SESSION_COOKIE_SECURE=False)
        self.client=app.test_client()

    def tearDown(self):
        for k,v in self.previous.items():
            if v is None:os.environ.pop(k,None)
            else:os.environ[k]=v
        self.tmp.cleanup()

    def test_agency_isolation_and_consent(self):
        self.assertEqual(self.client.get("/agency/").status_code,302)
        self.assertEqual(self.client.post("/agency/login",data={"email":"worker0@example.test","password":"test-password-long-123"}).status_code,302)
        response=self.client.get("/agency/")
        self.assertEqual(response.status_code,200)
        self.assertNotIn(b"OTHERCASE1",response.data)
        with self.client.session_transaction() as s:csrf=s["agency_csrf"]
        data={"csrf":csrf,"external_case_reference":"MYCASE001","county":"Dakota",
              "bedrooms_needed":"2","maximum_rent":"1500","housing_program":"HCV"}
        self.assertEqual(self.client.post("/agency/submit",data=data).status_code,400)
        data["consent_attested"]="1"
        self.assertEqual(self.client.post("/agency/submit",data=data).status_code,302)
        self.assertIn(b"MYCASE001",self.client.get("/agency/").data)
        self.assertNotIn(b"OTHERCASE1",self.client.get("/agency/").data)
        self.assertEqual(self.client.post("/agency/submit",data=data).status_code,409)
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            self.assertEqual(db.execute("SELECT partner_id FROM housing_referrals WHERE external_case_reference='MYCASE001'").fetchone()[0],self.ids[0])

if __name__=="__main__":unittest.main()
