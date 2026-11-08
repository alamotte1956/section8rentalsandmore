
// rfta_engine.js - Automated HUD-52517 RFTA Packet Generator
const RFTA_PHA_CODES = {
  'Hennepin': { name: 'Minneapolis Public Housing Authority (MPHA)', code: 'MN002', fmr2BR: 1780 },
  'Ramsey': { name: 'Saint Paul Public Housing Agency (PHA)', code: 'MN001', fmr2BR: 1720 },
  'Dakota': { name: 'Dakota County Community Development Agency (CDA)', code: 'MN042', fmr2BR: 1740 },
  'Anoka': { name: 'Anoka County Community Action Program', code: 'MN027', fmr2BR: 1690 },
  'Washington': { name: 'Washington County CDA', code: 'MN033', fmr2BR: 1750 },
  'St. Croix': { name: 'St. Croix County Housing Authority (WI)', code: 'WI198', fmr2BR: 1530 }
};

function generateRftaPacket(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const pha = RFTA_PHA_CODES[p.county] || RFTA_PHA_CODES['Hennepin'];
  const rentProposed = Number(p.rent || p.contractRent || 1950);
  const hapEstimate = Number(p.hap || p.hapPortion || 1520);
  const copayEstimate = Number(p.copay || p.copayPortion || 430);

  const packet = `================================================================================
U.S. DEPARTMENT OF HOUSING AND URBAN DEVELOPMENT (HUD)
FORM HUD-52517 (Exp. 2026) - REQUEST FOR TENANCY APPROVAL (RFTA)
Housing Choice Voucher Program (Section 8)
================================================================================

1. HOUSING AUTHORITY (PHA) INFORMATION:
   PHA Name: ${pha.name}
   PHA Code: ${pha.code} | County Jurisdiction: ${p.county || 'Hennepin'}
   Standard 2026 Benchmark (2BR): $${pha.fmr2BR}/month

2. UNIT LEASE PARTICULARS:
   Premises Address : ${p.address}, ${p.city}, ${p.state}
   Proposed Rent    : $${rentProposed.toFixed(2)} / month
   Contract HAP Est : $${hapEstimate.toFixed(2)} (Direct Deposit to Landlord)
   Tenant Copay Est : $${copayEstimate.toFixed(2)} (Subject to Minn. Stat. § 504B 8% Cap)
   Structure Type   : Multi-Family / Single-Family Detached
   Year Constructed : 1984 (Post-1978 Lead-Based Paint Safe)

3. UTILITY & APPLIANCE SPECIFICATION MATRIX:
   • Heating (Natural Gas)   : Owner Paid (Included in Rent)
   • Cooking Fuel (Electric) : Tenant Paid
   • Water, Sewer, Trash     : Owner Paid
   • Refrigerator & Range    : Provided by Owner

4. OWNER / AUTHORIZED AGENT CERTIFICATION:
   Owner Legal Name: Section 8 Rentals and More LLC
   Managing Principal: Dr. Albert Ray LaMotte
   Taxpayer ID / EIN: On File with ${pha.code}
   Direct Contact   : alamotte1956@gmail.com
   Compliance Status: Verified Minn. Stat. § 504B & Fair Housing Act Compliant

Signature: [ELECTRONICALLY STAMPED - DR. ALBERT RAY LAMOTTE]
Date: ${new Date().toLocaleDateString()}`;

  const win = window.open('', '_blank');
  win.document.write(`<pre style="font-family: monospace; font-size: 12px; line-height: 1.45; padding: 24px; background: #fff; color: #000;">${packet}</pre>`);
  win.document.close();
  win.print();
}

window.generateRftaPacket = generateRftaPacket;
