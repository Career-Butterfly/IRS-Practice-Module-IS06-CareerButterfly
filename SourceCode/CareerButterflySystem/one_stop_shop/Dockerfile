FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install the required Python libraries
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./ui ./ui

#Environment Variables
ENV CV_GENERATOR http://cv-and-resume-generator:8000/generate_cv
ENV RESUME_GENERATOR http://cv-and-resume-generator:8000/generate_resume
ENV JOB_RECOMMENDER  http://job-recommender:4000
ENV LEARNING_RESOURCE_RECOMMENDER http://learning-resource-service:8200
ENV OPEN_AI_KEY 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

EXPOSE 8501

CMD streamlit run ui/streamlit_app.py --client.showSidebarNavigation False
