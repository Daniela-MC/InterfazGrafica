import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("QA Systems Manager")
app.attributes("-fullscreen", True)

# Obtener dimensiones de pantalla
ancho = app.winfo_screenwidth()
alto = app.winfo_screenheight()

# Imagen de fondo
imagen = Image.open("Imagen1.jpg")
imagen = imagen.resize((ancho, alto))
fondo = ImageTk.PhotoImage(imagen)

label_fondo = customtkinter.CTkLabel(app, image=fondo, text="")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Título
titulo = customtkinter.CTkLabel(app, text="QA Systems Manager", font=("Segoe UI", 150, "bold"), text_color="black", bg_color='white')
titulo.pack(pady=40)

subtitulo = customtkinter.CTkLabel(app, text="LogIn", font=("Segoe UI", 80, "bold"), text_color="black", bg_color='white')
subtitulo.pack(pady=(0, 20))

def saludar():
    label.configure(text=f"Hola, {user.get()}!")
    
# Entrada
user = customtkinter.CTkEntry(app, placeholder_text="User", width=500)
user.place(relx=0.5, rely=0.4, anchor="center")

# Botón Saludar
boton_saludo = customtkinter.CTkButton(app, text="Saludar", command=saludar)
boton_saludo.place(relx=0.5, rely=0.5, anchor="center")

label = customtkinter.CTkLabel(app, text="", font=("Segoe UI", 80, "bold"), text_color="black", bg_color='white')
label.pack(pady=(100, 100))

# Botón para cerrar
def cerrar_app():
    app.destroy()

boton_salir = customtkinter.CTkButton(app, text="X", command=cerrar_app, width=20, height=20)
boton_salir.place(relx=0.95, rely=0.05, anchor="ne")  # esquina superior derecha

# Presionar Esc también cierra la app
app.bind("<Escape>", lambda event: cerrar_app())

app.mainloop()
