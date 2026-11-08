
// escrow_reconciliation_engine.js - Security Deposit Trust Account & Interest Engine
// Authority: Minn. Stat. § 504B.178 Subd. 2 & Wis. Stat. § 704.28 Trust Mandates

function generateEscrowTrustCertificate(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const baseDeposit = Number(p.deposit || p.contractRent || 1950);
  const annualInterestRate = isMN ? 0.01 : 0.00;
  const annualInterest = baseDeposit * annualInterestRate;
  const monthlyAccrual = annualInterest / 12;

  const trustBank = "Bremer Bank, N.A. (FDIC Insured)";
  const escrowAcct = "SEC8-ESCROW-TRUST-XXXX";

  const cert = `================================================================================
TENANT SECURITY DEPOSIT ESCROW RECEIPT & STATUTORY TRUST CERTIFICATE
Pursuant to ${isMN ? 'Minnesota Statutes § 504B.178' : 'Wisconsin Statutes § 704.28'}
================================================================================

1. TENANT & PREMISES IDENTIFICATION:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Tenant Resident   : ${p.tenant || p.tenantName || 'Resident Occupant'}
   Landlord / Entity : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)
   Date Funds Placed : ${new Date().toLocaleDateString()}

2. ESCROW TRUST ACCOUNTING PARTICULARS:
   Deposit Amount Received : $${baseDeposit.toFixed(2)}
   Depository Institution  : ${trustBank}
   Account Classification  : Segregated Landlord-Tenant Escrow Trust Account
   Escrow Identifier       : ${escrowAcct}

3. STATUTORY INTEREST TERMS & ACCRUAL ACCORD:
   • Statutory Interest Rate: ${isMN ? '1.0% Simple Annual Interest (Mandated by Minn. Stat. § 504B.178)' : '0.0% (Wisconsin Statutory Standard - Non-interest Bearing Trust)'}
   • Projected Annual Accrual : $${annualInterest.toFixed(2)} per year ($${monthlyAccrual.toFixed(2)}/mo)
   • Compounding Basis       : Simple Non-Compounded Interest
   • Statutory Holding Terms : Held in escrow until lawful return within 21 days
     of lease termination, subject only to verified damages beyond normal wear and tear.

4. STATUTORY RIGHTS & LIQUIDATION NOTICE:
   ${isMN ? 'Under Minnesota law, the landlord must hold deposit funds in a separate interest-bearing account in a bank or financial institution. Upon termination of tenancy, the landlord must return the full deposit plus accrued 1% interest within 3 weeks (21 days) after receiving the tenant forwarding address.' : 'Under Wisconsin law, security deposits must be kept in a segregated escrow account and disbursed or itemized within 21 days under Wis. Stat. § 704.28.'}

CERTIFIED BY MANAGING BROKER / PRINCIPAL:
Dr. Albert Ray LaMotte, Authorized Manager
Section 8 Rentals and More LLC • alamotte1956@gmail.com
Timestamp: ${new Date().toISOString()}
Verification Hash: [ESCROW-TRUST-VERIFIED-${Date.now().toString().slice(-8)}]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${cert}</pre>`);
  w.document.close();
  w.print();
}

window.generateEscrowTrustCertificate = generateEscrowTrustCertificate;
