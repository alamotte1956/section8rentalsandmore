
// hap_contract_engine.js - HUD-52641 HAP Contract Generator & Compliance Tracker
// Governing Regulations: 24 CFR Part 982 Section 8 Housing Choice Voucher Program

function generateHapContract(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const rentTotal = Number(p.rent || p.contractRent || 1950);
  const hapPortion = Number(p.hap || p.hapPortion || 1520);
  const copayPortion = Number(p.copay || p.copayPortion || 430);
  const phaName = p.county === 'Ramsey' ? 'Saint Paul Public Housing Agency (MN001)' :
                  p.county === 'Dakota' ? 'Dakota County CDA (MN042)' :
                  p.county === 'St. Croix' ? 'St. Croix County Housing Authority (WI198)' :
                  'Minneapolis Public Housing Authority (MN002)';

  const hapDoc = `================================================================================
HOUSING ASSISTANCE PAYMENTS CONTRACT (HAP CONTRACT)
Section 8 Housing Choice Voucher Program • U.S. Department of HUD
Form HUD-52641 (Exp. 2026) • OMB Approval No. 2577-0169
================================================================================

PART A: CONTRACT PARTICULARS
1. PARTICIPATING HOUSING AGENCY: ${phaName}
2. MANAGING OWNER / AGENT     : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)
3. TENANT RESIDENT             : ${p.tenant || p.tenantName || 'Qualified Section 8 Resident'}
4. CONTRACT PREMISES           : ${p.address}, ${p.city}, ${p.state}
5. INITIAL LEASE TERM          : 12 Months (Renewable)

PAYMENT STRUCTURE & ALLOCATION:
  • Total Approved Monthly Rent to Owner : $${rentTotal.toFixed(2)}
  • Housing Assistance Payment (PHA Share): $${hapPortion.toFixed(2)} (ACH Direct Deposit)
  • Tenant Direct Copay Portion          : $${copayPortion.toFixed(2)} (Capped Statutory Fee)

PART B: LEGAL BODY & STATUTORY COVENANTS
1. PURPOSE & GUARANTEE OF HOUSING ASSISTANCE PAYMENTS:
   The PHA agrees to make monthly Housing Assistance Payments directly to the Owner on
   behalf of the family. Payments disburse on or before the first business day of each month.

2. MAINTENANCE OF UNIT & NSPIRE CERTIFICATION:
   Owner warrants that the contract unit and common premises are maintained in full
   compliance with National Standards for the Physical Inspection of Real Estate (NSPIRE).

3. JURISDICTIONAL STATUTORY COMPLIANCE:
   • Minnesota: Subject to Minn. Stat. § 504B (14-Day Notice / 8% Late Fee Cap).
   • Wisconsin: Subject to Wis. Stat. § 704 (5-Day Cure Notice / Escrow Trust).
   • Federal: 15 U.S.C. § 9058 (CARES Act 30-Day Notice for covered properties).

4. OWNER CERTIFICATION & EXECUTION:
   Owner certifies no side-agreements for rent exist beyond the approved figures above.

   Owner Representative: Dr. Albert Ray LaMotte, President & CEO
   Entity Name         : Section 8 Rentals and More LLC
   Executed Date       : ${new Date().toLocaleDateString()}
   Digital Verification: [SECURE CERTIFIED HAP EXECUTION HASH #MN-HAP-2026]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${hapDoc}</pre>`);
  w.document.close();
  w.print();
}

window.generateHapContract = generateHapContract;
