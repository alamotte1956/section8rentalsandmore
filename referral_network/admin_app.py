"""Standalone referral partner admin service. Run behind HTTPS and authenticated reverse proxy.
Set REFERRAL_ADMIN_PASSWORD and FLASK_SECRET_KEY in the server environment.
Never deploy using the Flask development server in production.
"""
import os
import hmac
import secrets
import sqlite3
from pathlib import Path
from functools import wraps
from flask import Flask, abort, jsonify, redirect, render_template_string, request, session, url_for
from import_partners import import_partners

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("REFERRAL_DB_PATH", str(ROOT / "referrals.sqlite3")))
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                  SESSION_COOKIE_SECURE=True, MAX_CONTENT_LENGTH=16384)
if not app.secret_key:
    raise RuntimeError("Set FLASK_SECRET_KEY before starting referral admin")
if not os.environ.get("REFERRAL_ADMIN_PASSWORD"):
    raise RuntimeError("Set REFERRAL_ADMIN_PASSWORD before starting referral admin")

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("referral_admin"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

def csrf_ok():
    return hmac.compare_digest(session.get("csrf", ""), request.form.get("csrf", ""))

BASE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Referral Admin</title><style>
body{font:16px system-ui;background:#f3f6fa;color:#182638;margin:0}
header{background:#14243b;color:white;padding:18px 5%}main{max-width:1200px;margin:24px auto;padding:0 18px}
article{background:white;padding:20px;border-radius:12px;margin-bottom:15px}
input,select,button{font:inherit;padding:8px;margin:3px}button{background:#ef9d2c;border:0;border-radius:5px;cursor:pointer}
table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #ddd;text-align:left}
small{color:#526071}a{color:#174c83}header a{color:white}
@media(max-width:800px){table,tbody,tr,td{display:block}thead{display:none}td{padding:4px}}
</style></head><body><header><strong>Section 8 Rentals and More · Referral Administration</strong>
{% if session.get('referral_admin') %}<a style="float:right" href="{{ url_for('logout') }}">Log out</a>{% endif %}</header>
<main>{{ body|safe }}</main></body></html>"""

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        provided = request.form.get("password", "")
        expected = os.environ["REFERRAL_ADMIN_PASSWORD"]
        if hmac.compare_digest(provided.encode(), expected.encode()):
            session.clear()
            session["referral_admin"] = True
            session["csrf"] = secrets.token_urlsafe(32)
            return redirect(url_for("dashboard"))
    body = """<article><h1>Administrator sign in</h1><form method="post">
    <label>Password <input type="password" name="password" autocomplete="current-password" required></label>
    <button type="submit">Sign in</button></form></article>"""
    return render_template_string(BASE, body=body)

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.get("/")
@login_required
def dashboard():
    county = request.args.get("county", "")
    status = request.args.get("status", "")
    if county not in ("", "Hennepin", "Ramsey", "Dakota", "Anoka", "Washington"):
        abort(400)
    if status not in ("", "not_contacted", "contacted", "interested", "approved", "declined", "inactive"):
        abort(400)
    with connect() as db:
        rows = db.execute("""SELECT * FROM referral_partners WHERE
           (? = '' OR service_area LIKE '%' || ? || '%') AND
           (? = '' OR partnership_status = ?)
           ORDER BY CASE priority WHEN 'high' THEN 0 ELSE 1 END, organization_name
           LIMIT 500""", (county, county, status, status)).fetchall()
        counts = dict(db.execute("SELECT partnership_status,COUNT(*) FROM referral_partners GROUP BY partnership_status").fetchall())
    # Jinja auto-escapes all organization and contact fields.
    body = """<article><h1>Referral prospects ({{ rows|length }})</h1>
    <p>These are prospective organizations, not approved partners. Never enter tenant personal information here.</p>
    <p>All records: {% for key,val in counts.items() %}{{ key }}: {{ val }} · {% endfor %}</p>
    <form method="get"><label>County <select name="county"><option value="">All counties</option>
    {% for c in counties %}<option value="{{ c }}" {% if c==county %}selected{% endif %}>{{ c }}</option>{% endfor %}
    </select></label><label>Status <select name="status"><option value="">All statuses</option>
    {% for s in statuses %}<option value="{{ s }}" {% if s==status %}selected{% endif %}>{{ s }}</option>{% endfor %}
    </select></label><button>Filter</button></form></article>
    <article><table><thead><tr><th>Organization</th><th>Area / category</th><th>Contact</th><th>Outreach</th></tr></thead>
    <tbody>{% for p in rows %}<tr><td><strong>{{ p.organization_name }}</strong><br>
    <small>{{ p.verification_status }} · {{ p.priority }}</small></td>
    <td>{{ p.service_area or 'To verify' }}<br><small>{{ p.notes or '' }}</small></td>
    <td>{% if p.website %}<a href="{{ p.website }}" rel="noopener noreferrer" target="_blank">Source</a>{% endif %}
    <br>{{ p.phone or '' }}<br>{{ p.email or '' }}</td>
    <td><form method="post" action="{{ url_for('update_partner',partner_id=p.id) }}">
    <input type="hidden" name="csrf" value="{{ csrf }}">
    <select name="status" aria-label="Outreach status for {{ p.organization_name }}">
    {% for s in statuses %}<option value="{{ s }}" {% if s==p.partnership_status %}selected{% endif %}>{{ s }}</option>{% endfor %}
    </select><input name="note" maxlength="500" placeholder="Outreach note (optional)" aria-label="Outreach note">
    <button>Save</button></form></td></tr>{% endfor %}</tbody></table></article>"""
    return render_template_string(BASE, body=render_template_string(
        body, rows=rows, counts=counts, counties=("Hennepin","Ramsey","Dakota","Anoka","Washington"),
        statuses=("not_contacted","contacted","interested","approved","declined","inactive"),
        county=county,status=status,csrf=session["csrf"]))

@app.post("/partner/<int:partner_id>/status")
@login_required
def update_partner(partner_id):
    if not csrf_ok():
        abort(403)
    status = request.form.get("status", "")
    note = request.form.get("note", "").strip()
    allowed = ("not_contacted","contacted","interested","approved","declined","inactive")
    if status not in allowed or len(note)>500:
        abort(400)
    with connect() as db:
        current = db.execute("SELECT partnership_status,verification_status FROM referral_partners WHERE id=?", (partner_id,)).fetchone()
        if current is None:
            abort(404)
        if status == "approved" and current["verification_status"] != "verified":
            abort(400, "Verify organization before approving it")
        db.execute("UPDATE referral_partners SET partnership_status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?", (status,partner_id))
        db.execute("INSERT INTO referral_partner_events(partner_id,event_type,note) VALUES(?,?,?)",
                   (partner_id,"status:"+status,note))
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    import_partners(DB_PATH)
    app.run(host="127.0.0.1",port=8766,debug=False)
