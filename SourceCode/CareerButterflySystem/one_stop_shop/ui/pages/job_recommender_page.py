import streamlit as st
import pandas as pd
import os
import requests
import urllib.parse

def main():
    #set page to be wider
    st.set_page_config(layout='wide')
    create_session_state()
    #split page into 2 columns, column 2 occupies 5 times of space compared to column 1
    col1, col2 = st.columns([1, 5])
    #add button under first column
    with col1:
        back_button=st.button("Previous :arrow_left:")
        if back_button:
            st.switch_page("streamlit_app.py")
            
    with col2:
        #job preference section
        with st.form("Job Preferences"):
            job_preference_container=st.container()
            job_preference_container.header("Job Preference", divider='rainbow')
            job_position_options=['Cloud Engineer', 'AI Engineer', 'Data Analyst', 'Data Scientist', 'Machine Learning Engineer', 'QA Automation Tester', 'Software Engineer', 'Site Reliability Engineer', 'Support Engineer']
            st.session_state.job_title = job_preference_container.selectbox('Job Position: ', job_position_options, index=job_position_options.index(st.session_state.job_title))
            job_location_options=['Islandwide', 'North', 'South', 'East', 'West', 'Central', '']
            st.session_state.job_location = job_preference_container.selectbox("Desired Location", job_location_options, index=job_location_options.index(st.session_state.job_location))
            job_employment_type_options=['contract', 'permanent', '']
            st.session_state.job_employment_type = job_preference_container.selectbox("Desired Employment Type", job_employment_type_options, index=job_employment_type_options.index(st.session_state.job_employment_type))
            job_seniority_options=['fresh/entry level', 'executive', 'junior executive' ,'senior executive', 'manager', 'middle management', 'senior management', 'non-executive', '']
            st.session_state.job_seniority = job_preference_container.selectbox("Desired Seniority Level", job_seniority_options, index=job_seniority_options.index(st.session_state.job_seniority))
            st.session_state.job_experience = job_preference_container.number_input("Required Job Experience (no. of years)", step= 1, value=int(st.session_state.job_experience))
            #st.session_state.job_industry = job_preference_container.selectbox("Desired Job Industry", job_industry_options, job_industry_options.index(st.session_state.job_industry))
            job_priority_options=['work life and flexibility job aspect', 'career development and learning job aspect', 'compensation benefits and security job aspect', 'culture and environment job aspect', 'management and communication job aspect', 'diversity and inclusion job aspect', 'employee engagement and satisfaction job aspect', 'operational efficiency and resources job aspect', 'innovation and strategic vision job aspect', 'global impact and social responsibility job aspect']
            st.session_state.priority = job_preference_container.selectbox('Desired Aspect(s): ', job_priority_options, job_priority_options.index(st.session_state.priority)) 
            #st.session_state.my_preferred_salary=job_preference_container.text_input("Preferred Salary Range: ", st.session_state.my_preferred_salary)
            st.session_state.my_preferred_salary=job_preference_container.number_input('Minimum Salary: ', step= 1000, value=int(st.session_state.my_preferred_salary))
    
            #job priority mappings
            job_priority_mapping={'work life and flexibility job aspect': 'work_life_and_flexibility_job_aspect',
                'career development and learning job aspect': 'career_development_and_learning_job_aspect',
                'compensation benefits and security job aspect': 'compensation_benefits_and_security_job_aspect',
                'culture and environment job aspect': 'culture_and_environment_job_aspect',
                'management and communication job aspect': 'management_and_communication_job_aspect',
                'diversity and inclusion job aspect': 'diversity_and_inclusion_job_aspect',
                'employee engagement and satisfaction job aspect': 'employee_engagement_and_satisfaction_job_aspect',
                'operational efficiency and resources job aspect': 'operational_efficiency_and_resources_job_aspect',
                'innovation and strategic vision job aspect': 'innovation_and_strategic_vision_job_aspect',
                'global impact and social responsibility job aspect': 'global_impact_and_social_responsibility_job_aspect'}
    
            submit_button_get_job_rec = st.form_submit_button(label='Submit')
        
        recommended_jobs = []
        #if submit button, consolidate all necesary information, convert into a suitable structure and send to job recommender service
        if submit_button_get_job_rec:
            st.header("These are the recommended jobs: ", divider='rainbow')
            candidate_preferences_data={
                    'job_title':st.session_state.job_title,
                    'salary_range': str(st.session_state.my_preferred_salary),
                    'job_location': st.session_state.job_location,
                    'job_employment_type': st.session_state.job_employment_type,
                    'job_seniority': st.session_state.job_seniority,
                    'job_experience': st.session_state.job_experience,
                    'job_industry': st.session_state.job_industry,
                    'priority': job_priority_mapping.get(st.session_state.priority)
                }
            data_to_send={
                    "candidate_preferences":candidate_preferences_data,
                    "resume_info": st.session_state.resume_data
                }
            get_request_query = convert_dict_to_get_request(data_to_send)
            response = requests.get(get_request_query)
            if response.status_code == 200:
                st.session_state.recommended_jobs=response.json()
            else:
                st.session_state.recommended_jobs=recommended_jobs
        #parse and display each recommended job
        for company_details in st.session_state.recommended_jobs:
            if company_details.get("company_name") is not None:
                with st.expander(label=company_details.get("company_name")):
                    st.subheader("Job Title", divider="gray")
                    st.code(company_details.get("job_title"), language="markdown")
                    st.subheader("Job Location", divider="gray")
                    st.code(company_details.get("job_location"), language="markdown")
                    st.subheader("Job Employment Type", divider="gray")
                    st.code(company_details.get("job_employment_type"), language="markdown")
                    st.subheader("Job Seniority", divider="gray")
                    st.code(company_details.get("job_seniority"), language="markdown")
                    st.subheader("Job Experience Level", divider="gray")
                    st.code(company_details.get("job_experience_level"), language="markdown")
                    st.subheader("Job Industry", divider="gray")
                    st.code(company_details.get("job_industry"), language="markdown")
                    st.subheader("Salary Range", divider="gray")
                    st.code(company_details.get("job_salary_range").replace("to", " to "), language="markdown")
                    st.subheader("Number of Applications", divider="gray")
                    st.code(company_details.get("job_post_start_date"), language="markdown")
                    st.subheader("Application Closing Date", divider="gray")
                    st.code(company_details.get("job_post_close_date_list"), language="markdown")
                    st.subheader("Job Description", divider="gray")
                    st.code(company_details.get("job_description"), language="markdown")
                    st.subheader("", divider="gray")
                    select_button=st.button("Select This Job", key="select_job_" + str(st.session_state.recommended_jobs.index(company_details)))
            
                if select_button:
                    st.session_state.selected_job_company = company_details.get("company_name")
                    st.session_state.selected_job_description = company_details.get("job_description")
                    st.session_state.selected_job_title = company_details.get("job_title")
                    #switch to learning page
                    st.switch_page("pages/learning_page.py")     

def convert_dict_to_get_request(data_to_send):
    #dict1 = str(data_to_send['candidate_preferences']).replace('{', '%7B').replace('}', '%7D').replace('"', '%22').replace('[', '%5B').replace(']', '%5D').replace("'", '%27').replace("’", '').replace('#', '%23')
    #dict2 = str(data_to_send['resume_info']).replace('{', '%7B').replace('}', '%7D').replace('"', '%22').replace('[', '%5B').replace(']', '%5D').replace("'", '%27').replace("’", '').replace('#', '%23')
    
    dict1 = urllib.parse.quote(str(data_to_send['candidate_preferences']))
    dict2 = urllib.parse.quote(str(data_to_send['resume_info']))
    
    final_query = os.environ["JOB_RECOMMENDER"] + '?candidate_preferences=' + dict1 + '&' + 'resume_info=' + dict2
    return final_query

#initialize session state
def create_session_state():
    session_state_keys=["my_preferred_salary", "job_title", "job_location", "job_employment_type", "job_seniority", "job_experience", "job_industry", "priority", "recommended_jobs", "selected_job_company", "selected_job_description", "selected_job_title"]
    for key in session_state_keys:
        if (key == "job_experience") & (key not in st.session_state):
            st.session_state[key] = 0
        elif (key == "my_preferred_salary") & (key not in st.session_state):
            st.session_state[key] = 0
        elif (key == "recommended_jobs") & (key not in st.session_state):
            st.session_state[key] = []
        elif (key == "job_title") & (key not in st.session_state):
            st.session_state[key] = "Cloud Engineer"
        elif (key == "priority") & (key not in st.session_state):
            st.session_state[key] = "work life and flexibility job aspect"
        elif (key not in st.session_state):
            st.session_state[key] = "" 
                             
if __name__ == "__main__":
    main()