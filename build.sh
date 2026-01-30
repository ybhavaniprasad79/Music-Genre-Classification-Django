#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install numpy first (scikit-learn 0.22.1 needs it for building)
pip install "numpy<1.20"

# Install scikit-learn separately with no build isolation
pip install --no-build-isolation "scikit-learn==0.22.1"

# Install remaining requirements
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
