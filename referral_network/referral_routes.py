"""Admin-only referral pilot routes. No public or caseworker access yet."""
import re
import sqlite3
from flask import Blueprint, abort, redirect, render_template_string, request, session, url_for

referrals = Blueprint("referrals", __name__, url_prefix="/referrals")
COUNTIES = ("Hennepin", "Ramsey", "Dakota", "Anoka", "Washington")
PROGRAMS = ("HCV", "other_subsidy", "market_rate", "unknown")
STATUSES = ("new", "reviewing", "matched", "closed")

def require_admin():
    if not session.get("referral_admin"):
        abort(403)

def require_csrf():
    import hmac
    if not hmac.compare_digest(session.get("csrf", ""), request.form.get("csrf", "")):
        abort(403)

def init_referral_schema(db, schema_path):
    db.executescript(schema_path.read_text(encoding="utf-8"))

@referrals.get("/")
def list_referrals():
    require_admin()
    from admin_app import connect
    with connect() as db:
        rows = db.execute("""SELECT r.id,r.external_case_reference,r.county,r.bedrooms_needed,
          r.maximum_rent,r.housing_program,r.status,r.created_at,p.organization_name
          FROM housing_referrals r JOIN referral_partners p ON p.id=r.partner_id
          ORDER BY r.created_at DESC,r.id DESC LIMIT 200""").fetchall()
        partners = db.execute("""SELECT id,organization_name FROM referral_partners
          WHERE verification_status='verified' AND partnership_status='approved'
          ORDER BY organization_name""").fetchall()
    return render_template_string("""<!doctype html><html lang="en"><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1"><title>Housing Referrals</title>
    <body style="font:16px system-ui;max-width:960px;margin:30px auto;padding:12px">
    <h1>Housing referral pilot — administrator only</h1>
    <p><a href="/">Partner directory</a></p>
    <p>Do not enter tenant names, identifying numbers, medical information, or voucher IDs.
    Use an opaque case reference that cannot identify the applicant outside your own agency.</p>
    <h2>New referral</h2><form method="post" action="{{ url_for('referrals.create_referral') }}">
    <input type="hidden" name="csrf" value="{{ csrf }}">
    <label>Approved partner <select name="partner_id" required>
    {% for p in partners %}<option value="{{ p.id }}">{{ p.organization_name }}</option>{% endfor %}</select></label>
    <label>Anonymous case reference <input name="external_case_reference" pattern="[A-Za-z0-9_-]{8,40}" maxlength="40" required></label>
    <label>County <select name="county">{% for c in counties %}<option>{{ c }}</option>{% endfor %}</select></label>
    <label>Bedrooms <input type="number" name="bedrooms_needed" min="0" max="10" required></label>
    <label>Maximum rent <input type="number" name="maximum_rent" min="0" max="20000"></label>
    <label>Program <select name="housing_program">{% for p in programs %}<option value="{{ p }}">{{ p }}</option>{% endfor %}</select></label>
    <label><input type="checkbox" name="accessibility_requested" value="1">Accessibility requested</label>
    <label><input type="checkbox" name="consent_attested" value="1" required>Authorized consent has been obtained and documented by the referring agency</label>
    <button {% if not partners %}disabled{% endif %}>Create referral</button></form>
    {% if not partners %}<p>No verified and approved partners yet. Approve partners before accepting referrals.</p>{% endif %}
    <h2>Referral queue</h2><table border="1" cellpadding="8"><tr><th>Case</th><th>Partner</th><th>County</th><th>Bedrooms</th><th>Rent cap</th><th>Status</th></tr>
    {% for r in rows %}<tr><td>{{ r.external_case_reference }}</td><td>{{ r.organization_name }}</td>
    <td>{{ r.county }}</td><td>{{ r.bedrooms_needed }}</td><td>{{ r.maximum_rent or 'Not set' }}</td>
    <td><form method="post" action="{{ url_for('referrals.set_status', referral_id=r.id) }}">
    <input type="hidden" name="csrf" value="{{ csrf }}"><select name="status">
    {% for s in statuses %}<option value="{{ s }}" {% if r.status==s %}selected{% endif %}>{{ s }}</option>{% endfor %}
    </select><button>Update</button></form></td></tr>{% endfor %}</table></body></html>""",
    rows=rows,partners=partners,counties=COUNTIES,programs=PROGRAMS,statuses=STATUSES,csrf=session["csrf"])

@referrals.post("/")
def create_referral():
    require_admin()
    require_csrf()
    from admin_app import connect
    reference = request.form.get("external_case_reference","").strip()
    county = request.form.get("county","")
    program = request.form.get("housing_program","")
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,40}", reference) or county not in COUNTIES or program not in PROGRAMS:
        abort(400)
    if request.form.get("consent_attested") != "1":
        abort(400, "Consent attestation required")
    try:
        partner_id=int(request.form.get("partner_id",""))
        bedrooms=int(request.form.get("bedrooms_needed",""))
        cap_raw=request.form.get("maximum_rent","").strip()
        cap=int(cap_raw) if cap_raw else None
    except ValueError:
        abort(400)
    if not 0 <= bedrooms <= 10 or (cap is not None and not 0 <= cap <= 20000):
        abort(400)
    with connect() as db:
        partner=db.execute("SELECT id FROM referral_partners WHERE id=? AND verification_status='verified' AND partnership_status='approved'",(partner_id,)).fetchone()
        if partner is None:
            abort(403, "Partner must be verified and approved")
        try:
            cursor=db.execute("""INSERT INTO housing_referrals
                (partner_id,external_case_reference,county,bedrooms_needed,maximum_rent,
                 housing_program,accessibility_requested,consent_attested)
                 VALUES(?,?,?,?,?,?,?,1)""",
                 (partner_id,reference,county,bedrooms,cap,program,int(request.form.get("accessibility_requested")=="1")))
        except sqlite3.IntegrityError:
            abort(409, "Duplicate reference or invalid referral")
        db.execute("INSERT INTO housing_referral_events(referral_id,event_type) VALUES(?,'created')",(cursor.lastrowid,))
    return redirect(url_for("referrals.list_referrals"))

@referrals.post("/<int:referral_id>/status")
def set_status(referral_id):
    require_admin()
    require_csrf()
    status=request.form.get("status","")
    if status not in STATUSES:
        abort(400)
    from admin_app import connect
    with connect() as db:
        result=db.execute("UPDATE housing_referrals SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(status,referral_id))
        if result.rowcount != 1:
            abort(404)
        db.execute("INSERT INTO housing_referral_events(referral_id,event_type) VALUES(?,?)",(referral_id,"status:"+status))
    return redirect(url_for("referrals.list_referrals"))
