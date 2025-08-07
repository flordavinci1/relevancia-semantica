texto_original = content.lower()
palabras = limpiar_texto(texto_original)
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
    faltantes = [p for p in objetivos if p not in texto_original]
    if faltantes:
        st.warning("Estas palabras clave no aparecen en el contenido (o aparecen con otra forma):")
        for f in faltantes:
            st.markdown(f"- ❌ {f}")
    else:
        st.success("🎯 ¡Todas las palabras clave objetivo están presentes!")
