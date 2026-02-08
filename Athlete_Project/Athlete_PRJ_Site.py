import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

class Workout:
    def __init__(self):
        self.k_min = 48
        self.k_max = 53

    def _calculate_1rm(self, load, reps):
        epley = load * (1 + 0.0333 * reps)
        brzycki = load * (36 / (37 - reps))
        lombardi = load * math.pow(reps, 0.10)
        return (epley + brzycki + lombardi) / 3

# Configurazione Streamlit
st.set_page_config(page_title="Workout Analyzer", layout="wide")
st.title("🏋️ Workout Performance Analyzer")

user_workout = Workout()

# Sidebar per input comuni
st.sidebar.header("Dati Utente")
body_weight = st.sidebar.number_input("Peso Corporeo (kg)", min_value=1.0, value=75.0)

menu = st.sidebar.selectbox("Cosa vuoi calcolare?", 
    ["Squat 1RM", "Potential Vertical Jump", "Bench Press 1RM", "Power"])

# --- SEZIONE SQUAT ---
if menu == "Squat 1RM":
    st.header("Analisi Squat")
    load = st.number_input("Inserisci il carico dello Squat (kg):", value=100.0)
    reps = st.number_input("Inserisci le ripetizioni:", min_value=1, value=5)
    
    if st.button("Calcola"):
        max_weight = user_workout._calculate_1rm(load, reps)
        relative_strength = max_weight / body_weight
        st.metric("Estimated Squat 1RM", f"{round(max_weight)} kg")
        st.write(f"Sollevi circa **{round(relative_strength * 10)/10}** volte il tuo peso corporeo.")

# --- SEZIONE JUMP (CON GRAFICI) ---
elif menu == "Potential Vertical Jump":
    st.header("Potential Vertical Jump")
    col1, col2 = st.columns(2)
    with col1:
        standing_reach = st.number_input("Standing Reach (cm):", value=220.0)
        current_jump = st.number_input("Salto attuale (cm):", value=50.0)
    with col2:
        load = st.number_input("Carico Squat (kg):", value=100.0)
        reps = st.number_input("Ripetizioni Squat:", value=5)

    if st.button("Analizza Salto"):
        max_weight = user_workout._calculate_1rm(load, reps)
        min_jump = user_workout.k_min * (max_weight / body_weight)
        max_jump = user_workout.k_max * (max_weight / body_weight)
        relative_strength = round((max_weight / body_weight) * 10) / 10

        st.subheader(f"Potenziale: {round(min_jump)}-{round(max_jump)} cm")
        st.write(f"Reach potenziale: {round(standing_reach + min_jump)}-{round(standing_reach + max_jump)} cm")

        # --- GRAFICI  ---
        fig = plt.figure(figsize=(8,10))
        
        # Subplot 1
        plt.subplot(2,1,1)
        plt.xlim(0,3)
        plt.ylim(0,120)
        plt.plot([0,3],[50,50], label="Beginner (50-65cm)")
        plt.plot([0,3],[70,70], label="Intermediate (70-80cm)")
        plt.plot([0,3],[80,80], label="Excellent (80-90cm)")
        plt.plot([0,3],[90,90], label="Advanced (90-105cm)")
        plt.plot([0,3],[105,105], label="Elite (105+cm)")
        plt.plot(2.5, min_jump, 'ro', label="Min Potential Jump")
        plt.plot(2.5, max_jump, 'go', label="Max Potential Jump")
        plt.plot(1.5, current_jump, 'bo', label="Current Jump")
        plt.title("Jump Performance Chart")
        plt.ylabel("Height (cm)")
        plt.grid()
        plt.legend()

        # Subplot 2
        plt.subplot(2,1,2)
        plt.xlim(0, 2.5)
        plt.ylim(0, 120)
        plt.fill([2,2.5,2.5,2],[95,95,120,120], color='#90EE90', label="Ideal Ratio")
        plt.fill([2,2.5,2.5,2],[95,95,0,0], color='#FFF44F', label="Ideal Strength")
        plt.fill([0,0,2,2],[120,95,95,120], color='#87CEFA', label="Ideal Jump")
        plt.plot(relative_strength, current_jump, 'ro', label="Current Jump")
        plt.title("Jump vs Relative Strength Chart")
        plt.xlabel("Relative Strength (BW)")
        plt.ylabel("Jump Height (cm)")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        st.pyplot(fig)

# --- SEZIONE BENCH PRESS ---
elif menu == "Bench Press 1RM":
    st.header("Analisi Bench Press")
    load = st.number_input("Carico Bench Press (kg):", value=80.0)
    reps = st.number_input("Ripetizioni Bench Press:", min_value=1, value=5)
    
    if st.button("Calcola"):
        max_weight = user_workout._calculate_1rm(load, reps)
        relative_strength = max_weight / body_weight
        st.metric("Estimated Bench Press 1RM", f"{round(max_weight)} kg")
        st.write(f"Sollevi circa **{round(relative_strength * 10)/10}** volte il tuo peso corporeo.")

# --- SEZIONE POWER (GRAFICI ORIGINALI) ---
elif menu == "Power":
    st.header("Calcolo Potenza")
    load = st.number_input("Carico Squat (kg):", value=80.0)
    time = st.number_input("Tempo fase concentrica (s):", value=0.5, step=0.1)

    if st.button("Calcola Potenza"):
        relative_strength = round((load / body_weight) * 10) / 10
        power_index = relative_strength / time

        if power_index < 0.8: power_level = "Low"
        elif power_index < 1.5: power_level = "Medium"
        elif power_index < 2.5: power_level = "High"
        else: power_level = "Elite"

        st.success(f"Il tuo Power Level è: {power_level}")

        # --- GRAFICI ---
        fig = plt.figure(figsize=(8,10))

        plt.subplot(2,1,1)
        plt.xlim(0,3)
        plt.ylim(0,2)
        plt.plot([0,3],[0.7,0.7], label="Low")
        plt.plot([0,3],[1.0,1.0], label="Medium")
        plt.plot([0,3],[1.5,1.5], label="Advanced")
        plt.plot(1.5, power_index, 'ro', label="You")
        plt.title("Power Level Chart")
        plt.ylabel("Power Index")
        plt.grid()
        plt.legend()

        plt.subplot(2,1,2)
        plt.xlim(0,2.5)
        plt.ylim(0,2)
        plt.plot(time, relative_strength, 'ro', label="You")
        plt.fill([0,0.8,0.8,0],[2,2,1.25,1.25], color='#90EE90', label="Ideal Ratio")
        plt.fill([0,0.8,0.8,0],[1.25,1.25,0,0], color="#87CEFA", label="Ideal Time")
        plt.fill([0.8,0.8,2.5,2.52],[1.25,2,2,1.25], color="#FFF44F", label="Ideal Strength")
        plt.title("Strength vs Time Chart")
        plt.xlabel("Time (s)")
        plt.ylabel("Relative Strength (BW)")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        st.pyplot(fig)        st.pyplot(fig)

