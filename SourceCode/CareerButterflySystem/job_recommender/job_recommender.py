# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 20:08:05 2024

@author: kuany
"""
import os
import json as js_on
import requests
import pandas as pd

DATA_DIR = '/data'
SENTIMENT_SERVICE = os.environ['SENTIMENT_SERVICE']

def job_recommender(resume_data):
    
    candidate_information = resume_data['resume_info']
    candidate_preferences = resume_data['candidate_preferences']
    
    candidate_information = js_on.loads(candidate_information.replace("'", '"'))
    candidate_preferences = js_on.loads(candidate_preferences.replace("'", '"'))
    
    job_position_mapping = {
        'cloud engineer': 'cloud_engineer',
        'ai engineer': 'data_scientist_or_analyst',
        'data analyst': 'data_scientist_or_analyst',
        'data scientist': 'data_scientist_or_analyst',
        'machine learning engineer': 'data_scientist_or_analyst',
        'qa automation tester': 'qa_automation_tester',
        'software engineer': 'software_engineer',
        'site reliability engineer': 'sre',
        'support engineer': 'support_engineer'
    }
    
    ### Read curated data (.csv files)
    job_data = {}
    for x in os.listdir(DATA_DIR):
        job_data[x.split('.csv')[0]] = pd.read_csv(f'{DATA_DIR}/{x}').iloc[:, 1:]
    
    ### Get the job data of the job titles candidate is interested in.
    # data_df = job_data[candidate_preferences['job_title'].lower().lstrip()]
    data_df = job_data[job_position_mapping[candidate_preferences['job_title'].lower().lstrip()]]
    data_df['original_job_title'] = data_df['original_job_title'].apply(lambda x: x.lower())
    # data_df['original_job_title'] = data_df['original_job_title'].str.lower()
    # data_df = data_df[data_df['original_job_title'] == candidate_preferences['job_title'].lower().lstrip()]
    # data_df['job_title'] = candidate_preferences['job_title'].lower()
    
    ### Mapping postal district code to district location  
    mapping_district = {'01': 'South',
                        '02': 'South',
                        '03': 'South',
                        '04': 'South',
                        '05': 'West',
                        '06': 'Central',
                        '07': 'Central',
                        '08': 'Central',
                        '09': 'Central',
                        '10': 'Central',
                        '11': 'Central',
                        '12': 'Central',
                        '13': 'Central',
                        '14': 'Central',
                        '15': 'East',
                        '16': 'East',
                        '17': 'East',
                        '18': 'East',
                        '19': 'North',
                        '20': 'North',
                        '21': 'West',
                        '22': 'West',
                        '23': 'West',
                        '24': 'West',
                        '25': 'North',
                        '26': 'North',
                        '27': 'North',
                        '28': 'North'}
    
    ### Mapping postal sector to postal district code
    mapping_postal_sector = {'01': '01',
                              '02': '01',
                              '03': '01',
                              '04': '01',
                              '05': '01',
                              '06': '01',
                              '07': '02',
                              '08': '02',
                              '09': '04',
                              '10': '04',
                              '11': '05',
                              '12': '05',
                              '13': '05',
                              '14': '03',
                              '15': '03',
                              '16': '03',
                              '17': '06',
                              '18': '07',
                              '19': '07',
                              '20': '08',
                              '21': '08',
                              '22': '09',
                              '23': '09',
                              '24': '10',
                              '25': '10',
                              '26': '10',
                              '27': '10',
                              '28': '11',
                              '29': '11',
                              '30': '11',
                              '31': '12',
                              '32': '12',
                              '33': '12',
                              '34': '13',
                              '35': '13',
                              '36': '13',
                              '37': '13',
                              '38': '14',
                              '39': '14',
                              '40': '14',
                              '41': '14',
                              '42': '15',
                              '43': '15',
                              '44': '15',
                              '45': '15',
                              '46': '16',
                              '47': '16',
                              '48': '16',
                              '49': '17',
                              '50': '17',
                              '51': '18',
                              '52': '18',
                              '53': '19',
                              '54': '19',
                              '55': '19',
                              '56': '20',
                              '57': '20',
                              '58': '21',
                              '59': '21',
                              '60': '22',
                              '61': '22',
                              '62': '22',
                              '63': '22',
                              '64': '22',
                              '65': '23',
                              '66': '23',
                              '67': '23',
                              '68': '23',
                              '69': '24',
                              '70': '24',
                              '71': '24',
                              '72': '25',
                              '73': '25',
                              '75': '27',
                              '76': '27',
                              '77': '26',
                              '78': '26',
                              '79': '28',
                              '80': '28',
                              '81': '17',
                              '82': '19'}
    
    data_df['postal_sector'] = data_df['job_location'].fillna('').apply(lambda x: x[-6:-4] if x[-6:].isnumeric() else '')
    data_df['postal_district'] = data_df['postal_sector'].map(mapping_postal_sector).fillna('')
    data_df['postal_district_location'] = data_df['postal_district'].map(mapping_district).fillna(data_df['job_location'])
    
    ### Find the upper and lower salary amount
    
    data_df[['job_salary_lower_bracket', 'job_salary_upper_bracket']] = data_df['job_salary_range'].str.split('to', n=1, expand=True)
    data_df['job_salary_lower_bracket'] = data_df['job_salary_lower_bracket'].apply(lambda x: x.replace('$', '').replace(',', '')).astype(float)
    data_df['job_salary_upper_bracket'] = data_df['job_salary_upper_bracket'].apply(lambda x: x.replace('$', '').replace(',', '')).astype(float)
    
    ### clean job_title by applying lower case
    data_df['job_title_lower'] = data_df['job_title'].str.lower()
    ### clean job_employment_type column by filling NaN with contract and apply lower case
    data_df['job_employment_type_lower'] = data_df['job_employment_type'].fillna('contract').str.lower()
    ### clean job_seniority column by filling NaN with empty string and apply lower case
    data_df['job_seniority_lower'] = data_df['job_seniority'].fillna('').str.lower()
    ### clean job_experience column by filling NaN with '0 years exp' and extract only the number of years experience
    data_df['job_experience_level_clean'] = data_df['job_experience_level'].fillna('0 years exp').apply(lambda x: int(x.split(' year')[0]))
    ### clean job_industry column by fillng NaN with empty string and apply lower case
    data_df['job_industry_lower'] = data_df['job_industry'].fillna('').str.lower()
    
    ### Method: 
    ### - From the job preferences (job title, salary range, job location, job employment type, job seniority, job experience, job industry), 
    ###   filter out the jobs from the dataset we have (CSVs)
    
    job_title_condition = data_df['original_job_title'].isin([candidate_preferences['job_title'].lower()])
    filter_condition = job_title_condition 
    
    if len(candidate_preferences['job_location']) > 0:
        job_location_condition = data_df['postal_district_location'].str.lower().isin([candidate_preferences['job_location'], 'Islandwide'])
        filter_condition = filter_condition & job_location_condition
    if len(candidate_preferences['salary_range']) > 0:
        # job_salary_bracket_condition = (data_df['job_salary_lower_bracket'] <= candidate_preferences['salary_range'][0]) & (data_df['job_salary_upper_bracket'] >= candidate_preferences['salary_range'][0])
        job_salary_bracket_condition  = (data_df['job_salary_lower_bracket'] >= float(candidate_preferences['salary_range'][0]))
        filter_condition = filter_condition & job_salary_bracket_condition
    if len(candidate_preferences['job_employment_type']) > 0:
        job_employment_type_condition = (data_df['job_employment_type_lower'].apply(lambda x: x if candidate_preferences['job_employment_type'].lower() in x else 'no') != 'no')
        filter_condition = filter_condition & job_employment_type_condition
    if len(candidate_preferences['job_seniority']) > 0:
        job_seniority_condition = data_df['job_seniority_lower'].isin([candidate_preferences['job_seniority'].lower()])
        filter_condition = filter_condition & job_seniority_condition
    if len(str(candidate_preferences['job_experience'])) > 0:
        job_experience_condition = (data_df['job_experience_level_clean'] >= candidate_preferences['job_experience'])
        filter_condition = filter_condition & job_experience_condition
    if len(candidate_preferences['job_industry']) > 0:
        job_industry_condition = data_df['job_industry_lower'].isin([candidate_preferences['job_industry'].lower()])
        filter_condition = filter_condition & job_industry_condition
    
    ### Filter data_df using the above conditions
    filtered_df = data_df[filter_condition]
    filtered_df['job_title'] = candidate_preferences['job_title'].lower()
    
    ### Extract and prepare key information from resume to find similarity with filtered job descriptions
    candidate_key_information = [', '.join(list(candidate_information[key][0].values())) for key, val in candidate_information.items() if 'job' in key or 'degree' in key]
    if len(candidate_key_information) > 1:
        candidate_key_information = ', '.join(candidate_key_information)
    candidate_key_information = candidate_key_information + candidate_information['skill']
    
    def get_BOW_cosine_similarity_score(text_for_comparison):
        """
        Returns cosine similarity score between candidate key information extracted from resume and job description
    
        Input:
        - a list containing candidate key information extracted from resume and job description
    
        Output:
        - Cosine similarity score
        """
        from sklearn.feature_extraction.text import CountVectorizer
        
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_for_comparison)
        
        ### Consine Similarity
        from sklearn.metrics.pairwise import cosine_similarity
        # print('Similarity score : ',cosine_similarity(count_matrix))
    
        ### Cosine Similarity percentage
        # matchpercentage = cosine_similarity(count_matrix)[0][1]
        # matchpercentage = round(matchpercentage*100,2)
        # print('Your Resume {} % match to the job description !'.format(matchpercentage))
        return cosine_similarity(count_matrix)[0][1]
    
    filtered_df['BOW_cosine_similarity_score'] = filtered_df['job_description'].str.replace('\n', ' ').replace('-', '').replace('\t', ' ').apply(lambda x: get_BOW_cosine_similarity_score([candidate_key_information, x]))
    
    filtered_df.sort_values(['BOW_cosine_similarity_score'], ascending=False, inplace=True)
    
    # top_5_jobs = filtered_df.sort_values(['BOW_cosine_similarity_score'], ascending=False).head(5)
    
    ### Factor in the glassdoor company review sentiment analysis score (50%) + glassdoor company rating (50%)
    mapping_company_name_to_sentiment_table = {
        'alcon pte ltd': 'alcon',
        'accenture pte ltd': 'accenture',
        'alibaba southeast asia holding private limited': 'alibaba group',
        'amazon web services private limited': 'amazon', 
        'anacle systems limited': 'anacle systems',
        'bloomberg singapore pte. ltd.': 'bloomberg',
        'ctc global pte. ltd.': 'ctc global',
        'certis cisco protection services pte. ltd.': 'certis',
        'certis cisco aviation security pte. ltd.': 'certis',
        'certis tech-ops and services pte. ltd.': 'certis',
        'certis technology (singapore) pte. ltd.': 'certis',
        'certis cisco security pte. ltd.': 'certis',
        'chevron singapore pte. ltd.': 'chevron',
        'fugro singapore marine pte. ltd.': 'fugro',
        'google asia pacific pte. ltd.': 'google',
        'halliburton far east pte ltd': 'halliburton',
        'hyundai motor group innovation center in singapore pte. ltd.': 'hyundai motor',
        'incube8 pte. ltd.': 'incube8',
        'inland revenue authority of singapore': 'inland revenue authority of singapore',
        'johnson control(s) pte. ltd.': 'johnson controls',
        'kiteworks pte. ltd.': 'kiteworks',
        'lonza biologics tuas pte. ltd.': 'lonza biologics tuas',
        'msd international gmbh (singapore branch)': 'msd',
        'micron semiconductor asia operations pte. ltd.': 'micron technology',
        'ncs pte. ltd.': 'ncs',
        'netapp singapore pte. ltd.': 'netapp',
        'psa corporation limited': 'psa international',
        'panasonic asia pacific pte. ltd.': 'panasonic',
        'prudential assurance company singapore (pte) limited': 'prudential assurance singapore',
        'qualcomm cmda technologies asia-pacific pte ltd': 'qualcomm technologies',
        'roche singapore technical operations pte. ltd.': 'roche',
        'roche singapore pte. ltd.': 'roche',
        'rolls-royce solutions asia pte. ltd.': 'rolls-royce power systems',
        'sls bearings (singapore) private limited': 'sls bearings',
        'samsung electronics singapore pte. ltd.': 'samsung electronics',
        'schindler lifts (singapore) pte. ltd.': 'schindler',
        'seagate singapore international headquarters pte. ltd.': 'seagate technology',
        'siemens industry software pte. ltd.': 'siemens',
        'standard chartered bank (singapore) limited': 'standard chartered bank',
        'sivantos pte. ltd.': 'ws audiology'
    }
    
    filtered_df['company_name_mapped'] = filtered_df['company_name'].apply(lambda x: mapping_company_name_to_sentiment_table[x] if x in mapping_company_name_to_sentiment_table.keys() else x)
    
    if len(filtered_df['company_name_mapped'].tolist()) > 0:
        filtered_company_names = 'company_name_mapped=' + ','.join(filtered_df['company_name_mapped'].dropna().tolist())
    else:
        filtered_company_names = ''
    
    if len(candidate_preferences['job_title'].lower()) > 0:
        filtered_job_title = 'job_title=' + candidate_preferences['job_title'].lower()
    else:
        filtered_job_title = ''
        
    if (filtered_company_names != '') and (filtered_job_title != ''):
        request_joiner = '&'
    else:
        request_joiner = ''
    
    sentiment_data = requests.get(
        url=SENTIMENT_SERVICE+'/aggregate?{}{}{}'.format(filtered_company_names, request_joiner, filtered_job_title), 
        verify=False).text.split('\n')
    sentiment_data_df = pd.DataFrame([x.split(',') for x in sentiment_data])
    sentiment_data_df.columns = sentiment_data_df.iloc[0]
    sentiment_data_df = sentiment_data_df.iloc[1:, 1:]
    sentiment_data_df = sentiment_data_df.dropna()
    
    if sentiment_data_df.shape[0] == 0:
        filtered_df['sentiment_and_rating_score'] = 0
        filtered_df['priority_score'] = 0
        final_df = filtered_df
    else:
        if len(candidate_preferences['priority']) > 0:
            filtered_sentiment_data_df = sentiment_data_df[['company_name', 'job_position_category', 'weighted_score_mean', candidate_preferences['priority']+'_score_mean']]
            filtered_sentiment_data_df['company_name'] = filtered_sentiment_data_df['company_name'].apply(lambda x: x.lower())
            filtered_sentiment_data_df.rename(columns={'company_name':'company_name_mapped', 'job_position_category': 'job_title_lower', 'weighted_score_mean': 'sentiment_and_rating_score', candidate_preferences['priority']+'_score_mean': 'priority_score'}, inplace=True)
        else:
            filtered_sentiment_data_df = sentiment_data_df[['company_name', 'job_position_category', 'weighted_score_mean']]
            filtered_sentiment_data_df['company_name'] = filtered_sentiment_data_df['company_name'].apply(lambda x: x.lower())
            filtered_sentiment_data_df.rename(columns={'company_name':'company_name_mapped', 'job_position_category': 'job_title_lower', 'weighted_score_mean': 'sentiment_and_rating_score'}, inplace=True)
            filtered_sentiment_data_df['priority_score'] = 0
        final_df = filtered_df.merge(filtered_sentiment_data_df, on=['company_name_mapped', 'job_title_lower'], how='left')
        final_df[['sentiment_and_rating_score', 'priority_score']] = final_df[['sentiment_and_rating_score', 'priority_score']].fillna(0)
    
    ### Rank the job based on how similar the skillsets are when comparing resume and job description + the glassdoor company sentiment analysis and_rating score analysis score (50%) + priority rating score (50%)
    final_df['BOW_cosine_similarity_score_exist'] = final_df['BOW_cosine_similarity_score'].apply(lambda x: 1/3 if x != 0 else 0)
    final_df['sentiment_and_rating_score_exist'] = final_df['sentiment_and_rating_score'].apply(lambda x: 1/3 if x != 0 else 0)
    final_df['priority_score_exist'] = final_df['priority_score'].apply(lambda x: 1/3 if x != 0 else 0)
    
    final_df['final_score'] = final_df.apply(lambda x: ((x['BOW_cosine_similarity_score'] * (1/3)) + (x['sentiment_and_rating_score'] * (1/3)) + (x['priority_score'] * (1/3))) / (x['BOW_cosine_similarity_score_exist'] + x['sentiment_and_rating_score_exist'] + x['priority_score_exist']) if (x['BOW_cosine_similarity_score_exist'] + x['sentiment_and_rating_score_exist'] + x['priority_score_exist']) > 0 else 0, axis=1)
    
    final_df.sort_values(['final_score'], ascending=False)
    
    final_df['job_title'] = final_df['original_job_title']
    final_df.drop(['original_job_title'], axis=1, inplace=True)
    
    if final_df.shape[0] > 0:
        top_5_jobs = final_df.sort_values(['final_score'], ascending=False).head(5)
    else:
        top_5_jobs = data_df.head(5)
    return top_5_jobs.to_json(orient='records')