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

video_b64   = to_b64_video("assets/Intro.mp4")
miniatura_b64 = to_b64_img("assets/miniatura.png")
portada_b64   = to_b64_img("assets/portada.jpeg")

iframe_html = f"""
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    #layout {{
        display: flex;
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

    #thumb {{
        cursor: pointer;
        width: 100%;
        height: 100%;
        position: relative;
        display: block;
    }}

    #thumb img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        transition: filter 0.3s;
    }}

    #video-wrapper {{
        display: none;
        width: 100%;
        height: 100%;
        background: #000;
    }}

    #vid {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
    }}
</style>

<div id="layout">

    <div id="col-izq">
        <img src="data:image/jpeg;base64,{portada_b64}" alt="Portada">
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
    const thumb       = document.getElementById('thumb');
    const videoWrapper = document.getElementById('video-wrapper');
    const vid         = document.getElementById('vid');
    const thumbImg    = document.getElementById('thumb-img');

    function syncHeight() {{
        const colIzq = document.getElementById('col-izq');
        const colDer = document.getElementById('col-der');
        const h = colIzq.getBoundingClientRect().height;
        if (h > 0) {{
            colDer.style.height = h + 'px';
        }}
    }}

    const portadaImg = document.querySelector('#col-izq img');
    portadaImg.addEventListener('load', syncHeight);
    if (portadaImg.complete) syncHeight();

    window.addEventListener('resize', syncHeight);

    thumb.addEventListener('click', () => {{
        thumb.style.display = 'none';
        videoWrapper.style.display = 'block';
        vid.play();
    }});

    thumb.addEventListener('mouseover', () => {{
        thumbImg.style.filter = 'brightness(0.75)';
    }});

    thumb.addEventListener('mouseout', () => {{
        thumbImg.style.filter = 'brightness(1)';
    }});
</script>
"""

st.components.v1.html(iframe_html, height=1200, scrolling=False)
