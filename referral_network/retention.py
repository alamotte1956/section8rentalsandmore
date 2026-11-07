"""Retention maintenance for minimized referral records. Preview is the default."""
import argparse
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

def expired_referrals(db, days=180, now=None):
    if days < 30:
        raise ValueError("Retention must be at least 30 days")
    now=now or datetime.now(timezone.utc)
    cutoff=(now-timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    return db.execute("""SELECT id FROM housing_referrals
        WHERE status='closed' AND updated_at < ? ORDER BY id""",(cutoff,)).fetchall()

def purge(db, days=180, dry_run=True, now=None):
    ids=[r[0] for r in expired_referrals(db,days,now)]
    if not dry_run:
        for rid in ids:
            db.execute("DELETE FROM rental_match_reviews WHERE referral_id=?",(rid,))
            db.execute("DELETE FROM housing_referral_events WHERE referral_id=?",(rid,))
            db.execute("DELETE FROM housing_referrals WHERE id=?",(rid,))
    return len(ids)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True,type=Path)
    p.add_argument("--days",type=int,default=180)
    p.add_argument("--execute",action="store_true",help="Actually delete eligible records; default is preview")
    a=p.parse_args()
    with sqlite3.connect(a.db) as db:
        count=purge(db,days=a.days,dry_run=not a.execute)
    print(f"{'Deleted' if a.execute else 'Would delete'} {count} closed referrals older than {a.days} days")
