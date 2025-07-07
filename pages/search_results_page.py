from playwright.sync_api import TimeoutError as PlaywrightTimeout
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SearchResultsPage:
    def __init__(self, page):
        self.page = page

    def close_all_popups(self):
        logger.info("Attempting to close all known popups...")
        # print("ℹ️ Attempting to close all known popups...")

        try:
            self.page.locator("span.bgProperties.overlayCrossIcon").click(timeout=2000)
            logger.info("✅ Closed overlayCrossIcon popup")
            # print("✅ Closed overlayCrossIcon popup")
        except PlaywrightTimeout:
            print("ℹ️ No overlayCrossIcon popup found")

        try:
            self.page.locator("button:has-text('OK')").click(timeout=2000)
            print("✅ Closed OK button popup")
        except PlaywrightTimeout:
            logger.info("ℹ️ No overlayCrossIcon popup found")
            # print("ℹ️ No OK button popup found")

        try:
            self.page.locator("div.lockPricePopup span").click(timeout=2000)
            logger.info("✅ Closed Lock Price popup")
            # print("✅ Closed Lock Price popup")
        except PlaywrightTimeout:
            logger.info("ℹ️ No Lock Price popup found")
            # print("ℹ️ No Lock Price popup found")

    def close_lock_price_popup(self):
        logger.info("Closing lock price popup")
        self.close_all_popups()

    def close_coachmark(self):
        try:
            self.page.locator("span:has-text('Got It')").click(timeout=2000)
            logger.info("✅ Closed coachmark")
            # print("✅ Closed coachmark")
        except PlaywrightTimeout:
            logger.info("ℹ️ No coachmark found")
            # print("ℹ️ No coachmark found")

    def select_student_fare(self):
        try:
            self.page.locator("li:has(span.appendLeft7:has-text('Student'))").click(timeout=5000)
            logger.info("✅ Student fare selected")
            # print("✅ Student fare selected")
        except PlaywrightTimeout:
            logger.warning("❌ Student fare option not found")
            # print("❌ Student fare option not found")

    def apply_non_stop_filter(self):
        try:
            non_stop_checkbox=self.page.locator("label:has(p:has-text('Non Stop')) input[type='checkbox']").first
            non_stop_checkbox.check(timeout=5000)
            logger.info("✅ Non Stop filter applied")
            # print("✅ Non Stop filter applied")
        except PlaywrightTimeout:
            logger.warning("❌ Non Stop filter not found")
            # print("❌ Non Stop filter not found")

    def adjust_price_slider(self):
        logger.info("Adjusting One Way Price slider...")
        # print("✅ Adjusting One Way Price slider...")
        self.page.wait_for_timeout(1000)  # Let the page settle

        slider = self.page.locator("div.filtersOuter:has(p:has-text('One Way Price')) .rangeslider__handle").first
        slider.wait_for(state="visible", timeout=5000)

        slider.scroll_into_view_if_needed()
        slider.hover()
        box = slider.bounding_box()
        logger.debug(f"ℹ️ Slider box: {box}")
        # print(f"ℹ️ Slider box: {box}")

        if box:
            self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            self.page.mouse.down()
            self.page.mouse.move(
                box["x"] + box["width"] / 2 + 80,
                box["y"] + box["height"] / 2,
                steps=10
            )
            self.page.mouse.up()
            # print("✅ Price slider adjusted successfully")
            logger.info("✅ Price slider adjusted successfully")
        else:
            logger.error("❌ Could not locate slider bounding box")
            # print("❌ Could not locate slider bounding box")


    def click_search_button(self):
        try:
            self.page.locator("//span[text()='SEARCH FLIGHTS']").click(timeout=5000)
            logger.info("✅ Clicked SEARCH FLIGHTS button again.")
            # print("✅ Clicked SEARCH FLIGHTS button again.")
        except PlaywrightTimeout:
            logger.info("ℹ️ SEARCH FLIGHTS button not found or not needed.")
            # print("ℹ️ SEARCH FLIGHTS button not found or not needed.")

    def wait_for_flights_to_load(self):
        try:
            self.page.wait_for_selector(".listingCard", timeout=10000)
            logger.info("✅ Flights loaded successfully.")
            # print("✅ Flights loaded successfully.")
        except PlaywrightTimeout:
            logger.error("❌ Flights did not load in time.")
            # print("❌ Flights did not load in time.")

    def extract_flight_data(self,from_city, to_city):
        logger.info(f"🔍 Extracting flight data for {from_city} → {to_city}...")
        # print("🔍 Extracting flight data...")
        flights = []
        cards = self.page.locator(".listingCard")
        count = cards.count()
        logger.info(f"ℹ️ Found {count} flights.")
        # print(f"ℹ️ Found {count} flights.")

        for i in range(count):
            card = cards.nth(i)
            try:
                airline = card.locator(".airlineName").inner_text(timeout=3000)
                price = card.locator(".priceSection span.fontSize18").inner_text(timeout=3000)
                flights.append({
                    "Airline": airline,
                    "From": from_city,
                    "To": to_city,
                    "Price": price
                })
                logger.debug(f"✅ Extracted flight #{i + 1}: {airline} at {price}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to extract flight #{i + 1}: {e}")
                # print(f"⚠️ Failed to extract flight #{i}: {e}")
        logger.info(f"✅ Finished extracting {len(flights)} flights.")
        return flights
