import os
import tornado.web
import mysql.connector
import tornado.ioloop
import tornado.websocket
from tornado import template

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # Connexion à la base de données MariaDB
        try:
            conn = mysql.connector.connect(
                host="", #adresse IP du serveur MySQL
                user="", # Nom d'utilisateur pour la connexion à MySQL
                password="", # Mot de passe pour la connexion à MySQL
                database="" # Nom de la base de données à utiliser
            )
            print("Connexion à la base de données réussie")
        except mysql.connector.Error as error:
            print("Erreur de connexion à la base de données :", error)
    
        cursor = conn.cursor()
    
        # Récupération de toutes les données depuis la table 'data'
        query = "SELECT temperature, cpu_usage, ram_usage, ping_time FROM data ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        data = cursor.fetchone()
        temp, cpu, ram, wifi = data if data else (None, None, None, None)  # Si aucune donnée n'est disponible, définissez-les à None

        conn.close()

        filename = 'adminPI.html'
        loader = template.Loader('.')
        self.write(loader.load(filename).generate(temp=temp, proc=cpu, ram=ram, wifi=wifi))


if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "assets")}),
        (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "img")}),
        (r"/vues/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "vues")}),
    ])

    port = 2006
    app.listen(port)
    print('Listening on rasbperrypi:{}'.format(port))
    
    # Démarrer la boucle d'événements Tornado dans le même processus
    tornado.ioloop.IOLoop.current().start()

