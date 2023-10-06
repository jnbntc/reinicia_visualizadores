from cryptography.fernet import Fernet
import os

# Leer la clave desde el archivo o generar una nueva si el archivo no existe
if os.path.exists("encryption_key.pem"):
    with open("encryption_key.pem", "rb") as key_file:
        key = key_file.read()
else:
    print("No se encontró el archivo 'encryption_key.pem'. Por favor, asegúrate de que exista.")
    exit()

cipher_suite = Fernet(key)

# Pide el nombre del servidor y la contraseña al usuario
server_name = input("Ingrese el nombre del servidor: ")
password = input("Ingrese la contraseña: ").encode("utf-8")

# Encripta la contraseña
encrypted_password = cipher_suite.encrypt(password)

# Guarda la contraseña en un archivo seguro
encrypted_password_filename = f"{server_name}_encrypted_password.txt"

with open(encrypted_password_filename, "wb") as encrypted_password_file:
    encrypted_password_file.write(encrypted_password)

print(f"Contraseña encriptada guardada en {encrypted_password_filename}")
