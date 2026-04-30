from __future__ import annotations

from copy import deepcopy
from difflib import SequenceMatcher, get_close_matches


PHARMACIES = [
    {
        "id": "city-health-khi",
        "name": "City Health Pharmacy",
        "city": "Karachi",
        "address": "Clifton Block 5",
        "district": "South",
        "lat": 24.813,
        "lng": 67.033,
        "verified": True,
        "open_now": True,
        "delivery": True,
        "twenty_four_hour": True,
        "rating": 4.8,
        "trust_score": 96,
        "phone": "+92 21 111 223 334",
        "whatsapp": "923001112233",
        "pin_x": 25,
        "pin_y": 34,
        "distance_km": 0.8,
    },
    {
        "id": "green-cross-khi",
        "name": "Green Cross Medics",
        "city": "Karachi",
        "address": "Gulshan-e-Iqbal",
        "district": "East",
        "lat": 24.925,
        "lng": 67.089,
        "verified": True,
        "open_now": True,
        "delivery": True,
        "twenty_four_hour": False,
        "rating": 4.6,
        "trust_score": 92,
        "phone": "+92 21 111 554 900",
        "whatsapp": "923111119900",
        "pin_x": 66,
        "pin_y": 56,
        "distance_km": 1.4,
    },
    {
        "id": "medico-lhr",
        "name": "Medico Care Pharmacy",
        "city": "Lahore",
        "address": "Gulberg III",
        "district": "Central",
        "lat": 31.520,
        "lng": 74.345,
        "verified": True,
        "open_now": True,
        "delivery": True,
        "twenty_four_hour": False,
        "rating": 4.7,
        "trust_score": 94,
        "phone": "+92 42 111 778 899",
        "whatsapp": "9242111178899",
        "pin_x": 35,
        "pin_y": 28,
        "distance_km": 1.1,
    },
    {
        "id": "elite-lhr",
        "name": "Elite Pharmacy Hub",
        "city": "Lahore",
        "address": "DHA Phase 5",
        "district": "South",
        "lat": 31.470,
        "lng": 74.398,
        "verified": False,
        "open_now": False,
        "delivery": True,
        "twenty_four_hour": False,
        "rating": 4.2,
        "trust_score": 74,
        "phone": "+92 42 111 665 244",
        "whatsapp": "92421111665244",
        "pin_x": 62,
        "pin_y": 64,
        "distance_km": 2.3,
    },
    {
        "id": "sehat-point-isl",
        "name": "Sehat Point Pharmacy",
        "city": "Islamabad",
        "address": "F-7 Markaz",
        "district": "Capital",
        "lat": 33.717,
        "lng": 73.073,
        "verified": True,
        "open_now": True,
        "delivery": False,
        "twenty_four_hour": True,
        "rating": 4.9,
        "trust_score": 97,
        "phone": "+92 51 111 338 810",
        "whatsapp": "92511111338810",
        "pin_x": 44,
        "pin_y": 38,
        "distance_km": 0.6,
    },
    {
        "id": "noor-drug-rwp",
        "name": "Noor Drug Mart",
        "city": "Rawalpindi",
        "address": "Saddar",
        "district": "Potohar",
        "lat": 33.600,
        "lng": 73.067,
        "verified": False,
        "open_now": True,
        "delivery": True,
        "twenty_four_hour": False,
        "rating": 4.1,
        "trust_score": 68,
        "phone": "+92 51 111 520 520",
        "whatsapp": "92511111520520",
        "pin_x": 57,
        "pin_y": 70,
        "distance_km": 2.0,
    },
]


MEDICINES = [
    {
        "id": "glucophage-xr-500",
        "name": "Glucophage XR 500 mg",
        "brand_name": "Glucophage XR",
        "generic_name": "Metformin Hydrochloride",
        "composition_key": "metformin-500",
        "is_generic": False,
        "category": "Diabetes",
        "symptoms": ["diabetes", "high blood sugar", "insulin resistance"],
        "summary": "Extended-release metformin used to improve blood sugar control in type 2 diabetes.",
        "dosage": "Usually taken with food once daily or as prescribed by a doctor.",
        "side_effects": ["Nausea", "Stomach upset", "Loose stools"],
        "interactions": ["Alcohol", "Certain contrast dyes", "Excessive fasting"],
        "food_notes": "Take with meals to reduce stomach irritation.",
        "pregnancy": "Discuss with your doctor before use during pregnancy.",
        "availability_note": "Often available at verified urban pharmacies.",
        "alternatives": [
            {"medicine_id": "metformin-500-generic", "confidence": "Bioequivalent", "reason": "Same active ingredient and strength."},
        ],
    },
    {
        "id": "metformin-500-generic",
        "name": "Metformin 500 mg",
        "brand_name": "Metformin",
        "generic_name": "Metformin Hydrochloride",
        "composition_key": "metformin-500",
        "is_generic": True,
        "category": "Diabetes",
        "symptoms": ["diabetes", "high blood sugar", "insulin resistance"],
        "summary": "Lower-cost generic version of metformin for blood glucose control.",
        "dosage": "Commonly prescribed with meals one or two times a day.",
        "side_effects": ["Nausea", "Gas", "Abdominal discomfort"],
        "interactions": ["Alcohol", "Certain contrast dyes", "Severe dehydration"],
        "food_notes": "Best taken with food.",
        "pregnancy": "Use only under a doctor's supervision.",
        "availability_note": "Usually the cheapest option in the diabetes category.",
        "alternatives": [
            {"medicine_id": "glucophage-xr-500", "confidence": "Bioequivalent", "reason": "Brand and generic share the same active ingredient."},
        ],
    },
    {
        "id": "lipitor-20",
        "name": "Lipitor 20 mg",
        "brand_name": "Lipitor",
        "generic_name": "Atorvastatin",
        "composition_key": "atorvastatin-20",
        "is_generic": False,
        "category": "Cholesterol",
        "symptoms": ["high cholesterol", "heart disease risk"],
        "summary": "Statin medicine for lowering LDL cholesterol and supporting heart health.",
        "dosage": "Often taken once daily in the evening, as prescribed.",
        "side_effects": ["Muscle aches", "Headache", "Upset stomach"],
        "interactions": ["Grapefruit juice", "Certain antibiotics", "Heavy alcohol use"],
        "food_notes": "Can be taken with or without food.",
        "pregnancy": "Not recommended during pregnancy.",
        "availability_note": "High-demand item with several generic substitutes.",
        "alternatives": [
            {"medicine_id": "atorvastatin-20-generic", "confidence": "Bioequivalent", "reason": "Same salt, lower-cost generic."},
        ],
    },
    {
        "id": "atorvastatin-20-generic",
        "name": "Atorvastatin 20 mg",
        "brand_name": "Atorvastatin",
        "generic_name": "Atorvastatin",
        "composition_key": "atorvastatin-20",
        "is_generic": True,
        "category": "Cholesterol",
        "symptoms": ["high cholesterol", "heart disease risk"],
        "summary": "Generic statin option for LDL reduction and long-term cardiovascular care.",
        "dosage": "Usually taken once daily, often in the evening.",
        "side_effects": ["Muscle aches", "Constipation", "Fatigue"],
        "interactions": ["Grapefruit juice", "Certain antifungals", "Heavy alcohol use"],
        "food_notes": "May be taken with or without meals.",
        "pregnancy": "Avoid unless specifically directed by a doctor.",
        "availability_note": "Often the best savings opportunity in the comparison list.",
        "alternatives": [
            {"medicine_id": "lipitor-20", "confidence": "Bioequivalent", "reason": "Brand and generic versions of the same drug."},
        ],
    },
    {
        "id": "thyronorm-50",
        "name": "Thyronorm 50 mcg",
        "brand_name": "Thyronorm",
        "generic_name": "Levothyroxine Sodium",
        "composition_key": "levothyroxine-50",
        "is_generic": False,
        "category": "Thyroid",
        "symptoms": ["hypothyroidism", "fatigue", "weight gain"],
        "summary": "Thyroid hormone replacement used to treat hypothyroidism.",
        "dosage": "Usually taken on an empty stomach in the morning.",
        "side_effects": ["Palpitations", "Jitteriness", "Insomnia if overdosed"],
        "interactions": ["Iron supplements", "Calcium supplements", "Soy-heavy meals"],
        "food_notes": "Wait at least 30 to 60 minutes before eating.",
        "pregnancy": "Commonly used in pregnancy when clinically indicated, but dose must be monitored.",
        "availability_note": "Sensitive timing and consistent dosing matter more than the brand name.",
        "alternatives": [
            {"medicine_id": "levothyroxine-50-generic", "confidence": "Bioequivalent", "reason": "Same hormone and strength."},
        ],
    },
    {
        "id": "levothyroxine-50-generic",
        "name": "Levothyroxine 50 mcg",
        "brand_name": "Levothyroxine",
        "generic_name": "Levothyroxine Sodium",
        "composition_key": "levothyroxine-50",
        "is_generic": True,
        "category": "Thyroid",
        "symptoms": ["hypothyroidism", "fatigue", "weight gain"],
        "summary": "Generic thyroid replacement medicine for long-term hormone therapy.",
        "dosage": "Typically taken once daily before breakfast.",
        "side_effects": ["Palpitations", "Anxiety", "Sleep disturbance"],
        "interactions": ["Iron supplements", "Calcium supplements", "Antacids"],
        "food_notes": "Take on an empty stomach for best absorption.",
        "pregnancy": "Dose should be adjusted by a clinician during pregnancy.",
        "availability_note": "Stable supply is important because this is a maintenance medicine.",
        "alternatives": [
            {"medicine_id": "thyronorm-50", "confidence": "Bioequivalent", "reason": "Brand equivalent for the same hormone."},
        ],
    },
    {
        "id": "augmentin-625",
        "name": "Augmentin 625 mg",
        "brand_name": "Augmentin",
        "generic_name": "Amoxicillin + Clavulanate",
        "composition_key": "co-amoxiclav-625",
        "is_generic": False,
        "category": "Antibiotic",
        "symptoms": ["bacterial infection", "sinus infection", "dental infection"],
        "summary": "Broad-spectrum antibiotic commonly used for bacterial infections.",
        "dosage": "Should only be taken when prescribed and completed as directed.",
        "side_effects": ["Diarrhea", "Rash", "Nausea"],
        "interactions": ["Alcohol can worsen stomach upset", "Warfarin", "Allopurinol"],
        "food_notes": "Usually easier on the stomach when taken after meals.",
        "pregnancy": "Discuss risks and benefits with a doctor.",
        "availability_note": "Short supply at some pharmacies due to seasonal demand.",
        "alternatives": [
            {"medicine_id": "co-amoxiclav-625-generic", "confidence": "Bioequivalent", "reason": "Same antibiotic combination at a lower price."},
        ],
    },
    {
        "id": "co-amoxiclav-625-generic",
        "name": "Co-amoxiclav 625 mg",
        "brand_name": "Co-amoxiclav",
        "generic_name": "Amoxicillin + Clavulanate",
        "composition_key": "co-amoxiclav-625",
        "is_generic": True,
        "category": "Antibiotic",
        "symptoms": ["bacterial infection", "sinus infection", "dental infection"],
        "summary": "Generic broad-spectrum antibiotic for prescribed bacterial infections.",
        "dosage": "Take exactly as prescribed and finish the full course.",
        "side_effects": ["Loose stools", "Rash", "Nausea"],
        "interactions": ["Warfarin", "Methotrexate", "Alcohol"],
        "food_notes": "Taking with food can reduce stomach upset.",
        "pregnancy": "Use only when prescribed by a clinician.",
        "availability_note": "Useful to compare because prices can vary sharply between neighborhoods.",
        "alternatives": [
            {"medicine_id": "augmentin-625", "confidence": "Bioequivalent", "reason": "Same salt combination in a generic formulation."},
        ],
    },
]


_PHARMACY_BY_ID = {item["id"]: item for item in PHARMACIES}


STOCK = {
    "glucophage-xr-500": [
        {"pharmacy_id": "city-health-khi", "price": 575, "stock": "in_stock", "quantity": 18, "updated_minutes": 5, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 640, "stock": "low_stock", "quantity": 4, "updated_minutes": 14, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 590, "stock": "in_stock", "quantity": 11, "updated_minutes": 17, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 610, "stock": "in_stock", "quantity": 7, "updated_minutes": 9, "delivery_fee": 0},
        {"pharmacy_id": "elite-lhr", "price": 720, "stock": "in_stock", "quantity": 5, "updated_minutes": 22, "delivery_fee": 35},
    ],
    "metformin-500-generic": [
        {"pharmacy_id": "city-health-khi", "price": 455, "stock": "in_stock", "quantity": 30, "updated_minutes": 3, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 495, "stock": "in_stock", "quantity": 21, "updated_minutes": 11, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 470, "stock": "in_stock", "quantity": 14, "updated_minutes": 12, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 480, "stock": "low_stock", "quantity": 3, "updated_minutes": 25, "delivery_fee": 0},
        {"pharmacy_id": "noor-drug-rwp", "price": 530, "stock": "in_stock", "quantity": 8, "updated_minutes": 19, "delivery_fee": 15},
    ],
    "lipitor-20": [
        {"pharmacy_id": "city-health-khi", "price": 1230, "stock": "in_stock", "quantity": 9, "updated_minutes": 8, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 1380, "stock": "in_stock", "quantity": 6, "updated_minutes": 16, "delivery_fee": 25},
        {"pharmacy_id": "medico-lhr", "price": 1295, "stock": "low_stock", "quantity": 2, "updated_minutes": 21, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 1210, "stock": "in_stock", "quantity": 10, "updated_minutes": 6, "delivery_fee": 0},
        {"pharmacy_id": "elite-lhr", "price": 1540, "stock": "in_stock", "quantity": 4, "updated_minutes": 30, "delivery_fee": 35},
    ],
    "atorvastatin-20-generic": [
        {"pharmacy_id": "city-health-khi", "price": 890, "stock": "in_stock", "quantity": 22, "updated_minutes": 4, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 920, "stock": "in_stock", "quantity": 17, "updated_minutes": 13, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 865, "stock": "in_stock", "quantity": 12, "updated_minutes": 7, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 845, "stock": "in_stock", "quantity": 15, "updated_minutes": 10, "delivery_fee": 0},
        {"pharmacy_id": "noor-drug-rwp", "price": 1095, "stock": "low_stock", "quantity": 2, "updated_minutes": 26, "delivery_fee": 15},
    ],
    "thyronorm-50": [
        {"pharmacy_id": "city-health-khi", "price": 690, "stock": "in_stock", "quantity": 16, "updated_minutes": 6, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 740, "stock": "in_stock", "quantity": 9, "updated_minutes": 15, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 710, "stock": "in_stock", "quantity": 7, "updated_minutes": 10, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 680, "stock": "in_stock", "quantity": 13, "updated_minutes": 5, "delivery_fee": 0},
        {"pharmacy_id": "elite-lhr", "price": 835, "stock": "in_stock", "quantity": 4, "updated_minutes": 20, "delivery_fee": 35},
    ],
    "levothyroxine-50-generic": [
        {"pharmacy_id": "city-health-khi", "price": 515, "stock": "in_stock", "quantity": 19, "updated_minutes": 2, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 560, "stock": "low_stock", "quantity": 3, "updated_minutes": 12, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 540, "stock": "in_stock", "quantity": 8, "updated_minutes": 9, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 500, "stock": "in_stock", "quantity": 11, "updated_minutes": 6, "delivery_fee": 0},
        {"pharmacy_id": "noor-drug-rwp", "price": 640, "stock": "in_stock", "quantity": 6, "updated_minutes": 18, "delivery_fee": 15},
    ],
    "augmentin-625": [
        {"pharmacy_id": "city-health-khi", "price": 1485, "stock": "in_stock", "quantity": 7, "updated_minutes": 13, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 1600, "stock": "low_stock", "quantity": 3, "updated_minutes": 24, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 1510, "stock": "in_stock", "quantity": 5, "updated_minutes": 8, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 1440, "stock": "in_stock", "quantity": 12, "updated_minutes": 7, "delivery_fee": 0},
        {"pharmacy_id": "noor-drug-rwp", "price": 1750, "stock": "out_of_stock", "quantity": 0, "updated_minutes": 32, "delivery_fee": 15},
    ],
    "co-amoxiclav-625-generic": [
        {"pharmacy_id": "city-health-khi", "price": 1120, "stock": "in_stock", "quantity": 15, "updated_minutes": 4, "delivery_fee": 30},
        {"pharmacy_id": "green-cross-khi", "price": 1180, "stock": "in_stock", "quantity": 9, "updated_minutes": 12, "delivery_fee": 20},
        {"pharmacy_id": "medico-lhr", "price": 1105, "stock": "in_stock", "quantity": 13, "updated_minutes": 10, "delivery_fee": 25},
        {"pharmacy_id": "sehat-point-isl", "price": 1090, "stock": "in_stock", "quantity": 14, "updated_minutes": 8, "delivery_fee": 0},
        {"pharmacy_id": "noor-drug-rwp", "price": 1265, "stock": "low_stock", "quantity": 2, "updated_minutes": 28, "delivery_fee": 15},
    ],
}


def get_pharmacy(pharmacy_id: str) -> dict:
    return deepcopy(_PHARMACY_BY_ID[pharmacy_id])


def get_medicine(medicine_id: str) -> dict:
    for medicine in MEDICINES:
        if medicine["id"] == medicine_id:
            return deepcopy(medicine)
    raise KeyError(medicine_id)


def search_medicines(query: str | None = None) -> list[dict]:
    if not query:
        return [deepcopy(item) for item in MEDICINES]

    normalized_query = " ".join(query.lower().replace(",", " ").split())
    terms = [term for term in normalized_query.split(" ") if term]
    scored: list[tuple[float, dict]] = []

    for medicine in MEDICINES:
        fields = [
            medicine["id"],
            medicine["name"],
            medicine["brand_name"],
            medicine["generic_name"],
            medicine["category"],
            medicine["summary"],
            " ".join(medicine["symptoms"]),
        ]
        haystack = " ".join(fields).lower()

        score = 0.0
        if normalized_query in haystack:
            score += 6.0

        for term in terms:
            if term in haystack:
                score += 1.5

        for field in fields:
            field_lower = field.lower()
            if normalized_query and normalized_query in field_lower:
                score += 2.5
            score = max(score, SequenceMatcher(None, normalized_query, field_lower).ratio() * 4.0)

        if score > 0:
            scored.append((score, deepcopy(medicine)))

    if scored:
        scored.sort(key=lambda item: (-item[0], item[1]["name"]))
        return [item[1] for item in scored]

    close_names = [
        medicine["name"].lower()
        for medicine in MEDICINES
    ]
    close_brands = [
        medicine["brand_name"].lower()
        for medicine in MEDICINES
    ]
    close_generics = [
        medicine["generic_name"].lower()
        for medicine in MEDICINES
    ]
    close_candidates = get_close_matches(normalized_query, close_names + close_brands + close_generics, n=5, cutoff=0.45)
    fallback: list[dict] = []
    for medicine in MEDICINES:
        candidate_blob = {
            medicine["name"].lower(),
            medicine["brand_name"].lower(),
            medicine["generic_name"].lower(),
        }
        if any(candidate in candidate_blob for candidate in close_candidates):
            fallback.append(deepcopy(medicine))
    if fallback:
        return fallback

    return []


def get_medicine_offers(medicine_id: str) -> list[dict]:
    offers = []
    for row in STOCK.get(medicine_id, []):
        pharmacy = _PHARMACY_BY_ID[row["pharmacy_id"]]
        offer = deepcopy(row)
        offer["pharmacy"] = deepcopy(pharmacy)
        offer["total_price"] = row["price"] + row["delivery_fee"]
        offer["price_difference_vs_avg"] = 0.0
        offers.append(offer)
    offers.sort(key=lambda item: (item["stock"] != "in_stock", item["total_price"], item["pharmacy"]["distance_km"]))
    return offers
