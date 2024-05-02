### <<<<<<<<<<<<<<<<<<<< Start of Template >>>>>>>>>>>>>>>>>>>>

IRS-PM-2024-01-13-IS06PT-CareerButterfly

---

## SECTION 1 : PROJECT TITLE
## CareerButterfly - The One Stop Shop for your Tech Career

![image](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/Miscellaneous/System%20design.png)

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Layoffs are becoming a disturbing norm. Despite frequent layoffs, the median gross salary income for full-time employees in the Information and Communications sector is still on the rise. With the increasing demand for jobs and the increasing gross salary in the technology sector, getting a job the technology sector becomes increasingly more competitive. While there are many individual tools to help a job seeker in their path to search for a job that fits them, there is not a single platform that combines all the tools together and streamlines the processes to help ease the job-hunting process. This project aims to develop a single platform to streamline this process.

This project develops a single platform application built on Streamlit and uses microservices to recommend jobs fitted to user preferences, generate cover letter, resume and learning resources for our users, and provides an interactive behavioural interview chatbot for mock interview sessions. 

This project makes use of recommendation system, knowledge-based reasoning techniques and uses Large Language Model (LLM) and prompt engineering to develop a chatbot and generate documents detailed in the following pointers:

* **Job recommender** is a *recommendation system* that uses a weighted average score based on cosine similarity between user resume and job description, user review sentiment and user’s company rating score from company reviews and ratings, and user preference score from company reviews.

* **Cover letter generator and resume generator** both *use LLM and well-crafted effective prompts* that acts as instruction to guide the LLM to achieve the desired output customised for their application.

* **Learning resources recommender** uses *knowledge-based reasoning techniques* to recommend learning resources and generate learning resources document for the user to bridge the knowledge gap.

* **Behavioural question interview chatbot** is developed with the help of *LLM and prompt engineering* that identifies possible behavioural questions for user to practice in mock interview sessions with the chatbot and provides timely feedback to user on how to improve their answers in the future.


This project combines multiple job seeking tools together in a single platform and helps to streamline the process of finding a job suitable for our users in a timely manner. 


---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Soo Kuan Yong | A0291188U | Project Ideation, <br />Project Proposal Document, <br />Project Report(4 days), <br />Team management, <br />Develop Job Posts Web Crawler (3 days), <br />Develop Job Recommender (3 days), <br />Develop Resume Parser (1 day), <br />Develop Behavioural Interview Chatbot (1 day), <br />Integrate, Testing and Fine Turing (2 days) | e1330327@u.nus.edu |
| Zachary Chua Feng Kwan | A0180556B | Project Ideation, <br />Project Proposal Document, <br />Project Report(1 day), <br />Design and implementation of “Glassdoor Web Crawler” (3 days), <br />Design and implementation of “Company Sentiment Analysis” (2 days), <br />Explore cloud solutions (1 day), <br />Setup CI/CD pipeline (2 days), <br />Deployment and resolve deployment issues (5 days) | zacharychua@u.nus.edu |
| Ang Han Chuan Wilson | A0291657R | Project Ideation, <br />Project Proposal Document, <br />Promotion Video (2 days),<br />Research on Streamlit and openai functionalities (2 days), <br />CV and Resume Generator (2 days), <br />UI design and structure (3 days), <br />Integrate and fine tune resume parser and interviewer chatbot into UI (2 days), <br />Integrate, Testing and Fine Tuning of UI (3 days) | e1333153@u.nus.edu |
| Ng Min Teck | A0291213N | Project Ideation, <br />Project Proposal Document, <br />Technical Video (2 days),<br />Technical Skill Keyword Data Collection (3 days), <br />Learning Resource LLM Prompting and Scraping (4 days), <br />Implement Learning Resource Service (2 days), <br />Integrate, Testing and Fine Tuning (3 days) | ng_min_teck@u.nus.edu |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

Promotion Video: [[Youtube Promotion Video link]](https://youtu.be/d3A04fAH4ys)

Tech Video: [[Youtube Technical Video link]](https://youtu.be/QLvNFoyTtro)

---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`

[ProjectReport](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/tree/main/ProjectReport)

### [ 1 ] [CareerButterfly System](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/CareerButterflySystem/README.md)
---

#### Pre-requisite
* Docker desktop - https://www.docker.com/products/docker-desktop/
* OpenAI API Key - https://platform.openai.com/docs/quickstart
---

#### Setup
* Create a OpenAI API Key and navigate to the following Dockerfiles located at `SourceCode/CareerButterflySystem/cv_and_resume_generator/Dockerfile` and `SourceCode/CareerButterflySystem/one_stop_shop/Dockerfile`, replace and insert your API Key at the following line:
```
ENV OPEN_AI_KEY <API Key>
```
* Navigate to project directory
  > ```cd SourceCode/CareerButterflySystem```
* Build docker images with docker compose
  > ```docker compose up```
* The image below illustrates the connected containers and volumes in the docker compose
  * ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/CareerButterflySystem/docker_compose_architecture.png) 
* Navigate to url, `http://localhost:8501`, with browser
* The following diagram outlines the process flow chart of using the application
  > ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/CareerButterflySystem/streamlit_flowchart.png)
---

## Environment variables
Each individual project may have one or more environment variables. The environment variables are hardcoded into their respective Dockerfile. The following are the environment variables that you may choose to change.
* cv_and_resume_generator
  * OPEN_AI_KEY
    > The api key from OpenAI.
  <br/><b>Note: If you encounter "invalid key" error from OpenAI, you will need to replace it with your own OpenAI api key </b>
* one_stop_shop
  * OPEN_AI_KEY
    > The api key from OpenAI.
  <br/><b>Note: If you encounter "invalid key" error from OpenAI, you will need to replace it with your own OpenAI api key </b>
---

## Volume mounts
Each container, created by docker-compose, may have a volume mount. The volume mount binds the data, that was created by the data collectors.
* sentiment_service
  * `DataCollection/company_review_crawler/data` is mounted to `/data`
* job-recommender
  * `DataCollection/job_post_crawler/data` is mounted to `/data`
* learning-resource-service
  * `DataCollection/learning_resource_crawler/data` is mounted to `/data`
---


### [ 2 ] [Data Collection](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/DataCollection/README.md)
---

#### Pre-requisite
* Conda 23 - https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
* Python 3 - https://www.python.org/downloads/
* Jupyter - https://jupyter.org/install
---

#### Setup
##### 1. Scraping company reviews
  * Navigate to project directory
    > ```cd SourceCode/DataCollection/company_review_crawler```
  * Create conda environment
    > ```conda env create -f environment.yml```
  * Activate conda environment
    > ```conda activate company_review_crawler```
  * Run all cells in `crawl_reviews.ipynb`
    * Note: Results will be saved in the `data` folder which will later be used in ![Rating company reviews](#1.1.-Rating-company-reviews)
  * This diagram outlines the process of collecting company reviews
    * ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/DataCollection/data_collection_company_reviews.png)

##### 1.1. Rating company reviews
  * Run all cells in `company_reviews_sentiment.ipynb`
    * Note: Results will be saved in the `data` folder which will be used by `SourceCode/CareerButterflySystem/sentiment_service`
  * This diagram outlines the process of rating company reviews
    * ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/DataCollection/data_collection_rating_company_reviews.png)

##### 2. Scraping job posts
  * Navigate to project directory
    > ```cd SourceCode/DataCollection/job_post_crawler```
  * Create conda environment
    > ```conda create --name job_post_crawler python=3.10```
  * Activate conda environment
    > ```conda activate job_post_crawler```
  * Install python dependencies
    > ```pip install -r requirements.txt```
  * Create 2 folders and rename them as "new_data" and "data" respectively
    * Note: Ignore this step if folders already exist
  * Run `data_collection_job_information.py`
    > ```python data_collection_job_information.py```
    * Results will be saved in the `new_data` folder which will be used by later in
  * Run `rename_files.py`
    > ```python rename_files.py```
    * Results will be saved in the `data` folder which will be used by `SourceCode/CareerButterflySystem/job_recommender`
  * This diagram outlines the process of collecting job posts
    *  ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/DataCollection/data_collection_job_posts.png)

###### 3. Scraping learning resources
  * Navigate to project directory
    > ```cd SourceCode/DataCollection/learning_resource_crawler```
  * Create conda environment
    > ```conda env create -f environment.yml```
  * Activate conda environment
    > ```conda activate learning_resource_crawler```
  * Run all cells in `leetcode.ipynb`
    * Note: Results will be saved in the `data` folder which will later be used in `SourceCode/CareerButterflySystem/learning_resource_service`
  * Run all cells in `copilot query1.ipynb`
    * Note: Results will be saved in the `data` folder which will later be used in `SourceCode/CareerButterflySystem/learning_resource_service`
  * Run all cells in `CareerFuture Job Description And Tag Scraper.ipynb`
    * Note: Results will be saved in the `data` folder which will later be used in `SourceCode/CareerButterflySystem/learning_resource_service`
  * This diagram outlines the process of collecting for the skill learning resources
    * ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/DataCollection/data_collection_skill_learning_resource.png)
  * This diagram outlines the process of collecting for the leetcode learning resources
    * ![alt text](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/blob/main/UserGuide/DataCollection/data_collection_leetcode_learning_resource.png)

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

[ProjectReport](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/tree/main/ProjectReport)

**Sections in Project Report / Paper:**
- Executive Summary / Paper Abstract
- Market Research
- Project Description (Project Background, Project Objectives, Report Organisation)
- Project Solution (Job Recommender, Resume Generator, Cover Letter Generator, Behavioural Interview Chatbot, Learning Resource Recommender)
- Project Implementation (System Design, Deployment Architecture, Streamlit Application)
- Project Performance & Validation
- Project Conclusion
- Appendix of report: Project Proposal
- Appendix of report: Mapped System Functionalities against knowledge, techniques and skills of modular courses: MR, RS, CGS
- Appendix of report: Installation and User Guide
- Appendix of report: 1-2 pages individual project report per project member, including: Individual reflection of project journey: (1) personal contribution to group project (2) what learnt is most useful for you (3) how you can apply the knowledge and skills in other situations or your workplaces
- Appendix of report: List of Abbreviations
- Appendix of report: List of Figures
- Appendix of report: List of Table
- Appendix of report: References

---
## SECTION 7 : MISCELLANEOUS

`Refer to Github Folder: Miscellaneous`

[Miscellaneous](https://github.com/Career-Butterfly/IRS-Practice-Module-IS06-CareerButterfly/tree/main/Miscellaneous)

### UI Storyboard.pptx
---

### <<<<<<<<<<<<<<<<<<<< End of Template >>>>>>>>>>>>>>>>>>>>

---

**This [Machine Reasoning (MR)](https://www.iss.nus.edu.sg/executive-education/course/detail/machine-reasoning "Machine Reasoning") course is part of the Analytics and Intelligent Systems and Graduate Certificate in [Intelligent Reasoning Systems (IRS)](https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "Intelligent Reasoning Systems") series offered by [NUS-ISS](https://www.iss.nus.edu.sg "Institute of Systems Science, National University of Singapore").**

**Lecturer: [GU Zhan (Sam)](https://www.iss.nus.edu.sg/about-us/staff/detail/201/GU%20Zhan "GU Zhan (Sam)")**

[![alt text](https://www.iss.nus.edu.sg/images/default-source/About-Us/7.6.1-teaching-staff/sam-website.tmb-.png "Let's check Sam' profile page")](https://www.iss.nus.edu.sg/about-us/staff/detail/201/GU%20Zhan)

**zhan.gu@nus.edu.sg**
