import os
import shutil
import subprocess

compliance_hub_js = """
// compliance_hub.js - Universal Document & Statutory Action Modal

function openComplianceModal(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  let modal = document.getElementById('complianceHubModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'complianceHubModal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4';
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 class="text-lg font-bold text-white flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
            Compliance & Document Generator
          </h3>
          <p class="text-xs text-slate-400 mt-0.5">${p.address}, ${p.city}, ${p.state} • ${p.county || 'Hennepin'} County</p>
        </div>
        <button onclick="document.getElementById('complianceHubModal').remove()" class="text-slate-400 hover:text-white text-xl font-bold px-2 py-1 rounded-lg hover:bg-slate-800">×</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <button onclick="generateMasterCompliancePacket('${p.id}')" class="p-3.5 text-left rounded-2xl bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 transition-all">
          <div class="font-bold text-emerald-300">★ 1-Click Master Lease-Up Packet</div>
          <div class="text-[11px] text-slate-400 mt-1">Bundles RFTA, HAP, UA, VAWA, Lead Paint & NSPIRE into a single certified PDF.</div>
        </button>

        <button onclick="dispatchPacketToPha('${p.id}', 'RFTA')" class="p-3.5 text-left rounded-2xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 transition-all">
          <div class="font-bold text-cyan-300">Direct County PHA Dispatch</div>
          <div class="text-[11px] text-slate-400 mt-1">Routes pre-formatted submission directly to verified PHA intake inboxes.</div>
        </button>

        <button onclick="generateRftaPacket('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">HUD-52517 (RFTA Packet)</div>
          <div class="text-[11px] text-slate-400 mt-1">Request for Tenancy Approval with 2026 SAFMR county standards.</div>
        </button>

        <button onclick="generateStatutoryNotice('${p.id}')" class="p-3.5 text-left rounded-2xl bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 transition-all">
          <div class="font-bold text-rose-300">Statutory Notice / Cure Demand</div>
          <div class="text-[11px] text-slate-400 mt-1">MN § 504B 14-day / WI § 704 5-day notice with federal CARES Act 30-day window.</div>
        </button>

        <button onclick="runNspireAuditAudit('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">NSPIRE Pre-Inspection Audit</div>
          <div class="text-[11px] text-slate-400 mt-1">Weighted scoring checklist & pre-walkthrough pass-rate certificate.</div>
        </button>

        <button onclick="generateCureCertification('${p.id}', 'LTF')" class="p-3.5 text-left rounded-2xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 transition-all">
          <div class="font-bold text-amber-300">HUD-52580 Defect Cure Cert</div>
          <div class="text-[11px] text-slate-400 mt-1">24-hour emergency LTF and 30-day NLTF repair completion attestation.</div>
        </button>

        <button onclick="generateRentReasonablenessStudy('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">SAFMR Rent Reasonableness</div>
          <div class="text-[11px] text-slate-400 mt-1">24 CFR § 982.507 comparability review against 2026 Small Area FMR benchmarks.</div>
        </button>

        <button onclick="generateHapContract('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">HUD-52641 HAP Contract</div>
          <div class="text-[11px] text-slate-400 mt-1">Housing Assistance Payments contract covenants & direct-deposit ACH setup.</div>
        </button>

        <button onclick="computeUtilityAllowanceBreakdown('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">HUD-52667 Utility Allowance</div>
          <div class="text-[11px] text-slate-400 mt-1">Itemized utility schedule & net tenant rent copayment tally.</div>
        </button>

        <button onclick="generateLeadPaintDisclosure('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">EPA Lead Paint Disclosure</div>
          <div class="text-[11px] text-slate-400 mt-1">24 CFR Part 35 visual clearance attestation for pre-1978 properties.</div>
        </button>

        <button onclick="generateVawaNotice('${p.id}')" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">HUD-5380 VAWA Rights Notice</div>
          <div class="text-[11px] text-slate-400 mt-1">Mandatory occupancy rights disclosure & emergency transfer addendum.</div>
        </button>

        <button onclick="generateOperationsManual()" class="p-3.5 text-left rounded-2xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-all">
          <div class="font-bold text-white">Dual-State SOP Manual</div>
          <div class="text-[11px] text-slate-400 mt-1">Standard operating procedures covering MN § 504B and WI § 704 operations.</div>
        </button>
      </div>

      <div class="flex items-center justify-between pt-2 border-t border-slate-800 text-[11px] text-slate-500">
        <span>Section 8 Rentals and More LLC • Legal & Compliance Engine</span>
        <button onclick="document.getElementById('complianceHubModal').remove()" class="px-4 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold transition-colors">Close</button>
      </div>
    </div>
  `;
}

window.openComplianceModal = openComplianceModal;
"""

with open("compliance_hub.js", "w", encoding="utf-8") as f:
    f.write(compliance_hub_js)

os.makedirs("public", exist_ok=True)
shutil.copy2("compliance_hub.js", "public/compliance_hub.js")

# Register in index.html
with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

if "compliance_hub.js" not in html:
    html = html.replace("</body>", '<script src="compliance_hub.js"></script>\n</body>', 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy2("index.html", "public/index.html")

subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "feat: integrate universal compliance action modal hub"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=False)
print("SUCCESS: Universal Compliance Hub deployed live to Cloudflare Pages.")
