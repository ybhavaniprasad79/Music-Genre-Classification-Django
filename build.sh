#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install numpy first (required by scikit-learn 0.22.1)
pip install "numpy>=1.18.0"

# Install all other requirements
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
