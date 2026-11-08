
// portfolio_export_engine.js - Automated Backup, State Restore & CSV Export Engine
// Section 8 Rentals and More LLC • Twin Cities Metro & Western Wisconsin Operations

function exportPortfolioToJson() {
  const data = {
    version: '2026.11-PROD',
    exportedAt: new Date().toISOString(),
    entity: 'Section 8 Rentals and More LLC',
    principal: 'Dr. Albert Ray LaMotte',
    totalUnits: (window.state?.properties || []).length,
    properties: window.state?.properties || [],
    ledger: window.state?.accountingLedger || window.state?.ledger || []
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `sec8_portfolio_backup_${new Date().toISOString().slice(0, 10)}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function exportRentRollToCsv() {
  const props = window.state?.properties || [];
  if (props.length === 0) {
    alert("No active properties found in portfolio to export.");
    return;
  }

  const headers = [
    'Property ID', 'Address', 'City', 'State', 'County',
    'Bedrooms', 'Year Built', 'Gross Rent', 'HAP Subsidy', 'Tenant Copay',
    'Security Deposit', 'Tenant Name', 'Status'
  ];

  const rows = props.map(p => [
    p.id || '',
    `"${p.address || ''}"`,
    `"${p.city || ''}"`,
    p.state || 'MN',
    p.county || 'Hennepin',
    p.bedrooms || 2,
    p.yearBuilt || 1974,
    (p.rent || p.contractRent || 1950).toFixed(2),
    (p.hap || p.hapPortion || 1520).toFixed(2),
    (p.copay || p.copayPortion || 430).toFixed(2),
    (p.deposit || p.contractRent || 1950).toFixed(2),
    `"${p.tenant || p.tenantName || 'Resident Occupant'}"`,
    p.status || 'Active'
  ]);

  const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `rent_roll_summary_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function restorePortfolioFromJson(fileInput) {
  const file = fileInput.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (Array.isArray(data.properties)) {
        window.state = window.state || {};
        window.state.properties = data.properties;
        if (typeof window.savePortfolioState === 'function') {
          window.savePortfolioState();
        }
        if (typeof renderProperties === 'function') {
          renderProperties();
        }
        alert(`Successfully restored ${data.properties.length} properties from backup file.`);
      } else {
        alert("Invalid backup format: missing properties array.");
      }
    } catch (err) {
      alert("Error parsing backup file: " + err.message);
    }
  };
  reader.readAsText(file);
}

window.exportPortfolioToJson = exportPortfolioToJson;
window.exportRentRollToCsv = exportRentRollToCsv;
window.restorePortfolioFromJson = restorePortfolioFromJson;
