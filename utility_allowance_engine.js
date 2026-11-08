
// utility_allowance_engine.js - HUD Form HUD-52667 Utility Allowance Engine
// Authority: 24 CFR § 982.517 (Metro HRA, MPHA, Saint Paul PHA Schedules)

const PHA_UTILITY_SCHEDULES_2026 = {
  natural_gas_heat: { 1: 42, 2: 56, 3: 71, 4: 88 },
  electric_heat: { 1: 78, 2: 104, 3: 132, 4: 165 },
  cooking_electric: { 1: 12, 2: 15, 3: 18, 22: 22 },
  other_electric_base: { 1: 38, 2: 48, 3: 59, 4: 72 },
  water_sewer: { 1: 45, 2: 60, 3: 75, 4: 90 },
  trash_collection: { 1: 22, 2: 22, 3: 22, 4: 22 }
};

function computeUtilityAllowanceBreakdown(propId, tenantPaidUtilities = ['cooking_electric', 'other_electric_base']) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const beds = p.bedrooms || 2;
  let totalAllowance = 0;
  const itemized = [];

  tenantPaidUtilities.forEach(utilKey => {
    const rate = (PHA_UTILITY_SCHEDULES_2026[utilKey] && PHA_UTILITY_SCHEDULES_2026[utilKey][beds]) || 20;
    totalAllowance += rate;
    itemized.push({ utility: utilKey.replace(/_/g, ' ').toUpperCase(), allowance: rate });
  });

  const contractRent = Number(p.rent || p.contractRent || 1950);
  const grossRent = contractRent + totalAllowance;
  const hapPortion = Number(p.hap || p.hapPortion || 1520);
  const netTenantCopay = Math.max(0, contractRent - hapPortion);
  const isUrpHapReimbursement = (contractRent - hapPortion) < 0;

  const doc = `================================================================================
HUD SECTION 8 UTILITY ALLOWANCE SCHEDULE & NET RENT ITEMIZATION
HUD Form HUD-52667 • 24 CFR § 982.517 (2026 Metro PHA Standards)
================================================================================

1. PREMISES & UNIT ARCHITECTURE:
   Address: ${p.address}, ${p.city}, ${p.state}
   Unit Size: ${beds}-Bedroom Single/Multi-Family
   Jurisdiction: ${p.county || 'Hennepin'} County PHA Schedule
   Owner Entity: Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)

2. UTILITY RESPONSIBILITY BREAKDOWN:
${itemized.map(i => `   • [TENANT PAID] ${i.utility.padEnd(28)} : $${i.allowance.toFixed(2)}/mo`).join('
')}
   • [OWNER PAID]  SPACE HEATING (NATURAL GAS)  : INCLUDED IN CONTRACT RENT
   • [OWNER PAID]  WATER, SEWER, & REFUSE       : INCLUDED IN CONTRACT RENT
   -----------------------------------------------------------------------------
   TOTAL MONTHLY TENANT UTILITY ALLOWANCE (UA)  : $${totalAllowance.toFixed(2)}/mo

3. GROSS RENT & CONTRACT ALLOCATION:
   Requested Monthly Contract Rent to Owner     : $${contractRent.toFixed(2)}
   Total Monthly Gross Rent (Contract + UA)      : $${grossRent.toFixed(2)}
   PHA Housing Assistance Payment (Direct ACH)   : $${hapPortion.toFixed(2)}
   -----------------------------------------------------------------------------
   NET TENANT RENT COPAYMENT SHARE              : $${netTenantCopay.toFixed(2)}/mo
   ${isUrpHapReimbursement ? 'TENANT UTILITY REIMBURSEMENT PAYMENT (URP): YES (Negative Rent Credit)' : 'TENANT RENT COPAYMENT REQUIRED: YES (Subject to 8% Cap)'}

4. REGULATORY CERTIFICATION:
   Owner certifies utilities provided are in compliance with NSPIRE operational standards.
   Evaluation Completed: ${new Date().toLocaleDateString()}
   Officer: Dr. Albert Ray LaMotte, Managing Principal`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${doc}</pre>`);
  w.document.close();
  w.print();
}

window.computeUtilityAllowanceBreakdown = computeUtilityAllowanceBreakdown;
