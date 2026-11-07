"""Private agency portal: agency-scoped, consent-attested referral submission."""
import hmac
import secrets
import sqlite3
import uuid
from functools import wraps
from flask import Blueprint, abort, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash
from referral_routes import COUNTIES, PROGRAMS

agency = Blueprint("agency", __name__, url_prefix="/agency")

def agency_only(fn):
    @wraps(fn)
    def guarded(*args, **kwargs):
        if not session.get("agency_user_id") or not session.get("agency_partner_id"):
            return redirect(url_for("agency.signin"))
        return fn(*args, **kwargs)
    return guarded

def csrf_required():
    if not hmac.compare_digest(session.get("agency_csrf", ""),request.form.get("csrf", "")):
        abort(403)

@agency.route("/login",methods=["GET","POST"])
def signin():
    error=""
    if request.method=="POST":
        from admin_app import connect
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        with connect() as db:
            user=db.execute("""SELECT u.id,u.partner_id,u.password_hash,u.role FROM agency_users u
                JOIN referral_partners p ON p.id=u.partner_id
                WHERE u.email=? AND u.active=1 AND p.verification_status='verified'
                AND p.partnership_status='approved'""",(email,)).fetchone()
        if user and check_password_hash(user["password_hash"],password):
            session.clear()
            session["agency_user_id"]=user["id"]
            session["agency_partner_id"]=user["partner_id"]
            session["agency_csrf"]=secrets.token_urlsafe(32)
            return redirect(url_for("agency.home"))
        error="Invalid credentials or account not authorized"
    return render_template_string("""<!doctype html><html lang="en"><meta charset="utf-8">
      <title>Agency sign in</title><body style="font:16px system-ui;max-width:650px;margin:40px auto">
      <h1>Section 8 Rentals and More · Agency portal</h1><p>{{ error }}</p>
      <form method="post"><label>Email <input name="email" type="email" required></label>
      <label>Password <input name="password" type="password" required></label><button>Sign in</button></form>
      <p>Access is by invitation only. Contact your organization's portal administrator.</p></body></html>""",error=error)

@agency.post("/logout")
@agency_only
def signout():
    csrf_required()
    session.clear()
    return redirect(url_for("agency.signin"))

@agency.get("/")
@agency_only
def home():
    from admin_app import connect
    partner_id=session["agency_partner_id"]
    with connect() as db:
        current=db.execute("""SELECT u.id,p.organization_name FROM agency_users u
          JOIN referral_partners p ON p.id=u.partner_id
          WHERE u.id=? AND u.partner_id=? AND u.active=1 AND
          p.verification_status='verified' AND p.partnership_status='approved'""",
          (session["agency_user_id"],partner_id)).fetchone()
        if not current:
            session.clear()
            abort(403)
        referrals=db.execute("""SELECT external_case_reference,county,bedrooms_needed,status,created_at
          FROM housing_referrals WHERE partner_id=? ORDER BY id DESC LIMIT 100""",(partner_id,)).fetchall()
    return render_template_string("""<!doctype html><html lang="en"><meta charset="utf-8">
      <title>Agency referrals</title><body style="font:16px system-ui;max-width:960px;margin:30px auto">
      <h1>{{ organization }}</h1><h2>Private housing referral portal</h2>
      <p>Only your organization's referrals are shown. Do not submit tenant names, Social Security numbers,
      voucher IDs, or health information. Obtain and document client authorization before submitting.</p>
      <form method="post" action="{{ url_for('agency.signout') }}"><input type="hidden" name="csrf" value="{{ csrf }}"><button>Log out</button></form>
      <h3>New referral</h3><form method="post" action="{{ url_for('agency.submit') }}">
      <input type="hidden" name="csrf" value="{{ csrf }}">
      <p>A random, non-identifying reference number will be assigned automatically.</p>
      <label>County <select name="county">{% for c in counties %}<option>{{ c }}</option>{% endfor %}</select></label>
      <label>Bedrooms <input type="number" name="bedrooms_needed" min="0" max="10" required></label>
      <label>Maximum rent <input type="number" name="maximum_rent" min="0" max="20000"></label>
      <label>Program <select name="housing_program">{% for p in programs %}<option>{{ p }}</option>{% endfor %}</select></label>
      <label><input type="checkbox" name="accessibility_requested" value="1">Accessibility requested</label>
      <label><input type="checkbox" name="consent_attested" value="1" required>Applicant authorization obtained and documented by agency</label>
      <button>Submit housing referral</button></form>
      <h3>Our referrals</h3><table border="1" cellpadding="8"><tr><th>Reference</th><th>County</th><th>Bedrooms</th><th>Status</th></tr>
      {% for r in referrals %}<tr><td>{{ r.external_case_reference }}</td><td>{{ r.county }}</td>
      <td>{{ r.bedrooms_needed }}</td><td>{{ r.status }}</td></tr>{% endfor %}</table>
      </body></html>""",organization=current["organization_name"],referrals=referrals,
      counties=COUNTIES,programs=PROGRAMS,csrf=session["agency_csrf"])

@agency.post("/submit")
@agency_only
def submit():
    csrf_required()
    from admin_app import connect
    if "external_case_reference" in request.form:
        abort(400, "Case references are generated by the system")
    ref="REF_"+uuid.uuid4().hex
    county=request.form.get("county","")
    program=request.form.get("housing_program","")
    if county not in COUNTIES or program not in PROGRAMS:
        abort(400)
    if request.form.get("consent_attested")!="1":
        abort(400)
    try:
        bedrooms=int(request.form.get("bedrooms_needed",""))
        raw=request.form.get("maximum_rent","").strip()
        rent=int(raw) if raw else None
    except ValueError:
        abort(400)
    if not 0<=bedrooms<=10 or (rent is not None and not 0<=rent<=20000):
        abort(400)
    with connect() as db:
        eligible=db.execute("""SELECT u.id FROM agency_users u JOIN referral_partners p ON p.id=u.partner_id
            WHERE u.id=? AND u.partner_id=? AND u.active=1 AND
            p.verification_status='verified' AND p.partnership_status='approved'""",
            (session["agency_user_id"],session["agency_partner_id"])).fetchone()
        if not eligible:
            abort(403)
        try:
            cur=db.execute("""INSERT INTO housing_referrals(partner_id,external_case_reference,county,
                bedrooms_needed,maximum_rent,housing_program,accessibility_requested,consent_attested)
                VALUES(?,?,?,?,?,?,?,1)""",(session["agency_partner_id"],ref,county,bedrooms,rent,
                program,int(request.form.get("accessibility_requested")=="1")))
        except sqlite3.IntegrityError:
            abort(409,"Duplicate case reference")
        db.execute("INSERT INTO housing_referral_events(referral_id,event_type) VALUES(?,'agency_submitted')",(cur.lastrowid,))
    return redirect(url_for("agency.home"))
