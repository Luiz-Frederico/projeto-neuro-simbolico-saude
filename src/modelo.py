import keras
import numpy as np
import os

MODEL_PATH = "models/modelo_saude_6classes_l2_1000ep_v2.keras"

_modelo = None

def carregar_modelo():
    global _modelo
    if _modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
        # Carrega nativamente usando o Keras 3 instalado
        _modelo = keras.models.load_model(MODEL_PATH)
        print("✅ Modelo carregado com sucesso no Keras 3!")
    return _modelo

def predizer(temperatura, bpm):
    modelo = carregar_modelo()
    temp_norm = temperatura / 43.0
    bpm_norm = bpm / 180.0
    entrada = np.array([[temp_norm, bpm_norm]])
    probabilidades = modelo.predict(entrada, verbose=0)[0]
    return probabilidades