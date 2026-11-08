
// fmr_and_workorder_calcs.js - Yield, FMR Variance & Work Order Math

const hudFmrStandards2026 = {
  'Hennepin': { 1: 1450, 2: 1780, 3: 2240, 4: 2620 },
  'Ramsey': { 1: 1410, 2: 1720, 3: 2180, 4: 2550 },
  'Dakota': { 1: 1420, 2: 1740, 3: 2200, 4: 2580 },
  'St. Croix': { 1: 1220, 2: 1530, 3: 1950, 4: 2310 }
};

function calculatePropertyYieldVariance() {
  if (typeof state === 'undefined' || !state.properties) return;

  state.properties.forEach(p => {
    const beds = p.bedrooms || 2;
    const county = p.county || 'Hennepin';
    const benchmark = (hudFmrStandards2026[county] && hudFmrStandards2026[county][beds]) || 1750;
    const contract = Number(p.rent || p.contractRent || 0);
    const variance = contract - benchmark;
    p.safmrBenchmark = benchmark;
    p.safmrVariance = variance;
  });
}

function calculateWorkOrderTotals() {
  const pId = document.getElementById('detailPropertySelector')?.value || 'prop-1';
  const prop = state.properties.find(p => p.id === pId) || state.properties[0];
  if (!prop) return;

  const tasks = prop.tasks || [];
  const totalCost = tasks.reduce((sum, t) => sum + (Number(t.cost) || 0), 0);
  const pendingCount = tasks.filter(t => !t.done).length;
  const doneCount = tasks.filter(t => t.done).length;

  const elPending = document.getElementById('tasksPendingCount');
  const elDone = document.getElementById('tasksDoneCount');
  if (elPending) elPending.innerText = `${pendingCount} Pending ($${totalCost} est)`;
  if (elDone) elDone.innerText = `${doneCount} Done`;
}

// Bind to lifecycle and selection events
window.addEventListener('DOMContentLoaded', () => {
  calculatePropertyYieldVariance();
  calculateWorkOrderTotals();
});

document.addEventListener('change', (e) => {
  if (e.target && e.target.id === 'detailPropertySelector') {
    calculateWorkOrderTotals();
  }
});
