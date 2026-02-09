import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components
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

# --- LINK MODELLI 3D (CORRETTI) ---
URL_MANICHINO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Mannequin_ATH.glb"
URL_CANESTRO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Basket_Hoop.glb"

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    iframe { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

user_workout = Workout()

# --- FUNZIONE MOTORE 3D ---
def visualizzatore_3d_pro(altezza_m, salto_m, url_man, url_can):
    html_code = f"""
    <div id="container3d" style="width: 100%; height: 550px; background: #0e1117; border-radius: 10px; border: 1px solid #30363d;"></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

    <script>
        (function() {{
            const container = document.getElementById('container3d');
            container.innerHTML = ''; 

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1117);
            
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 550, 0.1, 1000);
            camera.position.set(7, 3, 12);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(window.innerWidth, 550);
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.9));
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(10, 20, 10);
            scene.add(light);

            const grid = new THREE.GridHelper(30, 30, 0x00d4ff, 0x333333);
            scene.add(grid);

            const loader = new THREE.GLTFLoader();

            // 1. CARICAMENTO CANESTRO (Scala e Posizione Regolate)
            loader.load('{url_can}', (gltf) => {{
                const hoop = gltf.scene;
                // Regola qui se il canestro sembra ancora troppo piccolo o grande
                hoop.scale.set(1.1, 1.1, 1.1); 
                hoop.position.set(3, 0, 0); 
                scene.add(hoop);
            }});

            // 2. CARICAMENTO MANICHINO
            loader.load('{url_man}', (gltf) => {{
                const athlete = gltf.scene;
                const box = new THREE.Box3().setFromObject(athlete);
                const size = box.getSize(new THREE.Vector3());
                
                const scaleFactor = {altezza_m} / (size.y || 1);
                athlete.scale.set(scaleFactor, scaleFactor, scaleFactor);
                
                // Lo mettiamo al centro e sollevato dal salto
                athlete.position.set(0, {salto_m}, 0); 
                scene.add(athlete);
            }});

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.target.set(1.5, 1.5, 0);
            controls.update();

            function animate() {{
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }}
            animate();
        }})();
    </script>
    """
    components.html(html_code, height=560)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    body_weight = st.number_input("Peso Corporeo (kg):", min_value=1.0, value=75.0, step=0.1)
    athlete_height = st.number_input("Altezza Atleta (cm):", value=175.0)
    st.markdown("---")
    st.info("Developed by **Salvatore Apa**")

st.title("🏋️ Athlete Performance Analyzer")
menu = st.tabs(["Squat 1RM", "Potential Jump", "Bench Press", "Power Analysis"])

# --- 1. SQUAT TAB ---
with menu[0]:
    st.header("Analisi Massimale Squat")
    col1, col2 = st.columns(2)
    with col1:
        load_sq = st.number_input("Carico (kg):", value=100.0, key="sq_l")
        reps_sq = st.number_input("Ripetizioni:", value=5, key="sq_r")
    max_sq = user_workout._calculate_1rm(load_sq, reps_sq)
    st.metric("Estimated 1RM Squat", f"{round(max_sq, 1)} kg")

# --- 2. JUMP TAB ---
with menu[1]:
    st.header("Potential Vertical Jump Analysis")
    c1, c2 = st.columns(2)
    with c1:
        standing_reach = st.number_input("Standing Reach (cm):", value=220.0)
        current_jump = st.number_input("Salto Attuale (cm):", value=50.0)
    with c2:
        load_j = st.number_input("Carico Squat per Calcolo Potenziale (kg):", value=100.0, key="j_l")
        reps_j = st.number_input("Reps Squat:", value=5, key="j_r")

    max_w_j = user_workout._calculate_1rm(load_j, reps_j)
    rel_s_j = max_w_j / body_weight
    pot_min = user_workout.k_min * rel_s_j
    pot_max = user_workout.k_max * rel_s_j

    st.markdown("### 📊 Analisi Grafica e Potenziale")
    fig = go.Figure()
    fig.add_shape(type="rect", x0=2, y0=95, x1=2.5, y1=120, fillcolor="rgba(144,238,144,0.1)", line_width=0)
    fig.add_shape(type="line", x0=rel_s_j-0.3, x1=rel_s_j+0.3, y0=pot_min, y1=pot_min, line=dict(color="orange", width=2, dash="dash"))
    fig.add_annotation(x=rel_s_j+0.3, y=pot_min, text=f"Min: {round(pot_min)}cm", showarrow=False, xanchor="left", font=dict(color="orange"))
    fig.add_shape(type="line", x0=rel_s_j-0.3, x1=rel_s_j+0.3, y0=pot_max, y1=pot_max, line=dict(color="#00ff00", width=2, dash="dash"))
    fig.add_annotation(x=rel_s_j+0.3, y=pot_max, text=f"Max: {round(pot_max)}cm", showarrow=False, xanchor="left", font=dict(color="#00ff00"))
    fig.add_trace(go.Scatter(x=[rel_s_j], y=[current_jump], mode='markers+text', marker=dict(size=18, color='red', line=dict(width=2, color='white')), name="Tu", text=["Tua Posizione"], textposition="bottom center"))
    fig.update_layout(title="Rapporto Forza/Salto", xaxis_title="Forza Relativa (BW)", yaxis_title="Salto (cm)", template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📍 Simulazione Biomeccanica al Picco")
    # Lancio del visualizzatore con i parametri altezza e salto
    visualizzatore_3d_pro(athlete_height/100, current_jump/100, URL_MANICHINO, URL_CANESTRO)
    
    tocco_totale = (standing_reach + current_jump) / 100
    diff = tocco_totale - 3.05
    if diff >= 0:
        st.success(f"🔥 Schiacciata possibile! Sei sopra il ferro di {int(diff*100)} cm.")
    else:
        st.warning(f"🏀 Ti mancano {int(abs(diff)*100)} cm per arrivare al ferro (3.05m).")

# --- 3. BENCH PRESS ---
with menu[2]:
    st.header("Analisi Panca Piana")
    l_bp = st.number_input("Carico (kg):", value=80.0, key="bp_l")
    r_bp = st.number_input("Reps:", value=5, key="bp_r")
    max_bp = user_workout._calculate_1rm(l_bp, r_bp)
    st.metric("1RM Panca", f"{round(max_bp, 1)} kg")

# --- 4. POWER ---
with menu[3]:
    st.header("Power Analysis")
    p_load = st.number_input("Carico Utilizzato (kg):", value=80.0)
    p_time = st.number_input("Tempo Fase Concentrica (s):", value=0.5)
    p_index = (p_load / body_weight) / p_time
    st.metric("Power Index", f"{round(p_index, 2)}")

