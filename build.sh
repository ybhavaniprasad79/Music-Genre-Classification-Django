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

# Aggressive pre-warming: compile librosa functions to avoid timeout
python << 'PYTHON_EOF'
import os
import librosa
import numpy as np

print('Pre-warming librosa functions...')
test_signal = np.random.randn(22050)

try:
    librosa.onset.onset_strength(y=test_signal, sr=22050)
    librosa.beat.tempo(onset_envelope=np.random.randn(100), sr=22050)
    librosa.feature.spectral_centroid(y=test_signal, sr=22050)
    librosa.feature.mfcc(y=test_signal, sr=22050)
    print('✓ Librosa JIT cache pre-warmed successfully')
except Exception as e:
    print(f'⚠ Warmup incomplete (non-critical): {e}')
PYTHON_EOF
