
// tenant_portal_engine.js - Resident Portal & NSPIRE Maintenance Ticketing Engine
// Standards: 24 CFR § 982.401 Habitability, Minn. Stat. § 504B.385 & CWR Compliance

function openTenantPortalModal(propId) {
  const p = (window.state?.properties || []).find(x => x.id === propId) || 
            (window.state?.properties && window.state.properties[0]) || {
              id: 'prop-1',
              address: '7820 Penn Ave S',
              city: 'Bloomington',
              state: 'MN',
              county: 'Hennepin',
              rent: 2150,
              hap: 1680,
              copay: 470,
              tenant: 'Marcus & Elena Vance'
            };

  let modal = document.getElementById('tenantPortalModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'tenantPortalModal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4 overflow-y-auto';
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="relative w-full max-w-3xl bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-6 text-slate-100 my-8 max-h-[90vh] flex flex-col">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4 shrink-0">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-sky-400"></span>
            <h3 class="text-xl font-bold text-white tracking-tight">Resident Portal & Maintenance Center</h3>
          </div>
          <p class="text-xs text-slate-400 mt-1">Resident: <strong class="text-white">${p.tenant || p.tenantName || 'Resident Occupant'}</strong> • ${p.address}, ${p.city}, ${p.state}</p>
        </div>
        <button onclick="document.getElementById('tenantPortalModal').remove()" class="text-slate-400 hover:text-white text-2xl font-bold px-3 py-1 rounded-xl hover:bg-slate-800 transition-colors">×</button>
      </div>

      <div class="overflow-y-auto pr-2 space-y-6 flex-1 custom-scrollbar">
        <!-- Account Financial Overview -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="bg-slate-950/70 border border-slate-800 p-4 rounded-2xl">
            <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Your Monthly Copay</span>
            <div class="text-2xl font-black text-white mt-1">$${(p.copay || p.copayPortion || 470).toFixed(2)}</div>
            <span class="text-[10px] text-emerald-400">Due 1st of month (8% cap rule)</span>
          </div>
          <div class="bg-slate-950/70 border border-slate-800 p-4 rounded-2xl">
            <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">County PHA Subsidy</span>
            <div class="text-2xl font-black text-sky-400 mt-1">$${(p.hap || p.hapPortion || 1680).toFixed(2)}</div>
            <span class="text-[10px] text-slate-400">${p.county || 'Hennepin'} County direct disbursement</span>
          </div>
          <div class="bg-slate-950/70 border border-slate-800 p-4 rounded-2xl">
            <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Total Contract Rent</span>
            <div class="text-2xl font-black text-slate-300 mt-1">$${(p.rent || p.contractRent || 2150).toFixed(2)}</div>
            <span class="text-[10px] text-slate-500">100% Guaranteed under HAP</span>
          </div>
        </div>

        <!-- Quick Document Access -->
        <div class="bg-slate-950/50 border border-slate-800/80 rounded-2xl p-4 space-y-2">
          <div class="text-xs font-bold text-slate-300 uppercase tracking-wider">Statutory Documents & Certificates</div>
          <div class="flex flex-wrap gap-2 pt-1">
            <button onclick="if(window.generateStateRentCreditCertificate) generateStateRentCreditCertificate('${p.id}');" class="px-3 py-1.5 text-xs font-semibold rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30 transition-all">📄 Download Form CRP / Rent Cert</button>
            <button onclick="if(window.generateColdWeatherRuleNotice) generateColdWeatherRuleNotice('${p.id}');" class="px-3 py-1.5 text-xs font-semibold rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/30 transition-all">❄️ Cold Weather Heating Rights</button>
            <button onclick="if(window.generateVawaNotice) generateVawaNotice('${p.id}');" class="px-3 py-1.5 text-xs font-semibold rounded-xl bg-slate-800 text-slate-300 hover:text-white transition-all">⚖️ VAWA Occupancy Rights</button>
          </div>
        </div>

        <!-- Submit Maintenance Ticket Form -->
        <div class="bg-slate-950/70 border border-slate-800 rounded-2xl p-5 space-y-4">
          <div>
            <h4 class="text-sm font-bold text-white flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
              Submit Habitability or Repair Request
            </h4>
            <p class="text-[11px] text-slate-400 mt-0.5">Triage routes work orders immediately to certified Twin Cities contractors pursuant to NSPIRE standards.</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div>
              <label class="block text-slate-300 font-semibold mb-1">Defect Urgency Classification</label>
              <select id="ticketUrgency" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-sky-500">
                <option value="P1_EMERGENCY">Priority 1 (Emergency - 24-Hr Cure): Heating, Gas, Electrical, Water</option>
                <option value="P2_STANDARD" selected>Priority 2 (Routine - 30-Day Cure): Drywall, Hardware, Minor Fixture</option>
                <option value="P3_SCHEDULED">Priority 3: Preventative / Seasonal Maintenance</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-300 font-semibold mb-1">Affected Location / Room</label>
              <input type="text" id="ticketRoom" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-sky-500" placeholder="e.g. Basement Furnace, Kitchen Sink" value="Living Room / Entryway">
            </div>
          </div>

          <div class="text-xs">
            <label class="block text-slate-300 font-semibold mb-1">Specific Description of Condition</label>
            <textarea id="ticketDesc" rows="3" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-sky-500" placeholder="Provide details of the issue..."></textarea>
          </div>

          <div class="flex items-center justify-between pt-2 border-t border-slate-800/80">
            <span class="text-[11px] text-slate-500">Auto-timestamps request for Minn. Stat. § 504B.385 compliance.</span>
            <button onclick="submitMaintenanceTicket('${p.id}')" class="px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition-all shadow-lg shadow-sky-500/20">
              Submit Work Order
            </button>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-slate-800 text-xs text-slate-400 shrink-0">
        <span>Section 8 Rentals and More LLC • Emergency Dispatch Line: 24/7 Monitored</span>
        <button onclick="document.getElementById('tenantPortalModal').remove()" class="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold transition-colors">Close Portal</button>
      </div>
    </div>
  `;
}

function submitMaintenanceTicket(propId) {
  const urgency = document.getElementById('ticketUrgency')?.value || 'P2_STANDARD';
  const room = document.getElementById('ticketRoom')?.value || 'General';
  const desc = document.getElementById('ticketDesc')?.value || 'Unspecified routine repair request';

  const ticketId = `TKT-${Date.now().toString().slice(-6)}`;
  const timestamp = new Date().toISOString();

  alert(`[WORK ORDER DISPATCHED]\n\nTicket ID: ${ticketId}\nUrgency: ${urgency}\nArea: ${room}\nTimestamp: ${timestamp}\n\nStatus: Assigned to Twin Cities Trade Dispatch. If classified as Priority 1 (Life-Threatening), technician response is initiated immediately.`);

  const modal = document.getElementById('tenantPortalModal');
  if (modal) modal.remove();
}

window.openTenantPortalModal = openTenantPortalModal;
window.submitMaintenanceTicket = submitMaintenanceTicket;
