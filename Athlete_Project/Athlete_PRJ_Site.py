import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- 1. CONFIGURAZIONE E STILE ---
st.set_page_config(
    page_title="Athlete Performance Lab | 3D",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# --- 2. DATABASE LINK MODELLI (Sostituisci con i tuoi link RAW di GitHub) ---
URL_MANICHINO = ""
URL_CANESTRO = "https://raw.githubusercontent.com/ApaSalvatore23/Athlete_Project/main/Athlete_Project/3D_Assets/Basket_Hoop.glb"

# --- 3. FUNZIONE MOTORE 3D (THREE.JS) ---
def visualizzatore_3d_pro(altezza_m, salto_m, url_man, url_can):
    html_code = f"""
    <div id="container3d" style="width: 100%; height: 500px; background: #0e1117; border-radius: 12px; overflow: hidden;"></div>
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

        const light = new THREE.AmbientLight(0xffffff, 0.7); scene.add(light);
        const pLight = new THREE.PointLight(0xffffff, 1); pLight.position.set(5, 10, 5); scene.add(pLight);

        const loader = new THREE.GLTFLoader();
        loader.load('{url_can}', (gltf) => {{
            const hoop = gltf.scene; hoop.position.set(2, 0, 0); scene.add(hoop);
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

        const grid = new THREE.GridHelper(20, 20, 0x444444, 0x222222); scene.add(grid);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        function animate() {{ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }}
        animate();
    </script>
    """
    components.html(html_code, height=500)

# --- 4. SIDEBAR (Input Costanti) ---
with st.sidebar:
    st.header("👤 Profilo Atleta")
    atleta_nome = st.text_input("Nome:", "Atleta Pro")
    peso = st.number_input("Peso (kg):", 40, 150, 75)
    altezza_cm = st.number_input("Altezza (cm):", 140, 230, 180)
    reach_cm = st.number_input("Standing Reach (cm):", 160, 300, 235)
    st.markdown("---")
    st.header("📋 Test Massimali")
    bench_1rm = st.number_input("Bench Press 1RM (kg):", 0, 300, 80)
    squat_1rm = st.number_input("Squat 1RM (kg):", 0, 400, 120)
    dl_1rm = st.number_input("Deadlift 1RM (kg):", 0, 500, 140)

# --- 5. CALCOLI ---
altezza_m = altezza_cm / 100
reach_m = reach_cm / 100
forza_relativa_squat = squat_1rm / peso
power_to_weight = (squat_1rm + dl_1rm + bench_1rm) / peso

# --- 6. MAIN INTERFACE ---
st.title(f"🚀 Performance Analysis: {atleta_nome}")

tab_3d, tab_forza, tab_dati = st.tabs(["🎮 Simulatore Salto 3D", "🏋️‍♂️ Analisi Forza", "📊 Report Finale"])

with tab_3d:
    col_jump, col_stat = st.columns([2, 1])
    with col_stat:
        st.subheader("Parametri Salto")
        salto_cm = st.slider("Vertical Jump (cm):", 20, 120, 60)
        salto_m = salto_cm / 100
        tocco_totale = reach_m + salto_m
        
        st.metric("Tocco Massimo", f"{tocco_totale:.2f} m")
        st.metric("Differenza vs Canestro", f"{tocco_totale - 3.05:.2f} m")
        
    with col_jump:
        if URL_MANICHINO == "URL_IL_TUO_MANICHINO_QUI":
            st.info("Configura i link RAW di GitHub per visualizzare il modello 3D.")
        else:
            visualizzatore_3d_pro(altezza_m, salto_m, URL_MANICHINO, URL_CANESTRO)

with tab_forza:
    st.subheader("Rapporto Forza-Peso")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    # Bench Press Ratio
    bench_ratio = bench_1rm / peso
    f_col1.metric("Bench/Peso", f"{bench_ratio:.2f}x")
    
    # Squat Ratio (Fondamentale per il salto)
    f_col2.metric("Squat/Peso", f"{forza_relativa_squat:.2f}x")
    
    # Totale Powerlifting
    f_col3.metric("P-to-W Ratio", f"{power_to_weight:.2f}x")

    # Grafico a barre dei massimali
    fig_forza = go.Figure(data=[
        go.Bar(name='Massimali (kg)', x=['Bench Press', 'Squat', 'Deadlift'], y=[bench_1rm, squat_1rm, dl_1rm], marker_color='#00d4ff')
    ])
    fig_forza.update_layout(template="plotly_dark", title="Profilo di Forza")
    st.plotly_chart(fig_forza, use_container_width=True)

with tab_dati:
    # Qui integriamo il calcolo della potenza esplosiva incrociando i dati
    potenza_w = (60.7 * salto_cm) + (45.3 * peso) - 2055
    st.write("### 📈 Analisi Biomeccanica")
    st.write(f"Con uno Squat di **{forza_relativa_squat:.2f}** volte il tuo peso e un salto di **{salto_cm}cm**, la tua efficienza esplosiva è:")
    
    if forza_relativa_squat > 2.0 and salto_cm > 70:
        st.success("✅ PROFILO ELITE: Forza e potenza sono perfettamente bilanciate.")
    elif forza_relativa_squat > 2.0 and salto_cm < 50:
        st.warning("⚠️ FORTE MA LENTO: Hai molta forza ma fatichi a convertirla in velocità. Lavora sulla pliometria.")
    else:
        st.info("💪 COSTRUZIONE BASE: Aumenta il massimale di Squat per avere più 'motore' per il salto.")

st.markdown("---")
st.caption("Jump Lab 3D - Gestione Pesi e Performance Verticale")

