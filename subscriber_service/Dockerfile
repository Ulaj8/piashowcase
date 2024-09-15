FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y sqlite3

COPY . .

CMD ["python", "subscriber_service.py"]
