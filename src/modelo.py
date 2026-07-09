"""
src/modelo.py
Responsável por carregar o modelo treinado e fornecer a função de predição.
"""

import tensorflow as tf
import numpy as np
import os

# Caminho relativo ao modelo (a partir da raiz do projeto)
MODEL_PATH = "models/modelo_saude_6classes_l2_1000ep_v2.keras"

# Carrega o modelo uma única vez (singleton)
_modelo = None

def carregar_modelo():
    """Carrega o modelo do disco, se ainda não estiver carregado."""
    global _modelo
    if _modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
        _modelo = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Modelo carregado com sucesso!")
    return _modelo

def predizer(temperatura, bpm):
    """
    Recebe temperatura e BPM (valores brutos) e retorna as probabilidades para as 6 classes.
    """
    modelo = carregar_modelo()
    # Normaliza os dados (mesmo padrão do notebook)
    temp_norm = temperatura / 43.0
    bpm_norm = bpm / 180.0
    entrada = np.array([[temp_norm, bpm_norm]])
    probabilidades = modelo.predict(entrada, verbose=0)[0]
    return probabilidades