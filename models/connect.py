import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname="databeez",
            user="bouddha",
            password = 'logyouin',
            host="localhost"
        )
        # print("Base de donnée connectée avec succès")
        return conn
    except psycopg2.Error as e:
        print(f"Echec de la connexion à la base de donnée {e}")
        return None
    