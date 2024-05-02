# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:38:08 2024

@author: kuany

### Resume Parser 
### Input: Resume (.pdf)
### Output: List containing job experiences, educational background, technical skills'
"""

import os
import PyPDF2 as pdf
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key = os.environ["OPEN_AI_KEY"].strip())

def get_chatgpt_repsonse(input):
    """
    Returns ChatGPT response based on given prompt

    Input: 
    - text prompt
    Output:
    - ChatGPT text response
    """
    response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=input, max_tokens=1949, temperature=0.99, user="user")
    text = response.choices[0].text
    return text

def input_pdf_text(uploaded_file):
    """
    Reads pdf and return extracted text
    
    Input:
    - PDF document
    Output:
    - extracted text
    """
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

def data_cleaning(response):
    """
    Returns cleaned and formatted text data based on Gemini response in a list

    Input:
    - ChatGPT text response
    Output:
    - a list containing cleaned and formatted text data
    """
    combined_text = ''
    start = 0
    cleaned_data = []
    for x in response.split('\n'):
        if ('job description:' not in x.lower()) and (start == 0) and ('-----------------------------' != x):
            cleaned_data.append(x.replace('-', ' to ').replace('\t', '').lstrip())
        else:
            if 'job description:' in x.lower():
                start = 1
                combined_text = ''
            if '-----------------------------' == x:
                start = 0
                cleaned_data.append(combined_text)
                combined_text = ''
            if start == 1:
                combined_text = combined_text + x.replace('-', '').replace('\t', '').lstrip() + ' '
    return cleaned_data

def candidate_information_categorization(cleaned_data):
    """
    Returns a dictionary containing candidate information

    Input:
    - cleaned and formatted ChatGPT text response
    Output:
    - a dictionary containing candidate information
    """
    saved_data = {}
    temp_skill_list = []
    temp_job_dict = {}
    for each_line in cleaned_data:
        if ('Name:' in each_line) and ('Company Name:' not in each_line):
            saved_data['name'] = each_line.split('Name:')[1].lstrip()
        if 'Total Years of Experiences:' in each_line:
            saved_data['years_of_experience'] = each_line.split('Total Years of Experiences:')[1].lstrip()
        if 'Job no.:' in each_line:
            job_num = each_line.split('Job no.:')[1].lstrip()
        if 'Company Name:' in each_line:
            temp_job_dict['company_name'] = each_line.split('Company Name:')[1].lstrip()
        if 'Job title:' in each_line:
            temp_job_dict['job_title'] = each_line.split('Job title:')[1].lstrip()
        if 'Job tenure period:' in each_line:
            temp_job_dict['job_tenure_period'] = each_line.split('Job tenure period:')[1].lstrip()
        if 'Job description:' in each_line:
            temp_job_dict['job_description'] = each_line.split('Job description:')[1].lstrip()
            saved_data['job_{}'.format(job_num)] = [temp_job_dict]
        if 'Degree no.:' in each_line:
            temp_degree_dict = {}
            degree_num = each_line.split('Degree no.:')[1].lstrip()
        if 'Degree title:' in each_line:
            temp_degree_dict['degree_title'] = each_line.split('Degree title:')[1].lstrip()
        if 'Degree years:' in each_line:
            temp_degree_dict['degree_years'] = each_line.split('Degree years:')[1].lstrip()
        if 'University:' in each_line:
            temp_degree_dict['university'] = each_line.split('University:')[1].lstrip()
            saved_data['degree_{}'.format(degree_num)] = [temp_degree_dict]
        if 'Programming Skills:' in each_line:
            temp_skill_list.append(each_line.split('Programming Skills:')[1].lstrip())
        if 'Data Analysis Skills:' in each_line:
            temp_skill_list.append(each_line.split('Data Analysis Skills:')[1].lstrip())
        if 'Data Science Skills:' in each_line:
            temp_skill_list.append(each_line.split('Data Science Skills:')[1].lstrip())
        if 'Data Visualization Skills:' in each_line:
            temp_skill_list.append(each_line.split('Data Visualization Skills:')[1].lstrip())
        if 'Front End Skills:' in each_line:
            temp_skill_list.append(each_line.split('Front End Skills:')[1].lstrip())
        if 'Back End Skills:' in each_line:
            temp_skill_list.append(each_line.split('Back End Skills:')[1].lstrip())
        if 'Cloud technology Skills:' in each_line:
            temp_skill_list.append(each_line.split('Cloud technology Skills:')[1].lstrip())
            saved_data['skill'] = ''.join(temp_skill_list)
    return saved_data

def get_resume_info(FILEPATH):
    text = input_pdf_text(FILEPATH)
    input_prompt='''
    Act as a skilled Recruiter or very experience ATS(Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analyst
    and big data engineer. Your task is to evaluate the resume and return the following information in this format. 
    For the skills, take note to add in technical skills gathered throughout the resume.
    For Job no., provide it in a numerical form.
    For Degree no., provide it in a numerical form.
    if the answer is not in provided resume just say, "answer is not available in the context", don't provide the wrong answer. Scan through the resume multiple times to ensure that no information was missed out:
    
    - Name: 
    - Work Experiences:
    -----------------------------
    \t- Job no.:
    \t- Company Name:
    \t- Job title:
    \t- Job tenure period:
    \t- Job description:
    -----------------------------
    - Education information:
    -----------------------------
    \t- Degree no.:
    \t- Degree title:
    \t- Degree years:
    \t- University:
    -----------------------------
    - Programming Skills:
    - Data Analysis Skills:
    - Data Science Skills:
    - Data Visualization Skills:
    - Front End Skills:
    - Back End Skills:
    - Cloud technology Skills:
    
    resume:{0}
    '''.format(text)  
    
    response=get_chatgpt_repsonse(input_prompt)
    cleaned_data = data_cleaning(response)
    cleaned_data = candidate_information_categorization(cleaned_data)
    
    return cleaned_data

def retrieve_degree_info(resume_info):
    ## retrieve degree information
    degree_info={}
    for key, value in resume_info.items():
        if key.startswith('degree_'):
            degree_info[key] = value[0]
    return degree_info

def retrieve_work_info(resume_info):
    ## retrieve work information
    work_info={}
    for key, value in resume_info.items():
        if key.startswith('job_'):
            work_info[key] = value[0]
    return work_info