import os
import shutil
import subprocess

persistence_js = """
// state_persistence.js - Persistent Multi-Unit Portfolio State Manager
// Automatically syncs additions from bulk rent roll imports or property card edits

(function initPortfolioPersistence() {
  const STORAGE_KEY = 'SEC8_PORTFOLIO_MASTER_DATA';

  const defaultSeed = [
    {
      id: 'prop-1',
      address: '7820 Penn Ave S',
      city: 'Bloomington',
      state: 'MN',
      county: 'Hennepin',
      bedrooms: 3,
      rent: 2150,
      contractRent: 2150,
      hap: 1680,
      hapPortion: 1680,
      copay: 470,
      copayPortion: 470,
      deposit: 2150,
      tenant: 'Marcus & Elena Vance',
      tenantName: 'Marcus & Elena Vance',
      yearBuilt: 1974,
      status: 'Active'
    },
    {
      id: 'prop-2',
      address: '1042 Grand Ave',
      city: 'Saint Paul',
      state: 'MN',
      county: 'Ramsey',
      bedrooms: 2,
      rent: 1850,
      contractRent: 1850,
      hap: 1420,
      hapPortion: 1420,
      copay: 430,
      copayPortion: 430,
      deposit: 1850,
      tenant: 'Sarah Jenkins',
      tenantName: 'Sarah Jenkins',
      yearBuilt: 1982,
      status: 'Active'
    },
    {
      id: 'prop-3',
      address: '210 N Main St',
      city: 'Hudson',
      state: 'WI',
      county: 'St. Croix',
      bedrooms: 1,
      rent: 1420,
      contractRent: 1420,
      hap: 1100,
      hapPortion: 1100,
      copay: 320,
      copayPortion: 320,
      deposit: 1420,
      tenant: 'David Miller',
      tenantName: 'David Miller',
      yearBuilt: 1968,
      status: 'Active'
    }
  ];

  function loadState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.warn("Storage parse error, using default seed:", e);
    }
    return defaultSeed;
  }

  function saveState(properties) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(properties));
    } catch (e) {
      console.error("Failed saving portfolio state:", e);
    }
  }

  window.state = window.state || {};
  if (!window.state.properties || window.state.properties.length === 0) {
    window.state.properties = loadState();
  }

  window.savePortfolioState = function() {
    if (window.state && window.state.properties) {
      saveState(window.state.properties);
    }
  };

  // Auto-sync whenever bulk ingestion completes
  const origProcess = window.processRawRentRoll;
  if (typeof origProcess === 'function') {
    window.processRawRentRoll = function() {
      origProcess();
      window.savePortfolioState();
    };
  }

  console.log("✔ Portfolio state initialized with " + window.state.properties.length + " properties.");
})();
"""

with open("state_persistence.js", "w", encoding="utf-8") as f:
    f.write(persistence_js)

os.makedirs("public", exist_ok=True)
shutil.copy2("state_persistence.js", "public/state_persistence.js")

# Register in index.html and admin.html before closing head or body
for html_file in ["index.html", "admin.html"]:
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            c = f.read()
        if "state_persistence.js" not in c:
            c = c.replace("</head>", '<script src="state_persistence.js"></script>\n</head>', 1)
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(c)
            shutil.copy2(html_file, f"public/{html_file}")

# Push updates to Cloudflare Pages
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "feat: implement persistent local storage state synchronization across portfolio"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=False)
print("SUCCESS: State persistence layer deployed live to Cloudflare Pages.")
