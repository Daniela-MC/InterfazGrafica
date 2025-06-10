import customtkinter
import requests
import json
from PIL import Image
from customtkinter import CTkImage

# Configuración de tema
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

contenedor_tabla = None
saludo_label = None
nombre_usuario = ""
contrasena_usuario = ""

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------
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

def mostrar_tabla_instancias(data):
    global contenedor_tabla

    if contenedor_tabla is not None:
        contenedor_tabla.destroy()

    # Contenedor general que agrupa encabezado y cuerpo con scroll
    contenedor_tabla = customtkinter.CTkFrame(app, fg_color="#CCCCCC")
    contenedor_tabla.pack(padx=20, pady=20, fill="both", expand=True)

    encabezados = ["ID", "Nombre", "Estado", "Usado por", "PowerON", "PowerOFF", "Notas"]

    # Frame fijo para encabezados
    encabezado_frame = customtkinter.CTkFrame(contenedor_tabla, fg_color="#CCCCCC")
    encabezado_frame.pack(fill="x")

    for col in range(len(encabezados)):
        encabezado_frame.grid_columnconfigure(col, weight=1, uniform="col")

    for col, nombre_columna in enumerate(encabezados):
        encabezado = customtkinter.CTkLabel(
            encabezado_frame,
            text=nombre_columna,
            font=("Segoe UI", 14, "bold"),
            text_color="black",
            fg_color="white",
            corner_radius=0
        )
        encabezado.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    # Scrollable Frame para datos
    cuerpo_frame = customtkinter.CTkScrollableFrame(contenedor_tabla, fg_color="#CCCCCC")
    cuerpo_frame.pack(fill="both", expand=True)

    for col in range(len(encabezados)):
        cuerpo_frame.grid_columnconfigure(col, weight=1, uniform="col")

    for fila, instancia in enumerate(data):
        valores = [
            instancia.get("id", "-"),
            instancia.get("name", "-"),
            instancia.get("status", {}).get("status", "-"),
            extraer_valor_tag(instancia.get("tags", []), "UsedBy"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOnTime"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOffTime"),
            extraer_valor_tag(instancia.get("tags", []), "Notes")
        ]

        for col, valor in enumerate(valores):
            if col == 2:  # Columna "Estado"
                if "ON" in valor:
                    color = "green"
                elif "OFF" in valor:
                    color = "red"
                else:
                    color = "black"
            else:
                color = "black"

            celda = customtkinter.CTkLabel(
                cuerpo_frame,
                text=valor,
                font=("Segoe UI", 13),
                text_color=color,
                fg_color="white",
                corner_radius=0
            )
            celda.grid(row=fila, column=col, sticky="nsew", padx=1, pady=1)

def mostrar_saludo():
    global saludo_label
    nombre, contrasena = getData()
    if not nombre or not contrasena:
        return

    for widget in [tituloPrincipal, titulo, user, boton_ingresar, password]:
        widget.destroy()

    saludo_label = customtkinter.CTkLabel(
        app,
        text=f"¡Hola, {nombre}! Bienvenid@ 🎉",
        font=("Segoe UI", 26, "bold"),
        text_color="black",
        bg_color='white'
    )
    saludo_label.pack(pady=(20, 10))

    try:
        url = "https://awstools.corp.latiniaservices.com/api/v1/instance"
        response = requests.get(url, auth=(nombre, contrasena))
        if response.status_code == 200:
            data = response.json()
        else:
            data = []
            print(f"Error al obtener datos: {response.status_code}")
    except requests.exceptions.RequestException as e:
        data = []
        print(f"Excepción al obtener datos: {e}")

    mostrar_tabla_instancias(data)

def mostrar_error(mensaje):
    resultado = customtkinter.CTkTextbox(
        app, width=800, height=400, font=("Courier", 14), text_color="black", fg_color="white"
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
        if response.status_code == 200:
            data = response.json()
            mostrar_tabla_instancias(data)
        else:
            print(f"Error al recargar: {response.status_code}")
    except Exception as e:
        print(f"Error al recargar: {e}")

# ----------------------------
# VENTANA PRINCIPAL
# ----------------------------
app = customtkinter.CTk()
app.title("QA Systems Manager")
app.attributes("-fullscreen", True)

ancho = app.winfo_screenwidth()
alto = app.winfo_screenheight()

# Fondo
imagen = Image.open("Imagen1.jpg")
fondo = CTkImage(light_image=imagen, dark_image=imagen, size=(ancho, alto))
label_fondo = customtkinter.CTkLabel(app, image=fondo, text="")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Títulos y login
tituloPrincipal = customtkinter.CTkLabel(app, text="QA Systems Manager", font=("Segoe UI", 60, "bold"), text_color="black", bg_color='white')
tituloPrincipal.pack(pady=(30, 30))

titulo = customtkinter.CTkLabel(app, text="Inicia sesión", font=("Segoe UI", 32, "bold"), text_color="black",  bg_color='white')
titulo.pack(pady=(10, 10))

user = customtkinter.CTkEntry(app, placeholder_text="User", width=300)
user.pack(pady=10)

password = customtkinter.CTkEntry(app, placeholder_text="Password", width=300, show="*")
password.pack(pady=10)

boton_ingresar = customtkinter.CTkButton(app, text="Ingresar", command=mostrar_saludo)
boton_ingresar.pack(pady=10)

# Botones superiores
boton_salir = customtkinter.CTkButton(app, text="❌", command=app.destroy, width=20, height=20, fg_color="white", hover_color='red', text_color="black")
boton_salir.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

boton_minimizar = customtkinter.CTkButton(app, text="➖", command=app.iconify, width=20, height=20, fg_color="white", hover_color='#444', text_color="black")
boton_minimizar.place(relx=1.0, rely=0.0, anchor="ne", x=-40, y=10)

boton_recargar = customtkinter.CTkButton(app, text="🔄 Recargar", command=recargar_pagina, fg_color="white", text_color="black", hover_color="#ddd")
boton_recargar.place(relx=1.0, rely=0.0, anchor="ne", x=-80, y=10)

app.bind("<Escape>", lambda event: app.destroy())

# Iniciar app
app.mainloop()
