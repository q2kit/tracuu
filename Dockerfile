FROM python:3.12-slim

RUN apt update && apt install -y nginx && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf

RUN pip install uv

WORKDIR /srv

COPY . .

RUN uv sync --locked

ENV PATH="/srv/.venv/bin:$PATH"

RUN DJANGO_STATIC_ROOT=/var/www/html/static/ python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "nginx && gunicorn -w 5 project.wsgi:application -b 0.0.0.0:8000"]
