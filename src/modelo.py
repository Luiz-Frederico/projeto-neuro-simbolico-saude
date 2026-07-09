import tensorflow as tf
import numpy as np
import os

# Isso é ESSENCIAL para carregar modelos salvos com Keras 3
tf.keras.config.enable_unsafe_deserialization()

MODEL_PATH = "models/modelo_saude_6classes_l2_1000ep_v2.keras"

_modelo = None

def carregar_modelo():
    global _modelo
    if _modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
        _modelo = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Modelo carregado com sucesso!")
    return _modelo

def predizer(temperatura, bpm):
    modelo = carregar_modelo()
    temp_norm = temperatura / 43.0
    bpm_norm = bpm / 180.0
    entrada = np.array([[temp_norm, bpm_norm]])
    probabilidades = modelo.predict(entrada, verbose=0)[0]
    return probabilidades