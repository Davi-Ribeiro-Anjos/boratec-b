#!/bin/sh

git restore .

git pull origin main

. venv/bin/activate

python manage migrate

sudo systemctl restart nginx

sudo systemctl status nginx

deactivate