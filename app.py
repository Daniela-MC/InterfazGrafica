import streamlit as st
import boto3
from botocore.exceptions import ClientError

# Para poner la imagen como fondo de pantalla
st.markdown(
    """
    <style>
    .stApp {
        background-image: url(https://assets.aboutamazon.com/dims4/default/dd7f211/2147483647/strip/false/crop/960x720+0+0/resize/960x720!/quality/90/?url=https%3A%2F%2Famazon-blogs-brightspot.s3.amazonaws.com%2F66%2Ff3%2Fcb7e8e804a1f991c96593cf465e1%2Faws-logo-white-on-si.jpg);
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)



#st.markdown("<h1 style='color: black;'> Inicio de sesión con AWS </h1>", unsafe_allow_html=True)
st.title("Inicio de sesión con AWS")
# Credenciales de acceso a AWS

aws_access_key = st.text_input("AWS Access Key ID", key="access_key")
aws_secret_key = st.text_input("AWS Secret Access Key", type="password", key="secret_key")

region = st.selectbox("Región",["eu-west-1","us-east-1"])

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


if st.button("Cerrar sesión"):
    for key in ["authenticated", "access_key", "secret_key", "region"]:
        st.session_state.pop(key, None)
    st.experimental_rerun()
