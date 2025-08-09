FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgresql+psycopg2://authuser:authpass@db:5432/authdb
ENV SECRET_KEY=supersecretkey

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]