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
        return load * (1 + 0.0333 * reps)

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Athlete Pro Analyzer", layout="wide")

URL_MANICHINO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Mannequin_ATH.glb"
URL_CANESTRO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Basket_Hoop.glb"

user_workout = Workout()

# --- MOTORE 3D BLINDATO ---
def visualizzatore_3d_final(altezza_m, salto_m, url_man, url_can):
    html_code = f"""
    <div id="container3d" style="width: 100%; height: 500px; background: #0e1117; border: 1px solid #30363d;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        const container = document.getElementById('container3d');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0e1117);
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, 500);
        container.appendChild(renderer.domElement);
        
        scene.add(new THREE.AmbientLight(0xffffff, 1));
        const grid = new THREE.GridHelper(20, 20, 0x00d4ff, 0x333333);
        scene.add(grid);

        const loader = new THREE.GLTFLoader();
        let modelsLoaded = 0;
        const group = new THREE.Group();
        scene.add(group);

        function checkFocus() {{
            modelsLoaded++;
            if(modelsLoaded === 2) {{
                const box = new THREE.Box3().setFromObject(group);
                const center = box.getCenter(new THREE.Vector3());
                const size = box.getSize(new THREE.Vector3());
                const maxDim = Math.max(size.x, size.y, size.z);
                camera.position.set(center.x, center.y + 2, maxDim * 2.5);
                controls.target.copy(center);
                controls.update();
            }}
        }}

        loader.load('{url_can}', (gltf) => {{
            const hoop = gltf.scene;
            hoop.position.set(2, 0, 0);
            group.add(hoop);
            checkFocus();
        }});

        loader.load('{url_man}', (gltf) => {{
            const athlete = gltf.scene;
            const box = new THREE.Box3().setFromObject(athlete);
            const size = box.getSize(new THREE.Vector3());
            const scale = {altezza_m} / (size.y || 1);
            athlete.scale.set(scale, scale, scale);
            athlete.position.set(0, {salto_m}, 0);
            group.add(athlete);
            checkFocus();
        }});

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        function animate() {{ requestAnimationFrame(animate); renderer.render(scene, camera); }}
        animate();
    </script>
    """
    components.html(html_code, height=520)

# --- UI STREAMLIT ---
with st.sidebar:
    body_weight = st.number_input("Peso (kg):", value=75.0)
    athlete_height = st.number_input("Altezza (cm):", value=175.0)

tab1, tab2 = st.tabs(["Dashboard", "Visualizzatore 3D"])

with tab1:
    st.title("Athlete Pro Analyzer")
    load = st.number_input("Carico Squat (kg):", value=100.0)
    reps = st.number_input("Reps:", value=5)
    jump = st.slider("Salto (cm):", 20, 120, 50)
    
    # Grafico Potenziale
    max_sq = user_workout._calculate_1rm(load, reps)
    rel_sq = max_sq / body_weight
    p_min, p_max = rel_sq * 48, rel_sq * 53
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[rel_sq], y=[jump], mode='markers', marker=dict(size=20, color='red')))
    fig.update_layout(template="plotly_dark", title=f"Potenziale: {round(p_min)}-{round(p_max)} cm")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🏀 Simulazione Salto")
    visualizzatore_3d_final(athlete_height/100, jump/100, URL_MANICHINO, URL_CANESTRO)
