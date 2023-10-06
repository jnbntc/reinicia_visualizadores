import mysql.connector
from datetime import datetime
import socket

def log_message(host, user, password, database, ip):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        hostname = socket.gethostname()
        
        message = f"Reinicio desde '{hostname}' servidor {ip}"
        
        query = "INSERT INTO reboot (messages, date) VALUES (%s, %s)"
        values = (message, current_time)
        
        cursor.execute(query, values)
        
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error al guardar el mensaje:", e)
