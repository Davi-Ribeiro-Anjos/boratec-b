#!/bin/sh

cd ~/backend

. venv/bin/activate

python sync_employees.py

deactivate

cd ~