# Système de Surveillance Raspberry Pi

Ce dépôt permet de surveiller les performances d'un Raspberry Pi 4 via une interface web.

## Fichiers du dépôt

- **info.html** : Page web affichant les caractéristiques du Raspberry Pi 4.
- **adminPI.html** : Interface utilisateur principale pour le système de surveillance.
- **mesure_valeur.py** : Script Python pour mesurer et enregistrer les paramètres système dans une base de données MySQL. **Assurez-vous de renseigner vos informations de connexion MySQL dans le code** :
  ```python
  # Configurer la connexion à la base de données
  db_connection = mysql.connector.connect(
      host="", #adresse IP du serveur MySQL
      user="",  # Nom d'utilisateur pour la connexion à MySQL
      password="",  # Mot de passe pour la connexion à MySQL
      database="" # Nom de la base de données à utiliser
  )
  ```
  
- **mesure_valeur_vps.py** : Script pour mesurer et enregistrer les paramètres système, destiné à être hébergé sur un serveur distant. **Renseignez vos informations de connexion à la base de données** :
  ```python
  # Configurer la connexion à la base de données
  db_connection = mysql.connector.connect(
      host="", #adresse IP du serveur MySQL distant 
      user="",  # Nom d'utilisateur de MariaDB
      password="",  # Mot de passe de MariaDB
      database="" # Nom de la base de données à utiliser
  )
  ```

- **transfert_valeur.py** : Serveur web basé sur Tornado qui affiche les données système récupérées. **Vérifiez vos informations de connexion MySQL dans le code** :
  ```python
  # Connexion à la base de données MariaDB
  try:
      conn = mysql.connector.connect(
          host="", #adresse IP du serveur MySQL
          user="", # Nom d'utilisateur pour la connexion à MySQL
          password="", # Mot de passe pour la connexion à MySQL
          database="" # Nom de la base de données à utiliser
      )
  ```

- **requirements.txt** : Liste des dépendances nécessaires pour exécuter les scripts Python.

## Instructions pour lancer le site

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/Estemobs/SiteStatsRaspberryPi.git
   ```

2. **Installez les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

3. **Lancez le script pour collecter les données** :
   - **Pour un Raspberry Pi** :
     ```bash
     python mesure_valeur.py
     ```
   - **Pour un serveur distant** :
     ```bash
     python mesure_valeur_vps.py
     ```

4. **Lancez le serveur web** :
   ```bash
   python transfert_valeur.py
   ```

5. **Accédez à l'interface utilisateur** dans votre navigateur à l'adresse :
   ```
   http://localhost:2006
   ```

## Note

Assurez-vous que la base de données est configurée correctement dans les scripts Python pour stocker les données.
Si vous avez besoin d'autres modifications ou ajouts, n'hésitez pas à demander !