
import subprocess
import time
import mysql.connector

# Paramètres de connexion à la base de données
HOST = "" #adresse IP du serveur MySQL
USER = "" # Nom d'utilisateur pour la connexion à MySQL
PASSWORD = "" # Mot de passe pour la connexion à MySQL
DATABASE = "" # Nom de la base de données à utiliser

# Connexion à la base de données
try:
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    print("Connexion à la base de données réussie")
except mysql.connector.Error as error:
    print("Erreur de connexion à la base de données :", error)

if connection.is_connected():
    cursor = connection.cursor()

 
while True:
    # Enregistrement de la température dans la base de données
    query = "DELETE FROM temperature WHERE date_temperature < DATE_SUB(SYSDATE(), INTERVAL 1 DAY)"
    cursor.execute(query)
    connection.commit()

    # Mesure de la température via vcgencmd
    temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
    temp = float(temp.decode().split("=")[1][:-3])
   
    # Enregistrement de la température dans la base de données
    query = "INSERT INTO temperature (température, date_temperature) VALUES ({}, SYSDATE())".format(temp)
    cursor.execute(query)
    connection.commit()
    print("Température actuelle :", temp)
    # Attendre une minute avant de mesurer à nouveau
    time.sleep(60)

# Fermeture de la connexion à la base de données
if connection.is_connected():
    cursor.close()
    connection.close()
    print("Connexion à la base de données fermée")