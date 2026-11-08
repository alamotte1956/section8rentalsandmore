
// screening_compliance_engine.js - Minn. Stat. § 504B.173 & Inclusive Screening Engine
// Handles Pre-Application Disclosures, Fee Receipts, and Statutory Adverse Action Notices

function generateScreeningCriteriaDisclosure(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const rent = Number(p.rent || p.contractRent || 1950);
  const copayEst = Number(p.copay || p.copayPortion || 430);

  const doc = `================================================================================
STATUTORY TENANT SCREENING CRITERIA & FEE DISCLOSURE
Pursuant to ${isMN ? 'Minn. Stat. § 504B.173 & Mpls. Code § 244.2030' : 'Wis. Stat. § 704 & Wis. Admin. Code ATCP § 134.05'}
Section 8 Housing Choice Voucher Inclusive Tenancy Policy
================================================================================

1. SUBJECT UNIT & JURISDICTION:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Managing Entity   : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)
   Total Rent        : $${rent.toFixed(2)}/mo
   Tenant Copay Est  : $${copayEst.toFixed(2)}/mo (Basis for Income Ratio Evaluation)
   Target Jurisdiction: ${p.county || 'Hennepin'} County

2. APPLICANT SCREENING FEE STATEMENT:
   Application Fee   : $45.00 per adult occupant (Exact Out-of-Pocket Screening Cost)
   Consumer Reporting: Professional Tenant Screening Services / NCIC / BCA Records
   Refund Guarantee  : If an applicant is rejected on criteria not disclosed herein,
                       or if the unit is leased to a prior applicant before screening
                       is conducted, the entire fee is refunded within 14 days.

3. TENANT SELECTION CRITERIA (INCLUSIVE EVALUATION):
   A. VOUCHER & SOURCE OF INCOME NON-DISCRIMINATION:
      • Section 8 Housing Choice Vouchers are welcomed and encouraged.
      • Income requirements evaluate only the TENANT'S COPAY SHARE (e.g. 2.5x of $${copayEst.toFixed(2)} = $${(copayEst * 2.5).toFixed(2)}),
        NEVER the full gross contract rent subsidized by the Housing Authority.

   B. CREDIT HISTORY THRESHOLD:
      • Medical debt and student loan balances are excluded from evaluation.
      • A lack of established credit history is NOT grounds for automatic rejection.

   C. CRIMINAL HISTORY STANDARDS (TWIN CITIES ORDINANCE COMPLIANCE):
      • Felony convictions older than seven (7) years are not disqualifying (excluding
        lifetime sex offender registration or manufacturing methamphetamine on premises).
      • Misdemeanors older than three (3) years are not disqualifying.
      • Arrest records without conviction are never considered.

   D. RENTAL HISTORY & PRIOR EVICTIONS:
      • Eviction actions older than three (3) years or dismissed/settled filings
        shall not be grounds for disqualification.

4. ADVERSE ACTION / REJECTION NOTIFICATION:
   If an application is rejected, Section 8 Rentals and More LLC will provide written notice
   within fourteen (14) days via electronic mail or certified mail specifying the exact
   criteria not met, the reporting agency used, and the applicant's right to dispute.

CERTIFICATION OF PRE-APPLICATION DELIVERY:
I certify that this disclosure was presented to the prospective applicant prior to
the collection of any applicant screening fee.

Authorized Housing Officer: Dr. Albert Ray LaMotte, Managing Principal
Section 8 Rentals and More LLC • Contact: alamotte1956@gmail.com
Execution Date: ${new Date().toLocaleDateString()}`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${doc}</pre>`);
  w.document.close();
  w.print();
}

function generateAdverseActionNotice(propId, applicantName = 'Applicant') {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const today = new Date();
  const notice = `================================================================================
STATUTORY ADVERSE ACTION NOTICE & REJECTION DISCLOSURE
Pursuant to Minn. Stat. § 504B.173, Subd. 3 & Fair Credit Reporting Act (15 U.S.C. § 1681m)
================================================================================

DATE OF NOTICE: ${today.toLocaleDateString()}
APPLICANT     : ${applicantName}
PREMISES      : ${p.address}, ${p.city}, ${p.state}
HOUSING ENTITY: Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)

PLEASE BE ADVISED that your application for tenancy has been evaluated and declined
based on the following specific criteria disclosed prior to application:

SPECIFIC BASIS FOR REJECTION:
[X] Unverifiable rental references or unsatisfied landlord money judgment within 36 months.
[ ] Inability to verify tenant copay income requirement.
[ ] Incomplete documentation required for PHA voucher packet submission.

CONSUMER REPORTING AGENCY USED:
  TransUnion / Equifax / Experian Rental Bureau
  Address: P.O. Box 2000, Chester, PA 19016 • Phone: (800) 888-4213
  Note: The reporting agency did not make the decision to take adverse action and
  cannot explain why the decision was made.

STATUTORY RIGHTS UNDER FEDERAL AND MINNESOTA LAW:
1. You have the right under FCRA to obtain a free copy of your consumer file within 60 days.
2. You have the right to dispute the accuracy or completeness of any information reported.
3. You may submit a written response explaining mitigating circumstances within 14 days.

Managing Officer : Dr. Albert Ray LaMotte, Principal & CEO
Entity           : Section 8 Rentals and More LLC • alamotte1956@gmail.com`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${notice}</pre>`);
  w.document.close();
  w.print();
}

window.generateScreeningCriteriaDisclosure = generateScreeningCriteriaDisclosure;
window.generateAdverseActionNotice = generateAdverseActionNotice;
