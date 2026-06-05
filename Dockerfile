FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir django==5.2

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py demo_init && python manage.py runserver 0.0.0.0:8000"]
