from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog

def decrypt_password(private_key_filename, encrypted_password_filename):
    # Cargar la clave privada desde el archivo
    with open(private_key_filename, "rb") as private_key_file:
        private_key = private_key_file.read()

    cipher_suite = Fernet(private_key)

    # Cargar la contraseña encriptada desde el archivo
    with open(encrypted_password_filename, "rb") as encrypted_password_file:
        encrypted_password = encrypted_password_file.read()

    # Desencriptar la contraseña
    decrypted_password = cipher_suite.decrypt(encrypted_password)

    # Mostrar la contraseña desencriptada en pantalla
    result_label.config(text="Contraseña desencriptada: " + decrypted_password.decode("utf-8"))

def select_files():
    private_key_filename = filedialog.askopenfilename(title="Seleccionar archivo de clave privada", filetypes=[("Archivos de Clave Privada", "*.pem")])
    encrypted_password_filename = filedialog.askopenfilename(title="Seleccionar archivo de contraseña encriptada", filetypes=[("Archivos de Contraseña Encriptada", "*.txt")])
    
    decrypt_password(private_key_filename, encrypted_password_filename)

# Crear la ventana de la aplicación
root = tk.Tk()
root.title("Desencriptador de Contraseña")

# Botón para seleccionar archivos
select_button = tk.Button(root, text="Seleccionar Archivos", command=select_files)
select_button.pack(padx=20, pady=20)

# Etiqueta para mostrar el resultado
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack()

# Iniciar el bucle de la aplicación
root.mainloop()
