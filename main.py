import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

def validar_longitud(char):
    # Permitir solo números
    return char.isdigit()

def generar_contrasena(longitud, usa_mayusculas, usa_numeros, usa_simbolos):
    caracteres = string.ascii_letters if usa_mayusculas else string.ascii_lowercase
    caracteres += string.digits if usa_numeros else ''
    caracteres += string.punctuation if usa_simbolos else ''
    
    if not (usa_mayusculas or usa_numeros or usa_simbolos):
        return "Debes habilitar al menos una de las opciones: mayúsculas, números o símbolos."
    
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

def generar_contrasena_y_mostrar():
    try:
        longitud = int(longitud_var.get()) if longitud_var.get() else 8
        if 8 <= longitud <= 16:
            usa_mayusculas = mayusculas_var.get()
            usa_numeros = numeros_var.get()
            usa_simbolos = simbolos_var.get()

            contrasena = generar_contrasena(longitud, usa_mayusculas, usa_numeros, usa_simbolos)
            resultado_var.set(contrasena if isinstance(contrasena, str) else f"Tu contraseña generada es: {contrasena}")
        else:
            resultado_var.set("La longitud debe estar entre 8 y 16.")
    except ValueError:
        resultado_var.set("Ingrese un número válido.")

def copiar_contrasena():
    ventana.clipboard_clear()
    ventana.clipboard_append(contrasena_entry.get())
    ventana.update()
    messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Contraseñas")

# Cambiar el ícono en la barra de título
ruta_icono = "./images/icon.ico"
imagen_icono = Image.open(ruta_icono)
imagen_icono = imagen_icono.resize((16, 16))
icono_ventana = ImageTk.PhotoImage(imagen_icono)

# Establecer el ícono en la barra de título
ventana.tk.call('wm', 'iconphoto', ventana._w, icono_ventana)

# Centrar la ventana en la pantalla
ancho_ventana = 400
alto_ventana = 300
x_pantalla = ventana.winfo_screenwidth() // 2 - ancho_ventana // 2
y_pantalla = ventana.winfo_screenheight() // 2 - alto_ventana // 2
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pantalla}+{y_pantalla}")

# Hacer que la ventana no sea redimensionable
ventana.resizable(width=False, height=False)

# Variables para almacenar los valores de las opciones
longitud_var = tk.StringVar(value="8")  # Valor por defecto
mayusculas_var = tk.BooleanVar()
numeros_var = tk.BooleanVar()
simbolos_var = tk.BooleanVar()
resultado_var = tk.StringVar()

# Validador para permitir solo números en el campo de longitud
validador_longitud = ventana.register(validar_longitud)

# Etiquetas y entradas
ttk.Label(ventana, text="Longitud de la contraseña (entre 8 y 16):").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
longitud_entry = ttk.Entry(ventana, textvariable=longitud_var, validate="key", validatecommand=(validador_longitud, '%S'))
longitud_entry.grid(column=1, row=0, padx=10, pady=5, sticky=tk.W)

ttk.Checkbutton(ventana, text="Incluir letras mayúsculas", variable=mayusculas_var).grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
ttk.Checkbutton(ventana, text="Incluir números", variable=numeros_var).grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
ttk.Checkbutton(ventana, text="Incluir símbolos", variable=simbolos_var).grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)

# Entry para mostrar la contraseña generada
contrasena_entry = ttk.Entry(ventana, textvariable=resultado_var, state='readonly', width=25)
contrasena_entry.grid(column=0, row=4, columnspan=2, pady=10)

# Botón y etiqueta para mostrar la contraseña generada
ttk.Button(ventana, text="Generar Contraseña", command=generar_contrasena_y_mostrar).grid(column=0, row=5, pady=5, columnspan=2)

# Configuración del botón de copiar con ícono
icono_copiar = ImageTk.PhotoImage(Image.open("./images/copy_icon.png").resize((20, 20)))
boton_copiar = ttk.Button(ventana, image=icono_copiar, command=copiar_contrasena)
boton_copiar.grid(column=1, row=4, pady=5, padx=(20, 0), sticky=tk.W) 

# Tooltip simple para el botón de copiar
def mostrar_tooltip(event):
    global ventana_tooltip
    ventana_tooltip = tk.Toplevel(ventana)
    ventana_tooltip.wm_overrideredirect(True)
    ventana_tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

    etiqueta_tooltip = tk.Label(ventana_tooltip, text="Copiar al portapapeles")
    etiqueta_tooltip.pack()

def ocultar_tooltip(event):
    ventana_tooltip.destroy()

boton_copiar.bind("<Enter>", mostrar_tooltip)
boton_copiar.bind("<Leave>", ocultar_tooltip)

# Etiqueta para mostrar "Developed by Ozkar"
ttk.Label(ventana, text="Developed by Ozkar").grid(column=0, row=6, columnspan=2, pady=5)

# Centrar el botón de copiar
ventana.grid_columnconfigure(1, weight=1)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
