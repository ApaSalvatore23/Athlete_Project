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

# Link Modelli 3D (Assicurati che siano i link RAW)
URL_MANICHINO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Mannequin_ATH.glb"
URL_CANESTRO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Basket_Hoop.glb"

# CSS personalizzato
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

user_workout = Workout()

# --- FUNZIONE MOTORE 3D (Three.js) ---
def visualizzatore_3d_pro(altezza_m, salto_m, url_man, url_can):
    html_code = f"""
    <div id="container3d" style="width: 100%; height: 500px; background: #0e1117; border-radius: 10px; border: 1px solid #30363d;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0e1117);
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / 500, 0.1, 1000);
        camera.position.set(4, 2, 6);
        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(window.innerWidth, 500);
        document.getElementById('container3d').appendChild(renderer.domElement);

        const light = new THREE.AmbientLight(0xffffff, 0.8); scene.add(light);
        const pLight = new THREE.PointLight(0xffffff, 1); pLight.position.set(5, 10, 5); scene.add(pLight);

        const loader = new THREE.GLTFLoader();
        loader.load('{url_can}', (gltf) => {{
            const hoop = gltf.scene; hoop.position.set(1.5, 0, 0); scene.add(hoop);
        }});
        loader.load('{url_man}', (gltf) => {{
            const athlete = gltf.scene;
            const box = new THREE.Box3().setFromObject(athlete);
            const size = box.getSize(new THREE.Vector3());
            const scaleFactor = {altezza_m} / size.y;
            athlete.scale.set(scaleFactor, scaleFactor, scaleFactor);
            athlete.position.set(0, {salto_m}, 0);
            scene.add(athlete);
        }});
        const grid = new THREE.GridHelper(10, 10, 0x444444, 0x222222); scene.add(grid);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        function animate() {{ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }}
        animate();
    </script>
    """
    components.html(html_code, height=500)

# --- SIDEBAR & CREDITS ---
with st.sidebar:
    st.title("Settings")
    body_weight = st.number_input("Peso Corporeo (kg):", min_value=1.0, value=75.0, step=0.1)
    athlete_height = st.number_input("Altezza Atleta (cm):", value=175.0)
    st.markdown("---")
    st.markdown("### 🚀 Credits")
    st.info("Developed by **Salvatore Apa**")
    st.write("Versione 2.0 (Pro)")

st.title("🏋️ Athlete Performance Analyzer")
menu = st.tabs(["Squat 1RM", "Potential Jump", "Bench Press", "Power Analysis"])

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

# --- 2. JUMP TAB (Modificata con 3D) ---
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

    t1, t2 = st.tabs(["📊 Grafico & Simulazione 3D", "📜 Dettagli Tecnici"])
    
    with t1:
        # Grafico Originale
        fig = go.Figure()
        fig.add_shape(type="rect", x0=2, y0=95, x1=2.5, y1=120, fillcolor="rgba(144,238,144,0.3)", line_width=0)
        fig.add_trace(go.Scatter(x=[rel_s_j], y=[current_jump], mode='markers+text', 
                                 marker=dict(size=18, color='red', line=dict(width=2, color='white')),
                                 name="Tu", text=["Tua Posizione"], textposition="top center"))
        fig.add_annotation(x=2.25, y=122, text="<b>🟩 RANGE IDEALE</b>", showarrow=False, font=dict(family="Arial", size=14, color="#90EE90"))
        fig.update_layout(title="Rapporto Forza/Salto", xaxis_title="Forza Relativa (BW)", yaxis_title="Salto (cm)", template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)

        # AGGIUNTA SIMULATORE 3D
        st.markdown("---")
        st.subheader("📍 Simulazione Biomeccanica al Picco")
        visualizzatore_3d_pro(athlete_height/100, current_jump/100, URL_MANICHINO, URL_CANESTRO)
        
        # Feedback Dunk
        tocco_totale = (standing_reach + current_jump) / 100
        diff_canestro = tocco_totale - 3.05
        if diff_canestro >= 0:
            st.success(f"🔥 Schiacciata possibile! Sei sopra il ferro di {int(diff_canestro*100)} cm.")
        else:
            st.warning(f"🏀 Ti mancano {int(abs(diff_canestro)*100)} cm per arrivare al ferro (3.05m).")

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
    fig_p = go.Figure()
    fig_p.add_trace(go.Bar(x=['Tuo Indice'], y=[p_index], marker_color='#87CEFA'))
    fig_p.add_shape(type="line", x0=-0.5, y0=1.5, x1=0.5, y1=1.5, line=dict(color="Red", dash="dash"))
    fig_p.update_layout(title="Power Index vs Benchmark (1.5)", template="plotly_dark", height=400)
    st.plotly_chart(fig_p, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 Athlete Pro Analyzer | Created by Salvatore Apa | Powered by Streamlit & Plotly")
