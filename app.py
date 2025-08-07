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
st.write(
