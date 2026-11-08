// portfolio_sanitizer.js - Production Sanitizer & Sample Data Purge Failsafe
function purgeSampleDataAndLockdown() {
  if (window.RBAC_SYSTEM && window.RBAC_SYSTEM.currentUser.role !== 'Admin') {
    alert("ACCESS DENIED: Only the Managing Principal (Admin) can purge portfolio data.");
    return;
  }
  const confirmed = confirm("Purge all 5 mock sample units and reset the ledger for fresh production entry?");
  if (!confirmed) return;
  if (typeof window.exportPortfolioToJson === 'function') window.exportPortfolioToJson();
  localStorage.setItem('SEC8_PORTFOLIO_MASTER_DATA', JSON.stringify([]));
  if (window.state) { window.state.properties = []; window.state.accountingLedger = []; }
  alert("Sample data purged. Clean production state initialized.");
  location.reload();
}
window.purgeSampleDataAndLockdown = purgeSampleDataAndLockdown;
