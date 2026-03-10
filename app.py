import streamlit as st
import base64

st.set_page_config(page_title="Portfolio | Asier Dorronsoro", layout="wide")

@st.cache_data
def to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Ocultamos la interfaz por defecto de Streamlit y ponemos el fondo oscuro
st.markdown("""
<style>
#MainMenu, header, footer { visibility: hidden; }
.block-container {
    padding-top: 1rem !important;
    max-width: 95% !important;
}
[data-testid="stAppViewContainer"] { background-color: #1a1a1a !important; }
[data-testid="stApp"]              { background-color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE ASSETS ---
video_b64     = to_b64("assets/Intro.mp4")
miniatura_b64 = to_b64("assets/miniatura.png")
portada_b64   = to_b64("assets/portada.jpeg")
elkar_b64     = to_b64("assets/elkarraizketa.jpeg")

# ─────────────────────────────────────────────
# WEB COMPLETA EN UN SOLO BLOQUE HTML/JS/CSS
# ─────────────────────────────────────────────
html_completo = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@600&display=swap');

    * {{ box-sizing: border-box; margin: 0; padding: 0;
         font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}

    html, body {{
        background: transparent;
        overflow-x: hidden;
        width: 100%;
    }}

    /* Padding general de la página */
    body {{ padding: 20px 24px 40px 24px; }}

    /* =========================================
       SECCIÓN 1: CABECERA (FOTO Y VÍDEO)
       ========================================= */
    #layout {{
        display: flex;
        flex-direction: row;
        gap: 24px;
        width: 100%;
        align-items: stretch;
    }}

    #col-izq {{
        flex: 2.4;
        border-radius: 12px;
        overflow: hidden;
        background-color: #1a1a1a; 
        box-shadow: 0 8px 30px rgba(0,0,0,0.7);
        display: flex; 
        transform: translateZ(0); 
    }}
    
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
        box-shadow: 0 8px 30px rgba(0,0,0,0.7);
        background: #000;
        transform: translateZ(0); 
    }}

    #thumb {{
        position: absolute;
        inset: 0;
        cursor: pointer;
        z-index: 2;
        border-radius: 12px;
    }}
    
    #thumb img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        border-radius: 12px; 
    }}

    #video-wrapper {{
        position: absolute;
        inset: 0;
        display: none;
        background: #000;
        z-index: 3;
        border-radius: 12px;
    }}
    
    #vid {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
        border-radius: 12px; 
    }}

    /* Efectos Hover Cabecera */
    #col-izq:hover, #col-der:hover {{
        box-shadow:
            0 20px 40px rgba(0,0,0,0.85),
            0 0 40px 8px  rgba(255,185,30,0.14),
            0 0 80px 16px rgba(255,140, 0,0.08),
            0 0 0    1px  rgba(255,200,60,0.18);
        transition: box-shadow 0.4s cubic-bezier(0.22,1,0.36,1);
    }}

    /* =========================================
       SECCIÓN 2: PRODUCTOS DIGITALES
       ========================================= */
    .products-section-container {{
        margin-top: 30px; 
        background-color: #000;
        padding: 60px 30px;
        border-radius: 28px;
        box-shadow: 
            0 0 50px 15px rgba(0, 0, 0, 0.3), 
            0 -1px 2px rgba(255, 255, 255, 0.1) inset;
        border: 1px solid rgba(255, 255, 255, 0.05);
        width: 100%;
    }}

    .title-wrapper {{ text-align: center; margin-bottom: 50px; }}

    .neon-title-text {{
        font-family: 'Quicksand', sans-serif;
        font-size: 52px;
        font-weight: 600;
        letter-spacing: 2px;
        color: transparent;
        -webkit-text-stroke: 1.5px #ffdf85;
        text-shadow:
            0 0  8px rgba(255,223,133,0.7),
            0 0 20px rgba(255,170,  0,0.8),
            0 0 40px rgba(255,140,  0,0.5);
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
        min-height: 400px;
        cursor: pointer;
        background: #1a1a1a;
        box-shadow: 0 8px 24px rgba(0,0,0,0.9);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        min-width: 0;
    }}

    .card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.85), 0 0 40px 8px rgba(255,185,30,0.14);
    }}

    .card-bg {{
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover; z-index: 1;
        opacity: 0.85;
        transition: opacity 0.4s ease;
    }}
    .card:hover .card-bg {{ opacity: 1; }}

    .card-gradient {{
        position: absolute; bottom: 0; left: 0;
        width: 100%; height: 75%;
        background: linear-gradient(to top, rgba(0,0,0,0.98) 0%, rgba(0,0,0,0.6) 40%, rgba(0,0,0,0) 100%);
        z-index: 2;
    }}

    .card-content {{ position: absolute; bottom: 20px; left: 20px; right: 20px; z-index: 5; color: white; }}
    .card-title {{ font-size: 22px; font-weight: bold; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
    .card-subtitle {{ font-size: 13px; color: #ccc; margin-bottom: 16px; line-height: 1.4; }}

    .card-btn {{
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 10px 14px;
        color: white;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        cursor: pointer;
        transition: background 0.2s, border-color 0.2s;
    }}
    .card-btn:hover {{ background: rgba(255,255,255,0.15); border-color: rgba(255,200,60,0.50); }}

    /* =========================================
       ADAPTACIÓN A MÓVIL
       ========================================= */
    @media (max-width: 768px) {{
        body {{ padding: 10px; }}
        
        #layout {{ flex-direction: column; height: auto; gap: 16px; }}
        #col-izq {{ width: 100%; height: auto; flex: none; }}
        #col-der {{ width: 100%; height: 380px; flex: none; position: relative; }}
        
        .products-section-container {{ padding: 40px 12px 50px; margin-top: 20px; border-radius: 20px; }}
        .neon-title-text {{ font-size: 30px; letter-spacing: 1px; }}
        .title-wrapper {{ margin-bottom: 40px; }}
        
        #cards-layout {{ flex-direction: column; gap: 16px; width: 100%; }}
        .card {{ flex: none; width: 100%; aspect-ratio: unset; height: 300px; }}
    }}
</style>
</head>
<body>

<div id="layout">
    <div id="col-izq">
        <img id="main-img" src="data:image/jpeg;base64,{portada_b64}" alt="Portada">
    </div>
    <div id="col-der">
        <div id="thumb">
            <img src="data:image/png;base64,{miniatura_b64}" alt="Miniatura">
        </div>
        <div id="video-wrapper">
            <video id="vid" controls playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
        </div>
    </div>
</div>

<div class="products-section-container">
    <div class="title-wrapper">
        <span class="neon-title-text">Productos Digitales</span>
    </div>
    <div id="cards-layout">
        <div class="card">
            <img class="card-bg" src="data:image/jpeg;base64,{elkar_b64}" alt="Entrevista IA">
            <div class="card-gradient"></div>
            <div class="card-content">
                <div class="card-title">Elkarr AI zketa 🎙️</div>
                <div class="card-subtitle">Entrevistas con líderes mundiales potenciadas por IA.</div>
                <button class="card-btn" data-url="https://tu-url-aqui.com/elkarraizketa">
                    <span>Explorar App</span><span>›</span>
                </button>
            </div>
        </div>
        <div class="card">
            <img class="card-bg" src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=800" alt="Red Ejecutiva">
            <div class="card-gradient"></div>
            <div class="card-content">
                <div class="card-title">Red Ejecutiva 🌐</div>
                <div class="card-subtitle">Ecosistema Vasco • Alta Dirección</div>
                <button class="card-btn" data-url="https://tu-url-aqui.com/red-ejecutiva">
                    <span>Explorar App</span><span>›</span>
                </button>
            </div>
        </div>
        <div class="card">
            <img class="card-bg" src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&q=80&w=800" alt="Radar Empresarial">
            <div class="card-gradient"></div>
            <div class="card-content">
                <div class="card-title">Radar Empresarial 📈</div>
                <div class="card-subtitle">Monitorización de tendencias y alertas con IA.</div>
                <button class="card-btn" data-url="https://tu-url-aqui.com/radar-empresarial">
                    <span>Explorar App</span><span>›</span>
                </button>
            </div>
        </div>
    </div>
</div>

<script>
    // Lógica del Vídeo
    const thumb        = document.getElementById('thumb');
    const videoWrapper = document.getElementById('video-wrapper');
    const vid          = document.getElementById('vid');

    thumb.addEventListener('click', () => {{
        thumb.style.display        = 'none';
        videoWrapper.style.display = 'block';
        vid.play();
        setTimeout(notifyHeight, 50);
    }});

    // Lógica de Botones Tarjetas
    document.querySelectorAll('.card-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            e.preventDefault();
            const url = btn.dataset.url;
            if (url) window.open(url, '_blank');
        }});
    }});

    // Sincronización de altura maestra para Streamlit (A prueba de cortes en móvil)
    function notifyHeight() {{
        const h = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight) + 20;
        window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
    }}

    window.addEventListener('load', notifyHeight);
    window.addEventListener('resize', notifyHeight);
    document.getElementById('main-img').addEventListener('load', notifyHeight);
    
    if (window.ResizeObserver) {{
        new ResizeObserver(notifyHeight).observe(document.body);
    }}

    // Despertadores para forzar el recalculo cuando las tarjetas del móvil ya han cargado
    setTimeout(notifyHeight, 500);
    setTimeout(notifyHeight, 1000);
    setTimeout(notifyHeight, 2000);
</script>

</body>
</html>
"""

# Le damos un height inmenso de base para que en móvil nazca desplegado.
# El script de arriba se encargará de recortarlo a la medida perfecta en milisegundos.
st.components.v1.html(html_completo, height=2500, scrolling=False)