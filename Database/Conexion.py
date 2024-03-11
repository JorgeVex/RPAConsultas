import mysql.connector

class ConexionMySQL:
    """
    Clase para establecer y gestionar la conexión con una base de datos MySQL.
    """
    def __init__(self, host="127.0.0.1", user="root", password="", database="consultaestadorues", port="3306"):
        """
        Constructor de la clase ConexionMySQL.

        Parameters:
            host (str): Dirección IP del servidor de la base de datos.
            user (str): Nombre de usuario para la conexión a la base de datos.
            password (str): Contraseña para la conexión a la base de datos.
            database (str): Nombre de la base de datos a la que se va a conectar.
            port (str): Puerto de conexión al servidor de la base de datos.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.port = port

    def conectar(self):
        """
        Método para establecer una conexión con la base de datos.

        Returns:
            mysql.connector.connection.MySQLConnection or None: Objeto de conexión si la conexión es exitosa, None en caso de error.
        """
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
        """
        Método para cerrar la conexión con la base de datos.
        """
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")
