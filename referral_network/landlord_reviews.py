"""Tenant-to-landlord reviews: moderation-first Flask blueprint.

Register on the authenticated API with app.register_blueprint(reviews_bp).
The host application must supply a tenant identity in flask.g.tenant_id and a
PostgreSQL connection factory in app.config['REVIEWS_DB_CONNECT'].
Do not expose this blueprint until tenant authentication and tenancy verification
are wired in. No tenant identity is included in public responses.
"""
import re
from flask import Blueprint, current_app, g, jsonify, request

reviews_bp = Blueprint("landlord_reviews", __name__, url_prefix="/api/v1/landlord-reviews")
SCHEMA = """
CREATE TABLE IF NOT EXISTS landlord_reviews (
 id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 tenant_id TEXT NOT NULL,
 landlord_id TEXT NOT NULL,
 rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
 maintenance SMALLINT NOT NULL CHECK (maintenance BETWEEN 1 AND 5),
 communication SMALLINT NOT NULL CHECK (communication BETWEEN 1 AND 5),
 fairness SMALLINT NOT NULL CHECK (fairness BETWEEN 1 AND 5),
 review_text TEXT NOT NULL CHECK (char_length(review_text) <= 1000),
 status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 reviewed_at TIMESTAMPTZ,
 UNIQUE (tenant_id, landlord_id)
);
CREATE INDEX IF NOT EXISTS landlord_reviews_public_idx
 ON landlord_reviews(landlord_id) WHERE status = 'approved';
"""

def connection():
    factory = current_app.config.get("REVIEWS_DB_CONNECT")
    if factory is None:
        raise RuntimeError("Review database is not configured")
    return factory()

def authenticated_tenant():
    identity = getattr(g, "tenant_id", None)
    if not identity:
        return None
    return str(identity)

def verified_tenancy(db, tenant_id, landlord_id):
    verifier = current_app.config.get("REVIEWS_VERIFY_TENANCY")
    return bool(verifier and verifier(db, tenant_id, landlord_id))

@reviews_bp.post("")
def submit():
    tenant_id = authenticated_tenant()
    if not tenant_id:
        return jsonify(error="Tenant login required"), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON object required"), 400
    landlord_id = data.get("landlord_id")
    if not isinstance(landlord_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", landlord_id):
        return jsonify(error="Invalid landlord"), 400
    try:
        values = [data.get(k) for k in ("rating","maintenance","communication","fairness")]
        if any(type(v) is not int or not 1 <= v <= 5 for v in values):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify(error="Ratings must be whole numbers from 1 to 5"), 400
    message = data.get("review_text", "")
    if not isinstance(message, str) or len(message) > 1000:
        return jsonify(error="Review text must be at most 1000 characters"), 400
    # Require human moderation; do not allow personal identifiers or threats in public reviews.
    with connection() as db:
        if not verified_tenancy(db, tenant_id, landlord_id):
            return jsonify(error="Verified tenancy required"), 403
        with db.cursor() as cur:
            cur.execute("""INSERT INTO landlord_reviews
                (tenant_id,landlord_id,rating,maintenance,communication,fairness,review_text)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (tenant_id,landlord_id) DO NOTHING RETURNING id""",
                (tenant_id,landlord_id,*values,message.strip()))
            inserted = cur.fetchone()
        db.commit()
    if not inserted:
        return jsonify(error="One review per verified tenant-landlord relationship"), 409
    return jsonify(status="pending_moderation"), 202

@reviews_bp.get("/<landlord_id>")
def public_reviews(landlord_id):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", landlord_id):
        return jsonify(error="Invalid landlord"), 400
    with connection() as db:
        with db.cursor() as cur:
            cur.execute("""SELECT rating,maintenance,communication,fairness,review_text,created_at
                FROM landlord_reviews WHERE landlord_id=%s AND status='approved'
                ORDER BY created_at DESC LIMIT 50""", (landlord_id,))
            rows = cur.fetchall()
    return jsonify(reviews=[dict(rating=r[0],maintenance=r[1],communication=r[2],
                fairness=r[3],review_text=r[4],created_at=r[5].isoformat()) for r in rows])
