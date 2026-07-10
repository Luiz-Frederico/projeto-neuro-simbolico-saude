import keras
import numpy as np
import os

# Aponta para o novo arquivo convertido
MODEL_PATH = "models/modelo_saude_6classes_l2_1000ep_v2.h5"

_modelo = None

def carregar_modelo():
    global _modelo
    if _modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
        # Carrega o formato .h5 de forma estável
        _modelo = keras.models.load_model(MODEL_PATH)
        print("✅ Modelo H5 carregado com sucesso!")
    return _modelo

def predizer(temperatura, bpm):
    modelo = carregar_modelo()
    temp_norm = temperatura / 43.0
    bpm_norm = bpm / 180.0
    entrada = np.array([[temp_norm, bpm_norm]])
    probabilidades = modelo.predict(entrada, verbose=0)[0]
    return probabilidades