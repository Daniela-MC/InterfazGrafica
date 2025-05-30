import boto3
import streamlit as st

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

#st.set_page_config(page_title="AWS EC2 Viewer", layout="centered")

# Paso 1: Mostrar formulario si no estamos autenticados
if "authenticated" not in st.session_state:
    st.title("Conexión a AWS")

    access_key = st.text_input("Access Key ID")
    secret_key = st.text_input("Secret Access Key", type="password")
    region = st.selectbox("Región", ["us-east-1", "eu-west-1", "us-east-2"])

    if st.button("Conectar"):
        try:
            # Intentar conexión para validar credenciales
            ec2 = boto3.client(
                "ec2",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            ec2.describe_instances()  # llamada para validar

            # Guardar en la sesión
            st.session_state.authenticated = True
            st.session_state.access_key = access_key
            st.session_state.secret_key = secret_key
            st.session_state.region = region

            st.experimental_rerun()  # recargar página
        except Exception as e:
            st.error(f"Error de autenticación: {e}")

# Paso 2: Mostrar tabla si ya estamos autenticados
else:
    st.title("Instancias EC2")

    ec2 = boto3.client(
        "ec2",
        aws_access_key_id=st.session_state.access_key,
        aws_secret_access_key=st.session_state.secret_key,
        region_name=st.session_state.region
    )

    response = ec2.describe_instances()

    data = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            data.append({
                "ID": instance["InstanceId"],
                "Estado": instance["State"]["Name"],
                "Tipo": instance["InstanceType"],
                "Zona": instance["Placement"]["AvailabilityZone"],
                "Lanzada": instance["LaunchTime"].strftime("%Y-%m-%d %H:%M:%S")
            })

    if data:
        st.table(data)
    else:
        st.info("No se encontraron instancias.")

    # 🔴 Botón de cierre de sesión
    if st.button("Cerrar sesión"):
        for key in ["authenticated", "access_key", "secret_key", "region"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
