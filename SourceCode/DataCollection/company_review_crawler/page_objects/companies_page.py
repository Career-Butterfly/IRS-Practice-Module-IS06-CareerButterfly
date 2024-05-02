from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import logging

class CompaniesPage:
    def __init__(self, driver):
        self.driver = driver
        self.logging = logging

    def filter_by_location(self, input_text, label):
        try:
            self.logging.info('[Companies] Attempting to filter by location...')
            self.driver.find_element(By.CSS_SELECTOR ,'div[data-test="location-autocomplete"] input[name="Location"]').send_keys(input_text)
            time.sleep(1)
            location_dropdown_opt_elems = self.driver.find_elements(By.CSS_SELECTOR ,'div[data-test="location-autocomplete"] ul.suggestions li')
            for elem in location_dropdown_opt_elems:
                label_elem = elem.find_element(By.CSS_SELECTOR, 'span.suggestionLabel')
                if label_elem.text.strip() == label:
                    elem.click()
                    break
            time.sleep(1)
        except Exception as e:
            self.logging.error('[Companies] Filter by location failed')
            raise e
        else:
            self.logging.info('[Companies] Filter by location success')

    def filter_by_job_function(self, labels):
        try:
            self.logging.info('Attempting to filter by job function...')
            self.driver.execute_script("document.querySelector('div[data-test=\"accordion-section-job-functions\"] div[role=\"button\"]').click()")
            time.sleep(1)
            keys = [label.lower().replace(' ', '-') for label in labels]
            for key in keys:
                self.driver.execute_script(f"document.querySelector('div[data-test=\"checkbox-{key}\"] input[type=\"checkbox\"]').click()")
            time.sleep(1)
        except Exception as e:
            self.logging.error('[Companies] Filter by job function failed')
            raise e
        else:
            self.logging.info('[Companies] Filter by job function success')

    def get_employee_cards(self):
        try:
            self.logging.info('[Companies] Waiting for presence of employer cards...')
            WebDriverWait(self.driver, 20).until(
                lambda browser: len(browser.find_elements(By.CSS_SELECTOR, 'div[data-test="employer-card-single"]')) >= 10
            )
            employer_card_elems = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-test="employer-card-single"]')
        except Exception as e:
            self.logging.error('[Companies] Finding employer cards failed')
            raise e
        else:
            self.logging.info('[Companies] Employer cards found')
            return employer_card_elems
    
    def change_page(self, page_no):
        try:
            self.logging.info(f'[Companies] Attempting to change to "Companies" page - {page_no}...')
            page_btn_elem = self.driver.find_element(By.CSS_SELECTOR, f'div.pageContainer button[data-test="pagination-link-{page_no}"]')
        except NoSuchElementException:
            self.logging.info('[Companies] Page number not found, attempting to find page...')
            self.driver.execute_script("(() => {\
                const paginationLinks = document.querySelectorAll('div.pageContainer button[data-test^=\"pagination-link-\"]');\
                paginationLinks[paginationLinks.length - 1].click();\
            })()")
            time.sleep(1)
            self.change_page(page_no)
        except Exception as e:
            self.logging.error(f'[Companies] Change to "Companies" page - {page_no} failed')
            raise e
        else:
            page_btn_elem.click()
            time.sleep(1)
            self.logging.info(f'[Companies] Change to "Companies" page - {page_no} success')
        

    def iterate_pages(self, page_op, end, start=1, suppress_page_error=False):
        for page_no in range(start, end + 1):
            if page_no > 1:
                self.change_page(page_no)
            try:
                employer_card_elems = self.get_employee_cards()
                for idx, elem in enumerate(employer_card_elems):
                    page_op(elem, idx)
            except Exception as e:
                if suppress_page_error:
                    self.logging.warning(f'[Companies] Error suppressed: {e}')
                    windows = self.driver.window_handles
                    for idx, window in enumerate(windows):
                        if idx == 0:
                            continue
                        self.driver.switch_to.window(window)
                        self.driver.close()
                    self.driver.switch_to.window(windows[0])
                    continue
                else:
                    self.logging.error(f'[Companies] Error occured: {e}')
                    raise e
