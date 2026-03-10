# ─────────────────────────────────────────────
# BLOQUE UNIFICADO: VIDEO, PORTADA Y PRODUCTOS
# ─────────────────────────────────────────────
html_completo = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@600&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}

  html, body {{
    background: transparent;
    overflow-x: hidden;
    width: 100%;
  }}

  body {{
    padding: 20px;
  }}

  /* ── SECCIÓN 1: VIDEO Y PORTADA (DESKTOP) ── */
  #layout {{
    display: flex;
    flex-direction: row;
    gap: 24px;
    width: 100%;
    height: 680px;
    align-items: stretch;
  }}

  #col-izq {{
    flex: 2.4;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0,0,0,0.7);
    transition: box-shadow 0.4s cubic-bezier(0.22,1,0.36,1);
    cursor: pointer;
    background-color: #000; /* Fondo negro por si la imagen no llena el ancho */
  }}
  #col-izq:hover {{
    box-shadow: 0 20px 40px rgba(0,0,0,0.85), 0 0 40px 8px rgba(255,185,30,0.14), 0 0 80px 16px rgba(255,140, 0,0.08), 0 0 0 1px rgba(255,200,60,0.18);
  }}
  #col-izq img {{
    width: 100%;
    height: 100%;
    object-fit: contain; /* <-- CAMBIADO: Antes cover, ahora contain para evitar recortes */
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
    box-shadow: 0 20px 40px rgba(0,0,0,0.85), 0 0 40px 8px rgba(255,185,30,0.14), 0 0 80px 16px rgba(255,140, 0,0.08), 0 0 0 1px rgba(255,200,60,0.18);
  }}

  #thumb {{ position: absolute; inset: 0; cursor: pointer; z-index: 2; }}
  #thumb img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  
  #video-wrapper {{ position: absolute; inset: 0; display: none; background: #000; z-index: 3; }}
  #vid {{ width: 100%; height: 100%; object-fit: contain; display: block; }}


  /* ── SECCIÓN 2: PRODUCTOS (DESKTOP) ── */
  .products-section-container {{
    margin-top: 60px;
    background-color: #000;
    padding: 80px 30px;
    border-radius: 28px;
    box-shadow: 0 0 60px 20px rgba(0,0,0,0.8);
    width: 100%;
  }}

  .title-wrapper {{ text-align: center; margin-bottom: 60px; }}

  .neon-title-text {{
    font-family: 'Quicksand', sans-serif; font-size: 52px; font-weight: 600;
    letter-spacing: 2px; color: transparent; -webkit-text-stroke: 1.5px #ffdf85;
    text-shadow: 0 0 8px rgba(255,223,133,0.7), 0 0 20px rgba(255,170, 0,0.8), 0 0 40px rgba(255,140, 0,0.5);
  }}

  #cards-layout {{
    display: flex; flex-direction: row; gap: 24px; width: 100%;
    max-width: 1200px; margin: 0 auto;
  }}

  .card {{
    flex: 1; position: relative; border-radius: 16px; overflow: hidden;
    aspect-ratio: 3 / 4; min-height: 400px; cursor: pointer;
    background: #1a1a1a; box-shadow: 0 8px 24px rgba(0,0,0,0.9);
    transition: transform 0.4s cubic-bezier(0.22,1,0.36,1), box-shadow 0.4s cubic-bezier(0.22,1,0.36,1);
    min-width: 0;
  }}
  .card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.85), 0 0 40px 8px rgba(255,185,30,0.14), 0 0 80px 16px rgba(255,140, 0,0.08), 0 0 0 1px rgba(255,200,60,0.18);
  }}

  .card-bg {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    object-fit: cover; z-index: 1; opacity: 0.85; transition: opacity 0.4s ease;
  }}
  .card:hover .card-bg {{ opacity: 1; }}

  .card::after {{
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 100%, rgba(255,170,30,0.07) 0%, transparent 70%);
    opacity: 0; transition: opacity 0.4s ease; z-index: 4; pointer-events: none;
  }}
  .card:hover::after {{ opacity: 1; }}

  .card-gradient {{
    position: absolute; bottom: 0; left: 0; width: 100%; height: 75%;
    background: linear-gradient(to top, rgba(0,0,0,0.98) 0%, rgba(0,0,0,0.6) 40%, rgba(0,0,0,0) 100%);
    z-index: 2;
  }}

  .card-content {{ position: absolute; bottom: 20px; left: 20px; right: 20px; z-index: 5; color: white; }}
  .card-title {{ font-size: 22px; font-weight: bold; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
  .card-subtitle {{ font-size: 13px; color: #ccc; margin-bottom: 16px; line-height: 1.4; }}

  .card-btn {{
    background: rgba(255,255,255,0.08); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 10px 14px;
    color: white; width: 100%; display: flex; justify-content: space-between; align-items: center;
    font-size: 13px; cursor: pointer; transition: background 0.2s, border-color 0.2s;
  }}
  .card:hover .card-btn {{ border-color: rgba(255,200,60,0.30); }}
  .card-btn:hover {{ background: rgba(255,255,255,0.15); border-color: rgba(255,200,60,0.50) !important; }}


  /* ── MÓVIL (UNIFICADO) ── */
  @media (max-width: 768px) {{
    body {{ padding: 10px; }}

    #layout {{ flex-direction: column; height: auto; gap: 16px; }}
    #col-izq {{ width: 100%; height: 240px; flex: none; }}
    #col-der {{ width: 100%; height: 380px; flex: none; position: relative; }}
    
    #thumb, #video-wrapper {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}

    .products-section-container {{ padding: 40px 12px 50px; margin-top: 20px; border-radius: 20px; }}
    .neon-title-text {{ font-size: 30px; letter-spacing: 1px; }}
    .title-wrapper {{ margin-bottom: 40px; }}

    #cards-layout {{ flex-direction: column; gap: 16px; width: 100%; max-width: 100%; }}
    .card {{ flex: none; width: 100%; min-width: 0; max-width: 100%; aspect-ratio: unset; height: 300px; min-height: unset; }}
  }}
</style>
</head>
<body>

<div id="layout">
  <div id="col-izq">
    <img src="data:image/jpeg;base64,{portada_b64}" alt="Portada">
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
  // Script para Video
  const thumb = document.getElementById('thumb');
  const videoWrapper = document.getElementById('video-wrapper');
  const vid = document.getElementById('vid');

  thumb.addEventListener('click', () => {{
    thumb.style.display = 'none';
    videoWrapper.style.display = 'block';
    vid.play();
    setTimeout(notifyHeight, 100);
  }});

  // Script para Cards
  document.querySelectorAll('.card-btn').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
          e.preventDefault();
          e.stopPropagation();
          const url = btn.dataset.url;
          if (url) window.open(url, '_blank');
      }});
  }});

  // Notificación de Altura unificada para Streamlit
  function notifyHeight() {{
      // body.scrollHeight suele ser más exacto que documentElement en un layout unificado
      const h = document.body.scrollHeight + 50; 
      window.parent.postMessage({{ type: 'streamlit:setFrameHeight', height: h }}, '*');
  }}

  window.addEventListener('load', notifyHeight);
  window.addEventListener('resize', notifyHeight);
  if (window.ResizeObserver) new ResizeObserver(notifyHeight).observe(document.body);
  setTimeout(notifyHeight, 200);
  setTimeout(notifyHeight, 800);
</script>

</body>
</html>
"""

# Renderizamos UNA SOLA VEZ con altura inicial amplia que se auto-ajustará
st.components.v1.html(html_completo, height=1200, scrolling=False)