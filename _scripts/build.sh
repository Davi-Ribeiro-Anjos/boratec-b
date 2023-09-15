#!/bin/sh

set -e

cd ~/app/

python3 manage.py runserver 0.0.0.0:8000

rm -rf ./__pycache__