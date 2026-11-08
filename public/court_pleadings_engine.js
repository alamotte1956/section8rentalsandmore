
// court_pleadings_engine.js - Statutory Eviction Court Complaint & Pleading Generator
// Authorities: Minn. Stat. § 504B.321, Wis. Stat. § 799.40 & 15 U.S.C. § 9058 (CARES Act)

function generateCourtEvictionPleadings(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const county = p.county || (isMN ? 'Hennepin' : 'St. Croix');
  const tenantName = p.tenant || p.tenantName || 'Resident Occupant';
  const delinquentCopay = Number(p.copay || p.copayPortion || 470.00);
  const lateFeeCapped = Math.min(delinquentCopay * 0.08, delinquentCopay * 0.08); // 8% cap Minn. Stat. § 504B.177
  const totalArrears = delinquentCopay + lateFeeCapped;
  const today = new Date().toLocaleDateString();

  let pleadingDoc = '';

  if (isMN) {
    pleadingDoc = `================================================================================
STATE OF MINNESOTA                                DISTRICT COURT
COUNTY OF ${county.toUpperCase()}                   FOURTH JUDICIAL DISTRICT (HOUSING COURT)
================================================================================
Section 8 Rentals and More LLC,
                       Plaintiff (Landlord),
vs.                                              EVICTION ACTION COMPLAINT
                                                 Pursuant to Minn. Stat. § 504B.321
${tenantName}, and all other occupants,         Court File No.: _____________________
                       Defendant(s) (Tenant).
================================================================================

COMPLAINT IN EVICTION (NON-PAYMENT OF TENANT COPAYMENT)

Plaintiff, for its Complaint against Defendant(s), states and alleges as follows:

1. PARTIES & PREMISES:
   Plaintiff is the authorized managing corporate entity of the residential real
   property situated at: ${p.address}, ${p.city}, MN (County of ${county}).
   Defendant(s) currently hold possession of the property as residential tenants.

2. SUBSIDIZED TENANCY & HAP CONTRACT:
   The tenancy is subject to a Housing Choice Voucher program direct subsidy via
   the ${county} County Public Housing Agency under Form HUD-52641.
   Plaintiff acknowledges that sovereign Housing Assistance Payments (HAP) are
   strictly segregated and that this action pertains exclusively to the unpaid
   contractual TENANT COPAYMENT PORTION under the residential lease.

3. DEFAULT & ITEMIZATION OF ARREARS:
   Defendant has failed and refused to pay the lawful tenant copayment:
   • Unpaid Tenant Monthly Copayment Share : $${delinquentCopay.toFixed(2)}
   • Lawful Late Fee (Capped at 8% max)    : $${lateFeeCapped.toFixed(2)} (Minn. Stat. § 504B.177)
   ------------------------------------------------------------------------------
   TOTAL ARREARS EXCLUSIVE OF COURT COSTS  : $${totalArrears.toFixed(2)}

4. STATUTORY NOTICE & CARES ACT COMPLIANCE:
   Pursuant to Minn. Stat. § 504B.321 and 15 U.S.C. § 9058 (CARES Act), Plaintiff
   personally served or transmitted by certified mail a written 30-Day Notice of
   Intent to File Eviction. More than 30 full days have elapsed, and Defendant has
   failed to cure the delinquency or surrender possession of the premises.

5. SERVICEMEMBERS CIVIL RELIEF ACT (SCRA) AFFIDAVIT (50 U.S.C. § 3931):
   Plaintiff certifies under penalty of perjury that Defendant is not currently
   on active military duty in the Armed Forces of the United States.

WHEREFORE, Plaintiff demands judgment against Defendant(s) for:
   1. Immediate restitution of the premises;
   2. Costs and disbursements allowed by statute;
   3. A Writ of Recovery of Premises pursuant to Minn. Stat. § 504B.365.

Dated: ${today}
Respectfully submitted,
SECTION 8 RENTALS AND MORE LLC

By: __________________________________________________
    Dr. Albert Ray LaMotte, Managing Principal & CEO
    Section 8 Rentals and More LLC • alamotte1956@gmail.com
    Authorized Agent for Plaintiff`;
  } else {
    pleadingDoc = `================================================================================
STATE OF WISCONSIN                                CIRCUIT COURT
COUNTY OF ${county.toUpperCase()}                   SMALL CLAIMS DIVISION
================================================================================
Section 8 Rentals and More LLC,
                       Plaintiff,
vs.                                              SUMMONS & COMPLAINT (EVICTION)
                                                 Wis. Stat. § 799.40 & § 704.17
${tenantName},                                   Case No.: _____________________
                       Defendant.
================================================================================

1. The Plaintiff is Section 8 Rentals and More LLC, managing property at:
   ${p.address}, ${p.city}, WI.
2. The Defendant breached the residential lease by failing to pay tenant rent of:
   $${delinquentCopay.toFixed(2)}.
3. Plaintiff served statutory 5-day / 30-day CARES Act notice on Defendant.
4. Plaintiff demands judgment for immediate possession and court filing disbursements.

Dated: ${today}
By: Dr. Albert Ray LaMotte, President & CEO`;
  }

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${pleadingDoc}</pre>`);
  w.document.close();
  w.print();
}

window.generateCourtEvictionPleadings = generateCourtEvictionPleadings;
