import mysql.connector
import os
import subprocess
import psutil

# Fonction pour obtenir la température du Raspberry Pi
def get_temperature():
    try:
        temp = subprocess.check_output(["vcgencmd", "measure_temp"])
        return temp.decode("utf-8")
    except Exception as e:
        return str(e)

# Fonction pour obtenir l'utilisation de la RAM en pourcentage
def get_ram_usage_percentage():
    ram = psutil.virtual_memory()
    return ram.percent

# Fonction pour obtenir l'utilisation du CPU en pourcentage
def get_cpu_usage_percentage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

# Fonction pour obtenir la latence (ping) en ms
def get_ping_latency():
    try:
        # Remplacez "google.com" par l'adresse IP ou le nom de domaine du serveur que vous souhaitez pinguer
        ping_output = subprocess.check_output(["ping", "-c", "4", "google.com"])
        ping_output = ping_output.decode("utf-8")
        lines = ping_output.split("\n")
        latency_line = lines[-2]  # La ligne qui contient les statistiques de latence

        # Extrait la latence moyenne en ms
        latency = float(latency_line.split("/")[-2])
        return latency
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # Récupérer les données
    temperature = get_temperature()
    ram_usage_percentage = get_ram_usage_percentage()
    cpu_usage_percentage = get_cpu_usage_percentage()
    ping_latency = get_ping_latency()

    temp_value = temperature.split('=')[1].split("'")[0]

    # Configurer la connexion à la base de données
    db_connection = mysql.connector.connect(
        host="", #adresse IP du serveur MySQL
        user="",  # Nom d'utilisateur pour la connexion à MySQL
        password="",  # Mot de passe pour la connexion à MySQL
        database="" # Nom de la base de données à utiliser
    )

    # Créer un objet de curseur
    cursor = db_connection.cursor()

    # Supprimer toutes les données existantes dans la table
    delete_query = "DELETE FROM data"
    cursor.execute(delete_query)
    
    # Insérer des données dans la table
    insert_query = "INSERT INTO data (temperature, cpu_usage, ram_usage, ping_time) VALUES (%s, %s, %s, %s)"
    data_values = (temp_value, cpu_usage_percentage, ram_usage_percentage, ping_latency)
    cursor.execute(insert_query, data_values)

    # Valider la transaction
    db_connection.commit()

    # Fermer la connexion
    cursor.close()
    db_connection.close()

    print(f"Température: {temp_value}°")
    print(f"Utilisation de la RAM: {ram_usage_percentage}%")
    print(f"Utilisation du CPU: {cpu_usage_percentage}%")
    print(f"Latence (Ping): {ping_latency} ms")


