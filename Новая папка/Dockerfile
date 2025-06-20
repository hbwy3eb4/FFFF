FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/

# --- Production reminders ---
# Для production: убедитесь, что статика собирается (python manage.py collectstatic)
# Для production: настройте MinIO и PostgreSQL в docker-compose.yml 