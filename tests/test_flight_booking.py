import sys
import os
import datetime
import pytest
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError
import json
from utils.logger import setup_logger

logger = setup_logger()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.home_page import HomePage
from pages.flights_page import FlightsPage
from pages.search_results_page import SearchResultsPage

os.makedirs("screenshots", exist_ok=True)


def take_screenshot(page, name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/{name}_{timestamp}.png"
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"📸 Screenshot saved: {screenshot_path}")
    return screenshot_path


@pytest.mark.parametrize(
    "dataset",
    [
        pytest.param(data, id=f"{data['From']}_to_{data['To']}_{data['DepartureDateAria']}")
        for data in json.load(open(os.path.join(os.path.dirname(__file__), "test_data.json")))
    ]
)
def test_flight_booking(dataset):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # print(f"🚩 Running test: {dataset['From']} to {dataset['To']} on {dataset['DepartureDateAria']}")
            logger.info(f"Visiting Goibibo...")
            page.goto("https://www.goibibo.com", timeout=60000)
            take_screenshot(page, "homepage_loaded")

            home = HomePage(page)
            home.close_login_popup()
            logger.info("Closed login popup")
            take_screenshot(page, "after_login_popup")

            flights = FlightsPage(page)
            flights.goto_flights()
            flights.dismiss_mini_popup()
            logger.info("Flights tab opened and mini popup dismissed")
            take_screenshot(page, "flights_page")

            flights.enter_from(dataset["From"], dataset["FromSuggestion"])
            flights.enter_to(dataset["To"], dataset["ToSuggestion"])
            take_screenshot(page, "after_route_selection")

            flights.open_departure_picker()
            flights.select_departure_date(dataset["DepartureMonthYear"], dataset["DepartureDateAria"])
            take_screenshot(page, "after_date_selection")

            flights.open_travellers_class_dropdown()
            flights.select_travellers_and_class(adults=dataset["Adults"], travel_class=dataset["TravelClass"])
            take_screenshot(page, "after_travelers_selection")

            with page.expect_navigation(timeout=30000):
                flights.search_flights()
            take_screenshot(page, "after_search_click")

            results = SearchResultsPage(page)

            # Always close popups before doing anything!
            results.close_all_popups()
            results.close_lock_price_popup()
            results.close_coachmark()

            # Wait for results URL or fallback
            try:
                page.wait_for_url("**/flights/**", timeout=20000)
            except TimeoutError:
                page.wait_for_selector(".listingCard", timeout=20000)

            take_screenshot(page, "results_page_loaded")

            # 🔑 Apply fare type, stop filter, slider:
            if dataset["FareType"].lower() == "student":
                results.select_student_fare()
                take_screenshot(page, "after_student_fare")

            if dataset["Stops"].lower() == "non stop":
                results.apply_non_stop_filter()
                take_screenshot(page, "after_non_stop_filter")

            # Make sure popups do not overlap
            results.close_all_popups()
            results.adjust_price_slider()
            take_screenshot(page, "after_price_slider")

            # ✅ This assumes you have a button to click to re-search, or comment this if not needed
            # results.click_search_button()
            # take_screenshot(page, "after_results_search")

            # page.wait_for_timeout(5000)
            results.close_coachmark()

            results.wait_for_flights_to_load()
            take_screenshot(page, "final_results_loaded")

            flights_data = results.extract_flight_data(dataset["From"], dataset["To"])

            # assert len(flights_data) > 0, "❌ No flights found!"
            # ✅ Save as CSV with From-To in filename
            filename = f"{dataset['From']}_to_{dataset['To']}.csv".replace(" ", "_")
            df = pd.DataFrame(flights_data)
            df.to_csv(filename, index=False)
            print(f"✅ Saved flights to {filename}")

            # filename = f"flight_results_{dataset['From']}_to_{dataset['To']}.xlsx".replace(" ", "_")
            # results.save_to_excel(flights_data, filename=filename)

        except TimeoutError as e:
            logger.error(f"⏰ Timeout occurred: {e}")
            take_screenshot(page, "timeout_error")
            # print(f"⏰ Timeout occurred: {e}")
            raise
        except AssertionError as e:
            logger.error(f"❌ Assertion failed: {e}")
            take_screenshot(page, "assertion_failure")
            # print(f"❌ Assertion failed: {e}")
            raise
        except Exception as e:
            logger.exception(f"❗ Unexpected error: {e}")
            take_screenshot(page, "unexpected_error")
            # print(f"❗ Unexpected error: {e}")
            raise
        finally:
            browser.close()
            logger.info("🛑 Browser closed.")
            # print("🛑 Browser closed.")