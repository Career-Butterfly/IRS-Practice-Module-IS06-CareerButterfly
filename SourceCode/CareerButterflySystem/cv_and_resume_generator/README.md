# CV And Resume Generator
This is a CV and Resume Generator that operates based on openai GPT model.

# Dockerfile
The Dockerfile located in the same directory as this README contains the following environment variables that can be modified as required:
- `OPEN_AI_KEY` key to utilize the openai API

# Deployment
This application is designed to be deployed as a Docker container. To deploy the application, open a command terminal in the same directory as this README:
```
docker compose up -d
```

The application will be accessible via http://localhost:8000/.

# Routes
This application has three routes: ping, generate_cv, generate_resume. 

## Ping Route
The ping route is used to simply check whether the service is up and running.

```
http://localhost:8000/ping
```
This should return a message: "cv and resume generator is up and running...".

## Generate CV Route
The generate_cv route is used to generate a cv based on the information provided to it. Send a POST request to the following:

```
http://localhost:8000/generate_cv
```
Provide the following data as a JSONObject along with the request:
```
{
    "company_name": "Google",
    "role": "Software Developer",
    "contact_person": "Technical Hiring Manager",
    "name": "John Doe",
    "email": "JohnDoe@gmail.com",
    "mobile_number": "12345678",
    "skills": ["Java", "Python", "SPARQL", "SQL"],
    "linkedin_profile": "https://www.linkedin.com/in/john-doe-123456789",
    "job_description": "Knowledge graph engineering, digital twin applications.",
    "passion": "Want to create new and innovative solutions"
  }
```
This will return a JSONObject similar to the following:
```
{
    "generated_txt": "\n\n[Your Name]\n[Address]\n[City, State ZIP Code]\n[Email Address]\n[Today’s Date]\n\n[Manager’s Name]\nHiring Manager\nGoogle\n[Address]\n[City, State ZIP Code]\n\nDear [Manager’s Name],\n\nI am writing to express my interest in the Software Developer position at Google, as advertised on your company’s career website. With a strong background in software development and a passion for innovation, I am confident that I possess the skills and qualities necessary to excel in this role.\n\nWith [X] years of experience in software development, I have honed my skills in various programming languages including Java, Python, SPARQL, and SQL. These skills have enabled me to develop efficient and user-friendly applications, as well as troubleshoot and maintain existing systems. My experience also includes working with knowledge graph engineering and digital twin applications, which align perfectly with the requirements of the Software Developer role at Google.\n\nFurthermore, I am constantly seeking opportunities to challenge myself and expand my knowledge. I am particularly excited about the opportunity to work at Google, a company renowned for its cutting-edge technology and innovative solutions. I am confident that my skills, combined with the resources and support provided by Google, will enable me to make valuable contributions towards the development of new and innovative solutions.\n\nI am highly motivated, a quick learner, and possess excellent problem-solving skills. My passion for creating impactful technology solutions drives me to constantly seek new challenges and push boundaries. I am confident that I would thrive in the fast-paced and dynamic environment at Google, and be a valuable asset to your team.\n\nI am excited about the possibility of joining the Google team and contributing to the company’s continued success. I would welcome the opportunity to discuss my qualifications with you in more detail. Thank you for considering my application. I have attached my resume for your review and kindly refer to my LinkedIn profile for additional information.\n\nSincerely,\n[Your Name]"
}
```

## Generate Resume Route
The generate_resume route is used to generate a resume based on the information provided to it. Send a POST request to the following:

```
http://localhost:8000/generate_resume
```
The generate_resume route accepts a JSONObject containing keys and values relevant to the content of a resume. For example:
```
{
    "name": "John Doe",
    "email": "JohnDoe@gmail.com",
    "mobile_number": "12345678",
    "linkedin_profile": "https://www.linkedin.com/in/john-doe-123456789",
    "skills": ["Java", "Python", "SPARQL", "SQL"],
    "education": {
        "degree_1": {
            "degree_title": "Bachelor in Computer Science",
            "degree_years": "2019 to 2022",
            "university": "NUS"
        }
    },
    "works_experiences": {
        "job_1": {
            "company_name": "Tech pte ltd",
            "job_title": "Software Developer",
            "job_tenure_period": "2022 to present",
            "job_description": "Create dockerized applications with Java"
        }
    }
}
```
This will return a JSONObject similar to the following:
```
{
    "generated_txt": "\n\nJohn Doe\nJohnDoe@gmail.com \n12345678 \nhttps://www.linkedin.com/in/john-doe-123456789 \n\nSkills:\n- Java\n- Python\n- SPARQL\n- SQL \n\nEducation:\nBachelor in Computer Science\nNUS\n2019 to 2022 \n\nWork Experience:\nSoftware Developer\nTech pte ltd\n2022 to present\nCreate dockerized applications with Java"
}
```