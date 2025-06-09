import customtkinter
import requests
import json
from PIL import Image
from customtkinter import CTkImage

# Configuración de tema
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------
def getData():
    contrasena = password.get().strip()
    nombre = user.get().strip()
    return nombre, contrasena

def extraer_valor_tag(tags, clave):
    for tag in tags:
        if tag["key"] == clave:
            return tag["value"]
    return "-"

def mostrar_tabla_instancias(data):
    contenedor = customtkinter.CTkScrollableFrame(app, fg_color="white", height=500)
    contenedor.pack(padx=20, pady=20, fill="both", expand=True)

    encabezados = ["ID", "Nombre", "Estado", "Usado por", "Propósito"]
    for col, nombre in enumerate(encabezados):
        lbl = customtkinter.CTkLabel(contenedor, text=nombre, font=("Segoe UI", 14, "bold"), text_color="black")
        lbl.grid(row=0, column=col, padx=10, pady=5)

    for fila, instancia in enumerate(data, start=1):
        id_ = instancia.get("id", "-")
        nombre = instancia.get("name", "-")
        estado = instancia.get("status", {}).get("status", "-")
        usado_por = extraer_valor_tag(instancia.get("tags", []), "UsedBy")
        proposito = extraer_valor_tag(instancia.get("tags", []), "Purpose")

        valores = [id_, nombre, estado, usado_por, proposito]

        for col, valor in enumerate(valores):
            if col == 2:
                color = "green" if "ON" in valor else "red" if "OFF" in valor else "gray"
                celda = customtkinter.CTkLabel(contenedor, text=valor, font=("Segoe UI", 13), text_color=color)
            else:
                celda = customtkinter.CTkLabel(contenedor, text=valor, font=("Segoe UI", 13), text_color="black")
            celda.grid(row=fila, column=col, padx=10, pady=3, sticky="w")

def mostrar_saludo():
    nombre, contrasena = getData()
    if not nombre or not contrasena:
        return

    for widget in [tituloPrincipal, titulo, user, boton_ingresar, password]:
        widget.destroy()

    saludo = customtkinter.CTkLabel(app, text=f"¡Hola, {nombre}! Bienvenid@ 🎉", font=("Segoe UI", 26, "bold"), text_color="black", bg_color='white')
    saludo.pack(pady=(50, 50))

    try:
        url = "https://awstools.corp.latiniaservices.com/api/v1/instance"
        response = requests.get(url, auth=(nombre, contrasena))
        if response.status_code == 200:
            data = response.json()
            mostrar_tabla_instancias(data)
        else:
            mensaje = f"Error en la consulta: {response.status_code}"
            mostrar_error(mensaje)
    except requests.exceptions.RequestException as e:
        mostrar_error(f"Error en la consulta: {e}")

def mostrar_error(mensaje):
    resultado = customtkinter.CTkTextbox(app, width=800, height=400, font=("Courier", 14), text_color="black", fg_color="white")
    resultado.insert("1.0", mensaje)
    resultado.pack(expand=True, fill="both", padx=20, pady=20)

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
tituloPrincipal.pack(pady=(10, 30))

titulo = customtkinter.CTkLabel(app, text="Inicia sesión", font=("Segoe UI", 32, "bold"), text_color="black",  bg_color='white')
titulo.pack(pady=(0, 10))

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

app.bind("<Escape>", lambda event: app.destroy())

# Iniciar app
app.mainloop()
