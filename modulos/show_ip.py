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

# Crear una función para ejecutar el comando en el servidor
def execute_command(ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)

        stdin, stdout, stderr = client.exec_command("ip add")
        output = stdout.read().decode("utf-8")

        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Salida del comando 'ip add' en {ip}:\n{output}")
        result_text.config(state="disabled")

        client.close()
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
root.title("SSH Command Execution")

# Crear un botón por cada IP
for name, ip in ip_server_list:
    button = tk.Button(root, text=name, command=lambda ip=ip: execute_command(ip))
    button.pack()

# Crear un área de texto para mostrar la salida del comando
result_text = tk.Text(root, state="disabled")
result_text.pack()

root.mainloop()
