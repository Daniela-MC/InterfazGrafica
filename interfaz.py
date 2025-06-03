import customtkinter

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")  

app = customtkinter.CTk()
app.geometry("400x200")

def saludar():
    label.configure(text=f"Hola, {entrada.get()}!")

entrada = customtkinter.CTkEntry(app, placeholder_text="Tu nombre")
entrada.pack(pady=10)

boton = customtkinter.CTkButton(app, text="Saludar", command=saludar)
boton.pack(pady=10)

label = customtkinter.CTkLabel(app, text="")
label.pack()

app.mainloop()
