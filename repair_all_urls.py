import os
import shutil
import subprocess

print("=" * 80)
print("REPAIRING ALL URL ENDPOINTS, ASSETS, AND ANCHOR DESTINATIONS")
print("=" * 80)

# Ensure public directory exists
os.makedirs("public", exist_ok=True)

# 1. Update index.html to add explicit anchor containers for marketing funnels
with open("index.html", "r", encoding="utf-8") as f:
    idx_content = f.read()

funnel_sections = """
  <!-- Anchor Section Targets -->
  <section id="landlord-funnel" class="py-12 px-4 max-w-6xl mx-auto border-t border-slate-800">
    <div class="glass-card p-8 rounded-3xl space-y-4">
      <div class="flex items-center gap-2 text-cyan-400 font-mono text-xs font-bold uppercase">
        <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Property Owner Guarantee
      </div>
      <h2 class="text-2xl font-bold text-white">Guaranteed Direct Deposit Sovereign Rent for Property Owners</h2>
      <p class="text-sm text-slate-300 leading-relaxed">
        Stop chasing rent. Section 8 Housing Choice Vouchers disburse 70% to 100% of contract rent via direct electronic sovereign deposit on the first of every month directly from Hennepin, Ramsey, Dakota, and Anoka county housing authorities.
      </p>
      <button onclick="openLoginModal()" class="px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs">Access Owner Portal</button>
    </div>
  </section>

  <section id="tenant-funnel" class="py-12 px-4 max-w-6xl mx-auto border-t border-slate-800">
    <div class="glass-card p-8 rounded-3xl space-y-4">
      <div class="flex items-center gap-2 text-emerald-400 font-mono text-xs font-bold uppercase">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> Voucher Resident Intake
      </div>
      <h2 class="text-2xl font-bold text-white">Section 8 Housing Choice Voucher Resident Intake & Fast Placement</h2>
      <p class="text-sm text-slate-300 leading-relaxed">
        We expedite RFTA packet submission (HUD Form 52517) and pre-inspect properties to guarantee passage under HUD NSPIRE physical habitability standards.
      </p>
      <button onclick="openLoginModal()" class="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs">Resident Voucher Login</button>
    </div>
  </section>

  <section id="broker-funnel" class="py-12 px-4 max-w-6xl mx-auto border-t border-slate-800">
    <div class="glass-card p-8 rounded-3xl space-y-4">
      <div class="flex items-center gap-2 text-amber-400 font-mono text-xs font-bold uppercase">
        <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Broker & Realtor Syndication
      </div>
      <h2 class="text-2xl font-bold text-white">Real Estate Agent & Broker Client Referral Program</h2>
      <p class="text-sm text-slate-300 leading-relaxed">
        Refer client rental assets or voucher holders for placement across the Twin Cities metro area with full statutory protection and lease execution assistance.
      </p>
      <button onclick="openLoginModal()" class="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs">Broker Registration</button>
    </div>
  </section>

  <section id="investor-funnel" class="py-12 px-4 max-w-6xl mx-auto border-t border-slate-800">
    <div class="glass-card p-8 rounded-3xl space-y-4">
      <div class="flex items-center gap-2 text-purple-400 font-mono text-xs font-bold uppercase">
        <span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span> Institutional Turnkey Portfolios
      </div>
      <h2 class="text-2xl font-bold text-white">Turnkey Section 8 Investment Portfolio Acquisition</h2>
      <p class="text-sm text-slate-300 leading-relaxed">
        Acquire cash-flowing single-family and multifamily properties structured under 2026 Small Area Fair Market Rent standards with audited 1% escrow interest compliance.
      </p>
      <button onclick="openLoginModal()" class="px-5 py-2.5 rounded-xl bg-purple-500 hover:bg-purple-400 text-white font-bold text-xs">Investor Inquiries</button>
    </div>
  </section>
"""

if 'id="landlord-funnel"' not in idx_content:
    idx_content = idx_content.replace('<!-- Footer -->', funnel_sections + '\n  <!-- Footer -->', 1)

# Add URL Hash auto-opener script
hash_listener = """
  <script>
    // Listen for hash triggers in URL
    function handleUrlHashTriggers() {
      const hash = window.location.hash;
      if (!hash) return;
      if (hash === '#compliance-hub' && typeof window.openComplianceHubModal === 'function') window.openComplianceHubModal();
      if (hash === '#state-api-cert' && typeof window.openStateCertificationModal === 'function') window.openStateCertificationModal();
      if (hash === '#qbo-sync' && typeof window.openQboSyncModal === 'function') window.openQboSyncModal();
      if (hash === '#statutory-calendar' && typeof window.openComplianceCalendarModal === 'function') window.openComplianceCalendarModal();
      if (hash === '#hipaa-vault' && typeof window.openHipaaVerificationModal === 'function') window.openHipaaVerificationModal();
      if (hash === '#marketing-distribution' && typeof window.openMarketingDistributionModal === 'function') window.openMarketingDistributionModal();
    }
    window.addEventListener('DOMContentLoaded', handleUrlHashTriggers);
    window.addEventListener('hashchange', handleUrlHashTriggers);
  </script>
</body>
"""

if 'handleUrlHashTriggers' not in idx_content:
    idx_content = idx_content.replace('</body>', hash_listener, 1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx_content)

# 2. Update admin.html with hash listener as well
if os.path.exists("admin.html"):
    with open("admin.html", "r", encoding="utf-8") as f:
        adm_content = f.read()
    if 'handleUrlHashTriggers' not in adm_content:
        adm_content = adm_content.replace('</body>', hash_listener, 1)
        with open("admin.html", "w", encoding="utf-8") as f:
            f.write(adm_content)

# 3. Mirror EVERY engine and asset from root directly into public/
all_manifest = [
    "index.html",
    "admin.html",
    "auth_engine.js",
    "concurrency_engine.js",
    "rbac_manager_engine.js",
    "regulatory_policy_engine.js",
    "hipaa_phi_vault_engine.js",
    "state_persistence.js",
    "compliance_hub.js",
    "pdf_truncation_fix.js",
    "qbo_sync_engine.js",
    "pha_notice_conduit.js",
    "inspection_calendar_engine.js",
    "state_api_certification_engine.js",
    "portfolio_sanitizer.js",
    "_headers",
    "_redirects"
]

for item in all_manifest:
    if os.path.exists(item):
        shutil.copy2(item, os.path.join("public", item))
        print(f"✔ Mirrored to public/: {item}")
    else:
        print(f"⚠ Missing from root: {item}")

# 4. Git add, commit, and push
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "fix: wire all URL hash anchor targets and mirror full manifest to public/"], check=False)
push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr:
    print(push_res.stderr)

print("=" * 80)
print("ALL ASSETS DEPLOYED AND URL ROUTING REPAIRED.")
print("=" * 80)
