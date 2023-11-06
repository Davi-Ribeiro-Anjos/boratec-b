#!/bin/sh

git restore .

git pull origin main

. venv/bin/activate

python manage.py migrate

sudo systemctl restart nginx

sudo systemctl status nginx

deactivate