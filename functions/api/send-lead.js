export async function onRequestPost({ request, env }) {
  try {
    const d = await request.json();
    const key = env.RESEND_API_KEY;
    if (!key) return new Response(JSON.stringify({ error: "Missing RESEND_API_KEY" }), { status: 500 });
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${key}`,
        "Content-Type": "application/json",
        "User-Agent": "Section8Rentals-App/1.0"
      },
      body: JSON.stringify({
        from: "Section 8 Intake <notifications@section8rentalsandmore.com>",
        to: ["info@section8rentalsandmore.com"],
        reply_to: d.email,
        subject: `New Lead: ${d.name} (${d.county})`,
        html: `<p><strong>Name:</strong> ${d.name}</p><p><strong>Email:</strong> ${d.email}</p><p><strong>County:</strong> ${d.county}</p><p><strong>Notes:</strong> ${d.notes}</p>`
      })
    });
    const result = await res.json();
    return new Response(JSON.stringify(result), { status: res.status });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
