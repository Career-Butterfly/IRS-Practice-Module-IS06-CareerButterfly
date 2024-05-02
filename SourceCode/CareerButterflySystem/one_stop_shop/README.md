# One Stop Shop
This is a streamlit application that acts as the UI for the one stop shop. It consists of one main page (`ui/streamlit_app.py`) and multiple pages (`/ui/pages/.`). 

# Dockerfile
The Dockerfile located in the same directory as this README contains the following environment variables that can be modified as required:
- `CV_GENERATOR` endpoint URL for the cv_generator service
- `RESUME_GENERATOR` endpoint URL for the resume_generator service
- `JOB_RECOMMENDER` endpoint URL for the job_recommender service
- `LEARNING_RESOURCE_RECOMMENDER` endpoint URL for the learning_resources_recommender service
- `OPEN_AI_KEY` key to utilize the openai API

# Deployment
This application is designed to be deployed as a Docker container. To deploy the application, open a command terminal in the same directory as this README:
```
docker compose up -d
```

The application will be accessible via http://localhost:8501/.