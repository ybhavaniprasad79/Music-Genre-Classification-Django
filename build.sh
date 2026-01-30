#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install build dependencies first
pip install wheel setuptools "Cython<3.0"
pip install "numpy<1.20" "scipy<1.6"

# Install scikit-learn separately with no build isolation
pip install --no-build-isolation "scikit-learn==0.22.1"

# Install remaining requirements
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
# Pre-warm numba cache for librosa to avoid timeout on first request
python -c "import librosa; librosa.util.valid_audio([0, 1, 0], mono=False)" 2>/dev/null || true