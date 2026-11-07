import os
import re
from urllib.parse import urlparse

BASE_DIR = r"C:\section8landlordsmn"

def audit_and_repair_links():
    print("=" * 70)
    print("SECTION 8 RENTALS AND MORE LLC - END-TO-END REPO AUDIT & REPAIR")
    print("=" * 70)

    # 1. Identify all html files in root
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".html")]
    all_files = set(os.listdir(BASE_DIR))
    
    print(f"[*] Discovered {len(html_files)} HTML pages in workspace:")
    for hf in sorted(html_files):
        print(f"    - {hf}")

    total_links_checked = 0
    broken_links_found = 0
    repaired_occurrences = 0

    # Pattern to match href and src attributes
    link_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

    for doc in html_files:
        path = os.path.join(BASE_DIR, doc)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        updated_content = content
        doc_dirty = False

        for match in link_pattern.finditer(content):
            target = match.group(1).strip()
            total_links_checked += 1

            # Skip empty, in-page anchors, external links, mailto, tel, javascript
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:")):
                continue

            parsed_path = urlparse(target).path
            cleaned_target = parsed_path.lstrip("./").lstrip("/")

            # Check if internal file exists
            if cleaned_target:
                # Disregard API endpoint routes handled by edge functions
                if cleaned_target.startswith("api/"):
                    continue

                if cleaned_target not in all_files and not os.path.exists(os.path.join(BASE_DIR, cleaned_target)):
                    broken_links_found += 1
                    print(f"[-] [BROKEN] In '{doc}': target '{target}' does not exist.")

                    # Auto-fix common misnomers
                    fixed_target = None
                    if "investor" in cleaned_target.lower():
                        fixed_target = "investor-dossier.html"
                    elif "dossier" in cleaned_target.lower():
                        fixed_target = "investor-dossier.html"
                    elif "presentation" in cleaned_target.lower():
                        fixed_target = "presentation.html"
                    elif "admin" in cleaned_target.lower():
                        fixed_target = "admin.html"
                    elif "rent" in cleaned_target.lower() and "guarantee" in cleaned_target.lower():
                        fixed_target = "landlord-guaranteed-rent.html"
                    elif "manager" in cleaned_target.lower():
                        fixed_target = "property-managers.html"
                    elif "conversion" in cleaned_target.lower():
                        fixed_target = "market-rate-conversions.html"
                    elif "relocation" in cleaned_target.lower() or "voucher" in cleaned_target.lower():
                        fixed_target = "voucher-relocation.html"
                    elif cleaned_target.endswith(".html"):
                        fixed_target = "index.html"

                    if fixed_target and fixed_target in all_files:
                        updated_content = updated_content.replace(f'"{target}"', f'"{fixed_target}"')
                        updated_content = updated_content.replace(f"'{target}'", f"'{fixed_target}'")
                        repaired_occurrences += 1
                        doc_dirty = True
                        print(f"    [+] Fixed: '{target}' -> '{fixed_target}'")

        if doc_dirty:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"[✓] Successfully patched links in: {doc}")

    print("-" * 70)
    print(f"Total links audited: {total_links_checked}")
    print(f"Broken links found:  {broken_links_found}")
    print(f"Repairs applied:     {repaired_occurrences}")
    print("=" * 70)

if __name__ == "__main__":
    audit_and_repair_links()
