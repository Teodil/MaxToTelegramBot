FROM python:3.14-slim

RUN apt-get update && apt-get install -y bash curl netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["sh", "-c", "while ! nc -z kafka 9092; do echo 'Waite for Kafka...'; sleep 2; done; python -m app.main"]
