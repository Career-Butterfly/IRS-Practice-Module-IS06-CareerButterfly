FROM python:3.10
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV SENTIMENT_SERVICE http://sentiment-service:8100

EXPOSE 4000

CMD ["python", "server.py"]
