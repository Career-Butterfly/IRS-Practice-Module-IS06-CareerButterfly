FROM python:3.10
WORKDIR /app

RUN pip install spacy
RUN python -m spacy download en_core_web_lg

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8200

CMD ["python", "learning_resource_service.py"]
