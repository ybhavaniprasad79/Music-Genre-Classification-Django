#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install build dependencies first
pip install "numpy>=1.18.0" "scipy>=0.17.0" "Cython<3.0"

# Install scikit-learn without build isolation
pip install --no-build-isolation "scikit-learn==0.22.1"

# Install all other requirements (skip scikit-learn since already installed)
pip install -r requirements.txt --ignore-installed scikit-learn

python manage.py collectstatic --no-input
python manage.py migrate
