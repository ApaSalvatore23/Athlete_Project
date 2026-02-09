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

# --- LINK MODELLI 3D ---
URL_MANICHINO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Mannequin_ATH.glb"
URL_CANESTRO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Basket_Hoop.glb"

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    iframe { border-radius: 10px; border: none; }
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
            
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 550, 0.1, 1000);
            camera.position.set(6, 3, 10);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(container.clientWidth, 550);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            // Illuminazione potenziata
            scene.add(new THREE.AmbientLight(0xffffff, 1));
            const light = new THREE.DirectionalLight(0xffffff, 1.2);
            light.position.set(5, 10, 7);
            scene.add(light);

            const grid = new THREE.GridHelper(20, 20, 0x00d4ff, 0x333333);
            scene.add(grid);

            const loader = new THREE.GLTFLoader();

            // 1. CARICAMENTO CANESTRO
            loader.load('{url_can}', (gltf) => {{
                const hoop = gltf.scene;
                // Calcolo scala automatica per il canestro (base 3.05m al ferro)
                const box = new THREE.Box3().setFromObject(hoop);
                const size = box.getSize(new THREE.Vector3());
                const hoopScale = 3.5 / size.y; // Standardizzazione altezza
                hoop.scale.set(hoopScale, hoopScale, hoopScale);
                
                hoop.position.set(3, 0, 0); 
                scene.add(hoop);
            }});

            // 2. CARICAMENTO MANICHINO
            loader.load('{url_man}', (gltf) => {{
                const athlete = gltf.scene;
                const box = new THREE.Box3().setFromObject(athlete);
                const size = box.getSize(new THREE.Vector3());
                
                // Scala basata sull'altezza atleta (m)
                const scaleFactor = {altezza_m} / (size.y || 1);
                athlete.scale.set(scaleFactor, scaleFactor, scaleFactor);
                
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

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / 550;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, 550);
            }});
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
    fig.add_shape(type="line", x0=rel_s_j-0.3, x1=rel_
