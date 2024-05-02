FROM python:3.12.2-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8100

CMD [ "python", "server.py"]