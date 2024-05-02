import random
import string
import streamlit as st
from utils import resume_parser
# Main App
def main(): 
    #set page to be wider
    st.set_page_config(layout='wide')
    
    #create session state that stores the widget values
    create_session_state()
    st.title("One Stop Shop 👨‍💻")
    with st.form(key='upload resume'):    
        uploaded_file = st.file_uploader("Start by uploading your resume (pdf)", type="pdf")
        submit_button_upload_resume = st.form_submit_button(label='Upload resume')
        #if press submit button and there is a selected file, run the resume parser
        if submit_button_upload_resume:
            if uploaded_file is not None:
                for x in range(10):
                    resume_data=resume_parser.get_resume_info(uploaded_file)
                    keys_to_check = ["name", "skill", "degree_1", "job_1"]
                    if all(key in resume_data for key in keys_to_check):
                        if resume_data["skill"].strip() != '' and resume_data["skill"].strip() is not None:
                            break
                st.session_state.resume_data=resume_data
    #parse resume data and display retrieved values in text boxes
    if len(st.session_state.resume_data) > 1:
        with st.form(key='Fill in or modify the following information: '): 
            personal_info_container=st.container()
            personal_info_container.header("Personal Information", divider='rainbow')
            st.session_state.resume_data["name"]=personal_info_container.text_input("Name: ", str(st.session_state.resume_data["name"]).replace("'", ''))
            st.session_state.my_email=personal_info_container.text_input("Email: ", st.session_state.my_email)
            st.session_state.my_mobile_number=personal_info_container.text_input("Mobile Number: ", st.session_state.my_mobile_number)
            st.session_state.resume_data["skill"]=personal_info_container.text_area("Skills: ", str(st.session_state.resume_data["skill"]).replace("'", ''))
            st.session_state.my_linkedin_profile=st.text_input("Linkedln Profile: ", st.session_state.my_linkedin_profile)
            st.session_state.degrees_info=resume_parser.retrieve_degree_info(st.session_state.resume_data)
            
            st.session_state.resume_data.update({"name": st.session_state.resume_data["name"].replace("'", '')})
            st.session_state.resume_data.update({"skill": st.session_state.resume_data["skill"].replace("'", '')})
            #Education container
            st.header("Education", divider='rainbow')           
            education_container=st.container()
            #display a section for each education/degree
            if len(st.session_state.degrees_info) > 0:
                for key in st.session_state.degrees_info:
                    integer = key.split("_")[1]
                    education_container.subheader("", divider="gray")
                    degree_info=st.session_state.degrees_info[key]
                    st.session_state.update({
                        key: {
                            'degree_title': degree_info['degree_title'],
                            'degree_years': degree_info['degree_years'],
                            'university': degree_info['university']
                        }
                    })
                    st.session_state[key]['degree_title']=education_container.text_input("Degree: ", str(st.session_state[key]['degree_title']).replace("'", ''), key="degree_title_" + integer)
                    st.session_state[key]['university']=education_container.text_input("University: ", str(st.session_state[key]['university']).replace("'", ''), key = "university_" + integer)
                    st.session_state[key]['degree_years']=education_container.text_input("Study Period: ", str(st.session_state[key]['degree_years']).replace("'", ''), key = "degree_years_" + integer)
                    #update session states
                    updated_education = {key: [{
                            'degree_title': str(st.session_state[key]['degree_title']).replace("'", ''),
                            'degree_years': str(st.session_state[key]['university']).replace("'", ''),
                            'university': str(st.session_state[key]['degree_years']).replace("'", '')
                        }]}
                    st.session_state.resume_data.update(updated_education)
                    
            st.session_state.work_experiences_info=resume_parser.retrieve_work_info(st.session_state.resume_data)
            #Work Experience container
            st.header("Work Experience", divider='rainbow')
            work_experience_container=st.container()
            #display a section for each work experience
            if len(st.session_state.work_experiences_info) > 0:
                for key in st.session_state.work_experiences_info:
                    integer = key.split("_")[1]
                    work_experience_container.subheader("", divider="gray")
                    work_info=st.session_state.work_experiences_info[key]
                    st.session_state.update({
                        key: {
                            'company_name': work_info['company_name'],
                            'job_title': work_info['job_title'],
                            'job_tenure_period': work_info['job_tenure_period'],
                            'job_description': work_info['job_description']
                        }
                    })
                    st.session_state[key]['company_name']=work_experience_container.text_input("Company: ", str(st.session_state[key]['company_name']).replace("'", ''), key="company_name_" + integer)
                    st.session_state[key]['job_title']=work_experience_container.text_input("Job Title: ", str(st.session_state[key]['job_title']).replace("'", ''), key="job_title_" + integer)
                    st.session_state[key]['job_tenure_period']=work_experience_container.text_input("Tenure Period: ", str(st.session_state[key]['job_tenure_period']).replace("'", ''), key="job_tenure_period_" + integer)
                    st.session_state[key]['job_description']=work_experience_container.text_area("Job Description: ", str(st.session_state[key]['job_description']).replace("'", ''), key="job_description_" + integer)     
                    #update session state
                    updated_work_experience = {
                        key: [{
                            'company_name': str(work_info['company_name']).replace("'", ''),
                            'job_title': str(work_info['job_title']).replace("'", ''),
                            'job_tenure_period': str(work_info['job_tenure_period']).replace("'", ''),
                            'job_description': str(work_info['job_description']).replace("'", '')
                        }]}
                    st.session_state.resume_data.update(updated_work_experience)
                    
            submit_button_get_job_rec = st.form_submit_button(label='Submit')
        ## switch to job recommender page
        if submit_button_get_job_rec:
            st.switch_page("pages/job_recommender_page.py")
#initialize session states
def create_session_state():
    session_state_keys=["my_name", "my_email", "my_mobile_number", "my_skills", "my_linkedin_profile", "resume_data", "degrees_info", "work_experiences_info"]
    for key in session_state_keys:
        if (key == "resume_data") & (key not in st.session_state):
            st.session_state[key] = {"skill":"*Mandatory* (e.g. Java, Python, SQL)"}
        elif (key == "degrees_info") & (key not in st.session_state):
            st.session_state[key] = {}
        elif (key == "work_experiences_info") & (key not in st.session_state):
            st.session_state[key] = {}
        elif (key == "my_skills") & (key not in st.session_state):
            st.session_state[key] = "*Mandatory* (e.g. Java, Python, SQL)"
        elif (key not in st.session_state):
            st.session_state[key] = ""

if __name__ == "__main__":
    main()
    
    
    