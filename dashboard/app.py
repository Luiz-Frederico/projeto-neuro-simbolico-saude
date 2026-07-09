"""
dashboard/app.py – Interface interativa com Streamlit (consumindo a API)
"""

import streamlit as st
import requests
import plotly.graph_objects as go

# --- Configuração da página ---
st.set_page_config(page_title="Classificador Neuro-Simbólico", layout="wide")

st.title("🧠 Classificador Neuro-Simbólico")
st.markdown("### Temperatura + Frequência Cardíaca → Diagnóstico")

# --- URL da API (configurável) ---
# Para desenvolvimento local: http://localhost:8000
# Para deploy: substituir pela URL pública da API
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# --- Entrada de dados ---
col1, col2 = st.columns(2)
with col1:
    temperatura = st.number_input(
        "Temperatura (°C)", 
        min_value=30.0, 
        max_value=43.0, 
        value=36.5, 
        step=0.1
    )
with col2:
    bpm = st.number_input(
        "Frequência Cardíaca (BPM)", 
        min_value=20, 
        max_value=200, 
        value=70, 
        step=1
    )

# --- Botão de classificação ---
if st.button("Classificar", type="primary"):
    with st.spinner("Classificando..."):
        try:
            response = requests.post(
                f"{API_URL}/v1/classificar",
                json={"temperatura": temperatura, "bpm": bpm},
                timeout=10
            )
            
            if response.status_code == 200:
                resultado = response.json()
                diagnostico = resultado["diagnostico"]
                confianca = resultado["confianca"]
                probs = resultado["probabilidades"]

                # Exibe diagnóstico
                if "Hiperpirexia" in diagnostico:
                    st.error(f"**Diagnóstico:** {diagnostico}")
                else:
                    st.success(f"**Diagnóstico:** {diagnostico}")
                
                st.metric("Confiança", f"{confianca*100:.1f}%")

                # Gráfico de barras
                classes = list(probs.keys())
                valores = list(probs.values())
                
                fig = go.Figure(data=[go.Bar(
                    x=classes, 
                    y=valores, 
                    marker_color=['#4CAF50' if v == max(valores) else '#E0E0E0' for v in valores]
                )])
                fig.update_layout(
                    title="Probabilidades por Classe",
                    yaxis_title="Probabilidade",
                    yaxis_range=[0, 1],
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Erro na API: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Não foi possível conectar à API. Certifique-se de que o servidor FastAPI está rodando.")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")

# --- Informações do projeto ---
with st.expander("ℹ️ Sobre este projeto"):
    st.markdown("""
    Este dashboard consome uma API FastAPI que utiliza um modelo de IA neuro-simbólica.
    
    **Classes disponíveis:**
    - Hipotermia (0)
    - Saudável (1)
    - Febril (2)
    - Febre (3)
    - Febre Alta (4)
    - Risco Cardiovascular (5)
    
    **Abordagem:**
    - Rede neural MLP para predição probabilística.
    - Filtro simbólico baseado em regras clínicas para decisões seguras.
    """)