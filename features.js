// features.js - Modular Feature Controller
const state = {
  properties: [
    { id: 'prop-1', address: '2418 Nicollet Ave', city: 'Minneapolis', state: 'MN', rent: 1950, hap: 1520, copay: 430, status: 'Paid', tenant: 'Keisha Johnson' },
    { id: 'prop-2', address: '892 University Ave W', city: 'Saint Paul', state: 'MN', rent: 2350, hap: 1880, copay: 470, status: 'Overdue', tenant: 'Carlos Rivera' },
    { id: 'prop-3', address: '410 2nd St S', city: 'Hudson', state: 'WI', rent: 1775, hap: 1340, copay: 435, status: 'Paid', tenant: 'Brian Schultz' }
  ],
  ledger: [
    { id: 'TX-901', date: '2026-11-01', unit: '2418 Nicollet Ave', cat: 'HAP Subsidy', amount: 1520 },
    { id: 'TX-902', date: '2026-11-02', unit: '2418 Nicollet Ave', cat: 'Tenant Copay', amount: 430 }
  ]
};

function switchTab(tabId) {
  const views = ['dashboard', 'reminders', 'accounting', 'evictions', 'calendar', 'onboarding'];
  views.forEach(v => {
    const el = document.getElementById('view-' + v);
    if (el) el.classList.add('hidden');
  });
  const target = document.getElementById('view-' + tabId);
  if (target) target.classList.remove('hidden');
  if (tabId === 'reminders') renderReminders();
  if (tabId === 'accounting') renderLedger();
  if (tabId === 'evictions') renderNotice();
}

function renderReminders() {
  const tb = document.getElementById('rentRemindersTableBody');
  if (!tb) return;
  tb.innerHTML = state.properties.map(p => `
    <tr class="hover:bg-slate-900/60 p-2 border-b border-slate-800">
      <td class="p-3 font-bold text-white">${p.address}</td>
      <td class="p-3 text-slate-300">${p.tenant}</td>
      <td class="p-3 font-bold text-blue-400">$${p.copay}</td>
      <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.status === 'Overdue' ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-400'}">${p.status}</span></td>
      <td class="p-3 text-right"><button onclick="alert('Notice sent to ${p.tenant}!')" class="px-2.5 py-1 bg-amber-600 text-white font-bold rounded text-xs">Send Reminder</button></td>
    </tr>
  `).join('');
}

function renderLedger() {
  const tb = document.getElementById('accountingLedgerBody');
  if (!tb) return;
  tb.innerHTML = state.ledger.map(t => `
    <tr class="hover:bg-slate-900/60 p-2 border-b border-slate-800">
      <td class="p-3 text-slate-400">${t.id}</td>
      <td class="p-3 text-white">${t.unit}</td>
      <td class="p-3 text-slate-300">${t.cat}</td>
      <td class="p-3 font-bold text-emerald-400">$${t.amount}</td>
    </tr>
  `).join('');
}

function renderNotice() {
  const c = document.getElementById('noticeDocumentCanvas');
  if (c) {
    c.innerText = `FORMAL NOTICE PURSUANT TO MINN. STAT. § 504B.321 / WIS. STAT. § 704.17\nDate: ${new Date().toLocaleDateString()}\nTenant: Carlos Rivera\nPremises: 892 University Ave W, Saint Paul, MN\nUnpaid Copay Share: $470.00\nLate Fee (8% Cap): $37.60\nTotal Required to Cure: $507.60\nLandlord: Dr. Albert Ray LaMotte • Section 8 Rentals and More LLC`;
  }
}
