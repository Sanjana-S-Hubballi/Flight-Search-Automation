from utils.logger import setup_logger

logger = setup_logger(__name__)
class FlightsPage:
    def __init__(self, page):
        self.page = page

        self.flights_tab = page.get_by_role("link", name="Flights", exact=True)
        self.departure_dropdown = page.locator("//span[text()='Departure']/following-sibling::p/span")
        self.add_return_flight = page.locator("p.gr_fswFld__info:has-text('Click to add a return flight for better discounts')")
        self.next_month_arrow = page.locator('span[aria-label="Next Month"]')
        self.travellers_class_dropdown = page.locator("span.fswDownArrowTraveller")
        self.plus_buttons = page.locator("svg[width='15'][height='15']")  # adults, children, infants
        self.travel_class_options = page.locator("ul.sc-12foipm-45 li")
        self.done_button = page.locator("a.sc-12foipm-64")
        self.search_button = page.locator("//span[text()='SEARCH FLIGHTS']")

    def goto_flights(self):
        self.flights_tab.click()

    def dismiss_mini_popup(self):
        popup = self.page.locator('p:has-text("LOGIN/SIGNUP")')
        if popup.is_visible():
            print("Mini LOGIN/SIGNUP popup visible — dismissing it...")
            self.page.locator('body').click()
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
            logger.info("Mini popup dismissed")

    def enter_from(self, search_text, suggestion_text):
        logger.info(f"Entering From city: {search_text}")
        self.page.get_by_text("Enter city or airport").nth(0).click()
        from_input = self.page.locator("input[type='text']").first
        from_input.fill(search_text)
        logger.info(f"Clicked suggestion: {suggestion_text}")
        self.page.get_by_text(suggestion_text, exact=False).click()

    def enter_to(self, search_text, suggestion_text):
        logger.info(f"Entering To city: {search_text}")
        to_input = self.page.locator("//span[text()='To']/following-sibling::input")
        to_input.click()
        to_input.fill(search_text)
        logger.info(f"Clicked suggestion: {suggestion_text}")
        self.page.locator("span.autoCompleteTitle", has_text=suggestion_text).first.click()

    def open_departure_picker(self):
        logger.info("Opening departure date picker")
        self.departure_dropdown.click()

    def select_departure_date(self, target_month_year, target_date_aria):
        logger.info(f"Selecting departure: {target_month_year} - {target_date_aria}")
        month_captions = self.page.locator("div.DayPicker-Caption > div")
        for _ in range(12):
            left_month = month_captions.nth(0).inner_text().strip()
            if left_month == target_month_year:
                self.page.locator(f'div.DayPicker-Day[aria-label="{target_date_aria}"]').click()
                logger.info(f"Departure date selected: {target_date_aria}")
                # print(f"Departure Selected: {target_date_aria}")
                break
            else:
                self.next_month_arrow.click()
                self.page.wait_for_timeout(500)

    def open_travellers_class_dropdown(self):
        logger.info("Opening travellers & class dropdown")
        self.travellers_class_dropdown.click()

    def select_travellers_and_class(self, adults=1, travel_class="economy"):
        logger.info(f"Selecting {adults} Adults, Class: {travel_class}")
        print("Setting Travellers & Class...")
        for _ in range(adults - 1):
            logger.debug("Clicked +1 Adult")
            self.plus_buttons.nth(0).click()
        class_map = {"economy": 0, "premium economy": 1, "business": 2, "first class": 3}
        index = class_map[travel_class.lower()]
        self.travel_class_options.nth(index).click()
        logger.info(f"Selected travel class: {travel_class}")
        self.done_button.click()
        logger.info("Confirmed travellers & class selection")

    def search_flights(self):
        logger.info("Clicking SEARCH FLIGHTS button")
        self.search_button.click()
