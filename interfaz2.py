#Codigo de prueba a ver si esto me guarda y actualiza
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("QA Systems Manager")
app.attributes("-fullscreen", True)

# Obtener dimensiones de pantalla
ancho = app.winfo_screenwidth()
alto = app.winfo_screenheight()  #######

# Imagen de fondo
imagen = Image.open("Imagen1.jpg")
imagen = imagen.resize((ancho, alto))
fondo = ImageTk.PhotoImage(imagen)
label_fondo = customtkinter.CTkLabel(app, image=fondo, text="")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Título
titulo = customtkinter.CTkLabel(app, text="QA Systems Manager", font=("Segoe UI", 150, "bold"), text_color="black", bg_color='white')
titulo.pack(pady=40)

# Función para cambiar de pantalla
def mostrar_saludo():
    nombre = user.get()
    if nombre.strip() == "":
        return
    
    #Destruir widgets de login
    user.destroy()
    boton_ingresar.destroy()
    subtitulo.destroy()

    # Crear saludo 
    saludo = customtkinter.CTkLabel(
        app, text=f"¡Hola, {nombre}! Bienvenido 🎉", font=("Segoe UI", 26, "bold"), text_color="black", bg_color="white")
    saludo.pack(pady=100)

# Widgets de Login
titulo = customtkinter.CTkLabel(app, text="Inicia sesión", font=("Segoe UI", 32, "bold"), text_color="white", bg_color="white")
titulo.pack(pady=(60, 10))

subtitulo = customtkinter.CTkLabel(app, text="Escribe tu nombre para continuar", font=("Segoe UI", 18), text_color="lightgray", bg_color="white")
subtitulo.pack(pady=(0, 30))

user = customtkinter.CTkEntry(app, placeholder_text="User", width=300)
user.pack(pady=10)

boton_ingresar = customtkinter.CTkButton(app, text="Ingresar", command=mostrar_saludo)
boton_ingresar.pack(pady=10)

# Botón para cerrar
def cerrar_app():
    app.destroy()

boton_salir = customtkinter.CTkButton(app, text="X", command=cerrar_app, width=20, height=20)
boton_salir.place(relx=0.95, rely=0.05, anchor="ne")  # esquina superior derecha

# Presionar Esc también cierra la app
app.bind("<Escape>", lambda event: cerrar_app())

app.mainloop()
