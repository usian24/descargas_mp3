import streamlit as st
import yt_dlp
import os

# 1. Configuración de la página
st.set_page_config(page_title="Descargador de mi hermanita", page_icon="💖", layout="centered")

# 2. Inyección de CSS de Alto Contraste, Centrado y Ajustes Estéticos
st.markdown("""
    <style>
    /* Fondo rosado claro para toda la app */
    .stApp, .stApp > header {
        background-color: #ffe6f2 !important; 
    }
    
    /* Centrado global y estructura limpia */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 750px !important;
    }
    
    /* Estilo del título principal: Grande, negro y centrado */
    h1 {
        color: #000000 !important; 
        text-align: center !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }
    
    /* Estilo del subtítulo */
    p, .stMarkdown p {
        color: #000000 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        text-align: center !important;
        margin-bottom: 25px !important;
    }
    
    /* Estilo de la caja de texto */
    .stTextInput {
        width: 100% !important;
        max-width: 650px !important; 
        margin: 0 auto !important; 
    }
    
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-size: 1.2rem !important;
        border-radius: 15px !important;
        border: 4px solid #ff4d94 !important;
        padding: 15px !important;
        text-align: center !important; 
        box-shadow: 0 4px 10px rgba(255, 77, 148, 0.2) !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #888888 !important;
        font-style: italic !important;
    }
    
    /* Contenedores de botones centrados */
    .stButton, .stDownloadButton {
        display: flex !important;
        justify-content: center !important;
        margin-top: 10px !important;
        width: 100% !important;
    }
    
    /* Estilo estético de los botones */
    .stButton>button, .stDownloadButton>button {
        background-color: #ff4d94 !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        padding: 12px 30px !important; 
        width: auto !important; 
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Efecto al pasar el mouse sobre el botón */
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #000000 !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Estilo de los mensajes de error/éxito */
    .stAlert {
        border-radius: 12px !important;
        max-width: 650px !important;
        margin: 15px auto !important;
    }
    
    .stSuccess {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-left: 5px solid #ff4d94 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Interfaz de Usuario
st.markdown("<h1>💖 Descargador de música de mi hermanita 💖</h1>", unsafe_allow_html=True)
st.markdown("<p>Pega el link aquí abajo para descargar tu música favorita.</p>", unsafe_allow_html=True)

url = st.text_input("", placeholder="Ejemplo: https://www.youtube.siquieres.me.pagas ;v...")

# Función para validar que sea de YouTube
def es_link_valido(enlace):
    return "youtube.com" in enlace or "youtu.be" in enlace

# Botón principal
boton_presionado = st.button("✨ Procesar y Descargar ✨")

# 4. Lógica de Descarga Maestra
if boton_presionado:
    if not url:
        st.warning("⚠️ ¡No seas oje, te olvidaste pegar el enlace!")
    elif not es_link_valido(url):
        st.error("🚫 ¡Oe, ese link no es de YouTube! Pega uno de verdad.")
    else:
        with st.spinner("Pérate... 🪄 extrayendo la rolita..."):
            try:
                # Motor de descarga con Trucos Anti-Bloqueo Nivel Dios
                opciones = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': '%(title)s.%(ext)s', 
                    'noplaylist': True,
                    'quiet': True, 
                    # --- MODO STEALTH ---
                    'extractor_args': {'youtube': {'player_client': ['android', 'ios']}}, 
                    'nocheckcertificate': True, 
                    'geo_bypass': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept-Language': 'es-ES,es;q=0.9',
                    }
                }

                # Ejecutamos la descarga y conversión
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    ruta_mp3 = os.path.splitext(filename)[0] + '.mp3'

                # Mensaje de celebración
                st.success("¡La música se descargó, ya ta ya! 🎉")
                
                # Leemos el archivo MP3
                with open(ruta_mp3, "rb") as file:
                    datos_mp3 = file.read()
                
                # Botón de descarga final
                st.download_button(
                    label="⬇️ Haz clic aquí para guardar tu MP3",
                    data=datos_mp3,
                    file_name=os.path.basename(ruta_mp3),
                    mime="audio/mpeg"
                )
                
                # Auto-Limpieza
                try:
                    os.remove(ruta_mp3)
                except Exception:
                    pass
                    
            except Exception as e:
                # Manejo de errores detallado
                st.error("💥 ¡Pucha, ocurrió un error rarazo al procesar el audio!")
                st.error(f"🛠️ DETALLE TÉCNICO PARA EL INGENIERO: {str(e)}")
                st.info("Nota: Si el error dice 'HTTP Error 403' o 'Sign in', YouTube está bloqueando la IP de la nube. Pruébalo de forma local.")