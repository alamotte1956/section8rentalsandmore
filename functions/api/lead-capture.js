export async function onRequestPost(context) {
  try {
    const contentType = context.request.headers.get("content-type") || "";
    let data = {};

    if (contentType.includes("application/json")) {
      data = await context.request.json();
    } else if (contentType.includes("application/x-www-form-urlencoded") || contentType.includes("multipart/form-data")) {
      const formData = await context.request.formData();
      for (const [key, value] of formData.entries()) {
        data[key] = value;
      }
    } else {
      return new Response(JSON.stringify({ error: "Unsupported Content-Type" }), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const { full_name, email, phone, property_address, bedrooms, campaign_id } = data;

    if (!full_name || !email || !phone) {
      return new Response(JSON.stringify({ error: "Missing required fields: full_name, email, and phone are mandatory." }), {
        status: 422,
        headers: { "Content-Type": "application/json" }
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
      campaign_id: campaign_id || "general",
      source_host: context.request.headers.get("host") || "section8rentalsandmore.pages.dev",
      ip: context.request.headers.get("cf-connecting-ip") || "0.0.0.0"
    };

    // Return successful capture response (ready for KV/D1 binding or Resend/SendGrid worker trigger)
    return new Response(JSON.stringify({
      success: true,
      message: "Owner inquiry registered successfully. Our underwriting desk will contact you within 24 hours.",
      lead: leadRecord
    }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: "Server error processing lead", details: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
}
