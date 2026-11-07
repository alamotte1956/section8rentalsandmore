# Referral network — Phase 1

29 unique prospects transcribed from user-supplied images. Names and geographic fit require confirmation. **No partnership is implied.**

Run against a new test SQLite file first:

```bash
python referral_network/import_partners.py --db referral_network_test.sqlite3
```

Import is idempotent and does not overwrite existing status or contact details. This repository currently contains standalone website assets and API fragments; do not assume the production application database uses this schema. Do not execute against production until the actual deployed app/database is identified, backed up, and a migration is reviewed.

Next: implement authenticated admin CRUD, agency verification and approval, privacy-conscious caseworker intake, consent and audit logs, matching integration, and email delivery tests. Never expose unverified organizations as approved partners or store client PII in this prospect table.
