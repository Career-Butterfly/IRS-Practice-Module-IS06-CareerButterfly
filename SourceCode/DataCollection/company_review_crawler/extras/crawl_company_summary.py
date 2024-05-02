#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Setup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from page_objects.login_page import LoginPage
from page_objects.companies_page import CompaniesPage
from page_objects.nav import Nav
from page_objects.company_details_page import CompanyDetailPage
from page_objects.utils import get_text_from_elem
import os
from datetime import date
import logging

options = Options()
options.add_argument("window-size=1200x600")

driver = webdriver.Chrome(options=options)

driver.get("https://www.glassdoor.sg")

filename_suffix = date.today().strftime('%Y-%m-%d')

logging.basicConfig(filename=f'crawl_summary_{filename_suffix}.log', encoding='utf-8', level=logging.INFO)

# Init page objects
login_page = LoginPage(driver)
nav = Nav(driver)
companies_page = CompaniesPage(driver)
companies_details_page = CompanyDetailPage(driver)


# In[2]:


# Login
login_page.login()


# In[3]:


# Route to 'Companies' page
nav.route_to_companies()

# Filter by location and job function in 'Companies' page
companies_page.filter_by_location('Singapore', 'Singapore (Singapore)')
companies_page.filter_by_job_function(['Engineering', 'Information Technology'])


# In[4]:


df = None
def crawl_company_summary(elem, idx):
    global df
    data = {
        'company_name': get_text_from_elem(elem, 'h2[data-test="employer-short-name"]'),
        'rating': get_text_from_elem(elem, 'span[data-test="rating"]'),
        'no_of_reviews': get_text_from_elem(elem, 'h3[data-test="cell-Reviews-count"]'),
        'no_of_salaries': get_text_from_elem(elem, 'h3[data-test="cell-Salaries-count"]'),
        'no_of_jobs':get_text_from_elem(elem, 'h3[data-test="cell-Jobs-count"]'),
        'location': get_text_from_elem(elem, 'span[data-test="employer-location"]'),
        'global_company_size': get_text_from_elem(elem, 'span[data-test="employer-size"]'),
        'industry': get_text_from_elem(elem, 'span[data-test="employer-industry"]'),
        'description': get_text_from_elem(elem, 'p')
    }
    df = pd.concat([df, pd.DataFrame([data])]) if df is not None else pd.DataFrame([data])


# In[5]:


# Crawl 'Companies' page
logging.info('Started crawling company summaries.')

companies_page.iterate_pages(
    crawl_company_summary,
    start=1,
    end=100,
    suppress_page_error=True
)

driver.quit()


# In[6]:


# Extract to csv
csv_filename = f'company_summary_{filename_suffix}.csv'

if os.path.isfile(f'./{csv_filename}'):
    df.to_csv(csv_filename, mode='a', header=False)
else:
    df.to_csv(csv_filename)

