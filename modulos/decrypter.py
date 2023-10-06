from cryptography.fernet import Fernet
import os

# Leer la clave desde el archivo o generar una nueva si el archivo no existe
if os.path.exists("encryption_key.pem"):
    with open("encryption_key.pem", "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open("encryption_key.pem", "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)

# Obtener una lista de archivos en el directorio actual
files_in_directory = os.listdir()

# Filtrar archivos por nombres que contienen "encrypted_password.txt"
server_files = [filename for filename in files_in_directory if filename.endswith("_encrypted_password.txt")]

server_passwords = {}

# Recorrer los archivos generados
for encrypted_password_filename in server_files:
    server_name = encrypted_password_filename.replace("_encrypted_password.txt", "")
    
    with open(encrypted_password_filename, "rb") as encrypted_password_file:
        encrypted_password = encrypted_password_file.read()

    decrypted_password = cipher_suite.decrypt(encrypted_password)
    server_passwords[server_name] = decrypted_password.decode("utf-8")

# Imprimir los nombres de servidores y contraseñas almacenados
for server, password in server_passwords.items():
    print(f"Servidor: {server}\tContraseña: {password}")
