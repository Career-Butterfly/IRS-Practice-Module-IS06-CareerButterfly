import requests
import streamlit.components.v1 as components
import streamlit as st

# Define the base URL of your Flask app
base_url = 'http://localhost:8200'

# Define the route endpoint and parameters
route = '/generate_learning_resource_html_format'
resume = """
Programming languages: C/C++, C#, Java, Python, Groovy, JavaScript, Typescript, HTML, CSS, Lua
C+±based frameworks & lib: Imgui, OpenGL, Vulkan, Nvidia PhysX, GLM, Rapidjson, FMod
C#-based frameworks & lib: .Net, WPF
Java-based frameworks & lib: Spring, Maven, JUnit, JPA
Python-based frameworks & lib: Pandas, Numpy, Matplotlib, Seaborn, PyTest, Pyspark, Sci-kit learn, NLTK,
Spacy, XGboost, pytorch, Html2text, pypandoc, Flask, werkzeug, waitress, apriori-python, scikit-surprise
Frameworks & Lib: Selenium, Seleniumbase
Databases: MS SQL, MySQL, Cassandra, SQLite, Neo4j
Cloud: Azure, AWS, Databrick
Game Engine: Unreal Engine, Unity
IDE: VS Code, IntelliJ, Anaconda, Pycharm
Other: PowerShell, bash, Ubuntu, Linux
"""
job_requirement="""
Qualifications

Required/Minimum Qualifications:

Bachelor's Degree in Computer Science, or related technical discipline AND 4+ years technical engineering experience with coding in languages including, but not limited to, C, C++, C#, Java, JavaScript, or Python
OR equivalent experience
A good handle on SQL and Database querying
Preferred Qualifications

Bachelor's Degree in Computer Science or related technical field AND 8+ years technical engineering experience with coding in languages including, but not limited to, C, C++, C#, Java, JavaScript, or Python
OR Master's Degree in Computer Science or related technical field AND 6+ years technical engineering experience with coding in languages including, but not limited to, C, C++, C#, Java, JavaScript, or Python
OR equivalent experience.
Hands-on experience from design through implementation of large-scale distributed data systems, setting examples for good data engineering practices, CI/CD and coding along the way
Proven experience providing technical leadership, drawing insights and communicating (both written and verbal) effectively with stakeholders
Familiarity with the Microsoft Azure cloud or similar experience with another cloud platform
Experience with Spark (Databricks or Synapse) or Modern Data Architectures such as Modern Data Warehouse and Data Mesh
Working with Transactional Systems (either NoSQL or traditional RDBMS)
Flexibility to travel when you believe it would be more efficient and effective to collocate with the customer or ISE engineering crew, and for occasional ISE-wide events (we comply with all local guidelines related to travel and worksite opening related to the Covid-19 pandemic) but also a willingness to work with a geographically-dispersed virtual team
"""

params = {
    'param1': resume,
    'param2': job_requirement,
    'param3': 'microsoft'
}

# Make a GET request to the Flask route with the parameters
response = requests.get(f"{base_url}{route}", params=params)

# Print the response text (or process it in another way)
components.html(response.text, scrolling=True, width=1280, height=720)

# Define the function to handle the download
def download_file():
    # Define the base URL of your Flask app
    #base_url = 'http://144.126.241.79/learning_resource'
    base_url = 'http://localhost:8200'
    # Define the route endpoint and parameters
    route = '/download_learning_resource'
    # Make the GET request to the Flask route
    response = requests.get(f"{base_url}{route}")
    return response.content

# Create the download button in Streamlit
st.download_button(
    label="Download Learning Resource",
    data=download_file(),
    file_name="learning_resource.zip",
    mime="application/zip"
)