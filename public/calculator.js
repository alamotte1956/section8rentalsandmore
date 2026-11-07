let fmrData = null;

async function initCalculator() {
  try {
    const res = await fetch("data/fmr_2027_client.json");
    fmrData = await res.json();
    populateCountyDropdown();
    renderUtilityCheckboxes();
    calculateRent();
  } catch (err) {
    console.error("Failed to load FY 2027 FMR client dataset:", err);
  }
}

function populateCountyDropdown() {
  const select = document.getElementById("countySelect");
  if (!select || !fmrData) return;
  select.innerHTML = "";

  const primaryGroup = document.createElement("optgroup");
  primaryGroup.label = "Core Footprint (Twin Cities & Western WI)";

  const otherGroup = document.createElement("optgroup");
  otherGroup.label = "All Other Minnesota Counties";

  const allCounties = Object.keys(fmrData.counties).sort();

  allCounties.forEach(county => {
    const opt = document.createElement("option");
    opt.value = county;
    opt.textContent = county;
    if (fmrData.primary_counties.includes(county)) {
      if (county === "Dakota County") opt.selected = true;
      primaryGroup.appendChild(opt);
    } else {
      otherGroup.appendChild(opt);
    }
  });

  select.appendChild(primaryGroup);
  select.appendChild(otherGroup);
}

function renderUtilityCheckboxes() {
  const container = document.getElementById("utilityCheckboxes");
  if (!container || !fmrData) return;
  container.innerHTML = "";

  for (const [key, util] of Object.entries(fmrData.utility_allowances)) {
    const label = document.createElement("label");
    label.style.display = "flex";
    label.style.alignItems = "center";
    label.style.gap = "8px";
    label.style.margin = "4px 0";

    const chk = document.createElement("input");
    chk.type = "checkbox";
    chk.name = "tenantUtility";
    chk.value = key;
    chk.addEventListener("change", calculateRent);

    label.appendChild(chk);
    label.appendChild(document.createTextNode(util.name));
    container.appendChild(label);
  }
}

function calculateRent() {
  if (!fmrData) return;

  const county = document.getElementById("countySelect").value;
  const bedrooms = document.getElementById("bedroomSelect").value;
  const brKey = `${bedrooms}BR`;

  const countyRecord = fmrData.counties[county];
  if (!countyRecord) return;

  const grossStandard = countyRecord.rates[brKey] || 0;

  const checkedUtils = Array.from(document.querySelectorAll("input[name='tenantUtility']:checked"))
    .map(el => el.value);

  let totalDeduction = 0;
  checkedUtils.forEach(key => {
    const allowance = fmrData.utility_allowances[key];
    if (allowance && allowance.rates[brKey]) {
      totalDeduction += allowance.rates[brKey];
    }
  });

  const netOwnerRent = Math.max(0, grossStandard - totalDeduction);

  document.getElementById("grossStandard").textContent = `$${grossStandard.toLocaleString()}`;
  document.getElementById("utilityDeductions").textContent = `-$${totalDeduction.toLocaleString()}`;
  document.getElementById("netOwnerRent").textContent = `$${netOwnerRent.toLocaleString()}`;
  document.getElementById("metroAreaLabel").textContent = countyRecord.metro_area;
}

document.addEventListener("DOMContentLoaded", () => {
  initCalculator();
  document.getElementById("countySelect")?.addEventListener("change", calculateRent);
  document.getElementById("bedroomSelect")?.addEventListener("change", calculateRent);
});