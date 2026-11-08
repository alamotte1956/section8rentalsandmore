
// marketing_distribution_engine.js - Target Landing Pages & Multi-Channel Syndication
// Section 8 Rentals and More LLC • Twin Cities Metro & Western Wisconsin Operations

const MARKETING_FUNNELS = {
  landlord_sec8: {
    title: 'Guaranteed Rent & Zero Vacancy: Twin Cities Section 8 Management',
    target: 'Private Landlords & Multi-Family Owners',
    headline: 'Unlock Higher Returns with HUD Guaranteed Direct Deposits',
    bullets: [
      'Maximize cash flow with 2026 Small Area FMR rent rates up to $2,450+ for 3-bedrooms.',
      'Sovereign direct deposit: 70–100% of rent backed directly by federal housing authorities.',
      'Full NSPIRE pre-inspection punchlists guarantee 1-pass inspection approvals.',
      'Automated Form HUD-52517 (RFTA) preparation submitted directly to county PHAs.'
    ],
    cta: 'Onboard Your Property for Section 8 Placement',
    socialHook: 'Tired of late rent payments? Guaranteed Section 8 voucher direct deposits protect your cash flow across Hennepin, Ramsey, and Dakota counties. We handle all HUD-52517 paperwork and NSPIRE compliance.'
  },
  landlord_conventional: {
    title: 'Dual-State Full-Service Management: Minnesota & Wisconsin',
    target: 'Market-Rate & Conventional Property Owners',
    headline: 'Turnkey Property Management Built on Strict Statutory Compliance',
    bullets: [
      'Comprehensive screening conforming to Minn. Stat. § 504B.173 pre-application standards.',
      'Segregated 1.0% interest-bearing escrow accounts under Minn. Stat. § 504B.178.',
      'Automated Form CRP delivery and annual Schedule E CPA-ready tax staging.',
      '24/7 priority emergency dispatch protecting mechanical and structural habitability.'
    ],
    cta: 'Request a Free Rental Analysis & Management Proposal',
    socialHook: 'Managing rentals in the Twin Cities or Western Wisconsin? Protect your asset with airtight Minn. Stat. § 504B compliance, 21-day escrow audits, and automated tax accounting.'
  },
  tenant_vouchers: {
    title: 'High-Quality Section 8 Housing in Prime Twin Cities Neighborhoods',
    target: 'Active Housing Choice Voucher Holders',
    headline: 'Welcome Home: Clean, Modern, NSPIRE-Certified Homes Ready for Immediate Lease-Up',
    bullets: [
      'Fast-track RFTA packet signing completed in under 24 hours.',
      'Strict adherence to Fair Housing Act & Assistance Animal protections (HUD FHEO 2020-01).',
      'Direct coordination with your county voucher worker for smooth intake.',
      'Responsive, professional property maintenance with clear communication.'
    ],
    cta: 'View Available Section 8 Homes & Submit Your Voucher',
    socialHook: 'Looking for a clean, welcoming rental in the Twin Cities metro that proudly accepts Section 8 vouchers? Explore our NSPIRE-inspected single-family and apartment homes with fast RFTA turnaround.'
  },
  agency_partners: {
    title: 'Direct Referral Portal for Housing Authorities & Case Managers',
    target: 'PHA Navigators, County Workers & Non-Profit Housing Advocates',
    headline: 'Reliable, Expedited Housing Placement for Your Voucher Clients',
    bullets: [
      'Real-time vacancy visibility across Hennepin, Ramsey, Dakota, and St. Croix counties.',
      'Digital packet submission directly to MPHA, Saint Paul PHA, and Dakota County CDA.',
      'Expedited 24-hour response on all caseworker inquiries and client screenings.',
      'Commitment to stable, long-term tenancy and proactive landlord communication.'
    ],
    cta: 'Partner With Section 8 Rentals and More LLC',
    socialHook: 'Housing case managers & PHA navigators: Partner with Section 8 Rentals and More LLC for reliable, rapid lease-up of your voucher clients in fully pre-inspected units.'
  }
};

function openMarketingDistributionModal() {
  let modal = document.getElementById('marketingModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'marketingModal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4 overflow-y-auto';
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="relative w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-6 text-slate-100 my-8 max-h-[90vh] flex flex-col">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4 shrink-0">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-violet-400"></span>
            <h3 class="text-xl font-bold text-white tracking-tight">Marketing Funnels & Social Syndication</h3>
          </div>
          <p class="text-xs text-slate-400 mt-1">Four targeted acquisition portals & automated Fair Housing-compliant syndication copy</p>
        </div>
        <button onclick="document.getElementById('marketingModal').remove()" class="text-slate-400 hover:text-white text-2xl font-bold px-3 py-1 rounded-xl hover:bg-slate-800 transition-colors">×</button>
      </div>

      <div class="overflow-y-auto pr-2 space-y-6 flex-1 custom-scrollbar">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${Object.entries(MARKETING_FUNNELS).map(([key, funnel]) => `
            <div class="bg-slate-950/70 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between space-y-4">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-violet-400 px-2 py-0.5 rounded-full bg-violet-500/10 border border-violet-500/20">${funnel.target}</span>
                  <button onclick="copySocialAd('${key}')" class="text-[11px] text-slate-400 hover:text-white bg-slate-800 px-2 py-1 rounded-lg transition-colors">📋 Copy Ad Text</button>
                </div>
                <h4 class="text-sm font-bold text-white mt-2.5">${funnel.title}</h4>
                <p class="text-xs text-slate-300 italic mt-1">${funnel.headline}</p>
                <ul class="mt-3 space-y-1.5 text-[11px] text-slate-400">
                  ${funnel.bullets.map(b => `<li class="flex items-start gap-1.5"><span class="text-emerald-400">✓</span> ${b}</li>`).join('')}
                </ul>
              </div>
              <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[10px] text-slate-500 font-mono">/funnels/${key}</span>
                <button onclick="previewLandingPage('${key}')" class="px-3 py-1.5 rounded-xl bg-violet-500/20 text-violet-300 border border-violet-500/30 hover:bg-violet-500/30 text-xs font-semibold transition-all">Preview Page</button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-slate-800 text-xs text-slate-400 shrink-0">
        <span>Section 8 Rentals and More LLC • Equal Housing Opportunity Compliant</span>
        <button onclick="document.getElementById('marketingModal').remove()" class="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold transition-colors">Close</button>
      </div>
    </div>
  `;
}

function copySocialAd(funnelKey) {
  const funnel = MARKETING_FUNNELS[funnelKey];
  if (!funnel) return;
  const text = `${funnel.title}\n\n${funnel.headline}\n\nKey Benefits:\n${funnel.bullets.map(b => '• ' + b).join('\n')}\n\n${funnel.socialHook}\n\nLearn more: https://section8rentalsandmore.pages.dev\nEqual Housing Opportunity.`;
  navigator.clipboard.writeText(text).then(() => {
    alert(`Copied Fair Housing-compliant ad copy for '${funnel.title}' to clipboard!`);
  });
}

function previewLandingPage(funnelKey) {
  const funnel = MARKETING_FUNNELS[funnelKey];
  if (!funnel) return;

  const w = window.open('', '_blank');
  w.document.write(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>${funnel.title}</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-slate-100 font-sans p-6 sm:p-12">
      <div class="max-w-3xl mx-auto space-y-8 bg-slate-900 border border-slate-800 rounded-3xl p-8 sm:p-12 shadow-2xl">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <span class="text-xs uppercase tracking-widest text-violet-400 font-bold">${funnel.target}</span>
          <span class="text-xs text-slate-400">Section 8 Rentals and More LLC</span>
        </div>
        <div>
          <h1 class="text-3xl sm:text-4xl font-black text-white tracking-tight">${funnel.title}</h1>
          <p class="text-lg text-slate-300 mt-3 font-medium">${funnel.headline}</p>
        </div>
        <div class="bg-slate-950/60 border border-slate-800 rounded-2xl p-6 space-y-3">
          <h2 class="text-xs font-bold uppercase tracking-wider text-slate-400">Program Advantages</h2>
          <ul class="space-y-2.5 text-sm text-slate-300">
            ${funnel.bullets.map(b => `<li class="flex items-start gap-2.5"><span class="text-emerald-400 font-bold">✓</span> ${b}</li>`).join('')}
          </ul>
        </div>
        <div class="pt-4 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="text-sm font-bold text-white">Equal Housing Opportunity</div>
            <div class="text-xs text-slate-400">Twin Cities Metro (MN) & Western Wisconsin (WI)</div>
          </div>
          <button class="px-6 py-3 rounded-2xl bg-violet-500 hover:bg-violet-400 text-slate-950 font-bold text-sm transition-all shadow-lg shadow-violet-500/20">
            ${funnel.cta}
          </button>
        </div>
      </div>
    </body>
    </html>
  `);
  w.document.close();
}

window.openMarketingDistributionModal = openMarketingDistributionModal;
window.copySocialAd = copySocialAd;
window.previewLandingPage = previewLandingPage;
