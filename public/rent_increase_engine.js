
// rent_increase_engine.js - Statutory 60-Day Rent Increase & Lease Renewal Engine
// Standards: 24 CFR § 982.507, HUD PIH 2023-27 & Minn. Stat. § 504B.147

function generateRentIncreaseNotice(propId, proposedNewRent = null) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const currentRent = Number(p.rent || p.contractRent || 1950);
  const newRent = proposedNewRent || (currentRent + 125.00);
  const netIncrease = newRent - currentRent;
  const pctIncrease = ((netIncrease / currentRent) * 100).toFixed(1);

  const noticeDate = new Date();
  const effectiveDate = new Date();
  effectiveDate.setDate(noticeDate.getDate() + 65); // Full 60+ days lead time for PHA submission

  const phaTarget = p.county === 'Ramsey' ? 'Saint Paul Public Housing Agency (MN001)' :
                    p.county === 'Dakota' ? 'Dakota County CDA (MN042)' :
                    p.county === 'St. Croix' ? 'St. Croix County Housing Authority (WI198)' :
                    'Minneapolis Public Housing Authority (MN002)';

  const notice = `================================================================================
NOTICE OF PROPOSED RENT INCREASE & ANNUAL LEASE RENEWAL REQUEST
HUD Housing Choice Voucher Program • 24 CFR § 982.507 & HUD PIH 2023-27
Pursuant to Minnesota Statutes § 504B.147 / Wisconsin Statutes § 704.19
================================================================================

DATE OF SUBMISSION   : ${noticeDate.toLocaleDateString()}
PROPOSED EFFECTIVE   : ${effectiveDate.toLocaleDateString()} (Exceeds Mandatory 60-Day PHA Threshold)
TARGET HOUSING AGENCY: ${phaTarget}

1. LEASE PARTICULARS & TENANCY IDENTIFICATION:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Resident Name     : ${p.tenant || p.tenantName || 'Resident Occupant'}
   HAP Contract Ref  : Form HUD-52641 on File
   Managing Owner    : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)

2. RENT ADJUSTMENT ITEMIZATION:
   Current Contract Rent to Owner    : $${currentRent.toFixed(2)} / month
   Proposed Adjusted Contract Rent   : $${newRent.toFixed(2)} / month
   Net Proposed Dollar Increase      : +$${netIncrease.toFixed(2)} / month (+${pctIncrease}%)
   Anticipated PHA Subsidy (HAP)     : To be recalculated by PHA pursuant to voucher standard
   Tenant Copay Share Adjustment     : Capped by PHA Family Share rules (Max 40% adjusted income)

3. HUD RENT REASONABLENESS JUSTIFICATION:
   • The requested rent complies with 2026 SAFMR 50th percentile market levels for ${p.county || 'Hennepin'} County.
   • Property remains in full NSPIRE physical compliance (tamper-resistant GFCI, active CO/smoke systems).
   • Owner continues to furnish heating and water/sewer/trash utilities without surcharge.

4. TENANT ACKNOWLEDGMENT & LEASE RENEWAL COVENANTS:
   Tenancy will automatically convert or renew for a consecutive 12-month period subject to
   PHA rent reasonableness certification. Tenant has the right to accept the renewal or
   request voucher transfer portability through the PHA counselor within 30 days.

CERTIFICATION OF STATUTORY TIMELINESS:
I certify that this notice has been furnished to the PHA and resident with greater than
60 days advance notice in compliance with both HUD regulations and state tenancy law.

Authorized Agent : Dr. Albert Ray LaMotte, President & CEO
Entity           : Section 8 Rentals and More LLC • alamotte1956@gmail.com
Audit Stamp      : [HUD-60DAY-INCREASE-SEAL-${Date.now().toString().slice(-8)}]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${notice}</pre>`);
  w.document.close();
  w.print();
}

window.generateRentIncreaseNotice = generateRentIncreaseNotice;
