
import tf_keras as keras
import numpy as np
import os

# --- PATCH DE COMPATIBILIDADE (Keras 3 -> Keras 2) ---
# Força o tf_keras a aceitar modelos gerados no Keras 3 contendo 'batch_shape' e 'optional'
from tf_keras.layers import InputLayer
_original_input_init = InputLayer.__init__

def _patched_input_init(self, *args, **kwargs):
    if 'batch_shape' in kwargs:
        kwargs['batch_input_shape'] = kwargs.pop('batch_shape')
    if 'optional' in kwargs:
        kwargs.pop('optional')
    _original_input_init(self, *args, **kwargs)

InputLayer.__init__ = _patched_input_init
# -----------------------------------------------------

MODEL_PATH = "models/modelo_saude_6classes_l2_1000ep_v2.keras"

_modelo = None

def carregar_modelo():
    global _modelo
    if _modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
        _modelo = keras.models.load_model(MODEL_PATH)
        print("✅ Modelo carregado com sucesso!")
    return _modelo

def predizer(temperatura, bpm):
    modelo = carregar_modelo()
    temp_norm = temperatura / 43.0
    bpm_norm = bpm / 180.0
    entrada = np.array([[temp_norm, bpm_norm]])
    probabilidades = modelo.predict(entrada, verbose=0)[0]
    return probabilidades