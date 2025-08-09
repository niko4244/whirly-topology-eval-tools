FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgresql+psycopg2://whirly:whirlypass@db:5432/whirly
ENV SECRET_KEY=supersecretkey

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]