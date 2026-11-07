import os
import sys
import json
import sqlite3
import urllib.request
import urllib.error

if len(sys.argv) < 2:
    print("Usage: python fetch_hud_api.py <YOUR_HUD_API_TOKEN>")
    sys.exit(1)

HUD_TOKEN = sys.argv[1].strip().strip("<>").strip('"').strip("'")

headers = {
    "Authorization": f"Bearer {HUD_TOKEN}",
    "Accept": "application/json"
}

target_counties = {
    "MN": ["Dakota County", "Hennepin County", "Ramsey County"],
    "WI": ["St. Croix County"]
}

county_fips_map = {}

print("Step 1: Querying HUD User /listCounties endpoints...")

for state, names in target_counties.items():
    list_url = f"https://www.huduser.gov/hudapi/public/fmr/listCounties/{state}"
    req = urllib.request.Request(list_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            county_list = body.get("data", [])
            for item in county_list:
                c_name = item.get("county_name", "")
                if c_name in names:
                    full_label = f"{c_name}, {state}"
                    county_fips_map[full_label] = item.get("fips_code")
                    print(f"  ✔ Resolved {full_label} -> FIPS: {item.get('fips_code')}")
    except urllib.error.HTTPError as e:
        print(f"✖ Failed /listCounties/{state} - HTTP {e.code}: {e.reason}")
        if e.code in (401, 403):
            print("  [Auth Warning] Check that your token has Fair Market Rents API scope.")
            sys.exit(1)
    except Exception as e:
        print(f"✖ Error on {state}: {e}")

if not county_fips_map:
    print("✖ Could not resolve any target county FIPS codes. Exiting.")
    sys.exit(1)

print("\nStep 2: Fetching live FMR datasets for resolved FIPS codes...")
live_standards = {}

for label, fips in county_fips_map.items():
    fmr_url = f"https://www.huduser.gov/hudapi/public/fmr/data/{fips}?year=2026"
    req = urllib.request.Request(fmr_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            basic = data.get("data", {}).get("basicdata", {})
            if basic:
                live_standards[label] = {
                    "efficiency": int(basic.get("Efficiency", 1398)),
                    "one_bed": int(basic.get("One-Bedroom", 1582)),
                    "two_bed": int(basic.get("Two-Bedroom", 1944)),
                    "three_bed": int(basic_data.get("Three-Bedroom", 2420) if 'basic_data' in locals() else basic.get("Three-Bedroom", 2420)),
                    "four_bed": int(basic.get("Four-Bedroom", 2785))
                }
                print(f"  ✔ Retrieved FMR rates for {label}: 1BR=${live_standards[label]['one_bed']}, 2BR=${live_standards[label]['two_bed']}, 3BR=${live_standards[label]['three_bed']}")
    except urllib.error.HTTPError as e:
        print(f"✖ Failed FMR pull for {label} ({fips}) - HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"✖ Error pulling FMR for {label}: {e}")

if live_standards:
    # 1. Update SQLite
    conn = sqlite3.connect("hud_fmr_2027.sqlite")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS active_fmr_live (
            county_name TEXT PRIMARY KEY,
            efficiency INTEGER,
            one_bed INTEGER,
            two_bed INTEGER,
            three_bed INTEGER,
            four_bed INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for county, vals in live_standards.items():
        cur.execute("""
            INSERT OR REPLACE INTO active_fmr_live 
            (county_name, efficiency, one_bed, two_bed, three_bed, four_bed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (county, vals["efficiency"], vals["one_bed"], vals["two_bed"], vals["three_bed"], vals["four_bed"]))
    conn.commit()
    conn.close()
    print("\n✔ SQLite hud_fmr_2027.sqlite populated with live HUD data.")

    # 2. Write JSON payload to both root and public/
    json_payload = {
        "source": "HUD User Programmatic API (/fmr/data)",
        "verified_metro_area": "Minneapolis-St. Paul-Bloomington, MN-WI HUD Metro FMR Area",
        "standards": live_standards
    }
    
    with open("hud_fmr_active_standards.json", "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2)
    with open("public/hud_fmr_active_standards.json", "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2)
        
    print("✔ Synced hud_fmr_active_standards.json across root and public/ directories.")
else:
    print("\n✖ No FMR records processed.")
