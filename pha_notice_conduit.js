// pha_notice_conduit.js - HUD 24 CFR § 982.310(e)(2)(ii) Concurrent Notice Conduit
(function() {
  'use strict';

  window.PHA_NOTICE_CONDUIT = {
    phaRegistry: {
      "MN002": { name: "Minneapolis Public Housing Authority (MPHA)", email: "caseworkers@mphaonline.org", address: "1001 Washington Ave N, Minneapolis, MN 55401" },
      "MN001": { name: "St. Paul Public Housing Agency", email: "section8@stpha.org", address: "555 Wabasha St N, St. Paul, MN 55102" },
      "MN042": { name: "Dakota County CDA", email: "cdahousing@dakotacda.state.mn.us", address: "1228 Town Centre Dr, Eagan, MN 55123" },
      "MN027": { name: "Anoka County Community Action Program (ACCAP)", email: "housing@accap.org", address: "1201 89th Ave NE, Blaine, MN 55434" },
      "MN033": { name: "Washington County CDA", email: "rentassistance@wchco.com", address: "7645 Currell Blvd, Woodbury, MN 55125" },
      "WI198": { name: "Hudson Housing Authority", email: "hudsonha@pressenter.com", address: "1301 Coulee Rd, Hudson, WI 54016" }
    },

    buildConcurrentNoticeDocket(propId, noticeType, remedyAmount) {
      const prop = (window.state?.properties || []).find(p => p.id === propId) || (window.state?.properties && window.state.properties[0]);
      if (!prop) throw new Error("Property record not located.");

      const phaCode = prop.pha ? prop.pha.split('(')[1]?.replace(')', '') : "MN002";
      const pha = this.phaRegistry[phaCode] || this.phaRegistry["MN002"];

      return {
        statutoryDirective: "HUD 24 CFR § 982.310(e)(2)(ii) Mandatory Concurrent Notice",
        caseDocketNumber: `PHA-SEC8-2026-${Date.now().toString(36).toUpperCase()}`,
        noticeType: noticeType || "14-Day Notice to Cure or Vacate (Minn. Stat. § 504B.321)",
        designatedPHA: pha,
        propertyAddress: `${prop.address}, ${prop.city}, ${prop.state} ${prop.zip}`,
        residentName: prop.tenant,
        tenantCopayArrears: Number(remedyAmount || prop.copay).toFixed(2),
        sovereignHAPSubsidiesSeparated: true,
        certificationOfService: {
          servedBy: "Dr. Albert Ray LaMotte (Managing Principal, Lic. No. 1893)",
          serviceDate: new Date().toISOString(),
          transmissionMethod: "Certified Electronic Encrypted Portal + USPS First Class Mail"
        }
      };
    }
  };
})();
