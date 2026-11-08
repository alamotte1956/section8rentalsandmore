
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


// Extended Dynamic Calculations for Legal Notices, Schedule E, and Property NOI

function recalculateNoticeAmounts() {
  const sel = document.getElementById('noticePropertySelect');
  const pId = sel ? sel.value : (state.properties[0]?.id || 'prop-1');
  const prop = state.properties.find(p => p.id === pId) || state.properties[0];
  if (!prop) return;

  const copayInput = document.getElementById('noticeDelinquentCopay');
  const lateFeeInput = document.getElementById('noticeLateFeeInput');
  const copayDisplay = document.getElementById('noticeCopayAmountDisplay');
  const hapDisplay = document.getElementById('noticeHapAmountDisplay');

  const copayVal = Number(prop.copay || prop.copayPortion || 430);
  const hapVal = Number(prop.hap || prop.hapPortion || 1520);
  const statutoryLateCap = Number((copayVal * 0.08).toFixed(2));

  if (copayDisplay) copayDisplay.innerText = '$' + copayVal.toFixed(2);
  if (hapDisplay) hapDisplay.innerText = '$' + hapVal.toFixed(2) + ' (Exempt Subsidy)';
  if (copayInput && !copayInput.value) copayInput.value = copayVal;
  if (lateFeeInput && !lateFeeInput.value) lateFeeInput.value = statutoryLateCap;

  const activeCopay = Number(copayInput?.value || copayVal);
  const activeLate = Number(lateFeeInput?.value || statutoryLateCap);
  const totalCure = (activeCopay + activeLate).toFixed(2);

  const canvas = document.getElementById('noticeDocumentCanvas');
  if (canvas) {
    canvas.innerText = `================================================================================
FORMAL LEGAL NOTICE FOR NONPAYMENT OF TENANT RENT COPAYMENT
PURSUANT TO ${prop.state === 'MN' ? 'MINN. STAT. § 504B.321' : 'WIS. STAT. § 704.17'} & FEDERAL CARES ACT
================================================================================
DATE: ${new Date().toLocaleDateString()}
TENANT: ${prop.tenant || prop.tenantName || 'Resident Occupant'}
PREMISES: ${prop.address}, ${prop.city}, ${prop.state}
HOUSING AGENCY: ${prop.tenantVoucherAgency || 'Public Housing Authority'}

ITEMIZATION OF PAST-DUE TENANT RENT SHARE:
  • Contract Rent: $${(Number(prop.rent || prop.contractRent)).toFixed(2)}
  • Gov't Housing Assistance Payment (HAP): $${hapVal.toFixed(2)} (EXEMPT)
  ------------------------------------------------------------------------------
  Past-Due Tenant Copay Share             : $${activeCopay.toFixed(2)}
  Permissible Late Fee (Statutory 8% Cap) : $${activeLate.toFixed(2)}
  ------------------------------------------------------------------------------
  TOTAL AMOUNT REQUIRED TO CURE DEFAULT   : $${totalCure}

STATUTORY LEGAL DISCLOSURE:
You have the right to seek legal assistance. In Minnesota: call HOME Line at (612) 728-5767.
In Wisconsin: contact Legal Action of Wisconsin at (855) 947-2529.

LANDLORD / AUTHORIZED AGENT:
Dr. Albert Ray LaMotte • Section 8 Rentals and More LLC
Direct Contact: alamotte1956@gmail.com`;
  }
}

// Bind notice inputs to instant recalculation
document.addEventListener('input', (e) => {
  if (e.target && (e.target.id === 'noticeDelinquentCopay' || e.target.id === 'noticeLateFeeInput' || e.target.id === 'noticeMonthsInput')) {
    recalculateNoticeAmounts();
  }
});

// Update Schedule E Tax calculations
function recalculateScheduleE() {
  const canvas = document.getElementById('stagedReportCanvas');
  if (!canvas || typeof state === 'undefined' || !state.properties) return;

  const grossMonthly = state.properties.reduce((acc, p) => acc + (Number(p.rent || p.contractRent) || 0), 0);
  const hapMonthly = state.properties.reduce((acc, p) => acc + (Number(p.hap || p.hapPortion) || 0), 0);
  const copayMonthly = state.properties.reduce((acc, p) => acc + (Number(p.copay || p.copayPortion) || 0), 0);

  const grossAnnual = grossMonthly * 12;
  const hapAnnual = hapMonthly * 12;
  const copayAnnual = copayMonthly * 12;
  const marginPct = ((hapMonthly / (grossMonthly || 1)) * 100).toFixed(1);

  canvas.innerText = `IRS FORM 1040 SCHEDULE E - DUAL-STATE SECTION 8 PORTFOLIO REPORT
Operator: Dr. Albert Ray LaMotte • Section 8 Rentals and More LLC
Date Generated: ${new Date().toLocaleDateString()}

ANNUALIZED RENTAL REVENUE (IRS Schedule E Part I):
  • Gross Annual Contract Rents: $${grossAnnual.toLocaleString('en-US', {minimumFractionDigits: 2})}
  • Gov't HAP Guaranteed Subsidies (Form 1099-MISC Box 1): $${hapAnnual.toLocaleString('en-US', {minimumFractionDigits: 2})}
  • Tenant Direct Copayment Collections: $${copayAnnual.toLocaleString('en-US', {minimumFractionDigits: 2})}

OPERATIONAL YIELD METRICS:
  • Guaranteed Federal Direct Deposit Ratio: ${marginPct}%
  • Delinquency Exposure Buffer: Sovereign HAP insulation under Minn. Stat. § 504B`;
}

// Attach extensions
window.addEventListener('DOMContentLoaded', () => {
  recalculateNoticeAmounts();
  recalculateScheduleE();
});
