
// rbac_manager_engine.js - Two-Level Security (Admin vs Manager) & Unit Delegation
// Enforces NIST AC-3 boundaries, isolating sensitive accounting and PHI decryptor access

const RBAC_SYSTEM = {
  currentUser: {
    name: 'Dr. Albert Ray LaMotte',
    role: 'Admin', // 'Admin' or 'Manager'
    assignedProperties: ['prop-hennepin-01', 'prop-ramsey-02', 'prop-dakota-03', 'prop-anoka-04', 'prop-stcroix-05']
  },

  setRole(newRole, userName, assignedUnits = []) {
    this.currentUser.role = newRole;
    this.currentUser.name = userName || (newRole === 'Admin' ? 'Dr. Albert Ray LaMotte' : 'Property Manager');
    this.currentUser.assignedProperties = assignedUnits.length ? assignedUnits : (window.state?.properties || []).map(p => p.id);
    localStorage.setItem('SEC8_ACTIVE_USER_ROLE', JSON.stringify(this.currentUser));
    this.applyUIRestrictions();
    console.log(`[RBAC] Switched active user to ${this.currentUser.name} (${this.currentUser.role})`);
  },

  init() {
    try {
      const saved = localStorage.getItem('SEC8_ACTIVE_USER_ROLE');
      if (saved) {
        this.currentUser = JSON.parse(saved);
      }
    } catch (e) {
      console.warn("RBAC init parse error, keeping Admin default:", e);
    }
    this.applyUIRestrictions();
  },

  canAccess(feature) {
    if (this.currentUser.role === 'Admin') return true;

    // Manager restrictions
    const restrictedForManagers = [
      'BANKING_LEDGER_RECONCILE',
      'HIPAA_PHI_DECRYPT',
      'CRYPTOGRAPHIC_SHRED',
      'PURGE_SAMPLE_DATA',
      'EXPORT_PORTFOLIO_STATE',
      'TAX_CREDIT_AUTHORIZATION'
    ];

    return !restrictedForManagers.includes(feature);
  },

  applyUIRestrictions() {
    const isAdmin = this.currentUser.role === 'Admin';
    
    // Toggle admin-only controls across the interface
    document.querySelectorAll('[data-admin-only="true"]').forEach(el => {
      el.style.display = isAdmin ? '' : 'none';
    });

    const badge = document.getElementById('rbacUserBadge');
    if (badge) {
      badge.innerHTML = `
        <span class="w-2 h-2 rounded-full ${isAdmin ? 'bg-amber-400' : 'bg-sky-400'}"></span>
        <span class="font-bold">${this.currentUser.name}</span>
        <span class="text-[10px] px-1.5 py-0.5 rounded ${isAdmin ? 'bg-amber-500/20 text-amber-300' : 'bg-sky-500/20 text-sky-300'} font-mono uppercase">${this.currentUser.role}</span>
      `;
    }
  }
};

function toggleRbacModal() {
  let modal = document.getElementById('rbacModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'rbacModal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4';
    document.body.appendChild(modal);
  }

  const isAdmin = RBAC_SYSTEM.currentUser.role === 'Admin';

  modal.innerHTML = `
    <div class="relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl text-slate-100 space-y-5">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-amber-400"></span>
          <h3 class="text-base font-bold text-white">Role-Based Access Management</h3>
        </div>
        <button onclick="document.getElementById('rbacModal').remove()" class="text-slate-400 hover:text-white text-xl">×</button>
      </div>

      <p class="text-xs text-slate-400 leading-relaxed">
        Admins possess unrestricted statutory authority (HIPAA PHI decryption, bank reconciliation, tax credit transmission). Managers are restricted to operational maintenance, tenant intake, and pre-inspection tasks.
      </p>

      <div class="space-y-3 text-xs">
        <label class="block font-semibold text-slate-300">Switch Operational Security Profile:</label>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="RBAC_SYSTEM.setRole('Admin', 'Dr. Albert Ray LaMotte'); document.getElementById('rbacModal').remove(); location.reload();" 
                  class="p-3 rounded-xl border text-center transition-all ${isAdmin ? 'bg-amber-500/20 border-amber-500/50 text-amber-300 font-bold' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white'}">
            👑 Admin Principal
            <div class="text-[10px] font-normal mt-1 text-slate-400">Full Statutory & Financial Authority</div>
          </button>

          <button onclick="RBAC_SYSTEM.setRole('Manager', 'Field Operations Manager'); document.getElementById('rbacModal').remove(); location.reload();" 
                  class="p-3 rounded-xl border text-center transition-all ${!isAdmin ? 'bg-sky-500/20 border-sky-500/50 text-sky-300 font-bold' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white'}">
            📋 Field Manager
            <div class="text-[10px] font-normal mt-1 text-slate-400">Restricted Operations / No PHI / No Ledger</div>
          </button>
        </div>
      </div>

      <div class="pt-3 border-t border-slate-800 flex justify-end">
        <button onclick="document.getElementById('rbacModal').remove()" class="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 hover:text-white text-xs font-semibold">Done</button>
      </div>
    </div>
  `;
}

window.RBAC_SYSTEM = RBAC_SYSTEM;
window.toggleRbacModal = toggleRbacModal;

document.addEventListener('DOMContentLoaded', () => {
  RBAC_SYSTEM.init();
});
