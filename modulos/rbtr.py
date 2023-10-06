import paramiko
import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Leer la clave de encriptación desde el archivo
if os.path.exists("encryption_key.pem"):
    with open("encryption_key.pem", "rb") as key_file:
        key = key_file.read()
else:
    print("No se encontró el archivo 'encryption_key.pem'. Por favor, asegúrate de que exista.")
    exit()

cipher_suite = Fernet(key)

# Leer las credenciales del archivo key.txt
with open("key.txt", "r") as key_file:
    credentials = key_file.read().strip()

username, encrypted_password = credentials.split(":")
password = cipher_suite.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")

# Crear una función para ejecutar el comando 'sudo reboot' en el servidor
def execute_reboot(ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)

        stdin, stdout, stderr = client.exec_command("sudo reboot")
        client.close()
        print(f"Se reinició el servidor {ip}")
    except Exception as e:
        messagebox.showerror("Error", f"Error en la conexión a {ip}: {e}")

# Leer las direcciones IP y nombres de servidor desde el archivo ip_list.txt
ip_server_list = []
with open("ip_list.txt", "r") as ip_file:
    for line in ip_file:
        name, ip = line.strip().split()
        ip_server_list.append((name, ip))

# Crear la interfaz gráfica
root = tk.Tk()
root.title("SSH Reboot")

# Crear un botón por cada IP
for name, ip in ip_server_list:
    button = tk.Button(root, text=name, command=lambda ip=ip: execute_reboot(ip))
    button.pack(padx=10, pady=5)

root.mainloop()
