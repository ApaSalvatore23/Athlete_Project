import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

class Workout:
    def __init__(self):
        self.k_min = 48
        self.k_max = 53

    def _calculate_1rm(self, load, reps):
        # Mantenuta la tua logica originale
        epley = load * (1 + 0.0333 * reps)
        brzycki = load * (36 / (37 - reps))
        lombardi = load * math.pow(reps, 0.10)
        return (epley + brzycki + lombardi) / 3

    # Funzioni di calcolo pure (senza input() o print())
    def get_squat_stats(self, bw, load, reps):
        max_weight = self._calculate_1rm(load, reps)
        rel_strength = max_weight / bw
        return max_weight, rel_strength

    def get_jump_stats(self, bw, reach, load, reps, current_jump):
        max_weight = self._calculate_1rm(load, reps)
        min_jump = self.k_min * (max_weight / bw)
        max_jump = self.k_max * (max_weight / bw)
        rel_strength = max_weight / bw
        return max_weight, min_jump, max_jump, rel_strength

# --- INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="Workout Analyzer", layout="wide")
st.title("🏋️ Workout & Jump Performance Analyzer")

# Inizializziamo la classe
user_workout = Workout()

# Sidebar per gli input comuni
st.sidebar.header("Dati Utente")
bw = st.sidebar.number_input("Peso Corporeo (kg)", min_value=1.0, value=75.0)

menu = st.sidebar.selectbox("Cosa vuoi calcolare?", 
    ["Squat 1RM", "Potential Vertical Jump", "Bench Press 1RM", "Power"])

if menu == "Squat 1RM":
    st.header("Analisi Squat")
    load = st.number_input("Carico Squat (kg)", value=100.0)
    reps = st.number_input("Ripetizioni Squat", min_value=1, value=5)
    
    if st.button("Calcola"):
        max_w, rel_s = user_workout.get_squat_stats(bw, load, reps)
        st.metric("Massimale Stimato (1RM)", f"{round(max_w)} kg")
        st.info(f"Sollevi circa {round(rel_s, 2)} volte il tuo peso corporeo.")

elif menu == "Potential Vertical Jump":
    st.header("Potenziale di Salto Verticale")
    col1, col2 = st.columns(2)
    with col1:
        reach = st.number_input("Standing Reach (cm)", value=220.0)
        current_j = st.number_input("Salto attuale (cm)", value=50.0)
    with col2:
        load = st.number_input("Carico Squat (kg)", value=100.0)
        reps = st.number_input("Ripetizioni Squat", value=5)

    if st.button("Analizza Salto"):
        max_w, min_j, max_j, rel_s = user_workout.get_jump_stats(bw, reach, load, reps, current_j)
        
        st.subheader(f"Il tuo potenziale: {round(min_j)} - {round(max_j)} cm")
        
        # --- Generazione Grafici ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
        
        # Grafico 1: Performance
        ax1.set_xlim(0, 3)
        ax1.set_ylim(0, 120)
        ax1.axhline(50, color='gray', linestyle='--', label="Beginner")
        ax1.axhline(70, color='blue', linestyle='--', label="Intermediate")
        ax1.axhline(90, color='gold', linestyle='--', label="Advanced")
        ax1.plot(1.5, current_j, 'bo', markersize=10, label="Attuale")
        ax1.plot(2.5, min_j, 'ro', label="Min Potenziale")
        ax1.plot(2.5, max_j, 'go', label="Max Potenziale")
        ax1.set_title("Jump Performance Chart")
        ax1.legend()

        # Grafico 2: Ratio
        ax2.set_xlim(0, 2.5)
        ax2.set_ylim(0, 120)
        ax2.fill([2,2.5,2.5,2],[95,95,120,120], color='#90EE90', alpha=0.5, label="Ideal Ratio")
        ax2.plot(rel_s, current_j, 'ro', label="Tu")
        ax2.set_xlabel("Relative Strength (BW)")
        ax2.set_ylabel("Jump Height (cm)")
        ax2.legend()

        st.pyplot(fig)

elif menu == "Power":
    st.header("Calcolo Potenza")
    load = st.number_input("Carico Squat (kg)", value=80.0)
    time = st.number_input("Tempo fase concentrica (secondi)", value=0.5, step=0.1)
    
    if st.button("Calcola Potenza"):
        rel_strength = load / bw
        power_index = rel_strength / time
        
        if power_index < 0.8: level = "Low"
        elif power_index < 1.5: level = "Medium"
        elif power_index < 2.5: level = "High"
        else: level = "Elite"
        
        st.success(f"Livello di Potenza: {level} (Index: {round(power_index, 2)})")
        
        # Grafico Potenza (Semplificato per Streamlit)
        fig, ax = plt.subplots()
        ax.bar(["Tuo Indice"], [power_index], color='orange')
        ax.axhline(1.5, color='red', label="Target Advanced")
        ax.set_ylim(0, 3)
        ax.legend()
        st.pyplot(fig)