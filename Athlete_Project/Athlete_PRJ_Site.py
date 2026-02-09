import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import math

# --- LOGICA DI CALCOLO ---
class Workout:
    def __init__(self):
        self.k_min = 48
        self.k_max = 53

    def _calculate_1rm(self, load, reps):
        epley = load * (1 + 0.0333 * reps)
        brzycki = load * (36 / (37 - reps))
        lombardi = load * math.pow(reps, 0.10)
        return (epley + brzycki + lombardi) / 3

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Athlete Pro Analyzer", layout="wide", initial_sidebar_state="expanded")

# CSS personalizzato per uno stile più moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

user_workout = Workout()

# --- SIDEBAR & CREDITS ---
with st.sidebar:
    st.title("Settings")
    body_weight = st.number_input("Peso Corporeo (kg):", min_value=1.0, value=75.0, step=0.1)
    st.markdown("---")
    st.markdown("### 🚀 Credits")
    st.info("Developed by **Salvatore Apa**")
    st.write("Versione 2.0 (Pro)")

st.title("🏋️ Athlete Performance Analyzer")
menu = st.tabs(["Squat 1RM", "Potential Jump", "Bench Press", "Power Analysis"])

# Funzione per scaricare i dati
def download_report(data_dict):
    df = pd.DataFrame([data_dict])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Scarica Report (.csv)", csv, "atleta_report.csv", "text/csv")

# --- 1. SQUAT TAB ---
with menu[0]:
    st.header("Analisi Massimale Squat")
    col1, col2 = st.columns(2)
    with col1:
        load_sq = st.number_input("Carico (kg):", min_value=0.0, value=100.0, key="sq_l")
        reps_sq = st.number_input("Ripetizioni:", min_value=1, value=5, key="sq_r")
    
    max_sq = user_workout._calculate_1rm(load_sq, reps_sq)
    rel_sq = max_sq / body_weight
    
    with col2:
        st.metric("Estimated 1RM", f"{round(max_sq, 1)} kg", delta=f"{round(rel_sq, 2)}x BW")
    
    if st.button("Genera Report Squat"):
        download_report({"Esercizio": "Squat", "1RM": max_sq, "Relative": rel_sq})

# --- 2. JUMP TAB ---
with menu[1]:
    st.header("Potential Vertical Jump Analysis")
    c1, c2 = st.columns(2)
    with c1:
        standing_reach = st.number_input("Standing Reach (cm):", value=220.0)
        current_jump = st.number_input("Salto Attuale (cm):", value=50.0)
    with c2:
        load_j = st.number_input("Carico Squat (kg):", value=100.0, key="j_l")
        reps_j = st.number_input("Reps Squat:", value=5, key="j_r")

    max_w_j = user_workout._calculate_1rm(load_j, reps_j)
    min_p_j = user_workout.k_min * (max_w_j / body_weight)
    max_p_j = user_workout.k_max * (max_w_j / body_weight)
    rel_s_j = max_w_j / body_weight

    t1, t2 = st.tabs(["📊 Grafico", "📜 Dettagli Tecnici"])
    
    with t1:
        fig = go.Figure()
        # Aree di performance
        fig.add_shape(type="rect", x0=2, y0=95, x1=2.5, y1=120, fillcolor="rgba(144,238,144,0.3)", line_width=0)
        fig.add_trace(go.Scatter(x=[rel_s_j], y=[current_jump], mode='markers+text', 
                                 marker=dict(size=18, color='red', line=dict(width=2, color='white')),
                                 name="Tu", text=["Tua Posizione"], textposition="top center"))
        fig.add_annotation(
            x=2.25, y=122, # Posizionato appena sopra il rettangolo verde
            text="<b>🟩 RANGE IDEALE</b>",
            showarrow=False,
            font=dict(family="Arial", size=14, color="#90EE90"), # Stesso verde
            align="center"
        )
        
        fig.update_layout(title="Rapporto Forza/Salto", xaxis_title="Forza Relativa (BW)", 
                          yaxis_title="Salto (cm)", template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.write(f"**Potenziale Stimato:** {round(min_p_j)} - {round(max_p_j)} cm")
        st.progress(min(current_jump/max_p_j, 1.0))

# --- 3. BENCH PRESS TAB ---
with menu[2]:
    st.header("Analisi Panca Piana")
    l_bp = st.number_input("Carico (kg):", value=80.0, key="bp_l")
    r_bp = st.number_input("Reps:", value=5, key="bp_r")
    max_bp = user_workout._calculate_1rm(l_bp, r_bp)
    st.metric("1RM Panca", f"{round(max_bp, 1)} kg", delta=f"{round(max_bp/body_weight, 2)}x BW")

# --- 4. POWER TAB ---
with menu[3]:
    st.header("Power & Velocity Analysis")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_load = st.number_input("Carico Utilizzato (kg):", value=80.0)
        p_time = st.number_input("Tempo Fase Concentrica (s):", value=0.5)
    
    p_rel = p_load / body_weight
    p_index = p_rel / p_time

    with col_p2:
        st.metric("Power Index", f"{round(p_index, 2)}")
        if p_index > 1.5: st.success("Livello: Elite")
        else: st.warning("Livello: Da migliorare")

    # Grafico Potenza Plotly
    fig_p = go.Figure()
    fig_p.add_trace(go.Bar(x=['Tuo Indice'], y=[p_index], marker_color='#87CEFA'))
    fig_p.add_shape(type="line", x0=-0.5, y0=1.5, x1=0.5, y1=1.5, line=dict(color="Red", dash="dash"))
    fig_p.update_layout(title="Power Index vs Benchmark (1.5)", template="plotly_dark", height=400)
    st.plotly_chart(fig_p, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 Athlete Pro Analyzer | Created by Salvatore Apa | Powered by Streamlit & Plotly")

