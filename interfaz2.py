import customtkinter
from PIL import Image, ImageTk
from customtkinter import CTkImage

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Ventana principal
app = customtkinter.CTk()
app.title("QA Systems Manager")
app.attributes("-fullscreen", True)

# Obtener dimensiones de pantalla
ancho = app.winfo_screenwidth()
alto = app.winfo_screenheight()  

# Imagen de fondo
imagen = Image.open("Imagen1.jpg")
fondo = CTkImage(light_image=imagen, dark_image=imagen, size=(ancho, alto))

label_fondo = customtkinter.CTkLabel(app, image=fondo, text="")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Título
tituloPrincipal = customtkinter.CTkLabel(app, text="QA Systems Manager", font=("Segoe UI", 60, "bold"), text_color="black", bg_color='white')
tituloPrincipal.pack(pady=(10, 30))

# Widgets de Login
titulo = customtkinter.CTkLabel(app, text="Inicia sesión", font=("Segoe UI", 32, "bold"), text_color="black",  bg_color='white')
titulo.pack(pady=(0, 10))

user = customtkinter.CTkEntry(app, placeholder_text="User", width=300)
user.pack(pady=10)

password = customtkinter.CTkEntry(app, placeholder_text="Password", width=300, show="*")
password.pack(pady=10)


# Funcion para guardar datos
def getData():
    contrasena = password.get().strip()
    nombre = user.get().strip()
    return nombre, contrasena

# Función para cambiar de pantalla
def mostrar_saludo():
    nombre, contrasena = getData()
    if not nombre:
        return
    
    #Destruir widgets de login
    for widget in [tituloPrincipal, titulo, user, boton_ingresar, password]:
        widget.destroy()

    # Crear saludo 
    saludo = customtkinter.CTkLabel(app, text=f"¡Hola, {nombre}! Bienvenid@ 🎉", font=("Segoe UI", 26, "bold"), text_color="black",  bg_color='white')
    saludo.pack(pady=(50, 50))

boton_ingresar = customtkinter.CTkButton(app, text="Ingresar", command=mostrar_saludo)
boton_ingresar.pack(pady=10)

# Botón para cerrar
def cerrar_app():
    app.destroy()

# Presionar Esc también cierra la app
app.bind("<Escape>", lambda event: cerrar_app())

boton_salir = customtkinter.CTkButton(app, text="❌", command=cerrar_app, width=20, height=20, fg_color="white", hover_color='red',text_color="black")
boton_salir.place(relx=1.0, rely=0.0, anchor="ne",  x=-10, y=10)  # esquina superior derecha

boton_minimizar = customtkinter.CTkButton(app, text="➖", command=app.iconify, width=20, height=20, fg_color="white", hover_color='#444',text_color="black")
boton_minimizar.place(relx=1.0, rely=0.0, anchor="ne",  x=-40, y=10)  # esquina superior derecha

app.mainloop()