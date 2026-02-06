FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "-c", "python manage.py migrate && python manage.py seed_data && python manage.py createsuperuser --noinput || true && gunicorn portal.wsgi:application --bind 0.0.0.0:8000"]
