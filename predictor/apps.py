from django.apps import AppConfig
from django.conf import settings
import os
import pickle

class PredictorConfig(AppConfig):
    name = 'predictor'
    # create path to models
    
    def ready(self):
        """Pre-warm numba JIT cache on startup to avoid timeout on first audio load"""
        try:
            import librosa
            import numpy as np
            
            # Pre-compile the heavy functions used in audio processing
            test_signal = np.random.randn(22050)  # 1 second at 22050 Hz
            
            # Pre-warm onset detection (this is the expensive one)
            _ = librosa.onset.onset_strength(y=test_signal, sr=22050)
            _ = librosa.beat.tempo(onset_envelope=np.random.randn(100), sr=22050)
            
            print("✓ Numba cache pre-warmed successfully")
        except Exception as e:
            print(f"⚠ Numba warmup warning (non-critical): {e}")
