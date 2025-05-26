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

st.markdown("<h1 style='color: black;'> Instancias AWS QA </h1>", unsafe_allow_html=True)
#st.title("Instancias AWS de QA")

# Se inserta imagen
#st.image("latinia.jpg", use_column_width=True)

# CSS personalizado para cambiar color del texto del input
st.markdown("<p style='color: black;'> ¿Cuál es tu nombre? "
" </p>", unsafe_allow_html=True)

# Entrada de texto
nombre = st.text_input("")

# Botón para mostrar saludo
if st.button("Saludar"):
    if nombre:
        #st.markdown(f"<p style='color: orange; font-size: 20px;'>¡Hola, {nombre}!</p>", unsafe_allow_html=True)
        st.markdown(
    f"""
    <div style='
        background-color: #ffeeba;
        padding: 10px;
        border-radius: 5px;
        color: #856404;
        font-weight: bold;
    '>
        ¡Hola, {nombre}!
    </div>
""", unsafe_allow_html=True)

    else:
       # st.warning("Por favor, escribe tu nombre.")
       st.markdown(
           f"""
    <div style='
        background-color: #ffeeba;
        padding: 10px;
        border-radius: 5px;
        color: #856404;
        font-weight: bold;
    '>
        Por favor, escribe tu nombre.
    </div>
       """, unsafe_allow_html=True)
