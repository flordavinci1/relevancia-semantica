import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# Stopwords en español (pueden ampliarse)
STOPWORDS = set([
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con",
    "no", "una", "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "este", "sí", "porque",
    "esta", "entre", "cuando", "muy", "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien"
])

st.set_page_config(page_title="Auditoría Semántica Educativa", layout="centered")
st.title("🧠 Auditoría de Relevancia Semántica")
st.write("Ingresá una URL o un texto y analizamos su universo semántico: términos frecuentes, bigramas y cobertura de tópicos.")

# Inputs
option = st.radio("¿Querés analizar una URL o pegar texto?", ["URL", "Texto manual"])
user_input = st.text_area("Ingresá la URL o el texto a analizar", height=200)

palabras_objetivo = st.text_input("Palabras clave objetivo (separadas por coma)", placeholder="Ej: compostaje, residuos, orgánico")

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ\s]', '', texto)
    palabras = texto.split()
    palabras = [p for p in palabras if p not in STOPWORDS and len(p) > 2]
    return palabras

def encontrar_bigramas(lista):
    bigramas = zip(lista, lista[1:])
    return Counter(bigramas).most_common(10)

if user_input:
    try:
        if option == "URL":
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
            }
            response = requests.get(user_input, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text(separator=' ', strip=True)
        else:
            content = user_input

        palabras = limpiar_texto(content)
        conteo = Counter(palabras).most_common(15)

        st.subheader("🔡 Términos más frecuentes")
        for palabra, freq in conteo:
            st.markdown(f"- **{palabra}**: {freq} veces")

        st.subheader("🔗 Bigrama frecuentes")
        bigramas = encontrar_bigramas(palabras)
        for (w1, w2), freq in bigramas:
            st.markdown(f"- **{w1} {w2}**: {freq} veces")

        if palabras_objetivo:
            st.subheader("📌 Presencia de palabras clave objetivo")
            objetivos = [p.strip().lower() for p in palabras_objetivo.split(",")]
            faltantes = [p for p in objetivos if not any(p in w for w in palabras)]
            if faltantes:
                st.warning("Estas palabras clave no aparecen en el contenido (o aparecen con otra forma):")
                for f in faltantes:
                    st.markdown(f"- ❌ {f}")
            else:
                st.success("🎯 ¡Todas las palabras clave objetivo están presentes!")

    except Exception as e:
        st.error(f"No se pudo analizar el contenido: {e}")

# CTA final
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>✨ Esta herramienta fue creada con fines educativos y de asistencia a profesionales que están comenzando en SEO.</p>
        <p>💌 Si te sirvió o tenés sugerencias, podés escribirme a <a href="mailto:florencia@crawla.com.ar">florencia@crawla.com.ar</a></p>
        <br>
        <a href="https://www.linkedin.com/in/florenciaestevez/" target="_blank">
            <button style="background-color:#4B8BBE; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:6px; cursor:pointer;">
                🌐 Conectá conmigo en LinkedIn
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
