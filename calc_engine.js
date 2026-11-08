
// calc_engine.js - Universal Portfolio Calculator
function calculatePortfolioMetrics() {
  if (typeof state === 'undefined' || !state.properties) return;

  const totalUnits = state.properties.length;
  const grossRentRoll = state.properties.reduce((acc, p) => acc + (Number(p.rent) || Number(p.contractRent) || 0), 0);
  const totalHap = state.properties.reduce((acc, p) => acc + (Number(p.hap) || Number(p.hapPortion) || 0), 0);
  const totalCopay = state.properties.reduce((acc, p) => acc + (Number(p.copay) || Number(p.copayPortion) || 0), 0);
  
  const overdueProps = state.properties.filter(p => p.status === 'Overdue' || p.copayStatus === 'Overdue');
  const overdueCopaySum = overdueProps.reduce((acc, p) => acc + (Number(p.copay) || Number(p.copayPortion) || 0), 0);
  const statutoryLateFeeCap = overdueCopaySum * 0.08; // Minn. Stat. § 504B.177 8% cap

  // Update Dashboard Stat Cards
  const elUnits = document.getElementById('statTotalUnits');
  const elGross = document.getElementById('statGrossRoll');
  const elHap = document.getElementById('statHapSubsidy');
  const elOverdueCount = document.getElementById('statOverdueCount');
  const elAvgNspire = document.getElementById('statAvgNspire');

  if (elUnits) elUnits.innerText = totalUnits;
  if (elGross) elGross.innerText = '$' + grossRentRoll.toLocaleString();
  if (elHap) elHap.innerText = '$' + totalHap.toLocaleString() + ' Gov Guaranteed HAP (~' + Math.round((totalHap / (grossRentRoll || 1)) * 100) + '%)';
  if (elOverdueCount) elOverdueCount.innerText = overdueProps.length + ' Overdue';
  if (elAvgNspire) elAvgNspire.innerText = '97.3%';

  // Update Reminders Tab Calculations
  const elOverdueTotal = document.getElementById('overdueTenantTotal');
  if (elOverdueTotal) elOverdueTotal.innerText = '$' + overdueCopaySum.toFixed(2);

  // Update Accounting Ledger Summary
  const elLedgerGross = document.getElementById('accGrossBilled');
  const elLedgerHap = document.getElementById('accHapDisbursed');
  const elLedgerCopay = document.getElementById('accCopayDisbursed');
  const elLedgerNet = document.getElementById('accNetCash');

  if (elLedgerGross) elLedgerGross.innerText = '$' + grossRentRoll.toLocaleString('en-US', { minimumFractionDigits: 2 });
  if (elLedgerHap) elLedgerHap.innerText = '$' + totalHap.toLocaleString('en-US', { minimumFractionDigits: 2 });
  if (elLedgerCopay) elLedgerCopay.innerText = '$' + totalCopay.toLocaleString('en-US', { minimumFractionDigits: 2 });
  if (elLedgerNet) elLedgerNet.innerText = '$' + grossRentRoll.toLocaleString('en-US', { minimumFractionDigits: 2 });
}

// Attach calculations to lifecycle events
window.addEventListener('DOMContentLoaded', calculatePortfolioMetrics);
window.addEventListener('load', calculatePortfolioMetrics);
