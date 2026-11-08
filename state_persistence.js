// state_persistence.js - Multi-County Portfolio State & Local Sync
window.state = {
  properties: [
    {
      id: "prop-1",
      address: "7820 Penn Ave S",
      city: "Bloomington",
      state: "MN",
      zip: "55431",
      county: "Hennepin",
      pha: "MPHA (MN002)",
      tenant: "Marcus & Elena Vance",
      contractRent: 2150.00,
      hap: 1680.00,
      copay: 470.00,
      status: "Active Voucher"
    },
    {
      id: "prop-2",
      address: "1423 University Ave W",
      city: "Saint Paul",
      state: "MN",
      zip: "55104",
      county: "Ramsey",
      pha: "St. Paul PHA (MN001)",
      tenant: "Tariq & Amina Al-Mansoor",
      contractRent: 2280.00,
      hap: 1810.00,
      copay: 470.00,
      status: "Active Voucher"
    },
    {
      id: "prop-3",
      address: "15320 Galaxie Ave",
      city: "Apple Valley",
      state: "MN",
      zip: "55124",
      county: "Dakota",
      pha: "Dakota CDA (MN042)",
      tenant: "Darnell & Kendra Washington",
      contractRent: 1980.00,
      hap: 1530.00,
      copay: 450.00,
      status: "Active Voucher"
    },
    {
      id: "prop-4",
      address: "412 2nd St",
      city: "Hudson",
      state: "WI",
      zip: "54016",
      county: "St. Croix (WI)",
      pha: "Hudson HA (WI198)",
      tenant: "Sarah Lindstrom",
      contractRent: 1890.00,
      hap: 1420.00,
      copay: 470.00,
      status: "Active Voucher"
    },
    {
      id: "prop-5",
      address: "2840 Coon Rapids Blvd NW",
      city: "Coon Rapids",
      state: "MN",
      zip: "55433",
      county: "Anoka",
      pha: "ACCAP (MN027)",
      tenant: "Brianna Jenkins",
      contractRent: 2180.00,
      hap: 1680.00,
      copay: 500.00,
      status: "Active Voucher"
    }
  ]
};

function renderAdminPortfolioGrid() {
  const tbody = document.getElementById("adminPropertyTableBody");
  if (!tbody || !window.state.properties) return;
  tbody.innerHTML = "";
  window.state.properties.forEach(p => {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-slate-900/50 transition-colors";
    tr.innerHTML = `
      <td class="py-3.5 px-3 font-semibold text-white">${p.address}<div class="text-[10px] text-slate-400">${p.city}, ${p.state} ${p.zip}</div></td>
      <td class="py-3.5 px-3 font-mono text-cyan-400">${p.county}<div class="text-[10px] text-slate-400">${p.pha}</div></td>
      <td class="py-3.5 px-3 text-slate-300">${p.tenant}</td>
      <td class="py-3.5 px-3 font-mono font-bold text-white">$${p.contractRent.toFixed(2)}</td>
      <td class="py-3.5 px-3 font-mono font-bold text-emerald-400">$${p.hap.toFixed(2)}</td>
      <td class="py-3.5 px-3 font-mono text-amber-300">$${p.copay.toFixed(2)}</td>
      <td class="py-3.5 px-3"><span class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 text-[10px] font-semibold">${p.status}</span></td>
      <td class="py-3.5 px-3 text-right">
        <button onclick="openComplianceHubModal()" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 text-[11px] font-semibold">Dockets</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

window.renderAdminPortfolioGrid = renderAdminPortfolioGrid;
document.addEventListener("DOMContentLoaded", renderAdminPortfolioGrid);
