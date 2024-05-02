import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Nav:
    def __init__(self, driver):
        self.driver = driver
        self.logging = logging

    def route_to_companies(self):
        try:
            self.logging.info('Attempting to route to "Companies"...')
            self.driver.get("https://www.glassdoor.sg/Reviews/index.htm")
            WebDriverWait(self.driver, 20).until(
                EC.url_to_be('https://www.glassdoor.sg/Reviews/index.htm')
            )
        except Exception as e:
            raise e
        else:
            self.logging.info('Successfully routed to "Companies"')