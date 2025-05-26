import streamlit as st

st.title("Demo de Componentes Básicos")

# Entrada de texto
nombre = st.text_input("¿Cuál es tu nombre?")

# Botón para mostrar saludo
if st.button("Saludar"):
    if nombre:
        st.success(f"¡Hola, {nombre}!")
    else:
        st.warning("Por favor, escribe tu nombre.")
