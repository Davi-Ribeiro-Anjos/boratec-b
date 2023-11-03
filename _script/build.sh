#!/bin/sh

git restore .

git pull

. venv/bin/activate

python manage migrate

sudo systemctl restart nginx

sudo systemctl status nginx

deactivate