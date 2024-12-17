import qrcode
import streamlit as st
from PIL import Image
import io

# Configuración de la página
st.set_page_config(page_title="Generador de Códigos QR", page_icon="🔗", layout="centered")

# Título de la aplicación
st.title("Generador de Códigos QR")

# Descripción
st.write("""
Genera tu propio código QR personalizable en segundos.  
Ingresa el texto o URL, selecciona los colores y descarga tu código QR.
""")

# Entrada de texto o URL
texto_qr = st.text_input("Texto o URL para el código QR", placeholder="https://www.ejemplo.com")

# Configuración avanzada del QR
st.subheader("Configuración avanzada")
color_llenado = st.color_picker("Color de cuadros", "#000000")  # Negro por defecto
color_fondo = st.color_picker("Color de fondo", "#FFFFFF")  # Blanco por defecto

# Botón para generar el código QR
if st.button("Generar Código QR"):
    if not texto_qr.strip():
        st.error("El texto o URL no puede estar vacío. Por favor, ingresa un valor válido.")
    else:
        try:
            # Crear el código QR (ajusta automáticamente la versión)
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_M,  # Corrección de errores media (15%)
                box_size=15,  # Tamaño fijo de cuadros
                border=4
            )
            qr.add_data(texto_qr)
            qr.make(fit=True)
            img = qr.make_image(fill_color=color_llenado, back_color=color_fondo)

            # Convertir la imagen a bytes y almacenar en sesión
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)  # Reiniciar puntero
            st.session_state["qr_image"] = img_bytes

            # Mostrar el código QR en la app
            st.image(st.session_state["qr_image"], caption="Código QR Generado", use_container_width=True)

            # Botón para descargar el código QR
            st.download_button(
                label="Descargar Código QR",
                data=st.session_state["qr_image"],
                file_name="codigo_qr.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Error al generar el QR: {e}")

# Mantener visible el QR anterior solo si aún no se ha generado uno nuevo
elif "qr_image" in st.session_state and not st.session_state.get("qr_updated", False):
    st.image(st.session_state["qr_image"], caption="Código QR Generado", use_container_width=True)
    st.session_state["qr_updated"] = True
else:
    st.session_state["qr_updated"] = False
