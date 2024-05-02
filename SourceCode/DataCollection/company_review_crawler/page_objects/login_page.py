import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

load_dotenv()

# Env variables
GLASSDOOR_USERNAME = os.getenv('GLASSDOOR_USERNAME')
GLASSDOOR_PASSWORD = os.getenv('GLASSDOOR_PASSWORD')

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.logging = logging

    def login(self):
        try:
            self.logging.info('Attempting to login...')
            email_input_elem = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#inlineUserEmail'))
            )
            email_input_elem.send_keys(GLASSDOOR_USERNAME)

            self.driver.find_element(By.CSS_SELECTOR, 'div.emailButton button').click()

            pwd_input_elem = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#inlineUserPassword'))
            )
            pwd_input_elem.send_keys(GLASSDOOR_PASSWORD)

            submit_btn_elem = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            submit_btn_elem.click()

            WebDriverWait(self.driver, 20).until(
                EC.url_to_be('https://www.glassdoor.sg/Job/index.htm')
            )
        except Exception as e:
            self.logging.error('Login failed')
            raise e
        else:
            self.logging.info('Login successful')
