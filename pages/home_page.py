from utils.logger import setup_logger

logger = setup_logger(__name__)

class HomePage:
    def __init__(self, page):
        self.page = page
        self.close_button = page.locator('span.logSprite.icClose')

    def goto(self):
        self.page.goto("https://www.goibibo.com")
        logger.info("Navigated to Goibibo")

    def close_login_popup(self):
        self.close_button.wait_for(state='visible', timeout=5000)
        self.close_button.click()
        logger.info("Closed login popup")