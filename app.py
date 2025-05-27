import streamlit as st
import boto3
from botocore.exceptions import ClientError

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

# Uso markdown para poder cambiar el color de la letra porque con streamlit nativo no puedo hacerlo
st.markdown("<h1 style='color: black;'> Instancias AWS QA </h1>", unsafe_allow_html=True)

st.markdown("<h1 style='color: black;'> Inicio de sesión con AWS </h1>", unsafe_allow_html=True)

# Credenciales de acceso a AWS
st.markdown("<p style='color: black;'> AWS Access Key ID </p>", unsafe_allow_html=True)
aws_access_key = st.text_input("", key="access_key")

st.markdown("<p style='color: black;'>AWS Secret Access Key </p>", unsafe_allow_html=True)
aws_secret_key = st.text_input("", type="password", key="secret_key")

region = st.selectbox("Región",["eu-west-1"])

if st.button("Iniciar sesión"):
    if not aws_access_key or not aws_secret_key:
        st.warning("⚠️ Por favor, completa ambos campos de credenciales.")
    else:
        try:
            # Conectarse a AWS STS para validar las credenciales
            sts = boto3.client(
                "sts",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region
            )
            identity = sts.get_caller_identity()
            arn = identity.get("Arn")
            st.success(f"✅ Credenciales válidas.\nConectado como: `{arn}`")
        except ClientError as e:
            st.error(f"❌ Error de autenticación: {e.response['Error']['Message']}")
