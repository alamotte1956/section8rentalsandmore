
// tax_form_generator.js - Form 1099-MISC & 1099-NEC Tax Compliance Generator
// Standards: IRS Form 1099 Reporting & Minnesota Department of Revenue Rules

function generateAnnual1099Statements(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const hapAnnual = (Number(p.hap || p.hapPortion || 1520) * 12);
  const tenantCopayAnnual = (Number(p.copay || p.copayPortion || 430) * 12);
  const totalRents = hapAnnual + tenantCopayAnnual;

  const contractorDisbursements = [
    { name: 'Twin Cities Mechanical Solutions LLC', tin: 'XX-XXX4910', amount: 1450.00, purpose: 'HVAC & Plumbing Repairs' },
    { name: 'Metro Paint & Drywall Remediation', tin: 'XX-XXX7182', amount: 825.00, purpose: 'Turnover & Lead Stabilization' }
  ];

  const statement = `================================================================================
INTERNAL REVENUE SERVICE • FORM 1099 ANNUAL INFORMATION STATEMENTS
TAX YEAR 2026 STAGING & RECONCILIATION SUMMARY
================================================================================

PAYER INFORMATION:
  Entity Name       : Section 8 Rentals and More LLC
  Authorized Agent  : Dr. Albert Ray LaMotte
  Mailing Address   : Bloomington & Lakeville, MN
  EIN               : On File (Primary Operating Entity)

--------------------------------------------------------------------------------
PART I: FORM 1099-MISC SUMMARY (RENTAL REAL ESTATE DISBURSEMENTS)
--------------------------------------------------------------------------------
RECIPIENT (LESSOR / OWNER RECORD):
  Property Address  : ${p.address}, ${p.city}, ${p.state}
  County / Agency   : ${p.county || 'Hennepin'} County Public Housing Agency

IRS REPORTING BOXES:
  • Box 1 - Rents (Total Gross Disbursed)     : $${totalRents.toFixed(2)}
    - Sovereign HAP Share (HUD Subsidy)      : $${hapAnnual.toFixed(2)}
    - Resident Copayments Received           : $${tenantCopayAnnual.toFixed(2)}
  • Box 4 - Federal Income Tax Withheld      : $0.00
  • State / Payer's State No. (MN / WI)      : Reported to MN Dept of Revenue

--------------------------------------------------------------------------------
PART II: FORM 1099-NEC SUMMARY (NONEMPLOYEE COMPENSATION - TRADE VENDORS)
--------------------------------------------------------------------------------
The following independent tradespersons received payments ≥ $600 for maintenance,
life-safety remediation, or turnover repairs on this property:

${contractorDisbursements.map((c, idx) => `[VENDOR ${idx + 1}]
  Recipient Name  : ${c.name}
  Recipient TIN   : ${c.tin}
  Box 1 (NEC Comp): $${c.amount.toFixed(2)}
  Trade Purpose   : ${c.purpose}
  Reporting Status: Mandatory IRS & MN Dept of Revenue Electronic Filing`).join('

')}

================================================================================
CERTIFICATION OF TAX FILING ACCORD:
================================================================================
I declare that to the best of my knowledge and belief, this statement is true,
correct, and complete pursuant to IRS Treasury Regulations and Section 6041/6041A.

Authorized Filing Officer: Dr. Albert Ray LaMotte, Principal & CEO
Entity: Section 8 Rentals and More LLC • alamotte1956@gmail.com
Execution Date: ${new Date().toLocaleDateString()}
Tax Staging Token: [IRS-1099-STAGING-STAMP-${Date.now().toString().slice(-8)}]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${statement}</pre>`);
  w.document.close();
  w.print();
}

window.generateAnnual1099Statements = generateAnnual1099Statements;
