"""
src/classificador.py
Contém a lógica de classificação neuro-simbólica:
- Mapeamento de classes
- Filtro simbólico (regras clínicas)
- Função principal classificar_paciente()
"""

from src.modelo import predizer

# Mapeamento de classes (sincronizado com o treinamento)
MAPEAMENTO_CLASSES = {
    0: "Hipotermia",
    1: "Saudável",
    2: "Febril",
    3: "Febre",
    4: "Febre Alta",
    5: "Risco Cardiovascular"
}

def classificar_paciente(temperatura, bpm):
    """
    Pipeline neuro-simbólico:
    1. Obtém as probabilidades da rede neural.
    2. Aplica o filtro simbólico baseado em conhecimento médico.
    3. Retorna o diagnóstico, a confiança (garantia) e as probabilidades completas.
    """
    # 1. Obtém probabilidades da rede (bastidores)
    probabilidades = predizer(temperatura, bpm)
    classe_ia = int(probabilidades.argmax())

    # 2. Filtro simbólico (regras estritas)
    # Regra: Hipotermia estrita (<= 35.0°C)
    if temperatura <= 35.0:
        return MAPEAMENTO_CLASSES[0], 1.0, probabilidades

    # Regra: Febril estrito (37.50 a 37.79°C)
    if 37.50 <= temperatura <= 37.79:
        return MAPEAMENTO_CLASSES[2], 1.0, probabilidades

    # Regra: Febre estrita (37.80 a 38.99°C)
    if 37.80 <= temperatura <= 38.99:
        return MAPEAMENTO_CLASSES[3], 1.0, probabilidades

    # Regra: Febre Alta estrita (>= 39.0°C)
    if temperatura >= 39.0:
        return MAPEAMENTO_CLASSES[4], 1.0, probabilidades

    # Zona térmica estável (35.01 a 37.49°C)
    if 35.01 <= temperatura <= 37.49:
        if 60.0 <= bpm <= 100.0:
            return MAPEAMENTO_CLASSES[1], 1.0, probabilidades
        else:
            return MAPEAMENTO_CLASSES[5], 1.0, probabilidades

    # Fallback (segurança)
    return MAPEAMENTO_CLASSES[classe_ia], probabilidades[classe_ia], probabilidades