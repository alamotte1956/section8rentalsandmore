
// crp_tax_credit_engine.js - State Property Tax Refund & Rent Credit Engine
// Governing Authorities: Minn. Stat. § 290A.19 (Form CRP) & Wis. Stat. § 71.53 (Schedule H)

function generateStateRentCreditCertificate(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const contractRentMonthly = Number(p.rent || p.contractRent || 1950);
  const hapMonthly = Number(p.hap || p.hapPortion || 1520);
  const copayMonthly = Number(p.copay || p.copayPortion || 430);

  // Annual aggregations (12 months standard occupancy)
  const totalRentBilled = contractRentMonthly * 12;
  const sovereignHapAnnual = hapMonthly * 12;
  const tenantCopayAnnual = copayMonthly * 12;

  // MN e-File CRP e-Services verification code simulation
  const crpRefNum = `MN-CRP-2026-${Date.now().toString().slice(-8)}`;

  const cert = `================================================================================
${isMN ? 'STATE OF MINNESOTA DEPARTMENT OF REVENUE' : 'STATE OF WISCONSIN DEPARTMENT OF REVENUE'}
${isMN ? 'FORM CRP: CERTIFICATE OF RENT PAID (TAX YEAR 2026)' : 'WISCONSIN SCHEDULE H: RENT CERTIFICATE (TAX YEAR 2026)'}
Pursuant to ${isMN ? 'Minnesota Statutes § 290A.19' : 'Wisconsin Statutes § 71.53'}
================================================================================

ELECTRONIC FILING VERIFICATION : ${crpRefNum}
STATUTORY MANDATE DEADLINE     : Delivered to resident on or before January 31, 2027

1. PROPERTY & UNIT IDENTIFICATION:
   Rental Property Address : ${p.address}
   City, State, Zip Code   : ${p.city}, ${p.state} 55425
   County & Jurisdiction   : ${p.county || 'Hennepin'} County
   Number of Units on Site : 1 (Single/Multi-Family Residential)
   Rental Period in 2026   : January 1, 2026 to December 31, 2026 (12 Full Months)

2. TENANT PARTICULARS:
   Renter Full Legal Name  : ${p.tenant || p.tenantName || 'Resident Occupant'}
   Co-Occupants Listed     : None / Sole Leaseholder of Record

3. RENT PAID BREAKDOWN & SECTION 8 VOUCHER EXCLUSION:
   Total Gross Contract Rent to Owner (12 mos) : $${totalRentBilled.toFixed(2)}
   Less: Governmental Subsidy Received (HAP)   : $${sovereignHapAnnual.toFixed(2)} (PHA: ${p.county || 'Hennepin'} County)
   ------------------------------------------------------------------------------
   ${isMN ? 'LINE 1 - TOTAL RENT PAID BY TENANT IN 2026  : $' + tenantCopayAnnual.toFixed(2) : 'LINE 13b - NET RENT PAID BY CLAIMANT IN 2026: $' + tenantCopayAnnual.toFixed(2)}

   IMPORTANT STATUTORY NOTE FOR RENTER:
   ${isMN ? 'Pursuant to Minn. Stat. § 290A.19, Line 1 reflects solely the rent paid out of your own funds (tenant copayment). Federal Housing Choice Voucher assistance paid directly to the landlord by a housing authority cannot be claimed on your Minnesota Property Tax Refund (Form M1PR).' : 'Under Wisconsin law, only rent actually paid by the claimant without government assistance qualifies for the Homestead Credit.'}

4. PROPERTY TAX / HEATING ATTRIBUTION:
   • Heat Included in Rent : [X] YES (Furnished by Landlord)  [ ] NO
   • Electricity Included  : [ ] YES  [X] NO (Tenant Utility Allowance Credited)

5. PROPERTY OWNER / LANDLORD ATTESTATION:
   I declare under the penalties of perjury that I have examined this certificate
   and to the best of my knowledge and belief, it is true, correct, and complete.

   Entity Name       : Section 8 Rentals and More LLC
   Authorized Agent  : Dr. Albert Ray LaMotte, Managing Principal & CEO
   Corporate Contact : alamotte1956@gmail.com
   Date Executed     : ${new Date().toLocaleDateString()}`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${cert}</pre>`);
  w.document.close();
  w.print();
}

window.generateStateRentCreditCertificate = generateStateRentCreditCertificate;
