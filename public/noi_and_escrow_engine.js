
// noi_and_escrow_engine.js - General Ledger NOI & Statutory Escrow Math

function calculatePropertyNOIBreakdown() {
  const container = document.getElementById('propertyExpenseCards');
  if (!container || typeof state === 'undefined' || !state.properties) return;

  container.innerHTML = '';
  state.properties.forEach(p => {
    const propTx = (state.accountingLedger || state.ledger || []).filter(tx => 
      (tx.propertyId && tx.propertyId === p.id) || 
      (tx.unitAddress && tx.unitAddress.includes(p.address)) ||
      (tx.unit && tx.unit.includes(p.address))
    );

    const revenue = propTx
      .filter(tx => tx.type === 'income' || (tx.category && tx.category.includes('Rent')) || (tx.cat && tx.cat.includes('HAP')))
      .reduce((sum, tx) => sum + (Number(tx.amount) || 0), 0) || Number(p.contractRent || p.rent || 0);

    const expense = propTx
      .filter(tx => tx.type === 'expense' || (tx.category && tx.category.includes('Maintenance')))
      .reduce((sum, tx) => sum + (Number(tx.amount) || 0), 0);

    const noi = revenue - expense;

    // Statutory Escrow Interest Calculation (Minn. Stat. § 504B.178: 1% annual simple interest)
    const deposit = Number(p.deposit || p.contractRent || p.rent || 0);
    const statutoryAnnualInterest = (deposit * 0.01).toFixed(2);

    container.innerHTML += `
      <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-white truncate">${p.address}</span>
          <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">QBO Active</span>
        </div>
        <div class="grid grid-cols-3 gap-2 text-center text-xs py-1.5 bg-slate-900/80 rounded-xl">
          <div><span class="text-[10px] text-slate-500 uppercase block">Revenue</span><strong class="text-emerald-400 font-mono">$${revenue}</strong></div>
          <div><span class="text-[10px] text-slate-500 uppercase block">Expense</span><strong class="text-rose-400 font-mono">$${expense}</strong></div>
          <div><span class="text-[10px] text-slate-500 uppercase block">NOI</span><strong class="text-teal-300 font-mono">$${noi}</strong></div>
        </div>
        <div class="text-[10px] text-slate-400 flex justify-between pt-1 border-t border-slate-900">
          <span>Trust Escrow: $${deposit}</span>
          <span class="text-amber-400 font-mono">1% Stat Int: +$${statutoryAnnualInterest}/yr</span>
        </div>
      </div>
    `;
  });
}

// Bind to tab switch and startup
window.addEventListener('DOMContentLoaded', calculatePropertyNOIBreakdown);
window.addEventListener('load', calculatePropertyNOIBreakdown);
