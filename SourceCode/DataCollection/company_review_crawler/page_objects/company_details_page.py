import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from page_objects.utils import get_text_from_elem
import random

class CompanyDetailPage:
    def __init__(self, driver):
        self.driver = driver
        self.logging = logging

    def change_tab(self, label):
        try:
            self.logging.info('[Company Details] Attempting to change to "Reviews" tab...')
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div.empLinksWrapper [href^=\"/{label}\"]'))
            )
            self.driver.execute_script(f"document.querySelector('div.empLinksWrapper [href^=\"/{label}\"]').click()")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'ol.empReviews.emp-{label.lower()}-feed'))
            )
        except Exception as e:
            self.logging.error('[Company Details] Change to "Reviews" tab failed')
            raise e
        else:
            self.logging.info('[Company Details] Change to "Reviews" tab success')

    def toggle_filter(self):
        try:
            self.logging.info('[Company Details] Attempting to toggle filter...')
            filter_toggle_btn_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[data-test="ContentFiltersFilterToggleBtn"]')
            filter_toggle_btn_elem.click()
        except Exception as e:
            self.logging.error('[Company Details] Toggle filter failed')
            raise e
        else:
            self.logging.info('[Company Details] Toggle filter success')

    def filter_by_location(self, id):
        try:
            self.logging.info('[Company Details] Attempting to filter by location...')
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="ContentFiltersSelectalocationDropdownContent"]'))
            )
            self.driver.execute_script("document.querySelector('div[data-test=\"ContentFiltersSelectalocationDropdownContent\"]').click()")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="ContentFiltersSelectalocationDropdownContent"] ul li'))
            )
            self.driver.execute_script(f"document.querySelector('div[data-test=\"ContentFiltersSelectalocationDropdownContent\"] ul li#{id}').click()")
            time.sleep(1)
        except Exception as e:
            self.logging.error('[Company Details] Filter by location failed')
            raise e
        else:
            self.logging.info('[Company Details] Filter by location success')

    def filter_by_job_fn(self, id):
        try:
            self.logging.info('[Company Details] Attempting to filter by job function...')
            job_function_selector_elem = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="ContentFiltersJobfunctionDropdownContent"]'))
            )
            job_function_selector_elem.click()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="ContentFiltersJobfunctionDropdownContent"] div.dropDownOptionsContainer ul li'))
            )
            self.driver.execute_script(f"document.querySelector('div[data-test=\"ContentFiltersJobfunctionDropdownContent\"] div.dropDownOptionsContainer ul li#{id}').click()")
            time.sleep(1)
        except Exception as e:
            self.logging.error('[Company Details] Filter by job function failed')
            raise e
        else:
            self.logging.info('[Company Details] Filter by job function success')

    def get_emp_name(self):
        return get_text_from_elem(self.driver, 'div[data-test="EmpInfo"] p.employerName')

    def get_review_list(self):
        try:
            self.logging.info('[Company Details] Attempting to get reviews...')
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ol.empReviews.emp-reviews-feed'))
            )
            list_item_elems = self.driver.find_elements(By.CSS_SELECTOR, 'ol.empReviews.emp-reviews-feed li')
        except Exception as e:
            self.logging.error('[Company Details] Get reviews failed')
            raise e
        else:
            self.logging.info('[Company Details] Get reviews success')
            return list_item_elems
    
    def change_page(self, page_no):
        try:
            self.logging.info(f'[Company Details] Attempting to change to "Reviews" page - {page_no}...')
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div.pageContainer a[data-test="pagination-link-{page_no}"]'))
            )
            page_btn_elem = self.driver.find_element(By.CSS_SELECTOR, f'div.pageContainer a[data-test="pagination-link-{page_no}"]')
            time.sleep(random.randint(3,5))
        except Exception as e:
            self.logging.error(f'[Company Details] Change to "Reviews" page - {page_no} failed')
            raise e
        else:
            page_btn_elem.click()
            time.sleep(1)
            self.logging.info(f'[Company Details] Change to "Reviews" page - {page_no} success')

    def iterate_pages(self, page_op, end, start=1, suppress_page_error=False):
        for page_no in range(start, end):
            if page_no > 1:
                self.change_page(page_no)
            try:
                list_item_elems = self.get_review_list()
                for idx, elem in enumerate(list_item_elems):
                    page_op(elem, idx)
            except Exception as e:
                if suppress_page_error:
                    self.logging.warning(f'[Company Details] Error suppressed: {e}')
                    continue
                else:
                    self.logging.error(f'[Company Details] Error occured: {e}')
                    raise e


