FROM python:3.14-slim

RUN apt update && apt install -y nginx redis-server supervisor && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip install uv

WORKDIR /srv

COPY . .

RUN uv sync --locked --no-dev

ENV PATH="/srv/.venv/bin:$PATH"

RUN DJANGO_STATIC_ROOT=/var/www/html/static/ python manage.py collectstatic --noinput

EXPOSE 8000

# CMD ["bash", "-c", "nginx && redis-server --daemonize yes && gunicorn -w 5 src.wsgi:application -b 0.0.0.0:8000"]
CMD ["/usr/bin/supervisord"]
