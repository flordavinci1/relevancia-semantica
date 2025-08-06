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
    texto
