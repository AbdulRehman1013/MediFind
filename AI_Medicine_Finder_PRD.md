# AI Medicine Finder & Price Comparator
## Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** April 2026  
**Status:** Ready for Development  
**Target Market:** Pakistan & South Asia (Scalable Globally)

---

## 1. Executive Summary

Medicines in Pakistan can vary by **30–300% in price** across different pharmacies for the identical product. Patients — especially those managing chronic conditions — waste hours searching for availability, overpay unknowingly, and sometimes unknowingly purchase expired or counterfeit stock. **MediFind** is an AI-powered medicine discovery and price comparison platform that solves this problem at the community level by combining real-time pharmacy data, AI-driven substitution logic, expiry verification signals, and usage guidance into a single, accessible interface.

---

## 2. Problem Statement

| Problem | Impact |
|---|---|
| Price variance for same medicine across pharmacies | Patients overpay by up to 300% |
| No centralized availability lookup | Wasted time visiting multiple pharmacies |
| Counterfeit & expired medicine risk | Health risk, no consumer-level detection tool |
| Unawareness of cheaper generic alternatives | Patients default to branded drugs unnecessarily |
| No accessible usage guidance | Misuse, missed doses, dangerous combinations |

### Who Is Affected?
- **Chronic patients** (diabetes, hypertension, thyroid) buying medicine monthly
- **Low-income households** where medicine costs are a significant burden
- **Caregivers** managing medicine for elderly dependents
- **Rural populations** with limited pharmacy access

---

## 3. Vision & Mission

**Vision:** Every person deserves to find safe, affordable medicine — instantly.

**Mission:** Use AI to make medicine price transparency, availability, and safety a basic utility — not a privilege.

---

## 4. Product Goals

1. **Transparency** — Show real-time or near-real-time price comparison across pharmacies
2. **Accessibility** — Works on low-end Android devices, supports Urdu language
3. **Safety** — Flag overpriced listings, detect potential counterfeit signals, warn about expiry
4. **Intelligence** — Suggest bioequivalent generic alternatives with confidence scoring
5. **Guidance** — Provide basic, verified usage information (dose, timing, interactions)

---

## 5. Target Users

### Primary Users
| Persona | Description | Key Need |
|---|---|---|
| **Chronic Patient** | 35–65 yrs, manages recurring prescriptions | Cheapest verified source, monthly reminders |
| **Budget Shopper** | Price-conscious buyer, first-time purchase | Instant price comparison, generic options |
| **Caregiver** | Manages meds for elderly parent/child | Availability alerts, interaction checker |
| **Rural Patient** | Limited local pharmacy options | Nearest availability, delivery options |

### Secondary Users
| Persona | Description |
|---|---|
| **Pharmacist / Retailer** | List inventory, attract new customers |
| **Healthcare NGO** | Bulk medicine sourcing data |
| **DRAP (Drug Regulatory Authority Pakistan)** | Compliance monitoring partner |

---

## 6. Core Features

### 6.1 Medicine Search & Discovery
- Search by brand name, generic name, or symptoms
- Multilingual support: English + Urdu
- Voice search (mobile)
- Barcode / QR scan to identify medicine
- Autocomplete with categorized suggestions

### 6.2 Price Comparison Engine
- Display prices across verified pharmacies (nearby first)
- Price history graph (7-day, 30-day trend)
- Highlight **cheapest verified source**
- Flag items priced **>25% above average** as "Overpriced ⚠️"
- Transparent pricing: show base price + delivery fee

### 6.3 Nearby Availability
- Map view with pharmacy pins and stock status
- Filter by: Open Now, Home Delivery, 24-Hour, Verified
- Distance-based sorting (GPS)
- Call / WhatsApp pharmacy directly from app
- Stock confidence indicator (last updated timestamp)

### 6.4 Generic & Substitute Recommender (AI)
- AI engine maps branded drugs → generic equivalents
- Show: Generic Name, Salt Composition, Manufacturer, Price Difference %
- Confidence tier: "Bioequivalent ✓", "Similar Composition", "Discuss with Doctor"
- One-tap switch to compare generic options

### 6.5 Overpriced & Risk Detector
- Automatic price anomaly flagging
- Pharmacy trust score (based on ratings, reports, registration status)
- Community reporting: "Report suspicious price" / "Report expired stock"
- DRAP registration verification badge

### 6.6 Usage Guidance Module
- Basic dosage information (from verified medical database)
- Common side effects
- Food/drug interaction warnings (top 5)
- "Do not use with" alerts
- Pregnancy / Breastfeeding safety flag
- Disclaimer: "Always consult your doctor" on every guidance card

### 6.7 User Personalization
- Saved medicines list (My Pharmacy)
- Price drop alerts (push notification)
- Prescription photo upload → auto-extract medicines via OCR
- Monthly refill reminders

### 6.8 Pharmacy Partner Dashboard
- Pharmacies register and list inventory
- Verified badge after DRAP license check
- Promoted listings (paid, clearly labeled)
- Analytics: views, comparison appearances, clicks

---

## 7. AI & Technology Architecture

### 7.1 AI Components

| Component | Technology | Purpose |
|---|---|---|
| **Search NLP** | LLM fine-tuned on drug names | Handle typos, brand↔generic mapping |
| **Substitute Engine** | Drug composition graph + similarity scoring | Recommend bioequivalent alternatives |
| **Price Anomaly Detector** | Statistical outlier model | Flag overpriced listings |
| **OCR Prescription Reader** | Vision model | Extract medicine names from prescriptions |
| **Usage Info Retrieval** | RAG on verified medical databases | Safe, cited drug information |

### 7.2 Tech Stack

**Frontend:**
- React Native (iOS + Android)
- Next.js (Web PWA)
- Urdu RTL support

**Backend:**
- Node.js / FastAPI microservices
- PostgreSQL + PostGIS (geo queries)
- Redis (caching, real-time updates)
- Elasticsearch (medicine search)

**AI/ML:**
- OpenAI / Claude API for NLP and guidance
- Custom fine-tuned model for drug substitution
- Computer Vision for barcode and prescription OCR

**Infrastructure:**
- AWS / local Pakistan cloud (for data residency)
- CDN for fast load times on 3G networks

---

## 8. Data Strategy

### 8.1 Data Sources
| Source | Data Type | Update Frequency |
|---|---|---|
| DRAP (Drug Regulatory Authority Pakistan) | Registered drugs, approved prices | Monthly |
| Partner Pharmacies (API) | Real-time stock & price | Every 30 min |
| Crowdsourced users | Price reports, expiry alerts | Real-time |
| WHO / BNF database | Drug compositions, interactions | Quarterly |
| Community pharmacy surveys | Baseline price benchmarks | Weekly |

### 8.2 Data Quality Controls
- Price submissions require pharmacy login
- Outlier prices held for review before publishing
- User-reported prices marked separately with confidence score
- Automated duplicate and fraud detection

---

## 9. Monetization Model

| Revenue Stream | Mechanism | Target |
|---|---|---|
| **Pharmacy Listings (Freemium)** | Free basic listing; paid for priority placement | Pharmacies |
| **Promoted Results** | Clearly labeled sponsored pharmacy cards | Pharmacies / Distributors |
| **B2B API Access** | Price & availability data for hospitals, insurers | Enterprises |
| **Insurance Integration** | Partner with insurers to show covered medicines | Insurers |
| **White Label** | Platform licensed to hospital chains / NGOs | Institutions |

**Year 1 Target Revenue:** PKR 15M  
**Year 2 Target Revenue:** PKR 60M

---

## 10. Success Metrics (KPIs)

### User Metrics
| KPI | Month 3 | Month 6 | Month 12 |
|---|---|---|---|
| Monthly Active Users | 10,000 | 50,000 | 200,000 |
| Searches per DAU | 3.2 | 4.0 | 5.0 |
| Retention (D30) | 25% | 35% | 45% |

### Product Metrics
| KPI | Target |
|---|---|
| Average savings per search | PKR 80+ |
| Price comparison accuracy | >92% |
| Pharmacy partner count | 500 by Month 6 |
| Prescription OCR accuracy | >88% |

### Safety Metrics
| KPI | Target |
|---|---|
| Overpriced flagging precision | >85% |
| Community counterfeit reports actioned | <48 hrs |
| DRAP verified pharmacies % | >70% of listings |

---

## 11. Competitive Landscape

| Competitor | Strengths | Weaknesses | Our Edge |
|---|---|---|---|
| **Dawaai.pk** | Online pharmacy, delivery | No price comparison, one-source | Multi-pharmacy comparison |
| **Sehat.com.pk** | Doctor + pharmacy | Limited price data | AI substitution engine |
| **PharmEasy (India)** | Scale, tech | Not in Pakistan | Local compliance + Urdu |
| **Manual search** | Zero cost | Time-consuming, inaccurate | Speed + intelligence |

**Our Moat:** AI-powered substitution engine + community price verification + DRAP integration = trust layer competitors lack.

---

## 12. Regulatory & Compliance

- Align with **DRAP (Drug Regulatory Authority of Pakistan)** guidelines
- No prescription medicines dispensed without verified prescription
- Drug usage info sourced from verified databases only, with clear disclaimers
- User health data stored in Pakistan (local data residency)
- GDPR-aligned privacy policy for international expansion
- Clear labeling: sponsored vs organic results

---

## 13. Roadmap

### Phase 1 — MVP (Month 1–3)
- [ ] Medicine search with price comparison (simulated data + 50 partner pharmacies)
- [ ] Nearby pharmacy map
- [ ] Generic substitute recommendations
- [ ] Basic usage guidance cards
- [ ] Android app launch (Lahore, Karachi pilot)

### Phase 2 — Growth (Month 4–6)
- [ ] Prescription OCR upload
- [ ] Price alerts & refill reminders
- [ ] Pharmacy partner onboarding portal
- [ ] Community reporting (fake/expired medicine)
- [ ] Urdu language full support
- [ ] iOS app

### Phase 3 — Scale (Month 7–12)
- [ ] DRAP API integration (official registered medicine prices)
- [ ] Insurance partnership (show covered medicines)
- [ ] Voice search (Urdu)
- [ ] B2B API for hospitals
- [ ] Expansion to other cities and regions

### Phase 4 — Expand (Year 2)
- [ ] Bangladesh, Sri Lanka markets
- [ ] AI interaction checker (multi-drug)
- [ ] Telemedicine integration

---

## 14. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Pharmacy data inaccuracy | High | High | Crowdsource verification + freshness timestamps |
| Regulatory pushback | Medium | High | Proactive DRAP partnership, no dispensing |
| Low pharmacy adoption | Medium | Medium | Field sales team + free tier value |
| Counterfeit info liability | Low | Very High | Strong disclaimers, user-report system, legal review |
| Price manipulation by pharmacies | Medium | Medium | Outlier detection, audit trails |

---

## 15. Design Principles

1. **Speed over Complexity** — Results in under 2 seconds on 3G
2. **Trust Signals Everywhere** — Verified badges, data freshness, source citations
3. **Accessible First** — Works on 2GB RAM phones, supports elderly users
4. **Transparent AI** — Never hide that results are AI-assisted; show confidence levels
5. **Safety as Default** — When in doubt, err toward caution and recommend doctor

---

## 16. Appendix

### A. Medicine Categories Covered (Phase 1)
- Antibiotics, Analgesics, Antihypertensives, Antidiabetics, Antihistamines, Vitamins/Supplements, Antacids, Thyroid medications, Contraceptives, Dermatologicals

### B. Sample User Story
> **Aisha**, 42, Lahore. Her father takes 6 medicines daily for diabetes and blood pressure. Every month, she spends 2 hours visiting 3 pharmacies to find the best prices. With MediFind, she searches once, sees all prices side-by-side, switches two branded medicines to verified generics, and saves PKR 1,200/month — automatically reordering via WhatsApp with the cheapest verified pharmacy.

### C. Glossary
- **Generic Medicine:** Same active ingredient as branded, different manufacturer, lower cost
- **Bioequivalent:** Generics proven to have same effect as brand in body
- **DRAP:** Drug Regulatory Authority of Pakistan
- **Salt Composition:** The active chemical compounds in a medicine
- **RAG:** Retrieval-Augmented Generation (AI technique for accurate, cited answers)

---

*Document prepared for: Founders / Product Team / Investors*  
*Confidential — Internal Use*
