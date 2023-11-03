#!/bin/sh

cd ~/backend

. venv/bin/activate

python sync_deliveries.py

deactivate