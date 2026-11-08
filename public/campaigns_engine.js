
// campaigns_engine.js - 4 Multi-Channel Ad Funnels & UTM Engine
let activeFunnel = 'landlords';

const funnelData = {
  landlords: {
    title: 'Property Owners & Multi-Family Landlords',
    headline: 'Stop Chasing Rent. Get 70–100% Guaranteed Direct Deposit Every Month.',
    sub: 'Eliminate vacancy loss with HUD voucher placement, SAFMR yield bumps, and complete statutory legal insulation.',
    cta: 'Schedule a Free Section 8 Rent Max Audit'
  },
  tenants: {
    title: 'Approved Housing Choice Voucher Holders',
    headline: 'Approved Voucher in Hand? Move Into a Certified Home in 48 Hours.',
    sub: 'We partner directly with MPHA, St. Paul PHA, Dakota CDA, and St. Croix HRA to expedite your HUD-52517 (RFTA) paperwork.',
    cta: 'Submit 60-Second Voucher Fast-Track e-App'
  },
  caseworkers: {
    title: 'PHA Housing Specialists & Case Managers',
    headline: 'Dedicated Direct-Placement Channel for Housing Caseworkers',
    sub: 'Pre-inspected units verified to pass MPHA and St. Paul PHA audits on first walkthrough with instant 24-hr RFTA turnaround.',
    cta: 'Request Priority Vacancy Roster'
  },
  investors: {
    title: 'Passive Turnkey Capital & Real Estate Investors',
    headline: 'Recession-Proof 12–16% Cash-on-Cash Returns Backed by Federal Subsidy',
    sub: 'Turnkey Section 8 acquisition, tenant screening, NSPIRE compliance, and QuickBooks Online class tracking.',
    cta: 'Download Investor Pro-Forma & Portfolio Deck'
  }
};

function selectCampaignType(key) {
  activeFunnel = key;
  renderCampaignCanvas();
}

function renderCampaignCanvas() {
  const c = document.getElementById('campaignCanvas');
  if (!c) return;
  const f = funnelData[activeFunnel] || funnelData.landlords;
  c.innerHTML = `
    <span class="px-2.5 py-0.5 rounded text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase">${f.title}</span>
    <h3 class="text-xl font-bold text-white mt-2">${f.headline}</h3>
    <p class="text-xs text-slate-300 mt-1 leading-relaxed">${f.sub}</p>
    <div class="pt-3 flex gap-3">
      <button onclick="alert('Inquiry recorded for ${activeFunnel}!')" class="px-5 py-2.5 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl text-xs">${f.cta}</button>
      <button onclick="copyTrackedCampaignUrl()" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold">Copy Tracked Link</button>
    </div>
  `;
}

function copyTrackedCampaignUrl() {
  const url = `${window.location.origin}${window.location.pathname}#ad-${activeFunnel}?utm_source=facebook_ads&utm_campaign=twin_cities_section8`;
  navigator.clipboard?.writeText(url).then(() => {
    alert('Tracked Ad URL copied to clipboard: ' + url);
  });
}
