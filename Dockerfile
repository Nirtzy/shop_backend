FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.main
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]