FROM python:3.12-slim

RUN apt update && apt install -y nginx && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /srv

COPY . .

RUN uv sync --system

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "nginx && gunicorn -w 5 project.wsgi:application -b 0.0.0.0:8000"]
