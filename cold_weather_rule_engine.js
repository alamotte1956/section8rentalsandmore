
// cold_weather_rule_engine.js - Winter Moratorium & Emergency Heating Compliance Engine
// Governing Authorities: Minn. Stat. § 216B.096 (Cold Weather Rule) & Wis. Admin. Code § PSC 134.062

function generateColdWeatherRuleNotice(propId) {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const today = new Date();
  const currentMonth = today.getMonth() + 1; // 1-12
  const currentDay = today.getDate();

  // MN Window: Oct 1 - Apr 30. WI Window: Nov 1 - Apr 15
  let inMoratorium = false;
  if (isMN) {
    inMoratorium = (currentMonth >= 10 || currentMonth <= 4);
  } else {
    inMoratorium = (currentMonth >= 11 || currentMonth <= 3 || (currentMonth === 4 && currentDay <= 15));
  }

  const tenantName = p.tenant || p.tenantName || 'Resident Occupant';
  const countyName = p.county || 'Hennepin';

  const doc = `================================================================================
STATUTORY COLD WEATHER RULE & EMERGENCY HEATING PROTECTION NOTICE
Pursuant to ${isMN ? 'Minnesota Statutes § 216B.096 (October 1 – April 30 Protection Period)' : 'Wisconsin Admin. Code § PSC 134.062 (November 1 – April 15 Moratorium)'}
HUD NSPIRE HEATING HABITABILITY MANDATE (24 CFR § 982.401)
================================================================================

1. PREMISES & SEASONAL STATUS:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Jurisdiction      : ${countyName} County (${p.state || 'MN'})
   Resident Tenant   : ${tenantName}
   Date of Notice    : ${today.toLocaleDateString()}
   Cold Weather Rule : ${inMoratorium ? 'ACTIVE (STATUTORY MORATORIUM IN EFFECT)' : 'INACTIVE (STANDARD UTILITY SCHEDULE)'}
   Managing Entity   : Section 8 Rentals and More LLC (Dr. Albert Ray LaMotte)

2. STATUTORY HEATING & HABITABILITY STANDARDS:
   • Minimum Temperature Requirement: Pursuant to HUD NSPIRE standards and municipal
     housing codes (Minneapolis Code § 244.430 / Saint Paul Code § 34.11), heating
     equipment must reliably maintain a minimum temperature of 68°F in all habitable rooms.
   • 24-Hour Emergency Status: Complete heating loss during sub-freezing conditions constitutes
     a Priority 1 Life-Threatening Deficiency (LTF) requiring remediation within 24 hours.

3. TENANT UTILITY DISCONNECTION PROTECTIONS (COLD WEATHER RULE):
   ${isMN ? 'Under Minn. Stat. § 216B.096, an electric or natural gas utility cannot disconnect residential service between October 1 and April 30 if: (1) disconnection affects the primary heat source; (2) household income is at or below 50% of state median income; and (3) resident establishes and honors a utility payment agreement.' : 'Under Wis. Admin. Code § PSC 134.062, utilities cannot disconnect residential gas or electric service used for space heating between November 1 and April 15.'}

4. EMERGENCY ENERGY ASSISTANCE PROGRAM (EAP) DIRECTORY:
   If you receive a utility disconnection warning or struggle with heating utility costs,
   contact the following authorized regional community action agencies immediately:
   • Hennepin County Community Action Partnership (CAP-HC)  : (952) 933-9639
   • Community Action Partnership of Ramsey & Washington    : (651) 645-6445
   • Community Action Partnership of Suburban Hennepin (CAPSH): (952) 933-1993
   • Dakota County Energy Assistance (EAP)                  : (651) 554-5751
   • St. Croix County Economic Support (Wisconsin HEAP)     : (715) 381-4360

5. LANDLORD COVENANTS & COLD WEATHER PROTOCOLS:
   • Landlord will never disconnect heating utilities under any circumstances.
   • Space heaters are prohibited as a permanent heating substitute.
   • Report furnace malfunctions immediately to the emergency dispatch line.

Certified By: Dr. Albert Ray LaMotte, Managing Principal & CEO
Section 8 Rentals and More LLC • Emergency Contact: alamotte1956@gmail.com
Audit Timestamp: [HUD-CWR-PROTECT-STAMP-${Date.now().toString().slice(-8)}]`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${doc}</pre>`);
  w.document.close();
  w.print();
}

window.generateColdWeatherRuleNotice = generateColdWeatherRuleNotice;
