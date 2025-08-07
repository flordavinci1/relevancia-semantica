import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

st.set_page_config(page_title="Análisis Semántico de URLs", layout="wide")

st.title("🔍 Análisis de contenido y palabras clave")

st.markdown("""
Esta herramienta extrae el contenido, título y metadescripción de cada página, y calcula las palabras clave más relevantes utilizando **TF-IDF**.
""")

urls_input = st.text_area("📋 Pegá las URLs (una por línea)", height=200)

if st.button("Analizar"):
    urls = [url.strip() for url in urls_input.split("\n") if url.strip()]
    
    if not urls:
        st.warning("Por favor, ingresá al menos una URL.")
    else:
        resultados = []

        for url in urls:
            try:
                response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, "html.parser")

                # Extraer title y meta description
                title_tag = soup.find("title")
                meta_desc_tag = soup.find("meta", attrs={"name": "description"})
                title = title_tag.text.strip() if title_tag else ""
                meta_description = meta_desc_tag["content"].strip() if meta_desc_tag and "content" in meta_desc_tag.attrs else ""

                # Extraer texto visible
                for script in soup(["script", "style", "noscript"]):
                    script.decompose()

                visible_text = soup.get_text(separator=' ', strip=True)

                resultados.append({
                    "url": url,
                    "title": title,
                    "meta_description": meta_description,
                    "text": visible_text
                })

            except Exception as e:
                resultados.append({
                    "url": url,
                    "title": "Error",
                    "meta_description": "No disponible",
                    "text": f"Error al acceder: {e}"
                })

        # Crear DataFrame
        df = pd.DataFrame(resultados)

        # Filtrar solo los textos válidos para análisis semántico
        textos_validos = df[df['text'].str.startswith("Error al acceder") == False]

        if not textos_validos.empty:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform(textos_validos['text'])
            feature_names = vectorizer.get_feature_names_out()

            # Obtener las top N palabras clave por documento
            top_n = 10
            keywords_por_url = []

            for i in range(tfidf_matrix.shape[0]):
                row = tfidf_matrix[i].toarray().flatten()
                indices_top = np.argsort(row)[::-1][:top_n]
                keywords = [feature_names[idx] for idx in indices_top if row[idx] > 0]
                keywords_por_url.append(", ".join(keywords))

            # Añadir las palabras clave al DataFrame original
            df.loc[textos_validos.index, 'keywords'] = keywords_por_url
        else:
            df['keywords'] = "No disponible"

        # Mostrar tabla
        st.markdown("### Resultados")
        st.dataframe(df[["url", "title", "meta_description", "keywords"]], use_container_width=True)

        # Permitir descarga como CSV
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Descargar resultados en CSV", data=csv, file_name="analisis_keywords.csv", mime="text/csv")
