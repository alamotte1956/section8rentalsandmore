// pha_notice_conduit.js - Concurrent PHA Notice Transmission & Certificate of Service
// Governing Rule: 24 CFR § 982.310(e)(2)(ii)
function generatePhaConcurrentNoticePacket(propId) {
  const p = (window.state?.properties || []).find(x => x.id === propId) || (window.state?.properties && window.state.properties[0]) || { id: 'prop-1', address: '7820 Penn Ave S', city: 'Bloomington', state: 'MN', county: 'Hennepin', phaName: 'Minneapolis Public Housing Authority' };
  const today = new Date().toLocaleDateString();
  const doc = `================================================================================
MANDATORY CONCURRENT HOUSING AUTHORITY NOTICE TRANSMITTAL
Pursuant to Code of Federal Regulations: 24 CFR § 982.310(e)(2)(ii)
================================================================================
DATE: ${today}
TO PUBLIC HOUSING AGENCY: ${p.phaName || 'County Public Housing Agency'} (${p.county || 'Hennepin'} County)
FROM: Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte, Managing Principal)
RE: Assisted Tenant: ${p.tenant || 'Resident Occupant'} • Address: ${p.address}, ${p.city}, ${p.state}

Pursuant to 24 CFR § 982.310(e)(2)(ii), the owner certifies concurrent delivery
of all tenancy cure notices and court pleadings to the Public Housing Agency.
Sovereign HAP disbursements remain intact; notice applies solely to tenant copayment.

CERTIFICATE OF SERVICE: Delivered via certified electronic transmittal on ${today}.
Dr. Albert Ray LaMotte, Managing Principal & CEO • Section 8 Rentals and More LLC
`;
  if (window.openFormattedPdfPrintWindow) {
    window.openFormattedPdfPrintWindow('HUD 24 CFR § 982.310(e) PHA NOTICE COPY', p.address, doc, true);
  } else {
    const w = window.open('', '_blank');
    w.document.write('<pre style="font-family: monospace; font-size: 11px; padding: 24px;">' + doc + '</pre>');
    w.document.close();
    w.print();
  }
}
window.generatePhaConcurrentNoticePacket = generatePhaConcurrentNoticePacket;
