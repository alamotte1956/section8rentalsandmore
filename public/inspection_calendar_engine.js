// inspection_calendar_engine.js - Statutory Inspection & Moratorium Calendar
function openComplianceCalendarModal() {
  const props = window.state?.properties || [];
  let modal = document.getElementById('calendarModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'calendarModal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4 overflow-y-auto';
    document.body.appendChild(modal);
  }
  const isCWR = [10,11,12,1,2,3,4].includes(new Date().getMonth() + 1);
  modal.innerHTML = `
    <div class="relative w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-6 text-slate-100 my-8">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 class="text-xl font-bold text-white">Statutory Inspection & Moratorium Calendar</h3>
          <p class="text-xs text-slate-400">NSPIRE 2026, EPA Lead Clearances & Minn. Stat. § 216B.096</p>
        </div>
        <button onclick="document.getElementById('calendarModal').remove()" class="text-slate-400 hover:text-white text-2xl font-bold">×</button>
      </div>
      <div class="space-y-3 text-xs">
        <div class="bg-slate-950 p-4 rounded-2xl border ${isCWR ? 'border-amber-500/50 bg-amber-950/10' : 'border-slate-800'}">
          <div class="font-bold text-amber-300">MN Cold Weather Rule Moratorium (Minn. Stat. § 216B.096)</div>
          <div class="text-slate-400 mt-1">Oct 1 - Apr 30: Continuous 68°F heating standard enforced across all habitable living spaces.</div>
        </div>
        ${props.map(p => `
          <div class="bg-slate-950 p-3 rounded-2xl border border-slate-800 flex justify-between">
            <div>
              <div class="font-bold text-white">${p.address}</div>
              <div class="text-slate-400">NSPIRE Annual Due: 2026-12-15 • County: ${p.county || 'Hennepin'}</div>
            </div>
            <span class="text-cyan-400 font-mono">SCHEDULED</span>
          </div>
        `).join('')}
      </div>
      <div class="text-right">
        <button onclick="document.getElementById('calendarModal').remove()" class="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs">Close</button>
      </div>
    </div>
  `;
}
window.openComplianceCalendarModal = openComplianceCalendarModal;
