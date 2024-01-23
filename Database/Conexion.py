import mysql.connector

class ConexionMySQL:
    def __init__(self, host="127.0.0.1", user="root", password="", database="consultaestadorues", port="8080"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.port = port

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            print("Conexión exitosa a la base de datos.")
            return self.connection
        except mysql.connector.Error as e:
            print(f"Error en la conexión a la base de datos: {e}")
            return None
        
    def desconectar(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")
