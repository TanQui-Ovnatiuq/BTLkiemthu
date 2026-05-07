from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass
class Flight:
    flight_id: str
    airline: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime


class AirService:
    def __init__(self) -> None:
        self.bookings = {
            "A001": {"user": "Lan", "created_at": datetime.now() - timedelta(days=3)},
            "A002": {"user": "Minh", "created_at": datetime.now() - timedelta(days=10)},
        }
        self.airlines = ["Vietnam Airlines", "VietJet Air", "Bamboo Airways", "Pacific Airlines"]
        now = datetime.now()
        self.flights = [
            Flight("VN101", "Vietnam Airlines", "SGN", "HAN", now + timedelta(hours=3), now + timedelta(hours=5)),
            Flight("VJ220", "VietJet Air", "DAD", "HAN", now + timedelta(hours=4), now + timedelta(hours=5, minutes=30)),
            Flight("QH500", "Bamboo Airways", "SGN", "DAD", now + timedelta(hours=6), now + timedelta(hours=7, minutes=20)),
        ]

    def confirm_booking(self, booking_id: str) -> bool:
        if not booking_id:
            raise ValueError("booking_id is required")
        return booking_id in self.bookings

    def find_airline(self, query: str) -> list[str]:
        if query is None:
            raise ValueError("query cannot be None")
        query = query.strip().lower()
        if not query:
            return self.airlines
        return [airline for airline in self.airlines if query in airline.lower()]

    def find_flights_by_location(self, origin: str, destination: str) -> list[Flight]:
        if not origin or not destination:
            raise ValueError("origin and destination are required")
        return [
            flight
            for flight in self.flights
            if flight.origin.lower() == origin.lower() and flight.destination.lower() == destination.lower()
        ]

    def check_flight_time(self, departure: datetime, arrival: datetime) -> float:
        if arrival <= departure:
            raise ValueError("arrival must be after departure")
        duration_hours = (arrival - departure).total_seconds() / 3600
        return round(duration_hours, 2)

    def send_checkin_reminder(self, booking_id: str, hours_before: int = 24) -> str:
        if booking_id not in self.bookings:
            raise KeyError("booking not found")
        if hours_before < 0 or hours_before > 48:
            raise ValueError("hours_before must be in range 0..48")
        return f"Reminder sent for {booking_id} before {hours_before}h"


class HotelService:
    def __init__(self) -> None:
        self.hotels = [
            {"id": "H001", "name": "Sunrise Hotel", "location": "Da Nang", "stars": 4, "price_per_night": 900000},
            {"id": "H002", "name": "Ocean View", "location": "Da Nang", "stars": 5, "price_per_night": 1800000},
            {"id": "H003", "name": "City Inn", "location": "Ha Noi", "stars": 3, "price_per_night": 700000},
        ]
        self.room_bookings: dict[str, dict[str, Any]] = {}
        self.reviews: dict[str, list[dict[str, Any]]] = {}

    def search_hotels(self, location: str, min_stars: int = 1) -> list[dict[str, Any]]:
        if not location:
            raise ValueError("location is required")
        return [
            h
            for h in self.hotels
            if h["location"].lower() == location.lower() and h["stars"] >= min_stars
        ]

    def book_room(self, hotel_id: str, user_name: str, nights: int) -> str:
        if nights <= 0:
            raise ValueError("nights must be > 0")
        if not any(h["id"] == hotel_id for h in self.hotels):
            raise KeyError("hotel not found")
        booking_id = f"B{len(self.room_bookings) + 1:03d}"
        self.room_bookings[booking_id] = {
            "hotel_id": hotel_id,
            "user_name": user_name,
            "nights": nights,
            "status": "booked",
        }
        return booking_id

    def cancel_room(self, booking_id: str) -> bool:
        booking = self.room_bookings.get(booking_id)
        if not booking:
            return False
        booking["status"] = "cancelled"
        return True

    def check_price(self, hotel_id: str, nights: int) -> int:
        if nights <= 0:
            raise ValueError("nights must be > 0")
        for hotel in self.hotels:
            if hotel["id"] == hotel_id:
                return hotel["price_per_night"] * nights
        raise KeyError("hotel not found")

    def review_hotel(self, hotel_id: str, rating: int, comment: str) -> bool:
        if rating < 1 or rating > 5:
            raise ValueError("rating must be 1..5")
        if not any(h["id"] == hotel_id for h in self.hotels):
            raise KeyError("hotel not found")
        self.reviews.setdefault(hotel_id, []).append({"rating": rating, "comment": comment})
        return True


class SearchPlanService:
    def __init__(self) -> None:
        self.saved_plans: dict[str, list[dict[str, Any]]] = {}

    def system_search(self, keyword: str) -> list[dict[str, Any]]:
        if not keyword or not keyword.strip():
            raise ValueError("keyword is required")
        keyword = keyword.lower()
        data = [
            {"category": "flight", "name": "Vietnam Airlines SGN-HAN", "price": 1500000, "rating": 4.5},
            {"category": "hotel", "name": "Ocean View Da Nang", "price": 1800000, "rating": 4.8},
            {"category": "restaurant", "name": "Pho 24", "price": 80000, "rating": 4.2},
        ]
        return [item for item in data if keyword in item["name"].lower()]

    def filter_results(
        self,
        results: list[dict[str, Any]],
        category: str | None = None,
        max_price: int | None = None,
        min_rating: float | None = None,
    ) -> list[dict[str, Any]]:
        filtered = results
        if category:
            filtered = [r for r in filtered if r.get("category") == category]
        if max_price is not None:
            filtered = [r for r in filtered if r.get("price", 0) <= max_price]
        if min_rating is not None:
            filtered = [r for r in filtered if r.get("rating", 0) >= min_rating]
        return filtered

    def personalized_suggestions(self, user_profile: dict[str, Any]) -> list[str]:
        if "preferences" not in user_profile:
            raise ValueError("preferences are required")
        prefs = user_profile["preferences"]
        suggestions = []
        if "beach" in prefs:
            suggestions.append("Go to Da Nang")
        if "culture" in prefs:
            suggestions.append("Visit Hoi An Old Town")
        if "food" in prefs:
            suggestions.append("Try local street food tour")
        return suggestions

    def save_plan(self, user_id: str, plan: list[dict[str, Any]]) -> bool:
        if not user_id:
            raise ValueError("user_id is required")
        self.saved_plans[user_id] = plan
        return True

    def optimize_itinerary(self, plan_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not plan_items:
            return []
        unique = {(item["day"], item["time"], item["activity"]): item for item in plan_items}
        return sorted(unique.values(), key=lambda x: (x["day"], x["time"]))
