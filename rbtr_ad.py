import paramiko
import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from ldap3 import Server, Connection, ALL
from tkinter import ttk
import mysql.connector
from datetime import datetime
import socket

# Configurar el archivo para el registro de errores
error_log_file = "error.log"

def log_error(message):
    with open(error_log_file, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        log_file.write(log_entry)

# Leer la clave de encriptación desde el archivo
if os.path.exists("encryption_key.pem"):
    with open("encryption_key.pem", "rb") as key_file:
        key = key_file.read()
else:
    log_error("No se encontró el archivo 'encryption_key.pem'. Por favor, asegúrate de que exista.")
    exit()

cipher_suite = Fernet(key)

# Leer las credenciales del archivo key.txt para el usuario SSH
with open("key.txt", "r") as key_file:
    ssh_credentials = key_file.read().strip()

ssh_username, encrypted_ssh_password = ssh_credentials.split(":")
ssh_password = cipher_suite.decrypt(encrypted_ssh_password.encode("utf-8")).decode("utf-8")

# Crear una función para ejecutar el comando 'sudo reboot' en el servidor
def execute_reboot(ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=ssh_username, password=ssh_password)

        stdin, stdout, stderr = client.exec_command("sudo reboot")
        client.close()
        print(f"Se reinició el servidor {ip}")
        log_message(ip)
    except Exception as e:
        error_message = f"Error en la conexión a {ip}: {e}"
        log_error(error_message)
        messagebox.showerror("Error", error_message)

# Función para autenticar con Active Directory
def authenticate_ad(user, password):
    try:
        server = Server('192.168.3.10', get_info=ALL)
        conn = Connection(server, user=f'{user}@indguidi.cmx', password=password)
        if conn.bind():
            return True
        else:
            return False
    except Exception as e:
        log_error(f"Error en la autenticación con Active Directory: {e}")
        return False

# Función para guardar el mensaje en la base de datos
def log_message(ip):
    try:
        connection = mysql.connector.connect(
            host="192.168.3.210",
            user=ssh_username,
            password=ssh_password,
            database="welding"
        )
        cursor = connection.cursor()
        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        hostname = socket.gethostname()
        
        message = f"Reinicio desde '{hostname}' usuario '{ad_username}' servidor {ip}"
        
        query = "INSERT INTO reboot (messages, date) VALUES (%s, %s)"
        values = (message, current_time)
        
        cursor.execute(query, values)
        
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        error_message = f"Error al guardar el mensaje: {e}"
        log_error(error_message)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Reinicia visualizadores")

# Estilo para los botones
style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 14))

# Intentar autenticar con Active Directory tres veces
authentication_attempts = 3
authenticated = False
for _ in range(authentication_attempts):
    ad_username = askstring("Autenticación Active Directory", "Usuario:")
    ad_password = askstring("Autenticación Active Directory", "Contraseña:", show='*')

    if authenticate_ad(ad_username, ad_password):
        authenticated = True
        break

if not authenticated:
    error_message = f"Autenticación Active Directory fallida para el usuario '{ad_username}'"
    log_error(error_message)
    messagebox.showerror("Error", error_message)
    root.destroy()
else:
    # Leer las direcciones IP y nombres de servidor desde el archivo ip_list.txt
    ip_server_list = []
    with open("ip_list.txt", "r") as ip_file:
        for line in ip_file:
            name, ip = line.strip().split()
            ip_server_list.append((name, ip))
        
        # Crear botones para cada servidor
        for name, ip in ip_server_list:
            button = ttk.Button(root, text=name, command=lambda ip=ip: execute_reboot(ip))
            button.pack(padx=20, pady=10)
        
        root.mainloop()
