import streamlit as st
import streamlit.components.v1 as components
import base64
import asyncio
import tempfile
import os
import edge_tts

st.set_page_config(
    page_title="Industrial3D Demo | GlobalInternet.py",
    page_icon="🩻",
    layout="wide"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        margin-bottom: 1rem;
    }
    .main-title h1 {
        color: #ffd966;
    }
    .main-title p {
        color: #a0b0c0;
    }
    .stButton>button {
        background-color: #e94560;
        color: white;
        border-radius: 30px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

# ========== LOGO / BRANDING ==========
st.sidebar.image("https://img.icons8.com/fluency/96/null/3d-printer.png", width=80)
st.sidebar.markdown("## **GlobalInternet.py**")
st.sidebar.markdown("**Industrial3D Demo**")
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Gesner Deslandes**, Engineer-in-Chief")
st.sidebar.markdown("📞 (509) 4738 5663")
st.sidebar.markdown("✉️ deslandes78@gmail.com")
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 GlobalInternet.py")

# ========== AI VOICE GENERATION FUNCTION ==========
async def text_to_speech(text, voice, output_path):
    comm = edge_tts.Communicate(text, voice)
    await comm.save(output_path)

def generate_audio(text, voice="en-US-JennyNeural"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(text_to_speech(text, voice, tmp_path))
    loop.close()
    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()
    os.unlink(tmp_path)
    return audio_bytes

# ========== 3D MODEL USING THREE.JS ==========
threejs_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>3D Medical Device Visualization</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #0a192f; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #info {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            background: rgba(0,0,0,0.6);
            padding: 8px 15px;
            border-radius: 8px;
            pointer-events: none;
            z-index: 10;
            font-size: 12px;
        }
        .controls-note {
            position: absolute;
            bottom: 15px;
            left: 20px;
            color: #ccc;
            background: rgba(0,0,0,0.5);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            pointer-events: none;
            z-index: 10;
        }
    </style>
</head>
<body>
    <div id="info">
        <strong>Medical CT Scanner</strong> – Drag to rotate | Right-click to pan | Scroll to zoom
    </div>
    <div class="controls-note">
        🖱️ Interactive 3D Model
    </div>

    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a192f);
        scene.fog = new THREE.FogExp2(0x0a192f, 0.008);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(5, 4, 8);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);

        const labelRenderer = new CSS2DRenderer();
        labelRenderer.setSize(window.innerWidth, window.innerHeight);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        labelRenderer.domElement.style.left = '0px';
        labelRenderer.domElement.style.pointerEvents = 'none';
        document.body.appendChild(labelRenderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.rotateSpeed = 1.0;
        controls.zoomSpeed = 1.2;
        controls.panSpeed = 0.8;
        controls.enableZoom = true;
        controls.enablePan = true;

        const ambientLight = new THREE.AmbientLight(0x404060);
        scene.add(ambientLight);
        const mainLight = new THREE.DirectionalLight(0xffffff, 1);
        mainLight.position.set(5, 10, 7);
        mainLight.castShadow = true;
        scene.add(mainLight);
        const fillLight = new THREE.PointLight(0x4466cc, 0.5);
        fillLight.position.set(-3, 2, 4);
        scene.add(fillLight);
        const backLight = new THREE.PointLight(0xffaa66, 0.4);
        backLight.position.set(0, 2, -5);
        scene.add(backLight);
        const rimLight = new THREE.PointLight(0xff66aa, 0.3);
        rimLight.position.set(2, 3, -4);
        scene.add(rimLight);

        const gridHelper = new THREE.GridHelper(20, 20, 0x88aaff, 0x335588);
        gridHelper.position.y = -1.2;
        scene.add(gridHelper);

        const group = new THREE.Group();

        const base = new THREE.BoxGeometry(3.5, 0.2, 2.8);
        const baseMat = new THREE.MeshStandardMaterial({ color: 0xdddddd, roughness: 0.4, metalness: 0.7 });
        const baseMesh = new THREE.Mesh(base, baseMat);
        baseMesh.position.y = -0.5;
        baseMesh.castShadow = true;
        baseMesh.receiveShadow = true;
        group.add(baseMesh);

        const gantryRing = new THREE.TorusGeometry(1.3, 0.15, 64, 100);
        const ringMat = new THREE.MeshStandardMaterial({ color: 0x88aaff, metalness: 0.8, roughness: 0.2 });
        const ring = new THREE.Mesh(gantryRing, ringMat);
        ring.rotation.x = Math.PI / 2;
        ring.position.y = 0.3;
        group.add(ring);

        const boreCyl = new THREE.CylinderGeometry(0.9, 0.9, 1.8, 32);
        const boreMat = new THREE.MeshStandardMaterial({ color: 0x1a2a4a, emissive: 0x112233, roughness: 0.3 });
        const bore = new THREE.Mesh(boreCyl, boreMat);
        bore.position.y = 0.3;
        group.add(bore);

        const frontRing = new THREE.TorusGeometry(1.15, 0.08, 64, 100);
        const rimMat = new THREE.MeshStandardMaterial({ color: 0xffaa66, metalness: 0.9 });
        const frontRim = new THREE.Mesh(frontRing, rimMat);
        frontRim.rotation.x = Math.PI / 2;
        frontRim.position.z = 0.95;
        frontRim.position.y = 0.3;
        group.add(frontRim);

        const panelGeo = new THREE.BoxGeometry(1.2, 0.8, 2.2);
        const panelMat = new THREE.MeshStandardMaterial({ color: 0xccccdd, metalness: 0.5 });
        const leftPanel = new THREE.Mesh(panelGeo, panelMat);
        leftPanel.position.set(-1.9, -0.1, 0);
        leftPanel.castShadow = true;
        group.add(leftPanel);
        const rightPanel = new THREE.Mesh(panelGeo, panelMat);
        rightPanel.position.set(1.9, -0.1, 0);
        rightPanel.castShadow = true;
        group.add(rightPanel);

        const topGeo = new THREE.BoxGeometry(2.2, 0.2, 1.6);
        const topMat = new THREE.MeshStandardMaterial({ color: 0xaaccff, metalness: 0.6 });
        const topCover = new THREE.Mesh(topGeo, topMat);
        topCover.position.set(0, 0.9, 0.2);
        group.add(topCover);

        const detectorRing = new THREE.TorusGeometry(1.0, 0.05, 32, 80);
        const detMat = new THREE.MeshStandardMaterial({ color: 0x44aaff, emissive: 0x004466 });
        const detRing = new THREE.Mesh(detectorRing, detMat);
        detRing.rotation.x = Math.PI / 2;
        detRing.position.y = 0.3;
        detRing.position.z = 0.2;
        group.add(detRing);

        scene.add(group);

        function makeLabel(text, color, position) {
            const div = document.createElement('div');
            div.textContent = text;
            div.style.color = color;
            div.style.fontSize = '16px';
            div.style.fontWeight = 'bold';
            div.style.textShadow = '1px 1px 0px black';
            div.style.background = 'rgba(0,0,0,0.6)';
            div.style.padding = '2px 8px';
            div.style.borderRadius = '20px';
            div.style.borderLeft = `3px solid ${color}`;
            div.style.fontFamily = 'sans-serif';
            const label = new CSS2DObject(div);
            label.position.copy(position);
            scene.add(label);
        }

        makeLabel('X‑Ray Source', '#ffaa66', new THREE.Vector3(-1.2, 0.6, 0.9));
        makeLabel('Detector Array', '#88ff88', new THREE.Vector3(1.2, 0.6, 0.9));
        makeLabel('Patient Bore', '#88aaff', new THREE.Vector3(0, 0.8, 1.2));
        makeLabel('Control Panel', '#ffaa88', new THREE.Vector3(2.1, -0.3, 0.8));

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
            labelRenderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', onWindowResize, false);
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
        }
    </script>
</body>
</html>
"""

# ========== MAIN PAGE ==========
st.markdown('<div class="main-title"><h1>🩻 Industrial3D – Medical Device Visualization</h1><p>High‑fidelity 3D interactive model of a CT scanner with AI voice explanation</p></div>', unsafe_allow_html=True)

# Display the 3D viewer
st.components.v1.html(threejs_code, height=500, scrolling=False)

# AI Voice Explanation
st.subheader("🎙️ AI Voice Narration")
voice_text = """This is a high‑fidelity 3D visualization of a medical CT scanner. The scanner uses X‑rays to create detailed cross‑sectional images of the body. Key components include the X‑ray source, detector array, and the patient bore. This model can be rotated, zoomed, and panned. High‑quality technical visualizations like this are used for sales presentations, training materials, and marketing to clearly demonstrate how complex equipment works. Industrial3D specializes in creating such visualizations for medical devices and industrial machinery. This software was built by Gesner Deslandes, Engineer‑in‑Chief at GlobalInternet.py."""

if st.button("🔊 Hear AI Explanation (Female Voice)", use_container_width=True):
    with st.spinner("Generating voice narration..."):
        audio_bytes = generate_audio(voice_text, "en-US-JennyNeural")
        st.audio(audio_bytes, format="audio/mp3")

st.caption("📌 Interactive 3D model – use mouse or touch to rotate, zoom, and pan.")
st.markdown("---")
st.markdown("**Contact us to create custom technical visualizations for your products.**")
