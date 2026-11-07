"""Dashboard smoke and security tests. Requires Flask."""
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

class AdminTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = {k: os.environ.get(k) for k in ("FLASK_SECRET_KEY","REFERRAL_ADMIN_PASSWORD","REFERRAL_DB_PATH")}
        os.environ.update(FLASK_SECRET_KEY="testing-only-secret-key-not-for-production",
                          REFERRAL_ADMIN_PASSWORD="testing-password",
                          REFERRAL_DB_PATH=str(Path(self.tmp.name)/"test.sqlite3"))
        from import_partners import import_partners
        import_partners(Path(os.environ["REFERRAL_DB_PATH"]))
        from admin_app import app
        app.config.update(TESTING=True, SESSION_COOKIE_SECURE=False)
        self.client = app.test_client()

    def tearDown(self):
        for key, val in self.old.items():
            if val is None: os.environ.pop(key, None)
            else: os.environ[key] = val
        self.tmp.cleanup()

    def test_authentication_and_approval_guard(self):
        self.assertEqual(self.client.get("/").status_code,302)
        self.assertEqual(self.client.post("/login",data={"password":"wrong"}).status_code,200)
        self.assertEqual(self.client.post("/login",data={"password":"testing-password"}).status_code,302)
        self.assertIn(b"Referral prospects",self.client.get("/").data)
        with self.client.session_transaction() as s: csrf=s["csrf"]
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            partner_id=db.execute("SELECT id FROM referral_partners WHERE organization_name='360 Communities'").fetchone()[0]
        endpoint=f"/partner/{partner_id}/status"
        self.assertEqual(self.client.post(endpoint,data={"status":"approved","csrf":csrf}).status_code,400)
        self.assertEqual(self.client.post(endpoint,data={"status":"contacted","csrf":"wrong"}).status_code,403)
        self.assertEqual(self.client.post(endpoint,data={"status":"contacted","csrf":csrf,"note":"Initial outreach"}).status_code,302)
        with sqlite3.connect(os.environ["REFERRAL_DB_PATH"]) as db:
            self.assertEqual(db.execute("SELECT partnership_status FROM referral_partners WHERE id=?",(partner_id,)).fetchone()[0],"contacted")
            self.assertEqual(db.execute("SELECT COUNT(*) FROM referral_partner_events WHERE partner_id=?",(partner_id,)).fetchone()[0],1)

if __name__=="__main__":
    unittest.main()
