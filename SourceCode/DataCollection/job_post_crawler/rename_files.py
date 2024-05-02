# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 21:35:34 2024

@author: kuany
"""

import os
import pandas as pd

OLD_DATA_FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/new_data/'
NEW_DATA_FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'

files = [OLD_DATA_FILEPATH + x for x in os.listdir(OLD_DATA_FILEPATH) if '.csv' in x]

mapping_table = {
    'cloud engineer': 'cloud_engineer',
    'AI Engineer': 'data_scientist_or_analyst',
    'data analyst': 'data_scientist_or_analyst',
    'data scientist': 'data_scientist_or_analyst',
    'Machine Learning Engineer': 'data_scientist_or_analyst',
    'qa automation tester': 'qa_automation_tester',
    'software engineer': 'software_engineer',
    'site reliability engineer': 'sre',
    'support engineer': 'support_engineer'
}

extract_filename_job_title = [x.split('/')[-1].split('_')[0] for x in files]
mapped_extract_filename_job_title = [mapping_table[x] for x in extract_filename_job_title]
for each_job_title in list(set(mapped_extract_filename_job_title)):
    each_job_title_df = pd.DataFrame()
    for file, old_file_name, new_file_name in zip(files, extract_filename_job_title, mapped_extract_filename_job_title):
        if each_job_title == new_file_name:
            temp_df = pd.read_csv(file)
            temp_df['original_job_title'] = old_file_name
            each_job_title_df = pd.concat([each_job_title_df, temp_df], axis=0)
    each_job_title_df = each_job_title_df.iloc[:, 1:]
    each_job_title_df.reset_index(drop=True, inplace=True)
    each_job_title_df = each_job_title_df.drop_duplicates()
    each_job_title_df.reset_index(inplace=True)
    each_job_title_df.to_csv(NEW_DATA_FILEPATH + each_job_title + '.csv', index=False)