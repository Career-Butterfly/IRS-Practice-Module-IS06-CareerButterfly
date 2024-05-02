from selenium.webdriver.common.by import By

def get_text_from_elem(elem, css_selector):
    try:
        return elem.find_element(By.CSS_SELECTOR, css_selector).text
    except:
        return None