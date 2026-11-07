"""Deterministic, explainable candidate matching. No automatic placements."""
import sqlite3

def find_candidates(db: sqlite3.Connection, referral_id: int, limit: int = 50):
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    referral = db.execute("""SELECT county,bedrooms_needed,maximum_rent,
        housing_program,accessibility_requested FROM housing_referrals WHERE id=?""",
        (referral_id,)).fetchone()
    if referral is None:
        raise ValueError("Unknown referral")
    county, bedrooms, max_rent, program, accessible = referral
    if max_rent is None:
        # Do not imply rent affordability when the limit is unknown.
        return []
    # HCV suitability is provisional: payment standards, utility allowance,
    # rent reasonableness, inspections and PHA approval must be verified.
    rows = db.execute("""SELECT id,listing_reference,county,bedrooms,monthly_rent,
      accessible,accepts_hcv,last_confirmed_at
      FROM rental_inventory
      WHERE availability='available'
        AND county=?
        AND bedrooms>=?
        AND monthly_rent<=?
        AND (?=0 OR accessible=1)
        AND (?!='HCV' OR accepts_hcv=1)
      ORDER BY monthly_rent ASC, bedrooms ASC, id ASC LIMIT ?""",
      (county,bedrooms,max_rent,int(bool(accessible)),program,limit)).fetchall()
    return [dict(row) if isinstance(row,sqlite3.Row) else {
        "id":row[0],"listing_reference":row[1],"county":row[2],
        "bedrooms":row[3],"monthly_rent":row[4],"accessible":row[5],
        "accepts_hcv":row[6],"last_confirmed_at":row[7]} for row in rows]
