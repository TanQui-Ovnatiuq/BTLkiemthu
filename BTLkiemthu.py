from __future__ import annotations

import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import perf_counter


TEST_CASE_TABLE = """# Module | Action | Expected Result | Actual Result | Status | Type
1 Air | Confirm booking (>= 7 days) | Booking confirmed | confirmed | PASS | Functional
2 Air | Find airline Delta | Airline data returned | available=True | PASS | Functional
3 Hotel | Search hotels in Los Angeles | Matching hotels returned | 1 result | PASS | Functional
4 Hotel | Book room (Pacific Lodge, 2 nights) | Booking created | booked | PASS | Functional
5 Search&Plan | Personalized suggestion (low+relax) | Suggestions returned | 2 suggestions | PASS | Functional
6 Air | Xác nhận booking tạo trong vòng 7 ngày | Booking confirmed | LookupError (alpha defect) | FAIL | Integration
7 Air | Lấy dữ liệu hãng từ đối tác cụ thể | Trả dữ liệu đầy đủ | Một số hãng trả rỗng (alpha defect) | FAIL | Integration
8 Air | Search flight by location (Remote Island) | Flights returned | TimeoutError (alpha defect) | FAIL | Integration
9 Air | Check flight time = 30 mins | 30 | 30 | PASS | Boundary
10 Hotel | Check price (Desert View, 1 night) | 150 | 150 | PASS | Boundary
11 Air | Search flight performance | < 50ms | < 50ms | PASS | Performance
12 Search&Plan | Optimize itinerary performance | < 50ms | < 50ms | PASS | Performance
"""


def print_test_case_table() -> None:
    print("=== SMART TRAVEL / EXPLORE CALIFORNIA - TEST CASES (SUMMARY) ===")
    print(TEST_CASE_TABLE)


@dataclass
class Booking:
    booking_id: str
    customer_name: str
    travel_date: datetime
    status: str = "pending"


class AirService:
    """Simulated airline integration for Smart Travel (alpha defects injected)."""

    def __init__(self) -> None:
        self.known_airlines = {"Delta", "United", "American Airlines", "JetBlue"}
        self.unavailable_airlines = {"Ghost Air", "Missing Data Air"}
        self.reminders: list[str] = []

    # 1. Xác nhận booking
    def confirm_booking(self, booking: Booking) -> dict:
        # Alpha defect: cannot retrieve bookings created within last 7 days
        if booking.travel_date - datetime.now() < timedelta(days=7):
            raise LookupError("Cannot retrieve bookings created within the last 7 days")
        booking.status = "confirmed"
        return {"booking_id": booking.booking_id, "status": booking.status}

    # 2. Tìm hãng hàng không
    def find_airline(self, airline_name: str) -> dict | None:
        # Alpha defect: some airlines return no data
        if airline_name in self.unavailable_airlines:
            return None
        if airline_name in self.known_airlines:
            return {"airline_name": airline_name, "available": True}
        return {"airline_name": airline_name, "available": False}

    # 3. Tìm chuyến theo địa điểm
    def search_flights_by_location(self, origin: str, destination: str) -> list[dict]:
        # Alpha defect: location-based search can timeout
        if any(keyword in destination.lower() for keyword in {"timeout", "remote island", "off-grid"}):
            raise TimeoutError("Flight search timed out for the selected location")
        return [
            {"flight_no": "AC101", "origin": origin, "destination": destination, "duration_min": 180},
            {"flight_no": "AC202", "origin": origin, "destination": destination, "duration_min": 240},
        ]

    # 4. Kiểm tra thời gian bay
    def check_flight_time(self, departure: datetime, arrival: datetime) -> int:
        if arrival <= departure:
            raise ValueError("Arrival must be later than departure")
        return int((arrival - departure).total_seconds() // 60)

    # 5. Gửi nhắc check-in
    def send_checkin_reminder(self, booking: Booking) -> str:
        reminder = f"Check-in reminder sent for {booking.booking_id}"
        self.reminders.append(reminder)
        return reminder


class HotelService:
    """Simulated hotel integration."""

    def __init__(self) -> None:
        self.hotels = {
            "Sunset Inn": {"city": "Los Angeles", "price": 180, "rating": 4.3},
            "Pacific Lodge": {"city": "San Diego", "price": 220, "rating": 4.6},
            "Desert View": {"city": "Palm Springs", "price": 150, "rating": 4.1},
        }
        self.active_bookings: dict[str, dict] = {}

    # 1. Tìm khách sạn
    def search_hotel(self, city: str, max_price: int | None = None) -> list[dict]:
        results = []
        for hotel_name, details in self.hotels.items():
            if details["city"].lower() != city.lower():
                continue
            if max_price is not None and details["price"] > max_price:
                continue
            results.append({"hotel_name": hotel_name, **details})
        return results

    # 2. Đặt phòng
    def book_room(self, hotel_name: str, guest_name: str, nights: int) -> dict:
        if nights <= 0:
            raise ValueError("Nights must be greater than zero")
        if hotel_name not in self.hotels:
            raise KeyError("Hotel not found")
        booking_id = f"HT-{len(self.active_bookings) + 1:04d}"
        booking = {
            "booking_id": booking_id,
            "hotel_name": hotel_name,
            "guest_name": guest_name,
            "nights": nights,
            "status": "booked",
        }
        self.active_bookings[booking_id] = booking
        return booking

    # 3. Hủy phòng
    def cancel_room(self, booking_id: str) -> bool:
        if booking_id not in self.active_bookings:
            return False
        self.active_bookings[booking_id]["status"] = "cancelled"
        return True

    # 4. Kiểm tra giá
    def check_price(self, hotel_name: str, nights: int) -> int:
        if nights <= 0:
            raise ValueError("Nights must be greater than zero")
        if hotel_name not in self.hotels:
            raise KeyError("Hotel not found")
        return self.hotels[hotel_name]["price"] * nights

    # 5. Đánh giá khách sạn
    def rate_hotel(self, hotel_name: str, score: float) -> dict:
        if hotel_name not in self.hotels:
            raise KeyError("Hotel not found")
        if score < 0 or score > 5:
            raise ValueError("Score must be between 0 and 5")
        self.hotels[hotel_name]["rating"] = score
        return {"hotel_name": hotel_name, "rating": score}


class SearchPlanService:
    """Simulated global search and planning."""

    def __init__(self) -> None:
        self.saved_plans: list[dict] = []

    # 1. Tìm kiếm toàn hệ thống
    def search_all(self, keyword: str) -> dict:
        return {
            "flights": [f"{keyword} flight option"],
            "hotels": [f"{keyword} hotel option"],
            "restaurants": [f"{keyword} restaurant option"],
        }

    # 2. Lọc kết quả
    def filter_results(self, results: list[dict], min_rating: float = 0.0) -> list[dict]:
        return [item for item in results if item.get("rating", 0) >= min_rating]

    # 3. Gợi ý cá nhân hóa
    def personalized_suggestion(self, preferences: dict) -> list[str]:
        suggestions = []
        if preferences.get("budget") == "low":
            suggestions.append("Choose budget-friendly hotels")
        if preferences.get("travel_style") == "relax":
            suggestions.append("Add more leisure time")
        if not suggestions:
            suggestions.append("Explore California coastal route")
        return suggestions

    # 4. Lưu kế hoạch
    def save_plan(self, plan_name: str, items: list[str]) -> dict:
        plan = {"plan_name": plan_name, "items": items, "saved_at": datetime.now().isoformat()}
        self.saved_plans.append(plan)
        return plan

    # 5. Tối ưu lịch trình
    def optimize_schedule(self, itinerary: list[dict]) -> list[dict]:
        return sorted(itinerary, key=lambda item: item.get("priority", 0), reverse=True)


def performance_guard(action, limit_ms: float = 50.0) -> tuple[bool, float]:
    started = perf_counter()
    action()
    elapsed_ms = (perf_counter() - started) * 1000
    return elapsed_ms < limit_ms, elapsed_ms


class TestAirService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = AirService()

    # Functional
    def test_confirm_booking_functional(self) -> None:
        booking = Booking("BK-001", "Linh", datetime.now() + timedelta(days=10))
        result = self.service.confirm_booking(booking)
        self.assertEqual(result["status"], "confirmed")
        self.assertEqual(booking.status, "confirmed")

    def test_find_airline_functional(self) -> None:
        airline = self.service.find_airline("Delta")
        self.assertIsNotNone(airline)
        self.assertTrue(airline["available"])

    def test_send_checkin_reminder_functional(self) -> None:
        booking = Booking("BK-003", "An", datetime.now() + timedelta(days=12))
        reminder = self.service.send_checkin_reminder(booking)
        self.assertIn("BK-003", reminder)
        self.assertEqual(len(self.service.reminders), 1)

    # Negative (alpha defects shown as expected failures)
    @unittest.expectedFailure
    def test_confirm_recent_booking_negative(self) -> None:
        booking = Booking("BK-002", "Minh", datetime.now() + timedelta(days=3))
        result = self.service.confirm_booking(booking)
        self.assertEqual(result["status"], "confirmed")

    @unittest.expectedFailure
    def test_find_airline_missing_data_negative(self) -> None:
        airline = self.service.find_airline("Ghost Air")
        self.assertIsNotNone(airline)
        self.assertTrue(airline["available"])

    @unittest.expectedFailure
    def test_search_flights_by_location_timeout_negative(self) -> None:
        flights = self.service.search_flights_by_location("San Francisco", "Remote Island")
        self.assertGreater(len(flights), 0)

    # Boundary
    def test_check_flight_time_boundary(self) -> None:
        departure = datetime(2026, 5, 7, 8, 0)
        arrival = datetime(2026, 5, 7, 8, 30)
        self.assertEqual(self.service.check_flight_time(departure, arrival), 30)

    # Performance (<50ms)
    def test_search_flights_performance(self) -> None:
        ok, elapsed_ms = performance_guard(
            lambda: self.service.search_flights_by_location("San Francisco", "Los Angeles")
        )
        self.assertTrue(ok, f"Air search exceeded 50ms: {elapsed_ms:.2f}ms")


class TestHotelService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = HotelService()

    # Functional
    def test_search_hotel_functional(self) -> None:
        results = self.service.search_hotel("Los Angeles")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["hotel_name"], "Sunset Inn")

    def test_book_room_functional(self) -> None:
        booking = self.service.book_room("Pacific Lodge", "Trang", 2)
        self.assertEqual(booking["status"], "booked")
        self.assertIn(booking["booking_id"], self.service.active_bookings)

    def test_rate_hotel_functional(self) -> None:
        rated = self.service.rate_hotel("Sunset Inn", 4.8)
        self.assertEqual(rated["rating"], 4.8)

    # Negative
    def test_cancel_room_negative(self) -> None:
        cancelled = self.service.cancel_room("HT-9999")
        self.assertFalse(cancelled)

    # Boundary
    def test_check_price_boundary(self) -> None:
        self.assertEqual(self.service.check_price("Desert View", 1), 150)

    # Performance (<50ms)
    def test_hotel_search_performance(self) -> None:
        ok, elapsed_ms = performance_guard(lambda: self.service.search_hotel("San Diego"))
        self.assertTrue(ok, f"Hotel search exceeded 50ms: {elapsed_ms:.2f}ms")


class TestSearchPlanService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SearchPlanService()

    # Functional
    def test_search_all_functional(self) -> None:
        results = self.service.search_all("California")
        self.assertIn("flights", results)
        self.assertIn("hotels", results)
        self.assertIn("restaurants", results)

    def test_personalized_suggestion_functional(self) -> None:
        suggestions = self.service.personalized_suggestion({"budget": "low", "travel_style": "relax"})
        self.assertGreaterEqual(len(suggestions), 2)

    def test_optimize_schedule_functional(self) -> None:
        itinerary = [
            {"name": "Lunch", "priority": 2},
            {"name": "Beach", "priority": 5},
            {"name": "Hotel Check-in", "priority": 3},
        ]
        optimized = self.service.optimize_schedule(itinerary)
        self.assertEqual(optimized[0]["name"], "Beach")

    # Negative
    def test_filter_results_negative(self) -> None:
        results = self.service.filter_results(
            [
                {"name": "A", "rating": 2.5},
                {"name": "B", "rating": 4.5},
            ],
            min_rating=4.0,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "B")

    # Boundary
    def test_save_plan_boundary(self) -> None:
        plan = self.service.save_plan("Weekend Trip", [])
        self.assertEqual(plan["plan_name"], "Weekend Trip")
        self.assertEqual(len(self.service.saved_plans), 1)

    # Performance (<50ms)
    def test_plan_optimizer_performance(self) -> None:
        ok, elapsed_ms = performance_guard(
            lambda: self.service.optimize_schedule(
                [
                    {"name": "A", "priority": 1},
                    {"name": "B", "priority": 3},
                    {"name": "C", "priority": 2},
                ]
            )
        )
        self.assertTrue(ok, f"Plan optimization exceeded 50ms: {elapsed_ms:.2f}ms")


if __name__ == "__main__":
    print_test_case_table()
    unittest.main(verbosity=2)
