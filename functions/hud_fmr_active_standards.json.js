// Cloudflare Pages Worker Edge Handler
export async function onRequest(context) {
  const body = {
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
};
  return new Response(JSON.stringify(body, null, 2), {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=0, must-revalidate"
    }
  });
}
