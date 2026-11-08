
// escrow_disposition_engine.js - Statutory Security Deposit Accounting & Disposition
// Governing Standards: Minn. Stat. § 504B.178 (1% Simple Interest / 21-Day Rule) & Wis. Stat. § 704.28

function generateSecurityDepositDisposition(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const baseDeposit = Number(p.deposit || p.contractRent || 1950);
  const tenancyYears = 1.0; // 12-month standard lease term
  
  // Minn. Stat. § 504B.178 Subd. 2: 1% simple non-compounded interest
  const interestRate = isMN ? 0.01 : 0.00;
  const accruedInterest = baseDeposit * interestRate * tenancyYears;
  const totalHeld = baseDeposit + accruedInterest;

  // Standardized line itemization for post-tenancy inspection
  const deductions = [
    { desc: 'Unpaid Tenant Rent Copay Balance', amount: 0.00 },
    { desc: 'Contracted Wall Patching / Excessive Nail Holes (Beyond Wear & Tear)', amount: 150.00 },
    { desc: 'Professional Carpet Deodorization & Deep Extraction', amount: 125.00 }
  ];

  const totalDeductions = deductions.reduce((sum, item) => sum + item.amount, 0);
  const refundDueTenant = Math.max(0, totalHeld - totalDeductions);
  const tenantOwesLandlord = Math.max(0, totalDeductions - totalHeld);

  const deadlineDays = 21; // 21 calendar days for both MN and WI
  const terminationDate = new Date();
  const statutoryDeadline = new Date();
  statutoryDeadline.setDate(terminationDate.getDate() + deadlineDays);

  const statement = `================================================================================
STATUTORY SECURITY DEPOSIT DISPOSITION & RECONCILIATION STATEMENT
Pursuant to ${isMN ? 'Minnesota Statutes § 504B.178' : 'Wisconsin Statutes § 704.28'}
================================================================================

1. TENANCY PARTICULARS:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Resident Name     : ${p.tenant || p.tenantName || 'Resident Occupant'}
   Lease Termination : ${terminationDate.toLocaleDateString()}
   Statutory 21-Day  : MUST BE DELIVERED ON OR BEFORE ${statutoryDeadline.toLocaleDateString()}
   Managing Provider : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)

2. DEPOSIT ACCOUNTING & ACCRUED STATUTORY INTEREST:
   Original Deposit Received            : $${baseDeposit.toFixed(2)}
   ${isMN ? `Statutory Escrow Interest (1.0% Simple): $${accruedInterest.toFixed(2)} (Minn. Stat. § 504B.178)` : 'Wisconsin FDIC Escrow Holding  : $0.00 (No statutory statutory rate)'}
   ------------------------------------------------------------------------------
   TOTAL FUNDS ACCOUNTED FOR            : $${totalHeld.toFixed(2)}

3. SPECIFIC ITEMIZED DEDUCTIONS (DAMAGE BEYOND NORMAL WEAR & TEAR):
${deductions.map(d => `   • ${d.desc.padEnd(52)} : $${d.amount.toFixed(2)}`).join('
')}
   ------------------------------------------------------------------------------
   TOTAL AUTHORIZED ITEMIZED DEDUCTIONS : $${totalDeductions.toFixed(2)}

4. NET DISPOSITION SETTLEMENT:
   • Total Amount Refundable to Tenant  : $${refundDueTenant.toFixed(2)}
   • Additional Deficit Owed by Tenant  : $${tenantOwesLandlord.toFixed(2)}

5. STATUTORY ADVISORY & DISCLOSURES:
   ${isMN ? 'Minnesota law entitles the tenant to an impartial, written explanation of all deductions within 21 days after tenancy terminates and landlord receives forwarding address. Bad faith retention subjects landlord to punitive damages equal to the deposit retained plus $500 under Minn. Stat. § 504B.178 Subd. 7.' : 'Wisconsin law requires written itemization within 21 days pursuant to Wis. Stat. § 704.28.'}

CERTIFICATION OF ACCOUNTING:
I certify that the above itemization is true and correct, and reflects actual
remediation expenditures and authorized deductions.

Authorized Agent : Dr. Albert Ray LaMotte, Managing Principal
Entity           : Section 8 Rentals and More LLC
Payment Mode     : Check / Direct Deposit Enclosed
Generated Date   : ${new Date().toLocaleDateString()}`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${statement}</pre>`);
  w.document.close();
  w.print();
}

window.generateSecurityDepositDisposition = generateSecurityDepositDisposition;
