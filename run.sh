cd /srv/tracuu && source .venv/bin/activate && gunicorn -w 5 mypham.wsgi:application -b 0.0.0.0:8000 --daemon && cd -
