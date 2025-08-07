import requests
from bs4 import BeautifulSoup
import streamlit as st
import re

# --- Función para extraer texto limpio de la URL ---
def get_clean_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Eliminamos scripts y estilos
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extraemos el texto visible
    return soup.get_text(separator=' ', strip=True)

# --- Función para análisis SEO ---
def analyze_content(text, keyword):
    keyword_lower = keyword.lower().strip()
    text_lower = text.lower()

    # Coincidencia exacta de la frase clave
    exact_match = keyword_lower in text_lower

    # Coincidencias parciales (para frases) usando regex
    keyword_words = keyword_lower.split()
    pattern = r'\b' + r'\W+'.join(re.escape(word) for word in keyword_words) + r'\b'
    regex_match = re.search(pattern, text_lower)

    return {
        "exact_match": exact_match,
        "regex_match": bool(regex_match),
        "total_words": len(text_lower.split()),
        "keyword_occurrences": text_lower.count(keyword_lower),
        "regex_occurrences": len(re.findall(pattern, text_lower))
    }

# --- Interfaz Streamlit ---
st.title("🔍 Análisis semántico de contenido web")
st.write("Esta herramienta analiza si una palabra o frase clave está presente en el contenido de una URL.")

url = st.text_input("Introduce la URL de la página", placeholder="https://ejemplo.com")
keyword = st.text_input("Introduce la palabra o frase clave", placeholder="seguros médicos para inmigrantes")

if url and keyword:
    try:
        with st.spinner("Analizando contenido..."):
            text = get_clean_text(url)
            result = analyze_content(text, keyword)

        st.success("✅ Análisis completo")
        st.markdown(f"**Total de palabras en la página:** {result['total_words']}")
        st.markdown(f"**Coincidencia exacta de la frase:** {'Sí ✅' if result['exact_match'] else 'No ❌'}")
        st.markdown(f"**Coincidencias por patrón flexible:** {'Sí ✅' if result['regex_match'] else 'No ❌'}")
        st.markdown(f"**Ocurrencias exactas:** {result['keyword_occurrences']}")
        st.markdown(f"**Ocurrencias por patrón flexible:** {result['regex_occurrences']}")

        if not result['exact_match'] and result['regex_match']:
            st.info("⚠️ Se detectó la frase clave de forma parcial o con variaciones (por ejemplo, separada por signos o stopwords). Podés revisar si está optimizada correctamente.")

        elif not result['exact_match'] and not result['regex_match']:
            st.warning("🚫 La palabra o frase clave no se encuentra en el contenido analizado. Podría faltar o estar demasiado transformada.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error al analizar la URL: {e}")
