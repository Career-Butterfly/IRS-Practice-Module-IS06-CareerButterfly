# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install the required Python libraries
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./CVandResumeGenerator ./CVandResumeGenerator

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py
ENV OPEN_AI_KEY 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

# Run Gunicorn with Flask app
CMD gunicorn --bind 0.0.0.0:8000 CVandResumeGenerator:app
