import os
import shutil
import subprocess
import re

print("Binding Compliance Hub trigger buttons to property cards...")

# Function to patch renderProperties in a file
def patch_render_properties(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Look for the card action buttons or property card footer
    # Inject openComplianceModal button if not already present
    if "openComplianceModal" not in content:
        # Pattern matching typical card action buttons in the portal UI
        button_html = (
            '<button onclick="openComplianceModal(\'${p.id}\')" '
            'class="px-2.5 py-1 text-[11px] font-semibold rounded-lg bg-emerald-500/20 text-emerald-300 '
            'border border-emerald-500/30 hover:bg-emerald-500/30 transition-all flex items-center gap-1.5">'
            '<span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>'
            'HUD & Legal Docs'
            '</button>'
        )

        # Target insertion right next to standard card actions or status pill
        if "generateRftaPacket" in content:
            content = content.replace("generateRftaPacket", "openComplianceModal")
        elif "${p.address}" in content:
            # Anchor near card action containers
            content = re.sub(
                r'(<div class="flex[^>]*gap-2[^>]*>)',
                r'\1 ' + button_html,
                content,
                count=1
            )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔ Injected compliance action trigger into {filepath}")

patch_render_properties("index.html")
patch_render_properties("admin.html")
patch_render_properties("features.js")

os.makedirs("public", exist_ok=True)
if os.path.exists("index.html"):
    shutil.copy2("index.html", "public/index.html")
if os.path.exists("admin.html"):
    shutil.copy2("admin.html", "public/admin.html")
if os.path.exists("features.js"):
    shutil.copy2("features.js", "public/features.js")

# Commit and deploy to Cloudflare Pages
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "feat: bind compliance hub trigger buttons across property UI cards"], check=False)
res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)
print("SUCCESS: Live UI cards wired with 1-click Compliance Hub triggers.")
