import customtkinter
import requests
from PIL import Image
from customtkinter import CTkImage

# Configuración de tema
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

contenedor_tabla = None
saludo_label = None
nombre_usuario = ""
contrasena_usuario = ""

def getData():
    global nombre_usuario, contrasena_usuario
    contrasena_usuario = password.get().strip()
    nombre_usuario = user.get().strip()
    return nombre_usuario, contrasena_usuario

def extraer_valor_tag(tags, clave):
    for tag in tags:
        if tag["key"] == clave:
            return tag["value"]
    return "-"

def obtener_snapshots(instance_id, nombre, contrasena):
    try:
        url = f"https://awstools.corp.latiniaservices.com/api/v1/instance/{instance_id}/snapshot"
        response = requests.get(url, auth=(nombre, contrasena))

      #  print(f"\n[DEBUG] Instance ID: {instance_id}")
      #  print(f"[DEBUG] Status Code: {response.status_code}")
      #
        print(f"[DEBUG] Response Text: {response.text}\n")

        if response.status_code == 200:
            snapshots = response.json()  # Aquí asumimos que es una lista
            if isinstance(snapshots, list):
                nombres = [s.get("name", "-") for s in snapshots]
                return ", ".join(nombres) if nombres else "-"
            else:
                return "-"
        else:
            return "-"
    except Exception as e:
        print(f"[ERROR] Excepción al obtener snapshots para {instance_id}: {e}")
        return "-"


def mostrar_tabla_instancias(data):
    global contenedor_tabla

    if contenedor_tabla is not None:
        contenedor_tabla.destroy()

    contenedor_tabla = customtkinter.CTkFrame(app, fg_color="#CCCCCC")
    contenedor_tabla.pack(padx=20, pady=20, fill="both", expand=True)

    encabezados = ["Nombre", "Estado", "Usado por", "PowerON", "PowerOFF", "OperGroup", "Notas", "Snapshot"]

    tabla_frame = customtkinter.CTkScrollableFrame(contenedor_tabla, fg_color="#CCCCCC")
    tabla_frame.pack(fill="both", expand=True)

    for col in range(len(encabezados)):
        if col not in [0, 1, 2, 3, 4, 5, 7]:
            tabla_frame.grid_columnconfigure(col, weight=2, uniform="col")

    for col, nombre_columna in enumerate(encabezados):
        label_kwargs = {
            "text": nombre_columna,
            "font": ("Segoe UI", 14, "bold"),
            "text_color": "black",
            "fg_color": "white",
            "corner_radius": 0
        }
        if col in [1, 2, 3, 4, 5, 7]:
            label_kwargs["width"] = 100
        elif col == 0:
            label_kwargs["width"] = 120

        encabezado = customtkinter.CTkLabel(tabla_frame, **label_kwargs)
        encabezado.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    for fila, instancia in enumerate(data, start=1):
        instance_id = instancia.get("id", "-")
        snapshots = obtener_snapshots(instance_id, nombre_usuario, contrasena_usuario)

        valores = [
            instancia.get("name", "-"),
            instancia.get("status", {}).get("status", "-"),
            extraer_valor_tag(instancia.get("tags", []), "UsedBy"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOnTime"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOffTime"),
            extraer_valor_tag(instancia.get("tags", []), "OperGroup"),
            extraer_valor_tag(instancia.get("tags", []), "Notes"),
            snapshots
        ]

        for col, valor in enumerate(valores):
            if col == 1:
                estado = valor.upper()
                color = "green" if "ON" in estado else "red" if "OFF" in estado else "black"
            else:
                color = "black"

            label_kwargs = {
                "text": valor,
                "font": ("Segoe UI", 13),
                "text_color": color,
                "fg_color": "white",
                "corner_radius": 0
            }
            if col in [1, 2, 3, 4, 5, 7]:
                label_kwargs["width"] = 100
            elif col == 0:
                label_kwargs["width"] = 120

            celda = customtkinter.CTkLabel(tabla_frame, **label_kwargs)
            celda.grid(row=fila, column=col, sticky="nsew", padx=1, pady=1)

def mostrar_saludo():
    global saludo_label
    nombre, contrasena = getData()
    if not nombre or not contrasena:
        return

    try:
        url = "https://awstools.corp.latiniaservices.com/api/v1/instance"
        response = requests.get(url, auth=(nombre, contrasena))

        if response.status_code == 200:
            for widget in [tituloPrincipal, titulo, user, boton_ingresar, password]:
                widget.destroy()

            saludo_label = customtkinter.CTkLabel(
                app,
                text=f"¡Hola, {nombre}! Bienvenid@ 🎉",
                font=("Segoe UI", 26, "bold"),
                text_color="black",
                bg_color='white'
            )
            saludo_label.pack(pady=(40, 40))

            data = response.json()
            mostrar_tabla_instancias(data)

        elif response.status_code == 401:
            mostrar_mensaje_login_error("🤔 ¡IMPOSTOR! 🫣")
            mostrar_mensaje_login_error("❌ Credenciales incorrectas. Intenta nuevamente.")
        else:
            mostrar_mensaje_login_error(f"⚠️ Error al obtener datos. Código: {response.status_code}")

    except requests.exceptions.RequestException as e:
        mostrar_mensaje_login_error(f"🔌 Error de conexión: {e}")

def mostrar_mensaje_login_error(mensaje):
    error_label = customtkinter.CTkLabel(
        app,
        text=mensaje,
        font=("Segoe UI", 20, "bold"),
        text_color="red",
        bg_color="white"
    )
    error_label.pack(pady=(10, 5))
    app.after(5000, error_label.destroy)

def mostrar_error(mensaje):
    global saludo_label
    if saludo_label:
        saludo_label.destroy()

    resultado = customtkinter.CTkTextbox(
        app, width=800, height=400, font=("Courier", 14),
        text_color="black", fg_color="white"
    )
    resultado.insert("1.0", mensaje)
    resultado.pack(expand=True, fill="both", padx=20, pady=20)

def recargar_pagina():
    if not nombre_usuario or not contrasena_usuario:
        print("Credenciales no disponibles para recargar.")
        return
    try:
        url = "https://awstools.corp.latiniaservices.com/api/v1/instance"
        response = requests.get(url, auth=(nombre_usuario, contrasena_usuario))
        response.raise_for_status()
        data = response.json()
        mostrar_tabla_instancias(data)
    except Exception as e:
        print(f"Error al recargar: {e}")

app = customtkinter.CTk()
app.title("QA Systems Manager")
app.iconbitmap("icono.ico")
app.attributes("-fullscreen", True)

ancho = app.winfo_screenwidth()
alto = app.winfo_screenheight()

imagen = Image.open("Imagen1.jpg")
fondo = CTkImage(light_image=imagen, dark_image=imagen, size=(ancho, alto))
label_fondo = customtkinter.CTkLabel(app, image=fondo, text="")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

tituloPrincipal = customtkinter.CTkLabel(app, text="QA Systems Manager", font=("Segoe UI", 100, "bold"), text_color="black", bg_color='white')
tituloPrincipal.pack(pady=(100, 100))

titulo = customtkinter.CTkLabel(app, text="Inicia sesión", font=("Segoe UI", 32, "bold"), text_color="black",  bg_color='white')
titulo.pack(pady=(20, 20))

user = customtkinter.CTkEntry(app, placeholder_text="User", width=300)
user.pack(pady=20)

password = customtkinter.CTkEntry(app, placeholder_text="Password", width=300, show="*")
password.pack(pady=20)

boton_ingresar = customtkinter.CTkButton(app, text="Ingresar", command=mostrar_saludo)
boton_ingresar.pack(pady=20)

boton_salir = customtkinter.CTkButton(app, text="❌", command=app.destroy, width=20, height=20, fg_color="white", hover_color='red', text_color="black")
boton_salir.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

boton_minimizar = customtkinter.CTkButton(app, text="➖", command=app.iconify, width=20, height=20, fg_color="white", hover_color='#444', text_color="black")
boton_minimizar.place(relx=1.0, rely=0.0, anchor="ne", x=-50, y=20)

boton_recargar = customtkinter.CTkButton(app, text="🔄", command=recargar_pagina, width=20, height=20, fg_color="white", text_color="black", hover_color="#ddd")
boton_recargar.place(relx=1.0, rely=0.0, anchor="ne", x=-80, y=20)

app.bind("<Escape>", lambda event: app.destroy())

app.mainloop()
