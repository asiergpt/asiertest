import streamlit as st
import base64

st.set_page_config(page_title="Portfolio | Asier Dorronsoro", layout="wide")

@st.cache_data
def to_b64_video(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

@st.cache_data
def to_b64_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.markdown("""
<style>
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 3rem !important; max-width: 95% !important; }
</style>
""", unsafe_allow_html=True)

video_b64     = to_b64_video("assets/Intro.mp4")
miniatura_b64 = to_b64_img("assets/miniatura.png")
portada_b64   = to_b64_img("assets/portada.jpeg")

iframe_html = f"""
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    /* ─── DESKTOP ─────────────────────────────────── */
    #layout {{
        display: flex;
        flex-direction: row;
        gap: 24px;
        width: 100%;
        align-items: stretch;
    }}

    #col-izq {{
        flex: 2.4;
        min-width: 0;
    }}

    #col-izq img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        border-radius: 12px;
    }}

    #col-der {{
        flex: 1;
        min-width: 0;
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Thumb: ocupa todo el col-der en desktop */
    #thumb {{
        cursor: pointer;
        width: 100%;
        height: 100%;
        display: block;
    }}

    #thumb img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        /* SIN transition para que el swap sea instantáneo */
    }}

    #video-wrapper {{
        display: none;
        width: 100%;
        height: 100%;
        background: #000;
        border-radius: 12px;
        overflow: hidden;
    }}

    #vid {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
    }}

    /* ─── MOBILE ──────────────────────────────────── */
    @media (max-width: 768px) {{
        #layout {{
            flex-direction: column;
            gap: 16px;
        }}

        /* Portada: ratio 4:3 */
        #col-izq {{
            flex: none;
            width: 100%;
        }}

        #col-izq img {{
            width: 100%;
            height: auto;
            aspect-ratio: 4 / 3;
            object-fit: cover;
            border-radius: 12px;
        }}

        /* Vídeo/miniatura: ratio 9:16 (vertical) */
        #col-der {{
            flex: none;
            width: 100%;
            /* Anulamos el height inline que pone syncHeight */
            height: auto !important;
            aspect-ratio: 9 / 16;
            border-radius: 12px;
        }}

        #thumb {{
            width: 100%;
            height: 100%;
        }}

        #thumb img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
        }}

        #video-wrapper {{
            width: 100%;
            height: 100%;
            border-radius: 12px;
        }}

        #vid {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
    }}
</style>

<div id="layout">

    <div id="col-izq">
        <img src="data:image/jpeg;base64,{portada_b64}" alt="Portada">
    </div>

    <div id="col-der">

        <div id="thumb">
            <img id="thumb-img"
                 src="data:image/png;base64,{miniatura_b64}"
                 alt="Miniatura">
        </div>

        <div id="video-wrapper">
            <video id="vid" controls playsinline
                   poster="data:image/png;base64,{miniatura_b64}">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
        </div>

    </div>
</div>

<script>
    const thumb        = document.getElementById('thumb');
    const videoWrapper = document.getElementById('video-wrapper');
    const vid          = document.getElementById('vid');
    const thumbImg     = document.getElementById('thumb-img');
    const colDer       = document.getElementById('col-der');

    /* ── syncHeight: solo en desktop ── */
    function isMobile() {{
        return window.innerWidth <= 768;
    }}

    function syncHeight() {{
        if (isMobile()) {{
            /* En móvil el aspect-ratio CSS controla la altura; limpiamos inline */
            colDer.style.height = '';
            return;
        }}
        const colIzq = document.getElementById('col-izq');
        const h = colIzq.getBoundingClientRect().height;
        if (h > 0) colDer.style.height = h + 'px';
    }}

    const portadaImg = document.querySelector('#col-izq img');
    portadaImg.addEventListener('load', () => {{
        syncHeight();
        notifyHeight();
    }});
    if (portadaImg.complete) {{ syncHeight(); notifyHeight(); }}
    window.addEventListener('resize', () => {{ syncHeight(); notifyHeight(); }});

    /* ── Swap instantáneo: sin transición, sin morphing ── */
    thumb.addEventListener('click', () => {{
        thumb.style.display  = 'none';
        videoWrapper.style.display = 'block';
        vid.play();
        notifyHeight();
    }});

    /* ── Hover solo en desktop (en móvil no hay hover real) ── */
    thumb.addEventListener('mouseover', () => {{
        if (!isMobile()) thumbImg.style.filter = 'brightness(0.75)';
    }});
    thumb.addEventListener('mouseout', () => {{
        thumbImg.style.filter = 'brightness(1)';
    }});

    /* ── Notifica altura real al iframe de Streamlit ── */
    function notifyHeight() {{
        const h = document.getElementById('layout').scrollHeight + 32;
        window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
    }}

    /* Observa cambios de tamaño del layout para ajustar el iframe */
    if (window.ResizeObserver) {{
        new ResizeObserver(notifyHeight).observe(document.getElementById('layout'));
    }}
</script>
"""

st.components.v1.html(iframe_html, height=1200, scrolling=False)
