import keras
from keras import layers, regularizers
import numpy as np
import os

# Caminho para o novo arquivo de pesos limpos
WEIGHTS_PATH = "models/modelo_saude_6classes_pesos.weights.h5"

_modelo = None

def construir_e_carregar_modelo():
    global _modelo
    if _modelo is None:
        if not os.path.exists(WEIGHTS_PATH):
            raise FileNotFoundError(f"Arquivo de pesos não encontrado em {WEIGHTS_PATH}")
        
        # 1. Reconstrói exatamente a arquitetura da sua rede
        model = keras.Sequential([
            layers.Input(shape=(2,)),
            layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.0001)),
            layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.0001)),
            layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.0001)),
            layers.Dense(6, activation='softmax')
        ])
        
        # 2. Injeta os pesos puramente matemáticos salvos do Colab
        model.load_weights(WEIGHTS_PATH)
        _modelo = model
        print("🧠 [Sucesso] Arquitetura reconstruída e pesos carregados perfeitamente!")
        
    return _modelo

def predizer(temperatura, bpm):
    modelo = construir_e_carregar_modelo()
    temp_norm = temperatura / 43.0
    bpm_norm = bpm / 180.0
    entrada = np.array([[temp_norm, bpm_norm]])
    probabilidades = modelo.predict(entrada, verbose=0)[0]
    return probabilidades