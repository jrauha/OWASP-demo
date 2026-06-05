# Django OWASP Top Ten Vulnerabilities Demo

This Django application is an intentionally vulnerable web app designed to demonstrate [the OWASP Top Ten security risks](https://owasp.org/www-project-top-ten/).

> ⚠️ **DISCLAIMER:**  
> This application is **intentionally insecure** and should **never** be deployed in a production environment. Use it only in isolated or controlled testing environments.

## Run with Docker

```bash
docker build -t owasp-demo .
docker run --rm -p 8000:8000 owasp-demo
```

Then open `http://localhost:8000`.

On startup the container automatically runs database migrations and loads the demo data with `python manage.py demo_init`.

## Run without Docker

Install Python 3.12+ and then run:

```bash
python3 -m pip install "django>=5.2,<6.0"
python3 manage.py migrate
python3 manage.py demo_init
python3 manage.py runserver
```

Then open `http://localhost:8000`.
