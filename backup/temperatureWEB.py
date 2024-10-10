import tornado.web
import mysql.connector
import tornado.ioloop
from tornado import template

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # Connexion à la base de données MariaDB
        try:
            conn = mysql.connector.connect(
                host="", #adresse IP du serveur MySQL
                user="", # Nom d'utilisateur pour la connexion à MySQL
                password="", # Mot de passe pour la connexion à MySQL
                database=""  # Nom de la base de données à utiliser
            )
            print("Connexion à la base de données réussie")
        except mysql.connector.Error as error:
            print("Erreur de connexion à la base de données :", error)
    
        cursor = conn.cursor()
    
        # Récupération de la dernière valeur de température
        query = "SELECT température FROM temperature ORDER BY date_temperature DESC LIMIT 1"
        cursor.execute(query)
        temp = cursor.fetchone()[0]
        print("Température récupérée de la base de données :", temp)
    
        conn.close()

        filename = 'adminPI.html'
        loader = template.Loader('.')
        self.write(loader.load(filename).generate(temp=temp))


app = tornado.web.Application([
    (r"/", IndexHandler),
])

if __name__ == '__main__':
    port = 5000
    app.listen(port)
    print('Listening on rasbperrypi:{}'.format(port))
    tornado.ioloop.IOLoop.current().start()

