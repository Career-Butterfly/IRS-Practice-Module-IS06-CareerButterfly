import streamlit as st
from openai import OpenAI
from streamlit_chat import message
import os

cleaned_data=st.session_state.resume_data
st.set_page_config(layout='wide')
client = OpenAI(api_key = os.environ["OPEN_AI_KEY"].strip())

### Extract and prepare key information from resume to find similarity with filtered job descriptions
candidate_key_information = [', '.join(list(cleaned_data[key][0].values())) for key, val in cleaned_data.items() if 'job' in key or 'degree' in key]
if len(candidate_key_information) > 1:
    candidate_key_information = ', '.join(candidate_key_information)
candidate_key_information = candidate_key_information + cleaned_data['skill']

#selected_job_description = "Responsibilities\nDemonstrate understanding of the business to identify, analyse and interpret patterns or trends in data sets that help in improving business performance.\nImport data from various external and internal sources to bring meaningful insights into the business.\nBuild and maintain tableau dashboard for departments and management to track key indicators.\nTo write R/Python scrips to transform existing data to obtain approximation of required data.\nIdentify data sources; collect data through manual or automated means; source missing data; clean, transform and organize data into usable format/structure.\nSupport in data flow and process flow documentation and identify gaps.\nRequirements\nA bachelor's degree in a related field such as mathematics, statistics, computer science, economics, or information management is required.\n2 to 5 years of relevant work experience\nStrong analytical skills are essential for interpreting complex data sets and identifying trends, patterns, and insights.\nProficiency in programming languages commonly used in data analysis such as Python, R, SQL, or others.\nExperience with data visualization tools such as Tableau, Power BI, or Matplotlib.\nUnderstanding of mathematical concepts such as probability, calculus, algebra, and statistics is crucial for analysing data effectively.\nUnderstanding of business processes and objectives to provide data-driven recommendations and insights that align with organizational goals.\nFamiliarity with database systems and data querying languages (MS SQL).\nInterested candidates who wish to apply for the advertised position, please click APPLY to submit your resume.\nEA License: 13C6305\nReg. No.: R22108000\nFor candidate who applied for the advertised position is deemed to have consented to us that we may collect, use, or disclose your personal information for purpose in connection with the services provided by us."
selected_job_description = st.session_state.selected_job_description
interview_questions_prompt = '''
Act as a skilled Interviewer with a deep understanding of tech field, software engineering, data science, data analyst and big data engineer.
Your task is to evaluate the resume and given job description to come up with possible interview questions to help your client interviewee to prepare for their upcoming interview.

resume:{0}
job description:{1}

Add the following at the end of your response:
Please provide me with your response, I will evaluate and provide feedback based on your answers.
'''.format(candidate_key_information, selected_job_description)

def set_up_interviewer(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages = [{"role": "assistant", "content":prompt}],
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    )
    message = response.choices[0].message.content
    return message

def api_calling(prompt):
    evaluate_user_prompt = '''
    Act as a skilled Interviewer with a deep understanding of tech field, software engineering, data science, data analyst and big data engineer.
    Evaluate user's interview answer, provide feedback on how they can improve their answers for their upcoming interviews.
    Be kind and encouraging in your response.
    Provide motivational words at the end of the response to help motivate the interviewee.
    interviewee's answer: {0}
    '''.format(prompt)
    messages = [{"role": "assistant", "content": evaluate_user_prompt}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
    message = response.choices[0].message.content
    return message

st.title("Interviewer ChatBot")
if 'user_input' not in st.session_state:
	st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
	st.session_state['openai_response'] = []
 
if 'openai_initial_response' not in st.session_state:
	st.session_state['openai_initial_response'] = []
 
interviewer_response=set_up_interviewer(interview_questions_prompt)
st.session_state.openai_initial_response.append(interviewer_response)

def get_text():
	input_text = st.text_area("write here: e.g. regarding question 1, <my response> ...", key="input")
	return input_text

col1, col2 = st.columns([1, 1])
with col1:        
    back_button=st.button("Previous :arrow_left:")
    if back_button:
        st.switch_page("pages/learning_page.py")
    message(st.session_state['openai_initial_response'][0], 
				avatar_style="miniavs")
with col2:
    user_input = get_text()
    submit_button = st.button("Submit")
    if submit_button or user_input:
        output = api_calling(user_input)
        output = output.lstrip("\n")
        
        # Store the output
        st.session_state.openai_response.append(user_input)
        st.session_state.user_input.append(output)

        message_history = st.empty()
        
        if st.session_state['user_input']:
            for i in range(len(st.session_state['user_input']) - 1, -1, -1):
                message(st.session_state["user_input"][i], 
				    key=str(i),avatar_style="icons")
                message(st.session_state['openai_response'][i], 
				    avatar_style="miniavs",is_user=True,
				    key=str(i) + 'data_by_user')
