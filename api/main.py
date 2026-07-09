"""
api/main.py – FastAPI para o classificador neuro-simbólico (versão profissional)
"""

import logging
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any

from src.classificador import classificar_paciente

# --- Configuração de logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Definição do modelo de entrada (com validação) ---
class Paciente(BaseModel):
    temperatura: float = Field(..., ge=30.0, le=43.0, description="Temperatura em °C (30-43)")
    bpm: int = Field(..., ge=20, le=200, description="Frequência cardíaca em BPM (20-200)")

    class Config:
        schema_extra = {
            "example": {
                "temperatura": 36.5,
                "bpm": 75
            }
        }

# --- Definição do modelo de saída ---
class ClassificacaoResponse(BaseModel):
    diagnostico: str
    confianca: float
    probabilidades: Dict[str, float]

# --- Inicialização da aplicação ---
app = FastAPI(
    title="Classificador Neuro-Simbólico API",
    description="""
    API para classificação de risco com base em temperatura corporal e frequência cardíaca.
    
    Utiliza uma abordagem neuro-simbólica:
    - Rede neural MLP para predição probabilística.
    - Filtro simbólico baseado em regras clínicas para decisões seguras.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Configuração de CORS (para permitir requisições do dashboard e outros clientes) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja a origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints ---

@app.get("/", tags=["Status"])
async def root():
    """Endpoint raiz para verificar se a API está ativa."""
    return {"message": "API do Classificador Neuro-Simbólico está ativa.", "version": app.version}

@app.get("/health", tags=["Status"])
async def health_check():
    """Endpoint para verificação de saúde (health check)."""
    return {"status": "healthy"}

@app.post("/v1/classificar", response_model=ClassificacaoResponse, tags=["Classificação"])
async def classificar(paciente: Paciente):
    """
    Classifica um paciente com base na temperatura e frequência cardíaca.
    
    - **temperatura**: valor em °C (30-43)
    - **bpm**: frequência cardíaca em BPM (20-200)
    
    Retorna o diagnóstico, confiança e as probabilidades para cada classe.
    """
    try:
        logger.info(f"Recebida requisição: {paciente.temperatura}°C, {paciente.bpm} BPM")
        
        classe, confianca, probabilidades = classificar_paciente(
            paciente.temperatura, 
            paciente.bpm
        )
        
        # Ajuste visual para hiperpirexia (se aplicável)
        if classe == "Febre Alta" and paciente.temperatura > 41.0:
            classe += " (Hiperpirexia)"
        
        return ClassificacaoResponse(
            diagnostico=classe,
            confianca=confianca,
            probabilidades={
                "Hipotermia": probabilidades[0],
                "Saudavel": probabilidades[1],
                "Febril": probabilidades[2],
                "Febre": probabilidades[3],
                "Febre Alta": probabilidades[4],
                "Risco Cardiovascular": probabilidades[5]
            }
        )
    except Exception as e:
        logger.error(f"Erro na classificação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar a classificação: {str(e)}"
        )