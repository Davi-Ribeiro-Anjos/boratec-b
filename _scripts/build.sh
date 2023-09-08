#!/bin/sh

set -e

clear

python3 manage.py runserver 0.0.0.0:8001

rm -rf ./__pycache__