
// portability_engine.js - Form HUD-52665 HCV Voucher Portability & Transfer Engine
// Authority: 24 CFR § 982.353 & 24 CFR § 982.355 (Inter-Agency Portability)

function generatePortabilityPacket(propId, destinationCounty = 'Ramsey') {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const currentCounty = p.county || 'Hennepin';
  const initialPha = currentCounty === 'Ramsey' ? 'Saint Paul PHA (MN001)' :
                     currentCounty === 'Dakota' ? 'Dakota County CDA (MN042)' :
                     currentCounty === 'St. Croix' ? 'St. Croix County HA (WI198)' :
                     'Minneapolis Public Housing Authority (MN002)';

  const receivingPha = destinationCounty === 'Ramsey' ? 'Saint Paul PHA (MN001)' :
                       destinationCounty === 'Dakota' ? 'Dakota County CDA (MN042)' :
                       destinationCounty === 'St. Croix' ? 'St. Croix County HA (WI198)' :
                       'Minneapolis Public Housing Authority (MN002)';

  const contractRent = Number(p.rent || p.contractRent || 1950);
  const hapPortion = Number(p.hap || p.hapPortion || 1520);
  const copayPortion = Number(p.copay || p.copayPortion || 430);
  const voucherSize = p.bedrooms || 2;

  const doc = `================================================================================
U.S. DEPARTMENT OF HOUSING AND URBAN DEVELOPMENT (HUD)
FORM HUD-52665 • FAMILY PORTABILITY INFORMATION
Housing Choice Voucher Program • 24 CFR § 982.355
================================================================================

PART I: INITIAL PUBLIC HOUSING AGENCY (PHA) INFORMATION & CERTIFICATION
1. INITIAL HOUSING AGENCY : ${initialPha}
2. RECEIVING HOUSING AGENCY: ${receivingPha}
3. TENANT RESIDENT HEAD    : ${p.tenant || p.tenantName || 'Resident Occupant'}
4. VOUCHER BEDROOM SIZE    : ${voucherSize}-Bedroom Voucher
5. CURRENT PREMISES ADDR   : ${p.address}, ${p.city}, ${p.state}
6. MANAGING OWNER / AGENT  : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)

FINANCIAL & SUBSIDY PARTICULARS:
• Current Contract Rent to Owner    : $${contractRent.toFixed(2)} / month
• Sovereign HAP Subsidy (Disbursed) : $${hapPortion.toFixed(2)} / month
• Tenant Adjusted Family Share      : $${copayPortion.toFixed(2)} / month
• Utility Allowance Credited        : Included per HUD-52667 Schedule
• Lease Fulfillment Status          : Term Satisfied / Mutual Rescission Executed

PART II: INTER-AGENCY BILLING & ABSORPTION NOTIFICATION:
Pursuant to 24 CFR § 982.355:
[ ] Receiving PHA Elects to ABSORB the Family into Local Voucher Allocation.
[X] Receiving PHA Elects to BILL Initial PHA:
    • Monthly HAP Billed to Initial PHA: $${hapPortion.toFixed(2)}
    • Administrative Fee (80% of Column B Rate): Billed per HUD PIH Guidelines
    • Billing Due Date: No later than the 1st of each calendar month.

LANDLORD LEASE RELEASE & CLEARANCE:
Section 8 Rentals and More LLC certifies that:
1. No pending statutory nonpayment or uncured lease default exists on the subject unit.
2. Tenant security deposit disposition will be executed strictly within 21 days pursuant
   to Minn. Stat. § 504B.178 / Wis. Stat. § 704.28.
3. HAP payment release requested to transfer upon mutual vacate date.

AUTHORIZED CERTIFYING OFFICIAL:
Dr. Albert Ray LaMotte, Managing Principal & CEO
Section 8 Rentals and More LLC • alamotte1956@gmail.com
Execution Date: ${new Date().toLocaleDateString()}
Portability Verification Code: [HUD-PORT-52665-SYNC-${Date.now().toString().slice(-8)}]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${doc}</pre>`);
  w.document.close();
  w.print();
}

window.generatePortabilityPacket = generatePortabilityPacket;
