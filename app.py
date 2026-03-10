import streamlit as st
import base64

st.set_page_config(page_title="Portfolio | Asier Dorronsoro", layout="wide")

# --- FUNCIONES DE CARGA ---
@st.cache_data
def to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Ocultar menús de Streamlit
st.markdown("""
<style>
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 95% !important; }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE ASSETS (¡Esto es lo que faltaba y daba el NameError!) ---
video_b64     = to_b64("assets/Intro.mp4")
miniatura_b64 = to_b64("assets/miniatura.png")
portada_b64   = to_b64("assets/portada.jpeg")
elkar_b64     = to_b64("assets/elkarraizketa.jpeg")

# =====================================================================
# --- BLOQUE 1: VIDEO Y PORTADA (Alineación perfecta) ---
# =====================================================================
iframe_header = f"""
<style>
    body {{ margin: 0; padding: 0; overflow: hidden; }}
    * {{ box-sizing: border-box; }}
    
    #layout {{ 
        display: flex; 
        flex-direction: row; 
        gap: 24px; 
        width: 100%; 
        align-items: stretch; 
    }}
    
    #col-izq {{ flex: 2.4; }}
    
    #col-izq img {{ 
        width: 100%; 
        height: auto; 
        display: block; 
        border-radius: 12px; 
    }}
    
    #col-der {{ 
        flex: 1; 
        border-radius: 12px; 
        overflow: hidden; 
        position: relative; 
    }}
    
    #thumb, #video-wrapper {{ 
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        width: 100%; 
        height: 100%; 
    }}
    
    #thumb img {{ 
        width: 100%; 
        height: 100%; 
        object-fit: cover; 
        display: block; 
    }}
    
    #video-wrapper {{ 
        background: #000; 
        display: none; 
    }}
    
    #vid {{ 
        width: 100%; 
        height: 100%; 
        object-fit: contain; 
        display: block; 
    }}

    @media (max-width: 768px) {{
        #layout {{ flex-direction: column; gap: 16px; }}
        #col-izq {{ width: 100%; }}
        #col-der {{ 
            width: 100%; 
            position: relative;
            aspect-ratio: 9 / 16; 
            height: auto; 
        }}
    }}
</style>

<div id="layout">
    <div id="col-izq">
        <img id="img-portada" src="data:image/jpeg;base64,{portada_b64}" alt="Portada">
    </div>
    <div id="col-der">
        <div id="thumb">
            <img id="thumb-img" src="data:image/png;base64,{miniatura_b64}" alt="Miniatura">
        </div>
        <div id="video-wrapper">
            <video id="vid" controls playsinline poster="data:image/png;base64,{miniatura_b64}">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
        </div>
    </div>
</div>

<script>
    const thumb = document.getElementById('thumb');
    const videoWrapper = document.getElementById('video-wrapper');
    const vid = document.getElementById('vid');

    function notifyHeight() {{
        const h = document.body.scrollHeight + 10; 
        window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
    }}

    document.getElementById('img-portada').addEventListener('load', notifyHeight);

    if (document.getElementById('img-portada').complete) {{
        notifyHeight();
    }}

    thumb.addEventListener('click', () => {{
        thumb.style.display = 'none';
        videoWrapper.style.display = 'block';
        vid.play();
        notifyHeight();
    }});

    if (window.ResizeObserver) {{
        new ResizeObserver(notifyHeight).observe(document.body);
    }}
</script>
"""

st.components.v1.html(iframe_header, height=800, scrolling=False)


# =====================================================================
# --- BLOQUE 2: SECCIÓN DE PRODUCTOS (Negro Puro, Sombra Sutil, Neón) ---
# =====================================================================
html_productos = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@600&display=swap');

    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    
    body {{ background-color: transparent; }}

    .products-section-container {{
        margin-top: 100px; 
        background-color: #000000; 
        padding: 80px 30px; 
        border-radius: 28px; 
        border: 1px solid rgba(255, 255, 255, 0.05);
        
        /* Sombra ambiental uniforme en los 4 lados */
        box-shadow: 
            0 0 50px 15px rgba(0, 0, 0, 0.3), 
            0 -1px 2px rgba(255, 255, 255, 0.1) inset, 
            0 0 20px rgba(255, 223, 133, 0.02) inset; 
    }}

    .title-wrapper {{
        text-align: center;
        margin-bottom: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }}

    .rocket-emoji {{
        font-size: 45px;
    }}

    .neon-title-text {{
        font-family: 'Quicksand', sans-serif; 
        font-size: 52px;
        font-weight: 600;
        letter-spacing: 2px;
        color: transparent; 
        -webkit-text-stroke: 1.5px #ffdf85; 
        text-shadow: 
            0 0 8px rgba(255, 223, 133, 0.7),
            0 0 20px rgba(255, 170, 0, 0.8),
            0 0 40px rgba(255, 140, 0, 0.5);
    }}

    #cards-layout {{
        display: flex;
        flex-direction: row;
        gap: 24px;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }}

    .card {{
        flex: 1;
        position: relative;
        border-radius: 16px;
        overflow: hidden;
        aspect-ratio: 3 / 4; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.8); 
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        background: #1e1e1e;
        min-height: 400px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }}
    
    .card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,1), 0 0 15px rgba(255, 255, 255, 0.05);
    }}
    
    .card-bg {{
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        object-fit: cover; z-index: 1;
        opacity: 0.85; 
    }}
    
    .card-gradient {{
        position: absolute; bottom: 0; left: 0; width: 100%; height: 75%;
        background: linear-gradient(to top, rgba(0,0,0,0.98) 0%, rgba(0,0,0,0.6) 40%, rgba(0,0,0,0) 100%);
        z-index: 2;
    }}
    
    .card-content {{
        position: absolute; bottom: 20px; left: 20px; right: 20px;
        z-index: 3; color: white;
    }}
    
    .card-title {{ font-size: 22px; font-weight: bold; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
    .card-subtitle {{ font-size: 13px; color: #ccc; margin-bottom: 16px; line-height: 1.4; }}
    
    .card-btn {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 10px 14px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        text-decoration: none;
        transition: background 0.2s, border 0.2s;
    }}
    
    .card-btn:hover {{ 
        background: rgba(255, 255, 255, 0.15); 
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    @media (max-width: 768px) {{
        #cards-layout {{ flex-direction: column; }}
        .card {{ aspect-ratio: 4 / 3; min-height: 320px; }}
        .products-section-container {{ padding: 50px 15px; margin-top: 60px; }}
        .neon-title-text {{ font-size: 32px; }}
        .rocket-emoji {{ font-size: 30px; }}
    }}
</style>

<div class="products-section-container" id="products-container">
    <div class="title-wrapper">
        <span class="rocket-emoji">🚀</span>
        <span class="neon-title-text">Productos Digitales</span>
    </div>
    
    <div id="cards-layout">
        <div class="card">
            <img class="card-bg" src="data:image/jpeg;base64,{elkar_b64}" alt="Entrevista IA">
            <div class="card-gradient"></div>
            <div class="card-content">
                <div class="card-title">Elkarr AI zketa 🎙️</div>
                <div class="card-subtitle">Entrevistas con líderes mundiales potenciadas por IA.</div>
                <a href="#" class="card-btn">
                    <span>Explorar App</span>
                    <span>›</span>
                </a>
            </div>
        </div>

        <div class="card">
            <img class="card-bg" src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=800" alt="Ecosistema Vasco">
            <div class="card-gradient"></div>
            <div class="card-content">
                <div class="card-title">Red Ejecutiva 🌐</div>
                <div class="card-subtitle">Ecosistema Vasco • Alta Dirección</div>
                <a href="#" class="card-btn">
                    <span>Explorar App</span>
                    <span>›</span>
                </a>
            </div>
        </div>

        <div class="card">
            <img class="card-bg" src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&q=80&w=800" alt="Noticias">
            <div class="card-gradient"></div>
            <div class="card-content">
                <div class="card-title">Radar Empresarial 📈</div>
                <div class="card-subtitle">Monitorización de tendencias y alertas con IA.</div>
                <a href="#" class="card-btn">
                    <span>Explorar App</span>
                    <span>›</span>
                </a>
            </div>
        </div>
    </div>
</div>

<script>
    function notifyHeight() {{
        const container = document.getElementById('products-container');
        if (container) {{
            const style = window.getComputedStyle(container);
            const marginTop = parseInt(style.marginTop, 10);
            const h = container.offsetHeight + marginTop + 40; 
            window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
        }}
    }}
    
    window.addEventListener('load', notifyHeight);
    window.addEventListener('resize', notifyHeight);
    if (window.ResizeObserver) {{
        new ResizeObserver(notifyHeight).observe(document.body);
    }}
    setTimeout(notifyHeight, 500);
</script>
"""

st.components.v1.html(html_productos, height=1000, scrolling=False)