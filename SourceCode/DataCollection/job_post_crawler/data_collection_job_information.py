# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 20:05:21 2024

@author: kuany
"""

import os
import time
import random
import pandas as pd
import datetime as dt
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def start_scraper(page_url, driver, delay, searching_job_title):
    """
    Navigates to https://www.mycareersfuture.gov.sg/ and search for job posts related to job title of interest.

    Inputs:
    - page_url: web URL of the site we are scraping
    - driver: webdriver we are using for the scrape
    - delay: add delay for driver to wait in case element has not load up
    - searching_job_title: the job title we are searching for

    Output:
    - 
    """
    a = True
    while a != False:
        try:
            driver.get(page_url)
            # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'search-text')))
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'search-text')))
            # element = driver.find_element(By.ID, "search-string-box") ### if you are in the job posting pages
            element = driver.find_element(By.ID, 'search-text') ### if you start on the main page
            element.clear()
            element.send_keys(searching_job_title)
            element.send_keys(Keys.ENTER)
            randnum = random.randint(1,10)
            time.sleep(randnum)
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.bg-white.mb3.w-100.dib.v-top.pa3.no-underline.flex-ns.flex-wrap.JobCard__card___22xP3')))
            a = False
        except:
            driver.quit()
            
def get_all_job_post_link():
    """
    Navigate through all the pages and return all job post links in a list

    Input: 
    -

    Output:
    - list containing all job post links
    """
    ### Get all job post links from all pages
    next_page = True
    all_job_post_links = []
    while next_page != False:
        ### Get job post links
        job_post_links_1 = driver.find_elements(By.CSS_SELECTOR, '.bg-white.mb3.w-100.dib.v-top.pa3.no-underline.flex-ns.flex-wrap.JobCard__card___22xP3')
        job_post_links_2 = driver.find_elements(By.CSS_SELECTOR, '.bg-washed-green.mb1.w-100.dib.v-top.pa3.relative.no-underline.flex-ns.flex-wrap.bt.bw1.b--green.JobCard__card___22xP3')
        job_post_links = job_post_links_1 + job_post_links_2
        job_post_links = [x.get_attribute('href') for x in job_post_links]
        ### Save all job post links into list
        all_job_post_links = all_job_post_links + job_post_links
        
        ### Check if next page exist
        try:
            page_navigation_buttons = driver.find_elements(By.CSS_SELECTOR, '.f5-5.pv2.ph3.mh1.dib.black-80.hover-bg-white.pointer')
            page_navigation_buttons_text = [x.text for x in page_navigation_buttons]
            if not page_navigation_buttons_text[-1].isnumeric():
                next_page = driver.find_elements(By.CSS_SELECTOR, '.f5-5.pv2.ph3.mh1.dib.black-80.hover-bg-white.pointer')
            else:
                next_page = False
            randnum = random.randint(1,10)
            time.sleep(randnum)
        except:
            next_page = False
            
        ### If next page exist
        if next_page != False:
            next_page[-1].click()
            time.sleep(1)
        else:
            print('Reach the final page')
    return all_job_post_links

def get_job_detail(job_post_link, delay):
    """
    Navigates to job post link and retrieve job details. Return details as individual variables

    Input:
    - job_post_link: Link to the job post
    - delay: add delay to wait

    Output:
    - company_name: Company name on the job post
    - job_title: Job title on the job post
    - job_location: Job location on the job post
    - job_employment_type: Job employment type (e.g. Full-time, Permanent, Contract, etc.)
    - job_seniority: Job seniority (e.g. Executive, Senior Executive, Manager, etc.)
    - job_experience_level: Job experience level (e.g. 1 - 2 years, 5 years, etc.)
    - job_industry: Industry of the job
    - job_salary_range: Salary range of the job post
    - job_salary_frequency: Unit of the salary (e.g. Monthly, Yearly, etc.)
    - job_post_start_date: Date of posting the job post
    - job_post_close_date: Last date of application
    - job_description: Description of the job
    """
    ### If error out, find out which index to continue at, run in next cell or find a way to loop. Possible to create a function for extracting data
    error_out = False
    while error_out == False:
        try:
            driver.get(job_post_link)
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.f6.fw6.mv0.black-80.mr2.di.ttu.truncate-lines.truncate-lines-3')))
            # WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.f6.fw6.mv0.black-80.mr2.di.ttu.truncate-lines.truncate-lines-3')))
            error_out = True
        except KeyboardInterrupt as e:
            break
        except:
            print('error out at {}'.format(job_post_link))
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.f6.fw6.mv0.black-80.mr2.di.ttu.truncate-lines.truncate-lines-3')))
        company_name = driver.find_elements(By.CSS_SELECTOR, '.f6.fw6.mv0.black-80.mr2.di.ttu.truncate-lines.truncate-lines-3')
        company_name = company_name[0].text
    except StaleElementReferenceException:
        company_name = ''
    except:
        company_name = driver.find_elements(By.CSS_SELECTOR, '.f6.fw6.mv0.black-80.mr2.di.ttu')[0].text + driver.find_elements(By.CSS_SELECTOR, '.f6.fw6.w-100.mv0.black-60')
    
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.f3.fw6.mv0.pv0.mb1.brand-sec.w-100.dib')))
        job_title = driver.find_elements(By.CSS_SELECTOR, '.f3.fw6.mv0.pv0.mb1.brand-sec.w-100.dib')[0].text
    except:
        job_title = driver.find_elements(By.CSS_SELECTOR, '.f3.fw6.mv0.pv0.mb1.brand-sec.w-100.dib')[0].text
    try:
        job_location = driver.find_elements(By.CSS_SELECTOR, '.black-80.f6.fw4.mv1.dib.pr3.mr1.icon-bw-location')[0].text
    except:
        job_location = ''
    try:
        job_employment_type = driver.find_elements(By.CSS_SELECTOR, '.black-80.f6.fw4.mv1.dib.pr3.mr1.icon-bw-employment-type')[0].text
    except:
        job_employment_type = ''
    try:
        job_seniority = driver.find_elements(By.CSS_SELECTOR, '.black-80.f6.fw4.mv1.dib.pr3.mr1.icon-bw-seniority')[0].text
    except:
        job_seniority = ''
    try:
        job_experience_level = driver.find_elements(By.CSS_SELECTOR, '.black-80.f6.fw4.mv1.dib.pr3.mr1.icon-bw-period')[0].text
    except:
        job_experience_level = ''
    try:
        job_industry = driver.find_elements(By.CSS_SELECTOR, '.black-80.f6.fw4.mv1.dib.pr3.mr1.icon-bw-category')[0].text
    except:
        job_industry = ''
    try:
        job_salary_range = driver.find_elements(By.CSS_SELECTOR, '.dib.f2-5.fw6.black-80')[0].text
    except: 
        job_salary_range = ''
    try:
        job_salary_frequency = driver.find_elements(By.CSS_SELECTOR, '.ttc.dib.f5.fw4.black-60.pr1.i.pb')[0].text
    except:
        job_salary_frequency = ''
    try:
        job_post_start_date = driver.find_elements(By.CSS_SELECTOR, '.purple.f6.fw4.pr3')[0].text
    except:
        job_post_start_date = ''
    try:
        job_post_close_date = driver.find_elements(By.CSS_SELECTOR, '.purple.f6.fw4.pr3.pt2.dib')[0].text
    except:
        job_post_close_date = ''
    try:
        job_description = driver.find_elements(By.CSS_SELECTOR, '.f5.fw4.black-80.lh-copy.break-word.JobDetails__job_details_page___2hMQp')[0].text
    except:
        job_description = ''

    randnum = random.randint(1,10)
    time.sleep(randnum)

    return company_name, job_title, job_location, job_employment_type, job_seniority, job_experience_level, job_industry, job_salary_range, job_salary_frequency, job_post_start_date, job_post_close_date, job_description

### Time taken
start = time.time()

# ### Create driver
# driver = webdriver.Chrome()
# action = ActionChains(driver)

### Go to the characters page
delay = 3
# page_url = 'https://www.mycareersfuture.gov.sg/search?search=data%20analyst&sortBy=relevancy&page=0'
page_url = 'https://www.mycareersfuture.gov.sg/'
# searching_job_title = 'data analyst'
# searching_job_title = ['data analyst', 'software engineer', 'AI Engineer', 'Machine Learning Engineer']
searching_job_title = ['cloud engineer', 'data analyst', 'data scientist', 'AI Engineer', 'Machine Learning Engineer', 'dev ops engineer',
                        'qa automation tester', 'software engineer', 'site reliability engineer', 'support engineer']

for each_job_search_title in searching_job_title:
    print('Looking for {}'.format(each_job_search_title))
    ### Create driver
    driver = webdriver.Chrome()
    action = ActionChains(driver)
    ### Navigate to the webpage and search for job posts related to job title of interest.
    # start_scraper(page_url, driver, delay, searching_job_title)
    start_scraper(page_url, driver, delay, each_job_search_title)
    
    ### Navigate through all the pages and return all job post links in a list
    all_job_post_link = get_all_job_post_link()
    
    driver.quit()
    time.sleep(1)
    
    ### Create driver
    driver = webdriver.Chrome()
    
    ### Navigate to the webpage and search for job posts related to job title of interest.
    # start_scraper(page_url, driver, delay, searching_job_title)
    start_scraper(page_url, driver, delay, each_job_search_title)
    
    company_name_list, job_title_list, job_location_list, job_employment_type_list, job_seniority_list, job_experience_level_list = [], [], [], [], [], []
    job_industry_list, job_salary_range_list, job_salary_frequency_list, job_post_start_date_list, job_post_close_date_list, job_description_list = [], [], [], [], [], []
    current_index = 0
    end_index = len(all_job_post_link) - 1
    pbar = tqdm(total = end_index+1)
    while current_index < end_index:
        try:
            company_name, job_title, job_location, job_employment_type, job_seniority, job_experience_level, job_industry, job_salary_range, job_salary_frequency, job_post_start_date, job_post_close_date, job_description = get_job_detail(all_job_post_link[current_index], delay)
            company_name_list.append(company_name)
            job_title_list.append(job_title)
            job_location_list.append(job_location)
            job_employment_type_list.append(job_employment_type)
            job_seniority_list.append(job_seniority)
            job_experience_level_list.append(job_experience_level)
            job_industry_list.append(job_industry)
            job_salary_range_list.append(job_salary_range)
            job_salary_frequency_list.append(job_salary_frequency)
            job_post_start_date_list.append(job_post_start_date)
            job_post_close_date_list.append(job_post_close_date)
            job_description_list.append(job_description)
            current_index += 1
            pbar.update(1)
        except KeyboardInterrupt as e:
            break
    pbar.close()
    driver.quit()
    time.sleep(1)
    
    data_df = pd.DataFrame({
        'company_name': company_name_list,
        'job_title': job_title_list,
        'job_location': job_location_list,
        'job_employment_type': job_employment_type_list,
        'job_seniority': job_seniority_list,
        'job_experience_level': job_experience_level_list,
        'job_industry': job_industry_list,
        'job_salary_range': job_salary_range_list,
        'job_salary_frequency': job_salary_frequency_list,
        'job_post_start_date': job_post_start_date_list,
        'job_post_close_date_list': job_post_close_date_list,
        'job_description': job_description_list
    }, index=[x for x in range(len(company_name_list))])
    
    end = time.time()
    print('time taken: {}'.format(end - start))
    
    ### Save extracted data into csv for further processing
    data_df.to_csv(os.getcwd() + '/new_data/' + '{}_{}.csv'.format(each_job_search_title, dt.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')))
    print('Completed {} job post data collection'.format(each_job_search_title))
    time.sleep(1)