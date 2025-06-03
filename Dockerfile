FROM python:3.12-slim

RUN apt update && apt autoremove -y && apt upgrade -y
RUN apt install -y nginx

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /srv

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD gunicorn -w 5 src.wsgi:application -b 0.0.0.0:8000
