import time
import unittest
from datetime import datetime, timedelta

from src.services import AirService, HotelService, SearchPlanService


class TestAirService(unittest.TestCase):
    def setUp(self) -> None:
        self.air = AirService()

    def test_confirm_booking_functional(self):
        self.assertTrue(self.air.confirm_booking("A001"))

    def test_find_airline_negative_none_query(self):
        with self.assertRaises(ValueError):
            self.air.find_airline(None)

    def test_send_checkin_reminder_boundary_zero_hours(self):
        result = self.air.send_checkin_reminder("A001", hours_before=0)
        self.assertIn("Reminder sent", result)

    def test_check_flight_time_negative_invalid_order(self):
        now = datetime.now()
        with self.assertRaises(ValueError):
            self.air.check_flight_time(now, now - timedelta(hours=1))

    def test_find_flights_performance_under_50ms(self):
        start = time.perf_counter()
        self.air.find_flights_by_location("SGN", "HAN")
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.05)


class TestHotelService(unittest.TestCase):
    def setUp(self) -> None:
        self.hotel = HotelService()

    def test_search_hotels_functional(self):
        results = self.hotel.search_hotels("Da Nang", min_stars=4)
        self.assertGreaterEqual(len(results), 1)

    def test_book_room_negative_nights(self):
        with self.assertRaises(ValueError):
            self.hotel.book_room("H001", "An", 0)

    def test_check_price_boundary_one_night(self):
        price = self.hotel.check_price("H001", 1)
        self.assertEqual(price, 900000)

    def test_cancel_room_functional(self):
        booking_id = self.hotel.book_room("H001", "Bao", 2)
        self.assertTrue(self.hotel.cancel_room(booking_id))

    def test_search_hotels_performance_under_50ms(self):
        start = time.perf_counter()
        self.hotel.search_hotels("Da Nang")
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.05)


class TestSearchPlanService(unittest.TestCase):
    def setUp(self) -> None:
        self.search = SearchPlanService()

    def test_system_search_functional(self):
        results = self.search.system_search("Da Nang")
        self.assertGreaterEqual(len(results), 1)

    def test_system_search_negative_empty_keyword(self):
        with self.assertRaises(ValueError):
            self.search.system_search("   ")

    def test_filter_results_boundary_exact_price(self):
        data = [
            {"category": "hotel", "price": 100, "rating": 4.0},
            {"category": "hotel", "price": 101, "rating": 4.0},
        ]
        filtered = self.search.filter_results(data, max_price=100)
        self.assertEqual(len(filtered), 1)

    def test_personalized_suggestions_negative_missing_preferences(self):
        with self.assertRaises(ValueError):
            self.search.personalized_suggestions({"name": "Lan"})

    def test_system_search_performance_under_50ms(self):
        start = time.perf_counter()
        self.search.system_search("Vietnam")
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.05)

    def test_optimize_itinerary_negative_missing_required_key(self):
        invalid_plan = [{"day": 1, "time": "08:00"}]
        with self.assertRaises(ValueError):
            self.search.optimize_itinerary(invalid_plan)


if __name__ == "__main__":
    unittest.main()
