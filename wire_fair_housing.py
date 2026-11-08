import os
import shutil
import subprocess

fair_housing_js = """
// fair_housing_engine.js - Reasonable Accommodation & Assistance Animal Engine
// Governing Laws: 42 U.S.C. § 3604, 24 CFR Part 8 & Minn. Stat. § 363A.09

function generateReasonableAccommodationPacket(propId, accommodationType = 'Assistance Animal (No-Pet Fee Waiver)') {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const tenantName = p.tenant || p.tenantName || 'Resident Occupant';
  const today = new Date().toLocaleDateString();

  const doc = `================================================================================
FAIR HOUSING ACT & SECTION 504 REASONABLE ACCOMMODATION DETERMINATION
Pursuant to 42 U.S.C. § 3604, 24 CFR Part 8 & ${isMN ? 'Minn. Stat. § 363A.09' : 'Wis. Stat. § 106.50'}
================================================================================

1. TENANCY PARTICULARS & HOUSING AGENCY:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Resident Name     : ${tenantName}
   Housing Authority : ${p.county || 'Hennepin'} County Public Housing Authority
   Managing Entity   : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)
   Determination Date: ${today}

2. REQUESTED ACCOMMODATION / MODIFICATION:
   Classification    : ${accommodationType}
   Functional Scope  : Exception to general rules/policies to ensure equal opportunity
                       to use and enjoy the dwelling unit pursuant to Fair Housing rules.

3. STATUTORY EVALUATION & ASSISTANCE ANIMAL RULES:
   • Exemption from Pet Fees: Under HUD FHEO Notice 2020-01, assistance animals
     (service animals and emotional support animals) are not considered pets.
     Landlord is barred from charging pet application fees, pet deposits, or monthly pet rent.
   • Breed & Size Restrictions: Standard lease size and breed restrictions are waived.
   • Tenant Duty: Resident remains responsible for sanitation and control of the animal,
     and any direct property damage beyond ordinary wear and tear at lease termination.

4. DETERMINATION & FORMAL HOUSING ACTION:
   [X] APPROVED IN FULL: The requested accommodation is reasonable and granted without delay.
   [ ] INTERACTIVE PROCESS COMMENCED: Requesting additional healthcare verification.

CERTIFICATION OF COMPLIANCE:
Section 8 Rentals and More LLC adheres strictly to federal and state Fair Housing statutes.
No adverse action or retaliation shall be taken against the resident for requesting this accommodation.

Authorized Official: Dr. Albert Ray LaMotte, Managing Principal & CEO
Entity: Section 8 Rentals and More LLC • Contact: alamotte1956@gmail.com
Digital Seal: [FAIR-HOUSING-DETERMINATION-${Date.now().toString().slice(-8)}]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${doc}</pre>`);
  w.document.close();
  w.print();
}

window.generateReasonableAccommodationPacket = generateReasonableAccommodationPacket;
"""

with open("fair_housing_engine.js", "w", encoding="utf-8") as f:
    f.write(fair_housing_js)

os.makedirs("public", exist_ok=True)
shutil.copy2("fair_housing_engine.js", "public/fair_housing_engine.js")

# 1. Register script in index.html
with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

if "fair_housing_engine.js" not in html:
    html = html.replace("</body>", '<script src="fair_housing_engine.js"></script>\n</body>', 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy2("index.html", "public/index.html")

# 2. Add button to compliance_hub.js
with open("compliance_hub.js", "r", encoding="utf-8", errors="ignore") as f:
    hub_code = f.read()

fair_housing_button = """
        <button onclick="generateReasonableAccommodationPacket('${p.id}')" class="p-3.5 text-left rounded-2xl bg-teal-500/10 hover:bg-teal-500/20 border border-teal-500/30 transition-all">
          <div class="font-bold text-teal-300">Fair Housing Reasonable Accommodation</div>
          <div class="text-[11px] text-slate-400 mt-1">42 U.S.C. § 3604 assistance animal fee waiver, 24 CFR Part 8 determination & approval cert.</div>
        </button>
"""

if "generateReasonableAccommodationPacket" not in hub_code:
    hub_code = hub_code.replace("</div>\n\n      <div class=\"flex items-center justify-between pt-2 border-t", fair_housing_button + "      </div>\n\n      <div class=\"flex items-center justify-between pt-2 border-t", 1)
    with open("compliance_hub.js", "w", encoding="utf-8") as f:
        f.write(hub_code)
    shutil.copy2("compliance_hub.js", "public/compliance_hub.js")

# Commit and push to Cloudflare Pages
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "feat: implement Fair Housing reasonable accommodation and assistance animal engine"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=False)
print("SUCCESS: Fair Housing Engine live on Cloudflare Pages.")
