import streamlit as st

# Para poner la imagen como fondo de pantalla
st.markdown(
    """
    <style>
    .stApp {
        background-image: url(https://i.ytimg.com/vi/m2AuliEdbQg/maxresdefault.jpg);
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color: black;'> Instancias AWS QA</h1>", unsafe_allow_html=True)
#st.title("Instancias AWS de QA")

# Se inserta imagen
#st.image("latinia.jpg", use_column_width=True)



# Entrada de texto
nombre = st.text_input("¿Cuál es tu nombre?")

# Botón para mostrar saludo
if st.button("Saludar"):
    if nombre:
        st.success(f"¡Hola, {nombre}!")
    else:
        st.warning("Por favor, escribe tu nombre.")
