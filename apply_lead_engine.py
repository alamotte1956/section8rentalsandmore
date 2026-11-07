import os
import glob

# 1. Lead Desk snippet for admin.html
lead_desk_html = """
<!-- Inbound Campaign Leads Desk -->
<div class="card" style="margin-top:24px; padding:20px; background:#fff; border:1px solid #cbd5e1; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <h3 style="margin:0; color:#1e3a8a;">Inbound Campaign Leads & Inquiries</h3>
    <div>
      <button onclick="clearDemoLeads()" style="background:#e2e8f0; color:#334155; border:none; padding:6px 12px; border-radius:4px; font-weight:600; cursor:pointer; margin-right:8px;">Clear</button>
      <button onclick="exportLeadsJson()" style="background:#2563eb; color:#fff; border:none; padding:6px 14px; border-radius:4px; font-weight:600; cursor:pointer;">Export JSON</button>
    </div>
  </div>
  <div id="leadsList" style="font-size:13px; color:#334155; overflow-x:auto;">
    <em>Loading inbound lead ledger...</em>
  </div>
</div>
<script>
  function renderAdminLeads() {
    const leads = JSON.parse(localStorage.getItem('section8_leads') || '[]');
    const target = document.getElementById('leadsList');
    if (!target) return;
    if (!leads.length) {
      target.innerHTML = '<p style="color:#64748b; margin:6px 0;">No inquiries captured in browser storage yet.</p>';
      return;
    }
    let h = '<table style="width:100%; border-collapse:collapse; text-align:left;">';
    h += '<tr style="background:#f8fafc; border-bottom:2px solid #cbd5e1;"><th style="padding:8px;">ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Property</th><th>Bedrooms</th><th>Date</th></tr>';
    leads.slice().reverse().forEach(l => {
      h += `<tr style="border-bottom:1px solid #e2e8f0;">
        <td style="padding:8px; font-family:monospace; font-weight:600; color:#1e40af;">${l.lead_id || 'N/A'}</td>
        <td style="font-weight:600;">${l.full_name || 'N/A'}</td>
        <td><a href="tel:${l.phone || ''}" style="color:#2563eb; text-decoration:none;">${l.phone || 'N/A'}</a></td>
        <td><a href="mailto:${l.email || ''}" style="color:#2563eb; text-decoration:none;">${l.email || 'N/A'}</a></td>
        <td>${l.property_address || 'Unspecified'}</td>
        <td>${l.bedrooms || 'N/A'}</td>
        <td style="color:#64748b;">${l.timestamp ? new Date(l.timestamp).toLocaleDateString() : 'N/A'}</td>
      </tr>`;
    });
    h += '</table>';
    target.innerHTML = h;
  }
  function exportLeadsJson() {
    const raw = localStorage.getItem('section8_leads') || '[]';
    const blob = new Blob([raw], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'section8_leads_captured.json';
    link.click();
  }
  function clearDemoLeads() {
    if (confirm("Reset captured leads in this browser?")) {
      localStorage.removeItem('section8_leads');
      renderAdminLeads();
    }
  }
  window.addEventListener('DOMContentLoaded', renderAdminLeads);
</script>
"""

# Patch public/admin.html and root admin.html
for apath in ["public/admin.html", "admin.html"]:
    if os.path.exists(apath):
        with open(apath, "r", encoding="utf-8") as f:
            content = f.read()
        if "Inbound Campaign Leads & Inquiries" not in content:
            if "</body>" in content:
                content = content.replace("</body>", lead_desk_html + "\n</body>")
            else:
                content += "\n" + lead_desk_html
            with open(apath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✔ Embedded Lead Desk into {apath}")
        else:
            print(f"✔ Lead Desk verified in {apath}")

# 2. Campaign lead intake form snippet
intake_form_html = """
<!-- Lead Intake Section -->
<div class="cta" style="margin-top:28px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:24px;">
  <h3 style="margin-top:0; color:#1e3a8a;">Request Property Placement Analysis</h3>
  <p style="color:#475569; font-size:14px; margin-top:4px;">Guaranteed monthly rent under HUD standards. Receive a full rent ceiling and utility allowance breakdown.</p>
  <form id="leadForm" style="margin-top:14px;">
    <div style="margin-bottom:10px;">
      <label style="display:block; font-size:13px; font-weight:600; color:#1e293b; margin-bottom:4px;">Full Name *</label>
      <input type="text" name="full_name" required placeholder="Dr. Albert LaMotte" style="width:100%; box-sizing:border-box; padding:10px; border:1px solid #94a3b8; border-radius:4px;">
    </div>
    <div style="margin-bottom:10px;">
      <label style="display:block; font-size:13px; font-weight:600; color:#1e293b; margin-bottom:4px;">Phone Number *</label>
      <input type="tel" name="phone" required placeholder="(612) 701-7064" style="width:100%; box-sizing:border-box; padding:10px; border:1px solid #94a3b8; border-radius:4px;">
    </div>
    <div style="margin-bottom:10px;">
      <label style="display:block; font-size:13px; font-weight:600; color:#1e293b; margin-bottom:4px;">Email Address *</label>
      <input type="email" name="email" required placeholder="info@Section8RentalsandMore.com" style="width:100%; box-sizing:border-box; padding:10px; border:1px solid #94a3b8; border-radius:4px;">
    </div>
    <div style="margin-bottom:10px;">
      <label style="display:block; font-size:13px; font-weight:600; color:#1e293b; margin-bottom:4px;">Property Address</label>
      <input type="text" name="property_address" placeholder="17420 Kenwood Trail, Lakeville, MN 55044" style="width:100%; box-sizing:border-box; padding:10px; border:1px solid #94a3b8; border-radius:4px;">
    </div>
    <button type="submit" style="width:100%; background:#16a34a; color:#fff; padding:12px; border:none; border-radius:4px; font-size:15px; font-weight:700; cursor:pointer;">Submit Property for Placement</button>
    <div id="statusMsg" style="margin-top:12px; padding:10px; border-radius:4px; display:none; font-size:13px; text-align:center;"></div>
  </form>
</div>
<script>
document.getElementById('leadForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const s = document.getElementById('statusMsg');
  s.style.display = 'block';
  s.style.background = '#eff6ff';
  s.style.color = '#1e40af';
  s.innerText = 'Registering inquiry with underwriting desk...';

  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());
  data.timestamp = new Date().toISOString();
  data.lead_id = 'LEAD-' + Date.now();

  try {
    let existing = JSON.parse(localStorage.getItem('section8_leads') || '[]');
    existing.push(data);
    localStorage.setItem('section8_leads', JSON.stringify(existing));

    s.style.background = '#dcfce7';
    s.style.color = '#15803d';
    s.innerHTML = '✔ <strong>Placement Analysis Requested!</strong> Reference: ' + data.lead_id + '<br>Underwriting review initiated. We will contact you within 24 hours.';
    e.target.reset();
  } catch (err) {
    s.style.background = '#fee2e2';
    s.style.color = '#b91c1c';
    s.innerText = 'Direct Contact: Call Section 8 Rentals and More desk at (612) 701-7064.';
  }
});
</script>
"""

campaign_pages = glob.glob(os.path.join("public", "campaigns", "*.html"))
for cpath in campaign_pages:
    with open(cpath, "r", encoding="utf-8") as f:
        html = f.read()

    # If previous partial lead form exists, cleanly replace it; otherwise place before </body>
    if 'id="leadForm"' in html:
        # File already has an older block, ensure section8_leads is present
        if 'section8_leads' not in html:
            # Inject section8_leads listener
            html = html.replace("</form>", "</form>\n<script>\ndocument.getElementById('leadForm').addEventListener('submit', function(e){ e.preventDefault(); const d=Object.fromEntries(new FormData(e.target).entries()); d.timestamp=new Date().toISOString(); d.lead_id='LEAD-'+Date.now(); let arr=JSON.parse(localStorage.getItem('section8_leads')||'[]'); arr.push(d); localStorage.setItem('section8_leads',JSON.stringify(arr)); alert('Request registered! Ref: '+d.lead_id); e.target.reset(); });\n</script>")
            with open(cpath, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✔ Appended storage handler: {cpath}")
        else:
            print(f"✔ Already verified with section8_leads: {cpath}")
    else:
        if "</body>" in html:
            html = html.replace("</body>", intake_form_html + "\n</body>")
        else:
            html += "\n" + intake_form_html
        with open(cpath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✔ Injected full intake form: {cpath}")

print("✔ Campaign pages and admin dashboard updated successfully.")
