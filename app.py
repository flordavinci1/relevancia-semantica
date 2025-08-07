import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Función para obtener el contenido de una URL
def obtener_contenido(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Error al acceder a la URL: {e}")
        return None

# Función para limpiar y extraer texto
def extraer_texto_limpio(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Eliminar scripts, styles y elementos irrelevantes
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Función para encontrar términos más frecuentes
def obtener_terminos_frecuentes(texto, min_len=4):
    palabras = re.findall(r'\b\w+\b', texto.lower())
    frecuentes = {}
    for palabra in palabras:
        if len(palabra) >= min_len:
            frecuentes[palabra] = frecuentes.get(palabra, 0) + 1
    ordenadas = sorted(frecuentes.items(), key=lambda x: x[1], reverse=True)
    return ordenadas[:30]

# Streamlit app
st.title("🔍 Relevancia semántica y tópicos del contenido")

url = st.text_input("🔗 Ingresá la URL a analizar")
keyword_objetivo = st.text_input("🎯 Palabra clave objetivo (opcional)").strip().lower()

if url:
    html = obtener_contenido(url)
    if html:
        texto = extraer_texto_limpio(html)
        st.subheader("📄 Contenido limpio (extracto)")
        st.write(texto[:800] + "...")

        st.subheader("🔤 Términos frecuentes en el contenido")
        top_palabras = obtener_terminos_frecuentes(texto)
        for palabra, frecuencia in top_palabras:
            if palabra == keyword_objetivo:
                st.markdown(f"- ✅ **{palabra}**: {frecuencia} apariciones")
            else:
                st.markdown(f"- {palabra}: {frecuencia}")

        if keyword_objetivo:
            todas_palabras = dict(top_palabras)
            if keyword_objetivo not in todas_palabras:
                st.warning(f"La palabra clave **{keyword_objetivo}** no se encontró en los términos más frecuentes.")
