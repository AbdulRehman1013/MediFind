const state = {
  dashboard: null,
  medicines: [],
  selectedMedicineId: null,
  selectedDetail: null,
  favorites: new Set(),
  location: {
    lat: null,
    lng: null,
    label: "Location off",
  },
  filters: {
    query: "",
    city: "",
    mode: "",
  },
};

const els = {};

function money(value) {
  if (value === null || value === undefined) {
    return "PKR --";
  }
  return new Intl.NumberFormat("en-PK", { maximumFractionDigits: 0 }).format(value);
}

function qsa(selector, root = document) {
  return [...root.querySelectorAll(selector)];
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json();
}

function currentLocationParams() {
  const params = new URLSearchParams();
  if (state.location.lat !== null && state.location.lng !== null) {
    params.set("lat", String(state.location.lat));
    params.set("lng", String(state.location.lng));
  }
  return params;
}

function setLocationStatus(text) {
  state.location.label = text;
  if (els.locationStatus) {
    els.locationStatus.textContent = text;
  }
}

async function enableLocation() {
  if (!navigator.geolocation) {
    setLocationStatus("Location unavailable");
    return;
  }

  setLocationStatus("Requesting location...");
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      state.location.lat = position.coords.latitude;
      state.location.lng = position.coords.longitude;
      setLocationStatus(`Near me: ${position.coords.latitude.toFixed(3)}, ${position.coords.longitude.toFixed(3)}`);
      await refreshAll();
    },
    (error) => {
      setLocationStatus("Location blocked");
      console.error(error);
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
  );
}

function setLoadingMeta(message) {
  if (els.resultMeta) {
    els.resultMeta.textContent = message;
  }
}

function updateCityOptions(cities) {
  const current = els.cityFilter.value;
  els.cityFilter.innerHTML = '<option value="">All cities</option>';
  cities.forEach((city) => {
    const option = document.createElement("option");
    option.value = city;
    option.textContent = city;
    els.cityFilter.appendChild(option);
  });
  if (cities.includes(current)) {
    els.cityFilter.value = current;
  }
}

async function loadDashboard() {
  const city = els.cityFilter.value || "";
  const params = currentLocationParams();
  if (city) params.set("city", city);
  const dashboard = await request(`/api/dashboard${params.toString() ? `?${params.toString()}` : ""}`);
  state.dashboard = dashboard;

  els.statMedicines.textContent = dashboard.total_medicines;
  els.statPharmacies.textContent = dashboard.verified_pharmacies;
  els.statSavings.textContent = `PKR ${money(dashboard.average_savings)}`;
  els.statFavorites.textContent = dashboard.favorites;
  els.reportCountPill.textContent = `${dashboard.reports} reports`;
  updateCityOptions(dashboard.cities);

  if (dashboard.best_value) {
    els.mapTitle.textContent = dashboard.best_value.name;
    els.mapStatus.textContent = `Best value from PKR ${money(dashboard.best_value.cheapest_price)}`;
  } else {
    els.mapTitle.textContent = "Nearby options";
    els.mapStatus.textContent = "Live inventory";
  }

  renderMapPins(state.selectedDetail || dashboard.best_value_detail);
}

async function loadMedicines() {
  const params = new URLSearchParams();
  if (state.filters.query) params.set("q", state.filters.query);
  if (state.filters.city) params.set("city", state.filters.city);
  if (state.filters.mode === "verified") params.set("verified", "true");
  if (state.filters.mode === "delivery") params.set("delivery", "true");
  const locationParams = currentLocationParams();
  locationParams.forEach((value, key) => params.set(key, value));

  setLoadingMeta("Searching...");
  const payload = await request(`/api/medicines${params.toString() ? `?${params.toString()}` : ""}`);
  state.medicines = payload.items;
  renderMedicineList();
  setLoadingMeta(`${payload.count} result${payload.count === 1 ? "" : "s"} found`);
  if (!state.selectedMedicineId && payload.items.length) {
    await selectMedicine(payload.items[0].id);
  }
}

function priceTag(card) {
  if (card.cheapest_price === null || card.cheapest_price === undefined) {
    return "No stock";
  }
  return `PKR ${money(card.cheapest_price)}`;
}

function statusClass(status) {
  if (status === "Available") return "green";
  if (status === "Limited stock") return "amber";
  return "red";
}

function renderMedicineList() {
  els.medicineList.innerHTML = "";
  if (!state.medicines.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No medicines matched your search. Try a generic name, a symptom, or remove one of the filters.";
    els.medicineList.appendChild(empty);
    return;
  }

  for (const medicine of state.medicines) {
    const card = document.createElement("article");
    card.className = `medicine-card ${medicine.id === state.selectedMedicineId ? "active" : ""}`;
    card.dataset.id = medicine.id;
    card.innerHTML = `
      <div>
        <div class="medicine-title">
          <span>${medicine.name}</span>
          <span class="status-pill ${statusClass(medicine.status)}">${medicine.status}</span>
        </div>
        <div class="medicine-subtitle">${medicine.summary}</div>
        <div class="medicine-meta">
          <span class="mini-tag">${medicine.brand_name}</span>
          <span class="mini-tag">${medicine.generic_name}</span>
          <span class="mini-tag">${medicine.available_count} pharmacies</span>
          ${medicine.favorite ? '<span class="mini-tag">Saved</span>' : ""}
        </div>
        <div class="tag-row">
          <span class="tag">${medicine.category}</span>
          <span class="tag">${medicine.is_generic ? "Generic" : "Brand"}</span>
          <span class="tag">${medicine.overpriced_count} overpriced flag${medicine.overpriced_count === 1 ? "" : "s"}</span>
        </div>
      </div>
      <div class="price-box">
        <strong>${priceTag(medicine)}</strong>
        <small>${medicine.savings !== null && medicine.savings !== undefined ? `Save PKR ${money(medicine.savings)}` : "No price data"}</small>
      </div>
    `;
    card.addEventListener("click", () => selectMedicine(medicine.id));
    els.medicineList.appendChild(card);
  }
}

function renderMapPins(detail) {
  const offers = detail?.offers || [];
  const map = els.availabilityMap;
  qsa(".map-pin", map).forEach((node) => node.remove());

  const currentOffers = offers.filter((offer) => offer.stock !== "out_of_stock");
  const source = currentOffers.length ? currentOffers : offers;
  source.slice(0, 6).forEach((offer, index) => {
    const pin = document.createElement("div");
    pin.className = "map-pin";
    const stockClass = offer.stock === "in_stock" ? "stock" : offer.stock === "low_stock" ? "low" : "out";
    pin.style.left = `${offer.pharmacy.pin_x}%`;
    pin.style.top = `${offer.pharmacy.pin_y}%`;
    pin.innerHTML = `<div class="pin-dot ${stockClass}"></div>`;
    pin.title = `${offer.pharmacy.name} - PKR ${money(offer.total_price)}`;
    pin.addEventListener("click", async (event) => {
      event.stopPropagation();
      await selectMedicine(detail.medicine.id);
      const offerCards = qsa(".offer-card");
      if (offerCards[index]) {
        offerCards[index].scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
    map.appendChild(pin);
  });
}

function renderOffers(offers) {
  els.offerList.innerHTML = "";
  offers.forEach((offer) => {
    const card = document.createElement("article");
    card.className = "offer-card";
    const stockLabel =
      offer.stock === "in_stock" ? "In stock" : offer.stock === "low_stock" ? `Low stock (${offer.quantity} left)` : "Out of stock";
    const stockClass = offer.stock === "in_stock" ? "green" : offer.stock === "low_stock" ? "amber" : "red";
    const verified = offer.pharmacy.verified ? "Verified" : "Unverified";
    const trustLabel = `${offer.pharmacy.trust_score}% trust`;
    card.innerHTML = `
      <div class="offer-top">
        <div>
          <div class="offer-title">${offer.pharmacy.name}</div>
          <div class="offer-subtitle">${offer.pharmacy.city} - ${offer.pharmacy.address}</div>
        </div>
        <div class="offer-price">PKR ${money(offer.total_price)}</div>
      </div>
      <div class="offer-badges">
        <span class="status-pill">${stockLabel}</span>
        <span class="status-pill">${verified}</span>
        <span class="status-pill">${trustLabel}</span>
        <span class="status-pill">${(offer.distance_from_user_km ?? offer.pharmacy.distance_km)} km away</span>
        ${offer.overpriced ? '<span class="status-pill red">Overpriced</span>' : ""}
      </div>
      <div class="offer-actions">
        <a class="primary-link" href="tel:${String(offer.pharmacy.phone).replace(/[^\d]/g, "")}">Call</a>
        <a href="https://wa.me/${String(offer.pharmacy.whatsapp).replace(/[^\d]/g, "")}" target="_blank" rel="noreferrer">WhatsApp</a>
      </div>
    `;
    els.offerList.appendChild(card);
  });
}

function renderAlternatives(alternatives) {
  els.alternativeList.innerHTML = "";
  if (!alternatives.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No substitutions found for this medicine.";
    els.alternativeList.appendChild(empty);
    return;
  }

  alternatives.forEach((alt) => {
    const card = document.createElement("article");
    card.className = "alternative-card";
    card.innerHTML = `
      <div class="alternative-top">
        <div>
          <div class="offer-title">${alt.name}</div>
          <div class="offer-subtitle">${alt.generic_name}</div>
        </div>
        <div class="offer-price">PKR ${money(alt.cheapest_price)}</div>
      </div>
      <div class="offer-badges">
        <span class="status-pill">${alt.confidence}</span>
        <span class="status-pill">${alt.savings !== null && alt.savings !== undefined ? `Save PKR ${money(alt.savings)}` : "Price matched"}</span>
      </div>
      <div class="offer-subtitle">${alt.reason}</div>
    `;
    card.addEventListener("click", () => selectMedicine(alt.medicine_id));
    els.alternativeList.appendChild(card);
  });
}

function renderDetail(detail) {
  state.selectedDetail = detail;
  const medicine = detail.medicine;
  state.selectedMedicineId = medicine.id;
  window.__mfSelectedMedicineId = medicine.id;
  window.__mfSelectedMedicineName = medicine.name;
  window.__mfSelectedGenericName = medicine.generic_name;

  qsa(".medicine-card").forEach((node) => {
    node.classList.toggle("active", node.dataset.id === medicine.id);
  });

  els.detailTitle.textContent = medicine.name;
  els.detailEmpty.hidden = true;
  els.detailContent.hidden = false;
  els.favoriteButton.hidden = false;
  if (els.reportMedicineId) {
    els.reportMedicineId.value = medicine.id;
  }
  if (els.reportSummaryLine) {
    els.reportSummaryLine.textContent = `${medicine.name} - ${medicine.generic_name}`;
  }
  els.favoriteButton.textContent = medicine.favorite ? "Saved" : "Save";
  els.favoriteBadge.textContent = medicine.favorite ? "Saved to favorites" : "Tap save to bookmark";
  els.medicineCategory.textContent = `${medicine.category} - ${medicine.is_generic ? "Generic" : "Brand"}`;
  els.medicineName.textContent = medicine.name;
  els.medicineSummary.textContent = medicine.summary;
  els.cheapestPrice.textContent = `PKR ${money(detail.summary.cheapest_price)}`;
  els.averagePrice.textContent = `PKR ${money(detail.summary.average_price)}`;
  els.savingsValue.textContent = detail.summary.cheapest_savings === null ? "PKR --" : `PKR ${money(detail.summary.cheapest_savings)}`;
  els.offerCount.textContent = `${detail.summary.offer_count} comparable offer${detail.summary.offer_count === 1 ? "" : "s"}`;
  els.pricingNote.textContent = `${detail.summary.total_price_rule} ${detail.summary.overpriced_rule}`;
  els.dosageText.textContent = medicine.dosage;
  els.foodText.textContent = medicine.food_notes;
  els.sideEffectsText.textContent = medicine.side_effects.join(", ");
  els.interactionText.textContent = medicine.interactions.join(", ");
  els.pregnancyText.textContent = medicine.pregnancy;

  els.medicineTags.innerHTML = "";
  [
    medicine.brand_name,
    medicine.generic_name,
    `${detail.summary.availability_score}% availability`,
    detail.summary.overpriced_count > 0 ? `${detail.summary.overpriced_count} overpriced flag${detail.summary.overpriced_count === 1 ? "" : "s"}` : "No pricing flags",
  ].forEach((label) => {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = label;
    els.medicineTags.appendChild(tag);
  });

  renderOffers(detail.offers);
  renderAlternatives(detail.alternatives);
  renderMapPins(detail);
}

async function selectMedicine(medicineId) {
  const city = els.cityFilter.value || "";
  const verified = els.stockFilter.value === "verified";
  const delivery = els.stockFilter.value === "delivery";
  const params = new URLSearchParams();
  if (city) params.set("city", city);
  if (verified) params.set("verified", "true");
  if (delivery) params.set("delivery", "true");
  const locationParams = currentLocationParams();
  locationParams.forEach((value, key) => params.set(key, value));
  const path = `/api/medicines/${encodeURIComponent(medicineId)}${params.toString() ? `?${params.toString()}` : ""}`;
  const detail = await request(path);
  renderDetail(detail);
  state.selectedMedicineId = medicineId;
  renderMedicineList();
}

function scrollToReport() {
  els.reportSection?.scrollIntoView({ behavior: "smooth", block: "start" });
  els.reportNote?.focus?.();
}

function wireQuickChips() {
  qsa(".chip", els.quickChips).forEach((chip) => {
    chip.addEventListener("click", () => {
      qsa(".chip", els.quickChips).forEach((node) => node.classList.remove("active"));
      chip.classList.add("active");
      els.searchInput.value = chip.dataset.query;
      state.filters.query = chip.dataset.query;
      refreshAll().catch(console.error);
    });
  });
}

function wireFilters() {
  const trigger = () => {
    state.filters.query = els.searchInput.value.trim();
    state.filters.city = els.cityFilter.value;
    state.filters.mode = els.stockFilter.value;
    refreshAll().catch(console.error);
  };

  els.searchInput.addEventListener("input", () => {
    state.filters.query = els.searchInput.value.trim();
    clearTimeout(window.__mfSearchTimer);
    window.__mfSearchTimer = setTimeout(() => refreshAll().catch(console.error), 180);
  });
  els.searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      trigger();
    }
  });
  els.cityFilter.addEventListener("change", trigger);
  els.stockFilter.addEventListener("change", trigger);
  els.searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    trigger();
  });
}

function wireFavoriteButton() {
  els.favoriteButton.addEventListener("click", async () => {
    if (!state.selectedMedicineId) return;
    await request(`/api/favorites/${encodeURIComponent(state.selectedMedicineId)}`, { method: "POST" });
    await refreshAll();
  });
}

function wireReportForm() {
  els.reportForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const medicineId = els.reportMedicineId?.value || state.selectedMedicineId || "";
    if (!medicineId) {
      els.reportMessage.textContent = "Select a medicine first so we know what to report.";
      return;
    }
    els.reportMessage.textContent = "Submitting report...";
    try {
      await request("/api/reports", {
        method: "POST",
        body: JSON.stringify({
          medicine_id: medicineId,
          pharmacy_id: null,
          report_type: els.reportType.value,
          note: els.reportNote.value.trim(),
        }),
      });
      els.reportMessage.textContent = "Report submitted. Thanks for helping keep pricing transparent.";
      els.reportNote.value = "";
      await loadDashboard();
    } catch (error) {
      els.reportMessage.textContent = `Could not submit report: ${error.message}`;
    }
  });
}

async function refreshAll() {
  await loadDashboard();
  await loadMedicines();
  if (state.selectedMedicineId) {
    await selectMedicine(state.selectedMedicineId);
  }
}

function wireButtons() {
  if (els.locationStatus) {
    setLocationStatus("Location off");
  }
  if (els.locationButton) {
    els.locationButton.addEventListener("click", () => enableLocation().catch(console.error));
  }
  if (els.useLocationHeroButton) {
    els.useLocationHeroButton.addEventListener("click", () => enableLocation().catch(console.error));
  }
  if (els.openReportButton) {
    els.openReportButton.addEventListener("click", scrollToReport);
  }
  if (els.openReportButtonInline) {
    els.openReportButtonInline.addEventListener("click", scrollToReport);
  }
  els.focusSearchButton.addEventListener("click", () => {
    els.searchInput.focus();
    els.searchInput.scrollIntoView({ behavior: "smooth", block: "center" });
  });
  els.openFilterButton.addEventListener("click", () => {
    els.stockFilter.value = "verified";
    state.filters.mode = "verified";
    refreshAll().catch(console.error);
  });
  els.refreshButton.addEventListener("click", () => refreshAll().catch(console.error));
}

function cacheElements() {
  const ids = [
    "refreshButton",
    "locationButton",
    "useLocationHeroButton",
    "locationStatus",
    "openReportButton",
    "openReportButtonInline",
    "reportCountPill",
    "focusSearchButton",
    "openFilterButton",
    "statMedicines",
    "statPharmacies",
    "statSavings",
    "statFavorites",
    "mapTitle",
    "mapStatus",
    "availabilityMap",
    "resultMeta",
    "searchInput",
    "cityFilter",
    "stockFilter",
    "searchForm",
    "quickChips",
    "medicineList",
    "detailTitle",
    "detailEmpty",
    "detailContent",
    "favoriteButton",
    "favoriteBadge",
    "medicineCategory",
    "medicineName",
    "medicineSummary",
    "medicineTags",
    "cheapestPrice",
    "averagePrice",
    "savingsValue",
    "offerCount",
    "pricingNote",
    "offerList",
    "dosageText",
    "foodText",
    "sideEffectsText",
    "interactionText",
    "pregnancyText",
    "alternativeList",
    "reportSection",
    "reportForm",
    "reportMedicineId",
    "reportType",
    "reportNote",
    "reportMessage",
    "reportSummaryLine",
  ];
  ids.forEach((id) => {
    els[id] = document.getElementById(id);
  });
}

async function bootstrap() {
  cacheElements();
  wireButtons();
  wireQuickChips();
  wireFilters();
  wireFavoriteButton();
  wireReportForm();
  try {
    const favs = await request("/api/favorites");
    state.favorites = new Set(favs.items.map((item) => item.medicine.id));
    await loadDashboard();
    await loadMedicines();
  } catch (error) {
    setLoadingMeta(`Unable to load data: ${error.message}`);
  }
}

document.addEventListener("DOMContentLoaded", bootstrap);

