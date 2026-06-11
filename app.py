import streamlit as st
import yt_dlp
import os

# 1. Configuración de la página
st.set_page_config(page_title="Descargador de mi hermanita", layout="centered")

# Crear carpeta de descargas si no existe en el proyecto
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'descargas')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# 2. Inyección de CSS
st.markdown("""
    <style>
    /* Fondo con degradado suave de rosado a celeste cielo */
    .stApp, .stApp > header {
        background: linear-gradient(135deg, #ffe6f2 0%, #cce6ff 100%) !important; 
    }
    
    /* Bajar el contenido y centrado global */
    .block-container {
        padding-top: 5rem !important; /* Aumentado para bajar el ícono y título */
        padding-bottom: 3rem !important;
        max-width: 750px !important;
    }
    
    /* Estilo del título principal */
    h1 {
        color: #003380 !important; 
        text-align: center !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }
    
    /* Estilo del subtítulo */
    p, .stMarkdown p {
        color: #004080 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    
    /* Nombre de la canción destacada */
    .nombre-cancion {
        color: #002244 !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        background-color: rgba(255, 255, 255, 0.6);
        padding: 15px;
        border-radius: 10px;
        border: 2px dashed #66b3ff;
        margin-top: 15px;
        margin-bottom: 15px;
        text-align: center !important;
    }
    
    /* Estilo de la caja de texto */
    .stTextInput {
        width: 100% !important;
        max-width: 650px !important; 
        margin: 0 auto !important; 
    }
    
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #003380 !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        border: 3px solid #80c1ff !important;
        padding: 15px !important;
        text-align: center !important; 
        box-shadow: 0 4px 10px rgba(0, 51, 128, 0.1) !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #99bbdd !important;
        font-style: italic !important;
    }
    
    /* TRUCO INFALIBLE: Centrar los botones forzando el contenedor principal de Streamlit */
    div[data-testid="stButton"], div[data-testid="stDownloadButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 10px !important;
    }
    
    /* Estilo estético de los botones */
    div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(90deg, #ff66a3, #66b3ff) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 12px 30px !important; 
        width: auto !important; 
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Efecto al pasar el mouse sobre el botón */
    div[data-testid="stButton"] > button:hover, div[data-testid="stDownloadButton"] > button:hover {
        background: #003380 !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 51, 128, 0.3) !important;
    }
    
    /* Cajas de mensajes y alertas */
    .stAlert {
        border-radius: 12px !important;
        max-width: 650px !important;
        margin: 15px auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Interfaz de Usuario Limpia
st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <svg width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#003380" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18V5l12-2v13"></path>
            <circle cx="6" cy="18" r="3"></circle>
            <circle cx="18" cy="16" r="3"></circle>
        </svg>
    </div>
    <h1>Descargador de música de mi hermanita 💖</h1>
    <p>Ingresa el enlace para obtener tu música, Jenifer.</p>
""", unsafe_allow_html=True)

url = st.text_input("", placeholder="Ejemplo: https://www.youtube.si.quieres.acepto.yape;V?v=...")

# Función para validar enlace
def es_link_valido(enlace):
    return "youtube.com" in enlace or "youtu.be" in enlace

# Botón principal
boton_presionado = st.button("Procesar y Descargar")

# 4. Lógica de Descarga Maestra
if boton_presionado:
    if not url:
        st.warning("ojete te olvidaste pegar el enlace.")
    elif not es_link_valido(url):
        st.error("Ese enlace no es de YouTube. Verifica y vuelve a intentar.")
    else:
        with st.spinner("perate se anda descargando..."):
            try:
                opciones = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }],
                    # Redirigimos la creación del archivo interno a tu carpeta "descargas"
                    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'), 
                    'noplaylist': True,
                    'quiet': True, 
                    'extractor_args': {'youtube': {'player_client': ['android', 'ios']}}, 
                    'nocheckcertificate': True, 
                    'geo_bypass': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
                        'Accept-Language': 'es-ES,es;q=0.9',
                    }
                }

                # Ejecutamos la descarga y extraemos la información
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    ruta_mp3 = os.path.splitext(filename)[0] + '.mp3'
                    
                    # Extraemos el nombre de la canción para mostrarlo
                    titulo_cancion = info.get('title', 'Audio Desconocido')

                # Mostramos el nombre de la canción de forma destacada (sin animación)
                st.markdown(f"<div class='nombre-cancion'>🎵 Lista para guardar:<br>{titulo_cancion}</div>", unsafe_allow_html=True)
                
                # Leemos el archivo MP3
                with open(ruta_mp3, "rb") as file:
                    datos_mp3 = file.read()
                
                # Botón de descarga final
                st.download_button(
                    label="ya ta ya Guardar MP3",
                    data=datos_mp3,
                    file_name=os.path.basename(ruta_mp3),
                    mime="audio/mpeg"
                )
                
                # Auto-Limpieza (borramos el archivo de la carpeta interna tras cargarlo en memoria)
                try:
                    os.remove(ruta_mp3)
                except Exception:
                    pass
                    
            except Exception as e:
                st.error("Ocurrió un error técnico al procesar el enlace.")
                st.info("Asegúrate de que el video sea público y vuelve a intentar.")