# Referral administration dashboard (development)

This is a standalone Flask admin application, **not yet integrated with the deployed Section 8 website**. The development branch does not change production data or grant agency accounts.

## Local testing

Use Python 3.11+ in a virtual environment. Install dependencies with:

```bash
pip install -r referral_network/requirements.txt
python -m unittest discover -s referral_network -p 'test_*.py'
```

Before running the server, set three environment variables:
- `FLASK_SECRET_KEY`: strong random secret; never commit it
- `REFERRAL_ADMIN_PASSWORD`: unique strong administrator password; never commit it
- `REFERRAL_DB_PATH`: absolute path to a **new** test SQLite database

Then run `python referral_network/admin_app.py`. The local server binds to 127.0.0.1:8766.

**Do not expose the development server to the public Internet.** The secure session cookie requires HTTPS. Production needs a proper WSGI server, HTTPS termination, secure persistent database, backups, rate limiting, administrator MFA, and review of authentication and authorization. The shared administrator password is a development-only bootstrap mechanism.

The admin app supports viewing and filtering prospect organizations, updating outreach status, and recording an audit event for each update. Only already-verified organizations may be approved. There is currently no UI to verify organizations; this must be built with role-based authorization and audit logging before partner approval.

Data sources include 65 prospect entries from the initial list and additional five-county research. Some names, contact details, and service coverage are unverified. No automated outreach is performed and no tenant personal information is stored.
