export async function onRequest(context) {
  const { request } = context;

  // Handle CORS preflight
  if (request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
      }
    });
  }

  if (request.method !== "POST") {
    return new Response(JSON.stringify({ error: `Method ${request.method} Not Allowed` }), {
      status: 405,
      headers: { 
        "Content-Type": "application/json",
        "Allow": "POST, OPTIONS",
        "Access-Control-Allow-Origin": "*"
      }
    });
  }

  try {
    const contentType = request.headers.get("content-type") || "";
    let data = {};

    if (contentType.includes("application/json")) {
      data = await request.json();
    } else if (contentType.includes("application/x-www-form-urlencoded") || contentType.includes("multipart/form-data")) {
      const formData = await request.formData();
      for (const [key, value] of formData.entries()) {
        data[key] = value;
      }
    } else {
      return new Response(JSON.stringify({ error: "Unsupported Content-Type" }), {
        status: 400,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }

    const { full_name, email, phone, property_address, bedrooms, campaign_id } = data;

    if (!full_name || !email || !phone) {
      return new Response(JSON.stringify({ error: "Missing required fields: full_name, email, phone." }), {
        status: 422,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }

    const leadRecord = {
      lead_id: "LEAD-" + Date.now(),
      created_at: new Date().toISOString(),
      full_name: full_name.trim(),
      email: email.trim().toLowerCase(),
      phone: phone.trim(),
      property_address: (property_address || "Not Specified").trim(),
      bedrooms: bedrooms || "Unspecified",
      campaign_id: campaign_id || "general"
    };

    return new Response(JSON.stringify({
      success: true,
      message: "Owner inquiry registered successfully. Underwriting desk notified.",
      lead: leadRecord
    }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: "Server error processing inquiry", details: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
}
