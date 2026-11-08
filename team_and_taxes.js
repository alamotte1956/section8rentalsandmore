
// team_and_taxes.js - Staff & Schedule E Engine
const staffState = {
  managers: [
    { name: 'Sarah Lindqvist', email: 'manager@section8rentals.com', region: 'All Metro Units', status: 'Active' },
    { name: 'Marcus Vance', email: 'mvance@section8rentals.com', region: 'Hennepin County', status: 'Active' }
  ]
};

function renderAssignedManagers() {
  const tbody = document.getElementById('assignedManagersTableBody');
  if (!tbody) return;
  tbody.innerHTML = staffState.managers.map(m => `
    <tr class="hover:bg-slate-900/60 p-2 border-b border-slate-800">
      <td class="p-3 font-bold text-white">${m.name}</td>
      <td class="p-3 text-slate-300 font-mono">${m.email}</td>
      <td class="p-3 text-slate-400">${m.region}</td>
      <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400">${m.status}</span></td>
      <td class="p-3 text-right"><button onclick="alert('Access verified for ${m.name}')" class="text-blue-400 hover:underline">Manage</button></td>
    </tr>
  `).join('');
}

function updateReportPreview() {
  const canvas = document.getElementById('stagedReportCanvas');
  if (!canvas) return;
  canvas.innerText = `IRS FORM 1040 SCHEDULE E - DUAL-STATE SECTION 8 PORTFOLIO REPORT\nOperator: Dr. Albert Ray LaMotte • Section 8 Rentals and More LLC\nDate Generated: ${new Date().toLocaleDateString()}\nTotal Monthly Gross Rents: $6,075.00\nGovernment HAP Subsidies: $4,740.00 (Form 1099-MISC Box 1)\nTenant Direct Copays: $1,335.00\nOperating Net Margin: 78.02% Guaranteed Direct Deposit`;
}

function printFormattedReport() {
  const content = document.getElementById('stagedReportCanvas')?.innerText || '';
  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 13px; line-height: 1.5; padding: 20px;">${content}</pre>`);
  w.document.close();
  w.print();
}
