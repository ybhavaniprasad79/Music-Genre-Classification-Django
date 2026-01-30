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
            # Pre-compile librosa utility functions
            librosa.util.valid_audio(np.array([0, 1, 0]), mono=False)
        except Exception:
            pass  # Ignore warmup errors