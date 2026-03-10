import streamlit as st
import base64

st.set_page_config(page_title="Portfolio | Asier Dorronsoro", layout="wide")

@st.cache_data
def to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.warning(f"⚠️ Archivo no encontrado: {path}")
        return ""

# ─────────────────────────────────────────────
# FIX 3 — VELOCIDAD: NO cargar el video al inicio
# Solo se cargan imágenes livianas (miniatura y portada)
# El video se inyecta en el DOM solo cuando el usuario hace click
# ─────────────────────────────────────────────
miniatura_b64 = to_b64("assets/miniatura.png")
portada_b64   = to_b64("assets/portada.jpeg")
elkar_b64     = to_b64("assets/elkarraizketa.jpeg")

# El video se lee pero se convierte a blob URL en el cliente
# para no bloquear la carga inicial del HTML
video_b64 = to_b64("assets/Intro.mp4")

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


# ─────────────────────────────────────────────
# BLOQUE 1: VIDEO Y PORTADA
# FIX 1 — IMAGEN: object-fit contain para no recortar
# FIX 2 — ESPACIO: altura del iframe reducida + padding-bottom eliminado
# FIX 3 — VELOCIDAD: video se carga solo al hacer click (lazy)
# ─────────────────────────────────────────────
iframe_header = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  html, body {{
    background: transparent;
    overflow-x: hidden;
    width: 100%;
  }}

  body {{
    /* FIX 2 — quitar padding-bottom para reducir espacio entre bloques */
    padding: 20px 20px 0px 20px;
  }}

  /* ── DESKTOP ── */
  #layout {{
    display: flex;
    flex-direction: row;
    gap: 24px;
    width: 100%;
    /* FIX 1 — altura responsiva en lugar de fija */
    height: clamp(320px, 55vw, 680px);
    align-items: stretch;
  }}

  #col-izq {{
    flex: 2.4;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0,0,0,0.7);
    transition: box-shadow 0.4s cubic-bezier(0.22,1,0.36,1);
    cursor: pointer;
    /* FIX 1 — fondo oscuro por si contain deja espacio vacío */
    background-color: #111;
  }}
  #col-izq:hover {{
    box-shadow:
      0 20px 40px rgba(0,0,0,0.85),
      0 0 40px 8px  rgba(255,185,30,0.14),
      0 0 80px 16px rgba(255,140, 0,0.08),
      0 0 0    1px  rgba(255,200,60,0.18);
  }}
  #col-izq img {{
    width: 100%;
    height: 100%;
    /* FIX 1 — contener la imagen completa sin recortar */
    object-fit: contain;
    object-position: center;
    display: block;
  }}

  #col-der {{
    flex: 1;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 30px rgba(0,0,0,0.7);
    background: #000;
    transition: box-shadow 0.4s cubic-bezier(0.22,1,0.36,1);
  }}
  #col-der:hover {{
    box-shadow:
      0 20px 40px rgba(0,0,0,0.85),
      0 0 40px 8px  rgba(255,185,30,0.14),
      0 0 80px 16px rgba(255,140, 0,0.08),
      0 0 0    1px  rgba(255,200,60,0.18);
  }}

  #thumb {{
    position: absolute;
    inset: 0;
    cursor: pointer;
    z-index: 2;
  }}
  #thumb img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}

  /* Overlay "play" encima de la miniatura */
  #play-btn {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 64px;
    height: 64px;
    background: rgba(255,185,30,0.85);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 3;
    pointer-events: none;
    transition: transform 0.2s ease, background 0.2s ease;
    box-shadow: 0 0 30px rgba(255,170,0,0.5);
  }}
  #thumb:hover #play-btn {{
    transform: translate(-50%, -50%) scale(1.12);
    background: rgba(255,200,60,0.95);
  }}
  #play-btn svg {{
    width: 26px;
    height: 26px;
    fill: #000;
    margin-left: 4px;
  }}

  /* FIX 3 — spinner visible mientras carga el video */
  #loading-spinner {{
    display: none;
    position: absolute;
    inset: 0;
    background: #000;
    z-index: 4;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 14px;
  }}
  #loading-spinner.visible {{
    display: flex;
  }}
  .spinner-ring {{
    width: 48px;
    height: 48px;
    border: 3px solid rgba(255,185,30,0.2);
    border-top-color: rgba(255,185,30,0.9);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }}
  .spinner-text {{
    color: rgba(255,200,80,0.7);
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 1px;
  }}
  @keyframes spin {{
    to {{ transform: rotate(360deg); }}
  }}

  #video-wrapper {{
    position: absolute;
    inset: 0;
    display: none;
    background: #000;
    z-index: 5;
  }}
  #vid {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
  }}

  /* ── MÓVIL ── */
  @media (max-width: 768px) {{
    body {{
      /* FIX 2 — sin padding-bottom en móvil */
      padding: 10px 10px 0px 10px;
    }}

    #layout {{
      flex-direction: column;
      /* FIX 1 — sin altura fija en móvil, se adapta al contenido */
      height: auto;
      gap: 12px;
    }}

    #col-izq {{
      width: 100%;
      /* FIX 1 — altura proporcional al ancho de pantalla en móvil */
      height: 56vw;
      min-height: 180px;
      flex: none;
      background-color: #111;
    }}

    #col-der {{
      width: 100%;
      /* FIX 1 — altura proporcional, no fija */
      height: 72vw;
      min-height: 240px;
      flex: none;
      position: relative;
    }}

    #thumb,
    #video-wrapper,
    #loading-spinner {{
      position: absolute;
      top: 0; left: 0;
      width: 100%;
      height: 100%;
    }}
  }}
</style>
</head>
<body>

<div id="layout">

  <!-- Columna izquierda: portada -->
  <div id="col-izq">
    <img src="data:image/jpeg;base64,{portada_b64}" alt="Portada" loading="eager">
  </div>

  <!-- Columna derecha: miniatura → video lazy -->
  <div id="col-der">

    <div id="thumb">
      <img src="data:image/png;base64,{miniatura_b64}" alt="Miniatura" loading="eager">
      <div id="play-btn">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </div>
    </div>

    <!-- FIX 3 — spinner mientras el video decodifica el base64 -->
    <div id="loading-spinner">
      <div class="spinner-ring"></div>
      <span class="spinner-text">Cargando video...</span>
    </div>

    <div id="video-wrapper">
      <video id="vid" controls playsinline></video>
    </div>

  </div>
</div>

<script>
  const thumb        = document.getElementById('thumb');
  const videoWrapper = document.getElementById('video-wrapper');
  const spinner      = document.getElementById('loading-spinner');
  const vid          = document.getElementById('vid');

  // FIX 3 — Convertir base64 a Blob URL para no bloquear el hilo principal
  // El video solo se decodifica cuando el usuario hace click
  function base64ToBlob(base64, mime) {{
    const binary = atob(base64);
    const arr    = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) arr[i] = binary.charCodeAt(i);
    return new Blob([arr], {{ type: mime }});
  }}

  let videoLoaded = false;
  const videoBase64 = "{video_b64}";

  thumb.addEventListener('click', () => {{
    if (videoLoaded) return;
    videoLoaded = true;

    // Mostrar spinner, ocultar miniatura
    thumb.style.display        = 'none';
    spinner.classList.add('visible');

    // Diferir la decodificación para no bloquear el render
    setTimeout(() => {{
      const blob = base64ToBlob(videoBase64, 'video/mp4');
      const url  = URL.createObjectURL(blob);

      vid.src = url;
      vid.addEventListener('canplay', () => {{
        spinner.classList.remove('visible');
        videoWrapper.style.display = 'block';
        vid.play();
        notifyHeight();
      }}, {{ once: true }});

      vid.load();
    }}, 50);
  }});

  // FIX 2 — Notificar altura exacta para reducir espacio entre bloques
  function notifyHeight() {{
    const h = document.documentElement.scrollHeight;
    window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
  }}

  window.addEventListener('load',   notifyHeight);
  window.addEventListener('resize', notifyHeight);
  if (window.ResizeObserver) {{
    new ResizeObserver(notifyHeight).observe(document.body);
  }}
  setTimeout(notifyHeight, 100);
  setTimeout(notifyHeight, 400);
</script>

</body>
</html>
"""

# FIX 2 — Reducir altura del iframe: el JS ajusta el resto automáticamente
# clamp() en CSS ya controla el layout, así que 650 es suficiente para desktop
st.components.v1.html(iframe_header, height=650, scrolling=False)


# ─────────────────────────────────────────────
# BLOQUE 2: SECCIÓN DE PRODUCTOS
# FIX 2 — ESPACIO: margin-top reducido para acercar ambos bloques
# ─────────────────────────────────────────────
html_productos = f"""
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

    body {{ padding: 0px 24px 40px 24px; }}

    .products-section-container {{
        /* FIX 2 — margin-top reducido drásticamente (era 60px) */
        margin-top: 12px;
        background-color: #000;
        padding: 80px 30px;
        border-radius: 28px;
        box-shadow: 0 0 60px 20px rgba(0,0,0,0.8);
        width: 100%;
    }}

    .title-wrapper {{
        text-align: center;
        margin-bottom: 60px;
    }}

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
        transition:
            transform  0.4s cubic-bezier(0.22,1,0.36,1),
            box-shadow 0.4s cubic-bezier(0.22,1,0.36,1);
        min-width: 0;
    }}

    .card:hover {{
        transform: translateY(-10px);
        box-shadow:
            0 20px 40px rgba(0,0,0,0.85),
            0 0 40px 8px  rgba(255,185,30,0.14),
            0 0 80px 16px rgba(255,140, 0,0.08),
            0 0 0    1px  rgba(255,200,60,0.18);
    }}

    .card-bg {{
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover; z-index: 1;
        opacity: 0.85;
        transition: opacity 0.4s ease;
    }}
    .card:hover .card-bg {{ opacity: 1; }}

    .card::after {{
        content: '';
        position: absolute; inset: 0;
        background: radial-gradient(
            ellipse at 50% 100%,
            rgba(255,170,30,0.07) 0%,
            transparent 70%
        );
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 4;
        pointer-events: none;
    }}
    .card:hover::after {{ opacity: 1; }}

    .card-gradient {{
        position: absolute; bottom: 0; left: 0;
        width: 100%; height: 75%;
        background: linear-gradient(
            to top,
            rgba(0,0,0,0.98) 0%,
            rgba(0,0,0,0.6)  40%,
            rgba(0,0,0,0)    100%
        );
        z-index: 2;
    }}

    .card-content {{
        position: absolute; bottom: 20px;
        left: 20px; right: 20px;
        z-index: 5; color: white;
    }}

    .card-title {{
        font-size: 22px; font-weight: bold;
        margin-bottom: 4px;
        display: flex; align-items: center; gap: 8px;
    }}

    .card-subtitle {{
        font-size: 13px; color: #ccc;
        margin-bottom: 16px; line-height: 1.4;
    }}

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
    .card:hover .card-btn {{ border-color: rgba(255,200,60,0.30); }}
    .card-btn:hover {{
        background: rgba(255,255,255,0.15);
        border-color: rgba(255,200,60,0.50) !important;
    }}
    .card-btn:active {{
        transform: scale(0.98);
    }}

    /* ── MÓVIL ── */
    @media (max-width: 768px) {{
        body {{ padding: 0px 10px 30px; }}

        .products-section-container {{
            padding: 40px 12px 50px;
            /* FIX 2 — margin-top mínimo en móvil */
            margin-top: 8px;
            border-radius: 20px;
        }}

        .neon-title-text {{ font-size: 30px; letter-spacing: 1px; }}
        .title-wrapper {{ margin-bottom: 40px; }}

        #cards-layout {{
            flex-direction: column;
            gap: 16px;
            width: 100%;
            max-width: 100%;
        }}

        .card {{
            flex: none;
            width: 100%;
            min-width: 0;
            max-width: 100%;
            aspect-ratio: unset;
            height: 300px;
            min-height: unset;
        }}
    }}
</style>
</head>
<body>

<div class="products-section-container">
    <div class="title-wrapper">
        <span class="neon-title-text">Productos Digitales</span>
    </div>
    <div id="cards-layout">

        <div class="card">
            <img class="card-bg"
                 src="data:image/jpeg;base64,{elkar_b64}"
                 alt="Entrevista IA"
                 loading="lazy">
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
            <img class="card-bg"
                 src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=800"
                 alt="Red Ejecutiva"
                 loading="lazy">
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
            <img class="card-bg"
                 src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&q=80&w=800"
                 alt="Radar Empresarial"
                 loading="lazy">
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
    document.querySelectorAll('.card-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            e.preventDefault();
            e.stopPropagation();
            const url = btn.dataset.url;
            if (url) window.open(url, '_blank');
        }});
    }});

    function notifyHeight() {{
        const h = document.documentElement.scrollHeight + 20;
        window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
    }}

    window.addEventListener('load',   notifyHeight);
    window.addEventListener('resize', notifyHeight);
    if (window.ResizeObserver) new ResizeObserver(notifyHeight).observe(document.body);
    setTimeout(notifyHeight, 200);
    setTimeout(notifyHeight, 600);
</script>

</body>
</html>
"""

st.components.v1.html(html_productos, height=1400, scrolling=False)
