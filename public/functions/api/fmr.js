export async function onRequest(context) {
  return new Response(JSON.stringify({
  "source": "HUD User Programmatic Dataset (MSP Metro FMR Area)",
  "verified_metro_area": "Minneapolis-St. Paul-Bloomington, MN-WI HUD Metro FMR Area",
  "standards": {
    "Dakota County, MN": {
      "efficiency": 1242,
      "one_bed": 1405,
      "two_bed": 1709,
      "three_bed": 2262,
      "four_bed": 2531
    },
    "Hennepin County, MN": {
      "efficiency": 1242,
      "one_bed": 1405,
      "two_bed": 1709,
      "three_bed": 2262,
      "four_bed": 2531
    },
    "Ramsey County, MN": {
      "efficiency": 1242,
      "one_bed": 1405,
      "two_bed": 1709,
      "three_bed": 2262,
      "four_bed": 2531
    },
    "St. Croix County, WI": {
      "efficiency": 1242,
      "one_bed": 1405,
      "two_bed": 1709,
      "three_bed": 2262,
      "four_bed": 2531
    }
  }
}, null, 2), {
    headers: {
      "content-type": "application/json;charset=UTF-8",
      "access-control-allow-origin": "*",
      "cache-control": "no-cache"
    }
  });
}
