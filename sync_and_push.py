import os
import shutil
import subprocess

print("==========================================================================")
print("SYNCHRONIZING REPOSITORY ROOT AND PUBLIC DIRECTORY FOR CLOUDFLARE PAGES")
print("==========================================================================")

# Ensure public directory exists
os.makedirs("public", exist_ok=True)

# List of critical web assets that need to be live on Cloudflare Pages
web_files = [
    "index.html",
    "admin.html",
    "admin_backup.html",
    "calculator.html",
    "calculator.js",
    "PROPERTY_OPERATIONS_MANUAL_PRINT.html",
    "investor-dossier.html",
    "presentation.html",
    "landlord-guaranteed-rent.html",
    "property-managers.html",
    "market-rate-conversions.html",
    "voucher-relocation.html",
    "hud_fmr_active_standards.json"
]

# Sync bi-directionally (if present in root, copy to public; if in public and missing in root, copy to root)
for f in web_files:
    root_path = f
    pub_path = os.path.join("public", f)

    if os.path.exists(root_path):
        shutil.copy2(root_path, pub_path)
        print(f"✔ Root -> Public: {f}")
    elif os.path.exists(pub_path):
        shutil.copy2(pub_path, root_path)
        print(f"✔ Public -> Root: {f}")
    else:
        print(f"⚠ Missing in both: {f}")

print("\nDeploying to Git / Cloudflare Pages...")
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "fix: synchronize all root and public web files for Cloudflare deployment"], check=False)
result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
