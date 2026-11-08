
// legal_notices_engine.js - Statutory Eviction Notice Engine (MN § 504B / WI § 704 / CARES Act)

function generateStatutoryNotice(propId, noticeType = 'auto') {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const rentTotal = Number(p.rent || p.contractRent || 1950);
  const hapPortion = Number(p.hap || p.hapPortion || 1520);
  const copayPortion = Number(p.copay || p.copayPortion || 430);
  const lateFeeCap = (copayPortion * 0.08).toFixed(2);
  const totalCureAmount = (copayPortion + Number(lateFeeCap)).toFixed(2);
  const today = new Date();

  // Determine notice period based on jurisdiction and CARES Act status
  let noticeDays = 14;
  let statuteTitle = 'MINNESOTA STATUTES § 504B.321 - 14-DAY WRITTEN NOTICE TO VACATE';
  let legalAidContact = 'HOME Line at (612) 728-5767 or Mid-Minnesota Legal Aid at (612) 334-5970';

  if (!isMN) {
    noticeDays = 5;
    statuteTitle = 'WISCONSIN STATUTES § 704.17(2) - 5-DAY NOTICE TO PAY RENT OR VACATE';
    legalAidContact = 'Legal Action of Wisconsin at (855) 947-2529';
  }

  // Federal CARES Act requirement for Section 8 Voucher Covered Properties
  let caresNoticeClause = `
FEDERAL CARES ACT STATUTORY NOTICE (15 U.S.C. § 9058):
Because this property participates in the HUD Section 8 Housing Choice Voucher program,
federal law mandates a minimum 30-day notice period prior to filing an eviction action
in court for nonpayment. The effective cure or vacate date reflects this federal threshold.`;
  noticeDays = Math.max(noticeDays, 30);

  const effectiveDate = new Date();
  effectiveDate.setDate(today.getDate() + noticeDays);

  const noticeText = `================================================================================
${statuteTitle}
AND 30-DAY NOTICE PURSUANT TO FEDERAL CARES ACT (15 U.S.C. § 9058)
================================================================================

DATE OF SERVICE: ${today.toLocaleDateString()}
EFFECTIVE EXPIRATION / CURE DATE: ${effectiveDate.toLocaleDateString()} (${noticeDays} Full Calendar Days)

TO TENANT(S) IN POSSESSION:
  Resident Name : ${p.tenant || p.tenantName || 'Resident Occupant'}
  Premises      : ${p.address}, ${p.city}, ${p.state}
  PHA Reference : ${p.county || 'Hennepin'} County Public Housing Authority

PLEASE TAKE NOTICE that you are indebted to the landlord for past-due rent copayment:

ITEMIZATION OF PAST-DUE TENANT RENT:
  1. Base Contract Rent to Owner                : $${rentTotal.toFixed(2)}
  2. Public Housing Agency Subsidy (HAP)        : $${hapPortion.toFixed(2)} (EXEMPT SOVEREIGN SHARE)
  ------------------------------------------------------------------------------
  3. Delinquent Tenant Direct Copayment Share    : $${copayPortion.toFixed(2)}
  4. Permissible Statutory Late Fee (8% Copay)  : $${lateFeeCap} (Minn. Stat. § 504B.177)
  ------------------------------------------------------------------------------
  TOTAL AMOUNT REQUIRED TO FULLY CURE DEFAULT   : $${totalCureAmount}

DEMAND FOR PAYMENT OR SURRENDER OF PREMISES:
You are hereby notified to either:
  (A) Pay the total past-due tenant copayment of $${totalCureAmount} in full on or before ${effectiveDate.toLocaleDateString()}, OR
  (B) Vacate and surrender full possession of the premises to the landlord.

FAILURE TO COMPLY:
If you do not pay the delinquent copayment or vacate the premises by the expiration date,
the landlord will initiate formal eviction proceedings in the District Court of ${p.county || 'Hennepin'} County.
${caresNoticeClause}

STATUTORY NOTICE OF LEGAL ASSISTANCE:
You have the right to seek legal advice and assistance. You may contact:
${legalAidContact}.

LANDLORD / AUTHORIZED AGENT ATTESTATION:
  Entity Name       : Section 8 Rentals and More LLC
  Authorized Agent  : Dr. Albert Ray LaMotte, Principal
  Contact Inquiries : alamotte1956@gmail.com
  Proof of Delivery : Delivered via Certified U.S. Mail and Electronic Delivery Stamped`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${noticeText}</pre>`);
  w.document.close();
  w.print();
}

window.generateStatutoryNotice = generateStatutoryNotice;
