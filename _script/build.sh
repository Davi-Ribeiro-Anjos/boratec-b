#!/bin/sh

git restore .

git pull origin main

. venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

sudo systemctl restart gunicorn.service

sudo systemctl status gunicorn.service

deactivate