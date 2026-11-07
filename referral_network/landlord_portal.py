"""Landlord self-registration and anonymous matching. Mount on authenticated Flask service."""
import sqlite3
from flask import Blueprint, request, session, redirect, url_for, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from referral_routes import COUNTIES

landlords = Blueprint("landlords", __name__, url_prefix="/landlords")

def connect():
    from admin_app import connect as get_db
    return get_db()

def init_schema(db):
    db.execute("""CREATE TABLE IF NOT EXISTS landlord_accounts (
        id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL, password_hash TEXT NOT NULL,
        active INTEGER NOT NULL DEFAULT 1, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    db.execute("""CREATE TABLE IF NOT EXISTS landlord_units (
        id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL REFERENCES landlord_accounts(id),
        county TEXT NOT NULL, bedrooms INTEGER NOT NULL, rent INTEGER NOT NULL,
        accessible INTEGER NOT NULL DEFAULT 0, available INTEGER NOT NULL DEFAULT 1)""")

def authenticated(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        uid = session.get("landlord_id")
        if not uid:
            return jsonify(error="Sign in required"), 401
        with connect() as db:
            active = db.execute("SELECT 1 FROM landlord_accounts WHERE id=? AND active=1",(uid,)).fetchone()
        if not active:
            session.clear()
            return jsonify(error="Sign in required"), 401
        return fn(*args, **kwargs)
    return wrapper

@landlords.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email","")).strip().lower()
    name = str(data.get("name","")).strip()
    password = str(data.get("password",""))
    if not 3 <= len(email) <= 254 or "@" not in email or not 2 <= len(name) <= 150 or not 12 <= len(password) <= 256:
        return jsonify(error="Valid email, landlord name and 12+ character password required"), 400
    with connect() as db:
        init_schema(db)
        try:
            db.execute("INSERT INTO landlord_accounts(email,name,password_hash) VALUES(?,?,?)",
                       (email,name,generate_password_hash(password)))
        except sqlite3.IntegrityError:
            return jsonify(error="Account already registered"), 409
    return jsonify(message="Registered; sign in to manage rental units"), 201

@landlords.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    with connect() as db:
        init_schema(db)
        user = db.execute("SELECT id,password_hash FROM landlord_accounts WHERE email=? AND active=1",
                          (str(data.get("email","")).strip().lower(),)).fetchone()
    if not user or not check_password_hash(user["password_hash"],str(data.get("password",""))):
        return jsonify(error="Invalid credentials"), 401
    session.clear()
    session["landlord_id"] = user["id"]
    return jsonify(message="Signed in")

@landlords.post("/logout")
@authenticated
def logout():
    session.clear()
    return jsonify(message="Signed out")

@landlords.post("/units")
@authenticated
def add_unit():
    data = request.get_json(silent=True) or {}
    try:
        county = str(data["county"])
        bedrooms = int(data["bedrooms"])
        rent = int(data["rent"])
    except (KeyError, ValueError, TypeError):
        return jsonify(error="County, bedrooms and rent required"), 400
    if county not in COUNTIES or not 0 <= bedrooms <= 10 or not 0 <= rent <= 20000:
        return jsonify(error="Invalid rental unit details"), 400
    with connect() as db:
        cur = db.execute("INSERT INTO landlord_units(owner_id,county,bedrooms,rent,accessible) VALUES(?,?,?,?,?)",
                         (session["landlord_id"],county,bedrooms,rent,int(data.get("accessible") is True)))
    return jsonify(id=cur.lastrowid), 201

@landlords.get("/units")
@authenticated
def units():
    with connect() as db:
        rows = db.execute("SELECT id,county,bedrooms,rent,accessible,available FROM landlord_units WHERE owner_id=?",
                          (session["landlord_id"],)).fetchall()
        results = []
        for row in rows:
            unit = dict(row)
            count = 0
            if unit["available"]:
                try:
                    count = db.execute("""SELECT COUNT(*) FROM housing_referrals r
                        JOIN referral_partners p ON p.id=r.partner_id
                        WHERE r.county=? AND r.bedrooms_needed<=?
                        AND (r.maximum_rent IS NULL OR r.maximum_rent>=?)
                        AND (r.accessibility_requested=0 OR ?=1)
                        AND p.verification_status='verified'
                        AND p.partnership_status='approved'""",
                        (unit["county"],unit["bedrooms"],unit["rent"],unit["accessible"])).fetchone()[0]
                except sqlite3.OperationalError:
                    count = 0
            unit["anonymous_preliminary_matches"] = count
            results.append(unit)
    return jsonify(units=results)

@landlords.post("/units/<int:unit_id>/availability")
@authenticated
def availability(unit_id):
    data = request.get_json(silent=True) or {}
    if type(data.get("available")) is not bool:
        return jsonify(error="Boolean available required"), 400
    with connect() as db:
        result = db.execute("UPDATE landlord_units SET available=? WHERE id=? AND owner_id=?",
                            (int(data["available"]),unit_id,session["landlord_id"]))
        if not result.rowcount:
            abort(404)
    return jsonify(message="Updated")
