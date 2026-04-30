from __future__ import annotations

from math import atan2, cos, radians, sin, sqrt
from pathlib import Path
from statistics import mean
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import data
from .db import add_report, init_db, list_favorites, report_count, toggle_favorite


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="MediFind",
    version="1.0.0",
    description="A user-friendly FastAPI medicine finder and price comparison app.",
)

app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")


class ReportPayload(BaseModel):
    medicine_id: str | None = Field(default=None, min_length=3)
    pharmacy_id: str | None = None
    report_type: Literal["overpriced", "expired", "counterfeit", "wrong_info"] = "overpriced"
    note: str | None = Field(default="", max_length=500)


def _static_index():
    return STATIC_DIR / "index.html"


def _resolve_offers(medicine_id: str, city: str | None = None, verified: bool = False, delivery: bool = False) -> list[dict]:
    offers = data.get_medicine_offers(medicine_id)
    filtered = []
    for offer in offers:
        pharmacy = offer["pharmacy"]
        if city and pharmacy["city"].lower() != city.lower():
            continue
        if verified and not pharmacy["verified"]:
            continue
        if delivery and not pharmacy["delivery"]:
            continue
        filtered.append(offer)
    return filtered


def _distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius_km = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(radius_km * c, 2)


def _attach_distance(offer: dict, lat: float | None = None, lng: float | None = None) -> dict:
    if lat is None or lng is None:
        offer["distance_from_user_km"] = offer["pharmacy"]["distance_km"]
        return offer
    pharmacy = offer["pharmacy"]
    offer["distance_from_user_km"] = _distance_km(lat, lng, pharmacy["lat"], pharmacy["lng"])
    return offer


def _price_summary(
    medicine_id: str,
    city: str | None = None,
    verified: bool = False,
    delivery: bool = False,
    lat: float | None = None,
    lng: float | None = None,
) -> dict:
    offers = [_attach_distance(offer, lat=lat, lng=lng) for offer in _resolve_offers(medicine_id, city=city, verified=verified, delivery=delivery)]
    if lat is not None and lng is not None:
        offers.sort(key=lambda item: (item["distance_from_user_km"], item["total_price"]))
    priced_offers = [offer for offer in offers if offer["stock"] != "out_of_stock"]

    if not priced_offers:
        return {
            "offers": offers,
            "count": 0,
            "average_price": None,
            "cheapest_price": None,
            "cheapest_pharmacy": None,
            "savings": None,
            "overpriced_count": 0,
        }

    average_price = round(mean(offer["total_price"] for offer in priced_offers), 2)
    cheapest = min(priced_offers, key=lambda item: item["total_price"])
    overpriced_count = 0
    for offer in offers:
        if offer["stock"] == "out_of_stock":
            continue
        offer["price_difference_vs_avg"] = round(((offer["total_price"] - average_price) / average_price) * 100, 1) if average_price else 0.0
        offer["overpriced"] = offer["total_price"] > average_price * 1.25
        if offer["overpriced"]:
            overpriced_count += 1

    return {
        "offers": offers,
        "count": len(priced_offers),
        "average_price": average_price,
        "cheapest_price": cheapest["total_price"],
        "cheapest_pharmacy": cheapest["pharmacy"],
        "savings": round(average_price - cheapest["total_price"], 2),
        "overpriced_count": overpriced_count,
    }


def _medicine_card(
    medicine: dict,
    city: str | None = None,
    verified: bool = False,
    delivery: bool = False,
    favorites: set[str] | None = None,
    lat: float | None = None,
    lng: float | None = None,
) -> dict:
    summary = _price_summary(medicine["id"], city=city, verified=verified, delivery=delivery, lat=lat, lng=lng)
    offers = summary["offers"]
    favorites = favorites or set()

    in_stock = [offer for offer in offers if offer["stock"] != "out_of_stock"]
    available_count = len(in_stock)
    cheapest = min(in_stock, key=lambda item: item["total_price"]) if in_stock else None
    status = "Out of stock" if not available_count else "Available"
    if any(offer["stock"] == "low_stock" for offer in in_stock):
        status = "Limited stock"
    cheapest_total = cheapest["total_price"] if cheapest else None

    return {
        "id": medicine["id"],
        "name": medicine["name"],
        "brand_name": medicine["brand_name"],
        "generic_name": medicine["generic_name"],
        "category": medicine["category"],
        "summary": medicine["summary"],
        "availability_note": medicine["availability_note"],
        "is_generic": medicine["is_generic"],
        "status": status,
        "available_count": available_count,
        "cheapest_price": cheapest_total,
        "average_price": summary["average_price"],
        "savings": summary["savings"],
        "overpriced_count": summary["overpriced_count"],
        "favorite": medicine["id"] in favorites,
    }


def _detail_for_medicine(
    medicine_id: str,
    city: str | None = None,
    verified: bool = False,
    delivery: bool = False,
    lat: float | None = None,
    lng: float | None = None,
) -> dict:
    try:
        medicine = data.get_medicine(medicine_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Medicine not found") from exc

    favorites = list_favorites()
    summary = _price_summary(medicine_id, city=city, verified=verified, delivery=delivery, lat=lat, lng=lng)
    offers = summary["offers"]
    active_offers = [offer for offer in offers if offer["stock"] != "out_of_stock"]
    availability_score = 0 if not offers else round((len(active_offers) / len(offers)) * 100)

    alternatives = []
    for alt in medicine["alternatives"]:
        try:
            alt_medicine = data.get_medicine(alt["medicine_id"])
        except KeyError:
            continue
        alt_summary = _price_summary(alt_medicine["id"], city=city, verified=verified, delivery=delivery, lat=lat, lng=lng)
        if alt_summary["count"]:
            alternatives.append(
                {
                    "medicine_id": alt_medicine["id"],
                    "name": alt_medicine["name"],
                    "brand_name": alt_medicine["brand_name"],
                    "generic_name": alt_medicine["generic_name"],
                    "confidence": alt["confidence"],
                    "reason": alt["reason"],
                    "cheapest_price": alt_summary["cheapest_price"],
                    "savings": alt_summary["savings"],
                    "favorite": alt_medicine["id"] in favorites,
                }
            )

    price_chart = [
        {
            "pharmacy": offer["pharmacy"]["name"],
            "base_price": offer["price"],
            "delivery_fee": offer["delivery_fee"],
            "price": offer["total_price"],
            "stock": offer["stock"],
            "overpriced": offer.get("overpriced", False),
        }
        for offer in offers
    ]

    cheapest_offer = min(active_offers, key=lambda item: item["total_price"]) if active_offers else None

    return {
        "medicine": {
            **medicine,
            "favorite": medicine_id in favorites,
        },
        "summary": {
            "offer_count": summary["count"],
            "average_price": summary["average_price"],
            "cheapest_price": summary["cheapest_price"],
            "cheapest_savings": summary["savings"],
            "overpriced_count": summary["overpriced_count"],
            "availability_score": availability_score,
            "overpriced_rule": "Marked when total price is more than 25% above the average comparable total price.",
            "total_price_rule": "Total price = base medicine price + delivery fee.",
        },
        "cheapest_offer": cheapest_offer,
        "offers": offers,
        "alternatives": alternatives,
        "price_chart": price_chart,
    }


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root() -> FileResponse:
    return FileResponse(_static_index())


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/dashboard")
def dashboard(city: str | None = None, lat: float | None = None, lng: float | None = None) -> dict:
    favorites = list_favorites()
    medicines = data.MEDICINES
    pharmacy_list = data.PHARMACIES

    filtered_pharmacies = [p for p in pharmacy_list if not city or p["city"].lower() == city.lower()]
    verified_pharmacies = [p for p in filtered_pharmacies if p["verified"]]
    available = 0
    savings_values = []
    for medicine in medicines:
        summary = _price_summary(medicine["id"], city=city, lat=lat, lng=lng)
        if summary["count"]:
            available += 1
            if summary["savings"] is not None:
                savings_values.append(summary["savings"])

    top_savings = max(savings_values) if savings_values else 0
    average_savings = round(mean(savings_values), 2) if savings_values else 0

    medicine_cards = [_medicine_card(medicine, city=city, favorites=favorites, lat=lat, lng=lng) for medicine in medicines]
    best_card = min(
        [card for card in medicine_cards if card["cheapest_price"] is not None],
        key=lambda item: item["cheapest_price"],
        default=None,
    )
    best_value_detail = _detail_for_medicine(best_card["id"], city=city, lat=lat, lng=lng) if best_card else None

    return {
        "total_medicines": len(medicines),
        "available_medicines": available,
        "verified_pharmacies": len(verified_pharmacies),
        "total_pharmacies": len(filtered_pharmacies),
        "favorites": len(favorites),
        "reports": report_count(),
        "average_savings": average_savings,
        "top_savings": top_savings,
        "best_value": best_card,
        "best_value_detail": best_value_detail,
        "cities": sorted({pharmacy["city"] for pharmacy in pharmacy_list}),
    }


@app.get("/api/medicines")
def list_medicines(
    q: str | None = Query(default=None, description="Search query"),
    city: str | None = None,
    verified: bool = False,
    delivery: bool = False,
    lat: float | None = None,
    lng: float | None = None,
) -> dict:
    favorites = list_favorites()
    matches = data.search_medicines(q)
    if city or verified or delivery:
        filtered_matches = []
        for medicine in matches:
            summary = _price_summary(medicine["id"], city=city, verified=verified, delivery=delivery, lat=lat, lng=lng)
            if summary["count"]:
                filtered_matches.append(medicine)
        matches = filtered_matches

    cards = [
        _medicine_card(medicine, city=city, verified=verified, delivery=delivery, favorites=favorites, lat=lat, lng=lng)
        for medicine in matches
    ]
    cards.sort(
        key=lambda item: (
            item["cheapest_price"] is None,
            item["cheapest_price"] if item["cheapest_price"] is not None else 0,
            item["name"],
        )
    )
    return {"items": cards, "count": len(cards)}


@app.get("/api/medicines/{medicine_id}")
def medicine_detail(
    medicine_id: str,
    city: str | None = None,
    verified: bool = False,
    delivery: bool = False,
    lat: float | None = None,
    lng: float | None = None,
) -> dict:
    return _detail_for_medicine(medicine_id, city=city, verified=verified, delivery=delivery, lat=lat, lng=lng)


@app.get("/api/pharmacies")
def list_pharmacies(
    medicine_id: str | None = None,
    city: str | None = None,
    verified: bool = False,
    delivery: bool = False,
    lat: float | None = None,
    lng: float | None = None,
) -> dict:
    pharmacies = data.PHARMACIES
    if city:
        pharmacies = [pharmacy for pharmacy in pharmacies if pharmacy["city"].lower() == city.lower()]
    if verified:
        pharmacies = [pharmacy for pharmacy in pharmacies if pharmacy["verified"]]
    if delivery:
        pharmacies = [pharmacy for pharmacy in pharmacies if pharmacy["delivery"]]

    if medicine_id:
        offers = _resolve_offers(medicine_id, city=city, verified=verified, delivery=delivery)
        offers = [_attach_distance(offer, lat=lat, lng=lng) for offer in offers]
        if lat is not None and lng is not None:
            offers.sort(key=lambda item: (item["distance_from_user_km"], item["total_price"]))
        offer_map = {offer["pharmacy"]["id"]: offer for offer in offers}
        pharmacies = [{**pharmacy, "offer": offer_map.get(pharmacy["id"])} for pharmacy in pharmacies if pharmacy["id"] in offer_map]

    return {"items": pharmacies, "count": len(pharmacies)}


@app.post("/api/favorites/{medicine_id}")
def favorite_medicine(medicine_id: str) -> dict:
    try:
        data.get_medicine(medicine_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Medicine not found") from exc
    return toggle_favorite(medicine_id)


@app.get("/api/favorites/{medicine_id}")
def favorite_status(medicine_id: str) -> dict:
    try:
        data.get_medicine(medicine_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Medicine not found") from exc
    favorites = list_favorites()
    return {
        "medicine_id": medicine_id,
        "favorited": medicine_id in favorites,
        "message": "Use POST on this same path to toggle the favorite state.",
    }


@app.get("/api/favorites")
def favorites() -> dict:
    favorite_ids = list(list_favorites())
    cards = []
    for medicine_id in favorite_ids:
        try:
            cards.append(_detail_for_medicine(medicine_id))
        except HTTPException:
            continue
    return {"items": cards, "count": len(cards)}


@app.post("/api/reports")
def create_report(payload: ReportPayload) -> dict:
    if not payload.medicine_id:
        raise HTTPException(status_code=400, detail="Select a medicine before submitting a report.")
    try:
        data.get_medicine(payload.medicine_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Medicine not found") from exc
    report = add_report(payload.medicine_id, payload.pharmacy_id, payload.report_type, payload.note)
    return {"ok": True, "report": report}


@app.get("/api/suggestions")
def suggestions(q: str | None = None) -> dict:
    matches = data.search_medicines(q)
    results = []
    for medicine in matches[:6]:
        results.append(
            {
                "id": medicine["id"],
                "name": medicine["name"],
                "category": medicine["category"],
                "generic_name": medicine["generic_name"],
            }
        )
    return {"items": results, "count": len(results)}
