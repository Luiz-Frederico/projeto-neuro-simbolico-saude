"""
dashboard/app.py – Interface médica futurista Industrial-Cyberpunk (Neuro-Symbolic Core)
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NEURO-SYMBOLIC CORE v2.4", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INICIALIZAÇÃO DO HISTÓRICO (SESSION STATE) ---
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- 3. INJEÇÃO DE ESTILO INDUSTRIAL CYBERPUNK (CSS CUSTOMIZADO) ---
st.markdown("""
<style>
    /* Fundo Principal e Barra Lateral unificados em Cinza-Chumbo / Cimento Queimado Escuro */
    .stApp, section[data-testid="stSidebar"] { 
        background-color: #222629 !important; 
    }
    
    /* Linha divisória da barra lateral */
    section[data-testid="stSidebar"] {
        border-right: 2px solid #00f2fe !important;
    }
    
    /* Títulos Principais em Neon */
    h1 {
        color: #00f2fe !important;
        text-shadow: 0 0 10px #00f2fe, 0 0 20px #00f2fe;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
    }
    
    /* Subtítulos e Títulos de Seções padronizados no Verde Industrial Brilhante */
    h3, h4, [data-testid="stMarkdownContainer"] h4 {
        color: #86c232 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Padronização de labels de inputs e status para Verde Brilhante */
    label, [data-testid="stWidgetLabel"] p, .stMarkdown p:not(.neon-footer p) {
        color: #86c232 !important;
        font-weight: bold !important;
        font-family: monospace;
    }
    
    /* Elementos de Input estilo aço escovado */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 2px solid #00f2fe !important;
        border-radius: 4px !important;
    }
    
    /* Números digitados em PRETO para leitura ideal no fundo cinza-claro */
    div[data-baseweb="input"] input {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    /* Customização dos botões + e - do step input */
    div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"] {
        background-color: transparent !important;
    }
    div[data-testid="stNumberInputStepDown"]:hover, div[data-testid="stNumberInputStepUp"]:hover,
    div[data-testid="stNumberInputStepDown"]:focus, div[data-testid="stNumberInputStepUp"]:focus {
        background-color: #86c232 !important;
        color: #000000 !important;
    }
    div[data-testid="stNumberInputStepDown"] button, div[data-testid="stNumberInputStepUp"] button {
        color: #000000 !important;
    }
    
    /* Classes dedicadas para os rodapés brilharem no azul neon */
    .neon-footer, .neon-footer p, .neon-caption, .neon-caption span {
        color: #00f2fe !important;
        text-shadow: 0 0 5px #00f2fe;
        font-weight: bold !important;
        font-family: monospace;
    }
    
    /* Cards de Métricas Estilizados com fundo escuro */
    div[data-testid="stMetric"] {
        background-color: #1a1a1a !important;
        padding: 15px !important;
        border-radius: 6px !important;
        border: 1px solid #4facfe !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #ffffff !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        color: #00f2fe !important;
        text-shadow: 0 0 5px #00f2fe;
    }
    
    /* Botão Primário Cyberpunk Industrial */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.6) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100% !important;
        height: 50px;
        font-size: 18px !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.01) !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.9) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. BARRA LATERAL (SIDEBAR) TÉCNICA ---
with st.sidebar:
    st.markdown("## 🤖 CORE ENGINE v2.4")
    st.markdown("---")
    
    st.markdown("### 📡 HARDWARE STATUS")
    st.markdown(
        '<div style="background-color: rgba(0, 255, 0, 0.1); padding: 10px; border-radius: 5px; border-left: 5px solid #00ff00; margin-bottom: 20px;">'
        '<span style="color: #00ff00; font-weight: bold; font-family: monospace;">🟢 ESP32 LINK: ONLINE</span>'
        '</div>', 
        unsafe_allow_html=True
    )
    
    st.markdown("### 🧠 ARQUITETURA DA IA")
    st.markdown(
        '<div style="background-color: rgba(0, 242, 254, 0.05); padding: 12px; border-radius: 5px; border: 2px solid #00f2fe; box-shadow: 0 0 10px #00f2fe; margin-bottom: 15px;">'
        '<span style="color: #00f2fe; font-weight: bold; font-family: monospace;"> Camada Conexionista:</span><br>'
        '<span style="color: #00f2fe; font-size: 14px; font-weight: normal;">Rede Neural Artificial (Keras/TF) treinada para extrair padrões complexos de Temperatura + BPM.</span>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<div style="background-color: rgba(186, 85, 211, 0.08); padding: 12px; border-radius: 5px; border: 2px solid #bd00ff; box-shadow: 0 0 10px #bd00ff; margin-bottom: 15px;">'
        '<span style="color: #bd00ff; font-weight: bold; font-family: monospace;"> Camada Simbólica:</span><br>'
        '<span style="color: #bd00ff; font-size: 14px; font-weight: normal;">Filtros lógicos especialistas que aplicam regras rígidas de segurança (ex: Hiperpirexia a partir de 41°C).</span>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown('<div class="neon-caption">FIAP • Inteligência Artificial & Machine Learning</div>', unsafe_allow_html=True)

# --- 5. ÁREA PRINCIPAL ---
st.title("🧠 NEURO-SYMBOLIC MEDICAL INTERFACE")
st.markdown("### Monitoramento e Diagnóstico por Inteligência Artificial")
st.markdown("---")

# Limpeza e higienização da string da URL base para evitar caminhos duplicados
try:
    API_URL = st.secrets["API_URL"].strip().rstrip("/")
except Exception:
    API_URL = "https://classificador-neuro-simbolico-api.onrender.com"

# --- 6. ENTRADA DE DADOS ---
col_inputs, col_lottie = st.columns([2, 1])

with col_inputs:
    st.markdown("#### 🎛️ Ajuste de Sinais Vitais")
    c1, c2 = st.columns(2)
    with c1:
        temperatura = st.number_input("Temperatura Corporal (°C)", min_value=30.0, max_value=43.0, value=36.5, step=0.1)
    with c2:
        bpm = st.number_input("Frequência Cardíaca (BPM)", min_value=20, max_value=200, value=70, step=1)
    
    st.markdown("")
    botao_inferencia = st.button("ATIVAR INFERÊNCIA NEURO-SIMBÓLICA")

with col_lottie:
    st.markdown(
        '<div style="text-align: center; padding: 25px; border: 2px dashed #ff0055; border-radius: 8px; background-color: #1a1a1a;">'
        '<span style="font-size: 50px; text-shadow: 0 0 15px #ff0055;">❤️</span><br>'
        '<span style="color: #ff0055; font-family: monospace; font-weight: bold; font-size: 12px;">PULSE MONITOR ACTIVE</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# --- 7. FLUXO DE EXECUÇÃO BLINDADO ---
if botao_inferencia:
    with st.spinner("Estabelecendo conexão segura com o cluster no Render... (Pode levar até 40s caso o cluster esteja acordando)"):
        try:
            payload = {"temperatura": temperatura, "bpm": bpm}
            
            # Estratégia adaptativa de rotas para garantir compatibilidade com o backend
            rotas_para_testar = [f"{API_URL}/predict", f"{API_URL}/v1/classificar", f"{API_URL}/classificar"]
            response = None
            erro_conexao = None
            
            for rota in rotas_para_testar:
                try:
                    response = requests.post(rota, json=payload, timeout=45)
                    if response.status_code in [200, 422]:
                        break
                except requests.exceptions.RequestException as e:
                    erro_conexao = e
                    continue
            
            if response is None:
                raise erro_conexao if erro_conexao else Exception("Incapaz de mapear rotas de destino.")

            if response.status_code == 200:
                dados = response.json()
                diagnostico = dados.get("diagnostico", "Não Identificado")
                probs = dados.get("probabilidades", {})
                
                # Só monta a parte gráfica se as probabilidades existirem de fato
                if probs and isinstance(probs, dict):
                    cor_alerta = "#00ff00"
                    if "Febre" in diagnostico or "Cardiovascular" in diagnostico:
                        cor_alerta = "#ff3366"
                    elif "Febril" in diagnostico or "Hipotermia" in diagnostico:
                        cor_alerta = "#ff9900"
                    
                    st.session_state.historico.insert(0, {
                        "Horário": time.strftime("%H:%M:%S"),
                        "Temperatura (°C)": f"{temperatura:.2f}",
                        "BPM": bpm,
                        "Diagnóstico Final": diagnostico
                    })
                    
                    st.markdown(f"### 📊 Resultado da Análise Coletada")
                    m1, m2, m3 = st.columns([1, 1, 2])
                    with m1:
                        st.metric(label="Temperatura Lida", value=f"{temperatura:.2f} °C")
                    with m2:
                        st.metric(label="Batimentos Cardíacos", value=f"{bpm} BPM")
                    with m3:
                        st.markdown(
                            f'<div style="background-color: #1a1a1a; padding: 18px; border-radius: 5px; border: 2px solid {cor_alerta}; box-shadow: 0 0 15px {cor_alerta}; text-align: center;">'
                            f'<span style="color: {cor_alerta}; font-weight: bold; font-family: monospace; font-size: 20px;">DIAGNÓSTICO: {diagnostico.upper()}</span>'
                            f'</div>', 
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("")
                    
                    # GRÁFICOS LADO A LADO BLINDADOS
                    g1, g2 = st.columns(2)
                    
                    with g1:
                        st.markdown("#### 🕸️ Assinatura Visual (Gráfico de Radar)")
                        categories = list(probs.keys())
                        values = list(probs.values())
                        if categories and values:
                            categories.append(categories[0])
                            values.append(values[0])
                            
                            fig_radar = go.Figure()
                            fig_radar.add_trace(go.Scatterpolar(
                                r=values,
                                theta=categories,
                                fill='toself',
                                fillcolor='rgba(0, 242, 254, 0.15)',
                                line=dict(color='#00f2fe', width=2.5),
                                name='Probabilidade'
                            ))
                            fig_radar.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.15)"),
                                    angularaxis=dict(gridcolor="rgba(255,255,255,0.15)", linecolor="rgba(255,255,255,0.15)")
                                ),
                                template="plotly_dark",
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                height=380
                            )
                            st.plotly_chart(fig_radar, use_container_width=True)
                        else:
                            st.warning("Dados de probabilidade insuficientes para gerar o gráfico radial.")
                    
                    with g2:
                        st.markdown("#### 📊 Distribuição Linear (Gráfico de Barras)")
                        classes_bar = list(probs.keys())
                        valores_bar = list(probs.values())
                        
                        if classes_bar and valores_bar:
                            fig_bar = go.Figure(data=[go.Bar(
                                x=classes_bar, 
                                y=valores_bar, 
                                marker_color=['#00f2fe' if v == max(valores_bar) else '#343a40' for v in valores_bar],
                                marker_line=dict(color='#4facfe', width=1.5)
                            )])
                            fig_bar.update_layout(
                                template="plotly_dark",
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                yaxis_range=[0, 1],
                                height=380
                            )
                            st.plotly_chart(fig_bar, use_container_width=True)
                        else:
                            st.warning("Dados de classe insuficientes para gerar o gráfico de barras.")
                else:
                    st.error("⚠️ Resposta estrutural inválida recebida da API (Dados de probabilidade corrompidos).")
            else:
                st.error(f"❌ O cluster respondeu com erro de processamento HTTP {response.status_code}. Valide os contratos de dados.")

        except requests.exceptions.Timeout:
            st.warning("⏳ **Cluster em Inicialização (Cold Start).** O Render demorou mais que 45 segundos para responder pois estava inativo. Aguarde 10 segundos e pressione o botão novamente para carregar os dados já aquecidos.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 **Falha de Link de Comunicação.** Não foi possível alcançar o barramento da API no Render. Verifique se o serviço do backend está ativo.")
        except Exception as e:
            st.error(f"🛠️ **Exceção de Runtime Interceptada:** {str(e)}")

# --- 8. HISTÓRICO DE CONSULTAS ---
if st.session_state.historico:
    st.markdown("---")
    st.markdown("### 📋 Histórico de Análises Acumuladas nesta Sessão")
    df_hist = pd.DataFrame(st.session_state.historico)
    st.dataframe(df_hist, use_container_width=True)

# --- RODAPÉ ---
st.markdown("---")
st.markdown('<div class="neon-footer">Desenvolvido por Luiz F. N. Campelo • AI & ML Engineer</div>', unsafe_allow_html=True)