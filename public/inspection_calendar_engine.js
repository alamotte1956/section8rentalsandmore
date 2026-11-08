// inspection_calendar_engine.js - Statutory Moratoriums & HUD NSPIRE Deadlines
(function() {
  'use strict';

  window.INSPECTION_CALENDAR = {
    // Evaluates live date against Minnesota & Wisconsin Cold Weather heating protections
    checkColdWeatherMoratorium(currentDate = new Date()) {
      const month = currentDate.getMonth() + 1; // 1-12
      // MN: October 1 to April 30 (Months 10, 11, 12, 1, 2, 3, 4)
      const mnActive = (month >= 10 || month <= 4);
      // WI: November 1 to April 15 (Months 11, 12, 1, 2, 3, or early 4)
      const wiActive = (month >= 11 || month <= 3 || (month === 4 && currentDate.getDate() <= 15));

      return {
        minnesota: {
          active: mnActive,
          standard: "68°F Habitable Indoor Temperature (Minn. Stat. § 216B.096)",
          moratoriumWindow: "October 1 – April 30",
          restriction: "Utility disconnect and heat reduction barred without protective disclosures."
        },
        wisconsin: {
          active: wiActive,
          standard: "PSC 134 Winter Moratorium Protection",
          moratoriumWindow: "November 1 – April 15",
          restriction: "Residential disconnection prohibited for essential heating service."
        }
      };
    },

    // NSPIRE 3.0 Priority Defect Time Calculator
    calculateNspireDeadlines(defectType, reportDate = new Date()) {
      const reportMs = reportDate.getTime();
      if (defectType === "P1_LIFE_THREATENING") {
        return {
          category: "Priority 1 - Life-Threatening Defect (HUD NSPIRE)",
          cureWindowHours: 24,
          deadline: new Date(reportMs + 24 * 60 * 60 * 1000).toISOString(),
          examples: "Gas leak, ungrounded panel, inoperable heating in winter, structural collapse."
        };
      }
      return {
        category: "Priority 2 - Non-Life-Threatening Defect",
        cureWindowHours: 720, // 30 Days
        deadline: new Date(reportMs + 30 * 24 * 60 * 60 * 1000).toISOString(),
        examples: "Dripping faucet, cracked window pane, interior door latch alignment."
      };
    }
  };
})();
