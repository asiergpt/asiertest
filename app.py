import streamlit as st
import base64

st.set_page_config(page_title="Portfolio | Asier Dorronsoro", layout="wide")

@st.cache_data
def to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

video_b64 = to_b64("assets/Intro.mp4")
miniatura_b64 = to_b64("assets/miniatura.png")
portada_b64 = to_b64("assets/portada.jpeg")
elkar_b64 = to_b64("assets/elkarraizketa.jpeg")
eme_b64 = to_b64("assets/malcubo.jpeg")
ras_b64 = to_b64("assets/rastreator.jpeg")

html_nativo = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@600&display=swap');

/* LIMPIEZA DE STREAMLIT */
#MainMenu, header, footer {{ visibility: hidden; display: none; }}
.block-container {{ padding: 2rem 1rem 0rem 1rem !important; max-width: 1400px !important; }}
[data-testid="stAppViewContainer"], [data-testid="stApp"] {{ background-color: #ffffff !important; }}
[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}

.portfolio-wrapper {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; width: 100%; background: white; color: black; box-sizing: border-box; overflow-x: hidden; }}

/* CABECERA */
.top-layout {{ display: flex; gap: 24px; margin-bottom: 30px; align-items: stretch; }}
.col-izq, .col-der {{ flex: 2.4; border-radius: 12px; overflow: hidden; background: #1a1a1a; box-shadow: 0 15px 35px rgba(0,0,0,0.15); display: flex; transition: all 0.4s ease; }}
.col-der {{ flex: 1; background: #000; justify-content: center; align-items: center; position: relative; }}

.col-izq:hover, .col-der:hover {{ box-shadow: 0 15px 35px rgba(0,0,0,0.2), 0 0 25px 4px rgba(255, 204, 102, 0.15); transform: translateY(-3px); }}
.col-izq img {{ width: 100%; height: auto; display: block; }}
.col-der video {{ width: 100%; height: 100%; object-fit: contain; border-radius: 12px; cursor: pointer; outline: none; }}

/* BLOQUES NEGROS */
.black-block {{ background-color: #000; border-radius: 28px; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.05); padding: 60px 30px; margin-bottom: 30px; width: 100%; }}
.neon-title {{ font-family: 'Quicksand', sans-serif; font-size: clamp(32px, 4vw, 52px); font-weight: 600; text-align: center; margin-bottom: 50px; color: transparent; -webkit-text-stroke: 1.5px #ffcc66; text-shadow: 0 0 10px rgba(255, 204, 102, 0.3); }}

/* TARJETAS DE PRODUCTOS - AJUSTE CLAVE DE WIDTH Y TOP/LEFT */
.cards-container {{ display: flex; gap: 24px; max-width: 1200px; margin: 0 auto; width: 100%; }}
.card-link {{ flex: 1; text-decoration: none; color: inherit; display: block; width: 100%; }}
.card {{ position: relative; border-radius: 16px; overflow: hidden; aspect-ratio: 3/4; background: #1a1a1a; transition: transform 0.4s ease, box-shadow 0.4s ease; width: 100%; height: 100%; display: block; }}
.card-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.7; transition: opacity 0.3s; display: block; }}
.card-gradient {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 70%; background: linear-gradient(to top, rgba(0,0,0,0.95), transparent); z-index: 2; }}
.card-content {{ position: absolute; bottom: 20px; left: 20px; right: 20px; z-index: 5; color: white; }}
.card-title {{ font-size: 22px; font-weight: bold; margin-bottom: 5px; line-height: 1.2; }}
.card-subtitle {{ font-size: 13px; color: #ccc; margin-bottom: 12px; line-height: 1.4; }}
.card-btn {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 10px; color: white; width: 100%; text-align: center; font-size: 13px; font-weight: 500; transition: all 0.3s; }}

.card-link:hover .card {{ transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.8), 0 0 35px 8px rgba(255, 204, 102, 0.2); }}
.card-link:hover .card-bg {{ opacity: 0.9; }}
.card-link:hover .card-btn {{ border-color: rgba(255, 204, 102, 0.5); background: rgba(255, 255, 255, 0.15); }}

/* TECH STACK */
.tech-padding {{ padding: 40px 20px; }}
.neon-small {{ margin-bottom: 30px; font-size: clamp(28px, 3vw, 36px); -webkit-text-stroke: 1.2px #ffcc66; }}
.tech-scroll {{ display: flex; gap: 20px; overflow-x: auto; padding-bottom: 20px; scroll-behavior: smooth; scrollbar-width: thin; scrollbar-color: rgba(255, 204, 102, 0.6) rgba(255, 255, 255, 0.05); }}
.tech-scroll::-webkit-scrollbar {{ height: 6px; }}
.tech-scroll::-webkit-scrollbar-track {{ background: rgba(255, 255, 255, 0.05); border-radius: 10px; }}
.tech-scroll::-webkit-scrollbar-thumb {{ background: rgba(255, 204, 102, 0.6); border-radius: 10px; }}
.tech-scroll::-webkit-scrollbar-thumb:hover {{ background: rgba(255, 204, 102, 0.9); }}

.tech-item {{ flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; width: 90px; }}
.tech-circle {{ width: 70px; height: 70px; background: #111; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; border: 2px solid rgba(255,255,255,0.1); transition: 0.3s; }}
.tech-name {{ color: white; font-size: 11px; opacity: 0.8; text-align: center; margin-top: 10px; width: 100%; word-wrap: break-word; transition: color 0.3s; }}

.tech-item:hover .tech-circle {{ border-color: #ffcc66; transform: scale(1.1); box-shadow: 0 0 20px rgba(255, 204, 102, 0.4); }}
.tech-item:hover .tech-name {{ color: #ffcc66; opacity: 1; }}

/* FOOTER */
.footer-minimal {{ background-color: #ffffff; color: #000000; padding: 60px 20px 40px; text-align: center; width: 100%; }}
.footer-links {{ display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; font-size: 14px; color: #333; }}
.footer-links a {{ text-decoration: none; color: inherit; font-weight: 500; transition: opacity 0.2s; }}
.footer-links a:hover {{ opacity: 0.6; color: #ffcc66; }}
.f-divider {{ color: #ccc; font-weight: 300; }}
.f-copyright {{ margin-top: 30px; font-size: 10px; letter-spacing: 3px; color: #aaa; text-transform: uppercase; }}

/* =========================================
   ADAPTACIÓN MÓVIL EXACTA Y FORZADA
   ========================================= */
@media (max-width: 768px) {{
    .top-layout, .cards-container, .footer-links {{ flex-direction: column; }}
    .f-divider {{ display: none; }}
    
    /* Obligamos a la tarjeta a ocupar todo el ancho, de lado a lado */
    .cards-container {{ width: 100%; gap: 20px; }}
    .card-link {{ width: 100%; display: block; }}
    .card {{ 
        width: 100% !important; 
        height: 380px !important; 
        aspect-ratio: auto !important; /* Desactiva la proporción del PC */
        display: block; 
    }}
    .card-bg {{ width: 100%; height: 100%; top: 0; left: 0; object-fit: cover; }}
    
    .col-der video {{ min-height: 250px; }}
    .black-block {{ padding: 40px 20px; width: 100%; }}
}}
</style>

<div class="portfolio-wrapper">
<div class="top-layout">
<div class="col-izq">
<img src="data:image/jpeg;base64,{portada_b64}" alt="Portada">
</div>
<div class="col-der">
<video controls poster="data:image/png;base64,{miniatura_b64}" preload="none">
<source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
</video>
</div>
</div>

<div class="black-block">
<div class="neon-title">Productos Digitales</div>
<div class="cards-container">
<a href="#" target="_blank" class="card-link">
<div class="card">
<img class="card-bg" src="data:image/jpeg;base64,{elkar_b64}">
<div class="card-gradient"></div>
<div class="card-content">
<div class="card-title">Elkarr AI zketa 🎙️</div>
<div class="card-subtitle">Conoce a Asier Dorronsoro • FAQ</div>
<div class="card-btn">Explorar App</div>
</div>
</div>
</a>
<a href="https://asier-dorronsoro-busca-trabajo.streamlit.app/" target="_blank" class="card-link">
<div class="card">
<img class="card-bg" src="data:image/jpeg;base64,{eme_b64}">
<div class="card-gradient"></div>
<div class="card-content">
<div class="card-title">M al cubo 🌐</div>
<div class="card-subtitle">Penetra el ecosistema empresarial Vasco • Alta Dirección</div>
<div class="card-btn">Explorar App</div>
</div>
</div>
</a>
<a href="#" target="_blank" class="card-link">
<div class="card">
<img class="card-bg" src="data:image/jpeg;base64,{ras_b64}">
<div class="card-gradient"></div>
<div class="card-content">
<div class="card-title">Rastreator 📈</div>
<div class="card-subtitle">Monitoriza noticias y eventos empresariales en el País Vasco • News & Network</div>
<div class="card-btn">Explorar App</div>
</div>
</div>
</a>
</div>
</div>

<div class="black-block tech-padding">
<div class="neon-title neon-small">Tech Stack</div>
<div class="tech-scroll">
<div class="tech-item"><div class="tech-circle">🐍</div><span class="tech-name">Python</span></div>
<div class="tech-item"><div class="tech-circle">💾</div><span class="tech-name">SQL</span></div>
<div class="tech-item"><div class="tech-circle">🟨</div><span class="tech-name">Javascript</span></div>
<div class="tech-item"><div class="tech-circle">🌐</div><span class="tech-name">CSS/HTML</span></div>
<div class="tech-item"><div class="tech-circle">🐙</div><span class="tech-name">GitHub</span></div>
<div class="tech-item"><div class="tech-circle">🚀</div><span class="tech-name">Streamlit</span></div>
<div class="tech-item"><div class="tech-circle">🔍</div><span class="tech-name">BigQuery</span></div>
<div class="tech-item"><div class="tech-circle">📊</div><span class="tech-name">Scikit-Learn</span></div>
<div class="tech-item"><div class="tech-circle">✨</div><span class="tech-name">Gemini</span></div>
<div class="tech-item"><div class="tech-circle">💬</div><span class="tech-name">ChatGPT</span></div>
<div class="tech-item"><div class="tech-circle">📝</div><span class="tech-name">Claude</span></div>
<div class="tech-item"><div class="tech-circle">🎬</div><span class="tech-name">Higgsfield</span></div>
<div class="tech-item"><div class="tech-circle">🖼️</div><span class="tech-name">Freepik</span></div>
<div class="tech-item"><div class="tech-circle">👤</div><span class="tech-name">HeyGen</span></div>
<div class="tech-item"><div class="tech-circle">🔎</div><span class="tech-name">Magnific.ai</span></div>
<div class="tech-item"><div class="tech-circle">🍌</div><span class="tech-name">Banana 2</span></div>
<div class="tech-item"><div class="tech-circle">📹</div><span class="tech-name">Google Veo</span></div>
<div class="tech-item"><div class="tech-circle">🎞️</div><span class="tech-name">Kling</span></div>
<div class="tech-item"><div class="tech-circle">🌀</div><span class="tech-name">Wan</span></div>
<div class="tech-item"><div class="tech-circle">💃</div><span class="tech-name">Seedance</span></div>
<div class="tech-item"><div class="tech-circle">🦜</div><span class="tech-name">LangChain</span></div>
<div class="tech-item"><div class="tech-circle">👥</div><span class="tech-name">Crew.AI</span></div>
</div>
</div>

<div class="footer-minimal">
<div class="footer-links">
<span>San Sebastián, España</span>
<span class="f-divider">|</span>
<a href="tel:+34681049678">+34 681 049 678</a>
<span class="f-divider">|</span>
<a href="mailto:asierdorronaldaz@outlook.com">asierdorronaldaz@outlook.com</a>
<span class="f-divider">|</span>
<a href="https://linkedin.com/in/asierdorronsoro" target="_blank">LinkedIn: /asierdorronsoro</a>
</div>
<div class="f-copyright">ASIER DORRONSORO • 2026</div>
</div>
</div>
"""

st.markdown(html_nativo, unsafe_allow_html=True)