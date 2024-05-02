from openai import OpenAI
from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)
client = OpenAI(api_key = os.environ["OPEN_AI_KEY"].strip())

# Show an instructional message at the app root
@app.route('/')
def default():
    logging.info("Executing default route...")
    msg  = "cv and resume generator is up and running..."
    return msg

@app.route('/ping', methods=['GET'])
def ping():
    logging.info("Executing ping route...")
    msg  = "cv and resume generator is up and running..."
    return msg

@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    logging.info("Executing generate CV route...")
    # Parse the request data as JSON
    request_data = request.get_json()
    
    prompt_str = prompt_generation_cv(request_data["name"], request_data["email"], request_data["mobile_number"], request_data["linkedin_profile"], str(request_data["skills"]), request_data["contact_person"],
                         request_data["company_name"], request_data["role"], request_data["job_description"], request_data["passion"])
    
    generated_cv_txt = instruct_model(client, prompt_str)
    
    response_data = {"generated_txt": generated_cv_txt}
    
    return jsonify(response_data)

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    logging.info("Executing generate resume route...")
    # Parse the request data as JSON
    request_data = request.get_json()
    
    prompt_str = prompt_generation_resume(request_data)
    
    generated_cv_txt = instruct_model(client, prompt_str)
    
    response_data = {"generated_txt": generated_cv_txt}
    
    return jsonify(response_data)

def prompt_generation_cv(name, email, mobile_number, linkedin_profile, skills, contact_person, company_name, role, job_description, passion):
    prompt_str = ("Write a cover letter to " + contact_person + " for a " + role + " job at " + company_name +"." + "My name is " + name +", my email is " + email + " . My mobile numer is " + mobile_number + " . My linkedln profile is " + linkedin_profile + " . My skills are " + skills + " . I am excited about the job because " + job_description + " I am passionate about "+ passion + " . Do not assume anything and replace any missing information with [placeholders].")
    return prompt_str

def prompt_generation_resume(data_dump):
    prompt_str=("Write a structured and professional resume with the following information: " + str(data_dump) + ", extract the information from the json object provided. Do not assume any missing information and instead replace them with [placeholders]. ")
    return prompt_str

#def prompt_generation_resume(name, email, mobile_number, linkedin_profile, skills, degree, major, university, gpa):
#    data_dump = {"name": name, "email":email, "mobile number": mobile_number, "skills": skills, "linkedln profile":linkedin_profile, "degree":degree, "major":major, "university":university, "gpa":gpa}
#    prompt_str=("Write a structured and professional resume with the following information: " + str(data_dump) + ", extract the information from the json object provided. Do not assume any missing information and instead replace them with [placeholders]. ")
#    return prompt_str

def instruct_model(client, prompt_str):
        # The Model
        response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt_str, max_tokens=1949, temperature=0.99, user="user")
        print("The response is " + response.choices[0].text)
        text = response.choices[0].text
        print("Prompt:", prompt_str)
        print("Response:", text)
        return text
    
if __name__ == "__main__":
    app.run()