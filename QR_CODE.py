import qrcode
import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io

# Función para redondear bordes de una imagen completa de manera proporcional
def round_image(image, radius_percentage=20):
    """Redondea los bordes de una imagen usando una máscara, el radio es proporcional al tamaño de la imagen."""
    width, height = image.size
    radius = min(width, height) * radius_percentage / 100  # Convertir el porcentaje en valor absoluto
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)
    rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)
    return rounded_image

# Configuración de la página
st.set_page_config(page_title="Generador de Códigos QR Redondeados", page_icon="🔗", layout="centered")

# Título de la aplicación
st.title("Generador de Códigos QR con Bordes Redondeados y Logo")

# Entrada de texto o URL
texto_qr = st.text_input("Texto o URL para el código QR", placeholder="https://www.ejemplo.com")

# Crear un expander para la "Configuración avanzada"
with st.expander("Configuración avanzada", expanded=False):
    # Configuración avanzada del QR
    color_llenado = st.color_picker("Color de cuadros", "#000000")  # Negro por defecto
    color_fondo = st.color_picker("Color de fondo", "#FFFFFF")  # Blanco por defecto

    # Slider para elegir el redondeo del QR en porcentaje
    redondeo_qr = st.slider("Redondeo del QR (%)", min_value=0, max_value=100, value=0, step=1)

    # Cargar la imagen del logo
    logo_file = st.file_uploader("Carga tu logo (opcional, formato PNG)", type=["png"])

    # Slider para elegir el redondeo del logo en porcentaje
    redondeo_logo = st.slider("Redondeo del logo (%)", min_value=0, max_value=100, value=20, step=1)

# Botón para generar el código QR
if st.button("Generar Código QR"):
    if not texto_qr.strip():
        st.error("El texto o URL no puede estar vacío. Por favor, ingresa un valor válido.")
    else:
        try:
            # Crear el código QR
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Corrección alta (30%)
                box_size=15,
                border=4
            )
            qr.add_data(texto_qr)
            qr.make(fit=True)
            img = qr.make_image(fill_color=color_llenado, back_color=color_fondo).convert("RGBA")

            # Redondear los bordes del QR según el valor del slider
            if redondeo_qr > 0:
                img = round_image(img, radius_percentage=redondeo_qr)

            # Si el usuario subió un logo, agregarlo al centro del QR
            if logo_file:
                logo = Image.open(logo_file).convert("RGBA")

                # Redondear los bordes del logo según el valor del slider
                logo = round_image(logo, radius_percentage=redondeo_logo)  # Usar el valor del slider para el redondeo

                # Redimensionar el logo
                qr_width, qr_height = img.size
                logo_size = min(qr_width, qr_height) // 5
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

                # Posicionar el logo centrado
                pos_x = (qr_width - logo_size) // 2
                pos_y = (qr_height - logo_size) // 2

                # Pegar el logo redondeado sobre el QR
                img.paste(logo, (pos_x, pos_y), mask=logo.split()[3])  # Usar el canal alfa como máscara

            # Convertir a bytes para descarga
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Mostrar la imagen
            st.image(img, caption="Código QR Generado", use_container_width=True)

            # Botón de descarga
            st.download_button(
                label="Descargar Código QR",
                data=img_bytes,
                file_name="codigo_qr_redondeado.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Error al generar el QR: {e}")
