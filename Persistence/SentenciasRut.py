from tkinter import messagebox
from Database.Conexion import ConexionMySQL
from Util.SeleniumRues import SeleniumRues
import tkinter as tk
import tkinter.ttk as ttk
import datetime

class ProveedorRut:
    """
    Clase para representar un proveedor RUT.
    """
    def __init__(self, numNit, razonSocial, dv, estado):
        """
        Constructor de la clase ProveedorRut.

        Parámetros:
            numNit (str): Número de NIT del proveedor.
            razonSocial (str): Razón social del proveedor.
            dv (str): Dígito de verificación del proveedor.
            estado (str): Estado del proveedor.
        """
        self.numNit = numNit
        self.razonSocial = razonSocial
        self.dv = dv
        self.estado = estado

class ConsultaRUT:
    """
    Clase para representar una consulta RUT.
    """
    def __init__(self, numNit, dv, fecha_str):
        """
        Constructor de la clase ConsultaRUT.

        Parámetros:
            numNit (str): Número de NIT consultado.
            dv (str): Dígito de verificación consultado.
            fecha_str (str): Fecha de la consulta en formato de cadena.
        """
        self.numNit = numNit
        self.dv = dv
        self.fecha_str = fecha_str

class SentenciasRUT:
    """
    Clase para realizar operaciones relacionadas con la tabla consultarr en la base de datos.
    """
    def __init__(self):
        """
        Constructor de la clase SentenciasRUT.
        """
        self.conexion = ConexionMySQL()
        self.selenium_rues = SeleniumRues()

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.desconectar()

    def conectar(self):
        """
        Establece la conexión a la base de datos.

        Retorna:
            object: Objeto de conexión a la base de datos.
        """
        return self.conexion.conectar()

    def desconectar(self):
        """
        Cierra la conexión a la base de datos.
        """
        self.conexion.desconectar()

    def insertar_proveedor_rut_en_db(self, razon_social, estado):
        """
        Inserta o actualiza un proveedor RUT en la base de datos.

        Parámetros:
            razon_social (str): Razón social del proveedor.
            estado (str): Estado del proveedor.
        """
        conn = self.conectar()
        if conn is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO proveedorrut (NombreRUT, EstadoRUT) "
                f"VALUES ('{razon_social}', '{estado}') "
                f"ON DUPLICATE KEY UPDATE NombreRUT = '{razon_social}', EstadoRUT = '{estado}'"
            )
            conn.commit()
            print("Operación de base de datos exitosa.")
        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")
        finally:
            cursor.close()
            conn.close()

    def obtener_todos_los_resultados_rut(self):
        """
        Obtiene todos los registros de la tabla 'consultarr'.

        Retorna:
            list: Lista de tuplas que representan los resultados.
        """
        print(type(self))  # Agrega esta línea para imprimir el tipo de objeto
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM consultarr")
        resultados = cursor.fetchall()

        cursor.close()
        self.desconectar()

        return resultados

    def obtener_info_proveedor(self, identificacion_limpia):
        """
        Obtiene información de proveedores de RUT y RUES para una identificación dada.

        Parámetros:
            identificacion_limpia (str): Identificación limpia del proveedor.

        Retorna:
            dict: Diccionario que contiene información combinada de proveedores de RUT y RUES.
        """
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            # Consultar datos de proveedorrut
            cursor.execute(f"""
                SELECT rut.idProveedorRUT, rut.NombreRUT, rut.DvRUT, rut.EstadoRUT
                FROM proveedorrut rut
                WHERE rut.idProveedorRUT = '{identificacion_limpia}'
            """)
            resultados_rut = cursor.fetchall()

            # Consultar datos de proveedorrues
            cursor.execute(f"""
                SELECT r.ProvNit, r.ProvNombre, r.FechaRegistro, r.FechaUltimaActualizacion, r.Estado, r.CamaraComercio, r.Matricula, r.OrganizacionJuridica, r.Categoria, r.ActividadesEconomicas
                FROM proveedorrues r
                WHERE r.ProvNit = '{identificacion_limpia}'
            """)
            resultados_rues = cursor.fetchall()

            conn.close()

            resultados_combinados = {
                'proveedorrut': resultados_rut,
                'proveedorrues': resultados_rues
            }

            # Imprime los resultados para verificar
            print(resultados_combinados)

            return resultados_combinados
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def insertar_proveedorrut_segunda(self, numNit, apellidos, nombres, dv, estado, fecha_Actual):
        """
        Inserta un proveedor RUT en la base de datos.

        Parámetros:
            numNit (str): Número de NIT del proveedor.
            apellidos (str): Apellidos del proveedor.
            nombres (str): Nombres del proveedor.
            dv (str): Dígito de verificación del proveedor.
            estado (str): Estado del proveedor.
            fecha_Actual (datetime.datetime): Fecha actual.
        """
        try:
            conn = self.conexion.conectar()
            cursor = conn.cursor()

            cursor.execute(
                f"INSERT INTO proveedorrut (idProveedorRUT, NombreRUT, DvRUT, EstadoRUT) "
                f"VALUES ('{numNit}', '{apellidos} {nombres}', '{dv}', '{estado}') "
                f"ON DUPLICATE KEY UPDATE NombreRUT = '{apellidos} {nombres}', DvRUT = '{dv}', EstadoRUT = '{estado}'"
            )
            conn.commit()

            cursor.execute(
                f"INSERT INTO consultarr (Proveedor, FechaConsultaRUT, ProveedorId, ProveedorDv) "
                f"VALUES ('{apellidos} {nombres}', NOW(), '{numNit}', '{dv}')"
            )
            conn.commit()

        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")

        finally:
            cursor.close()
            self.conexion.desconectar()

    def insertar_proveedorrut_primera(self, numNit, razonSocial, dv, estado):
        """
        Inserta un proveedor RUT en la base de datos.

        Parámetros:
            numNit (str): Número de NIT del proveedor.
            razonSocial (str): Razón social del proveedor.
            dv (str): Dígito de verificación del proveedor.
            estado (str): Estado del proveedor.
        """
        try:
            conn = self.conexion.conectar()
            cursor = conn.cursor()

            cursor.execute(
                f"INSERT INTO proveedorrut (idProveedorRUT, NombreRUT, DvRUT, EstadoRUT) "
                f"VALUES ('{numNit}', '{razonSocial}', '{dv}', '{estado}') "
                f"ON DUPLICATE KEY UPDATE NombreRUT = '{razonSocial}', DvRUT = '{dv}', EstadoRUT = '{estado}'"
            )
            conn.commit()

            cursor.execute(
                f"INSERT INTO consultarr (idconsultarr, Proveedor, FechaConsultaRUT, ProveedorId, ProveedorDv) "
                f"VALUES (NULL, '{razonSocial}', NOW(), '{numNit}', '{dv}')"
            )
            conn.commit()

        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")

        finally:
            cursor.close()
            self.conexion.desconectar()
            
    def mostrar_resultados(self, resultados, title):
        """
        Muestra los resultados en una ventana modal.

        Parámetros:
            resultados (list): Lista de tuplas que representan los resultados.
            title (str): Título de la ventana.
        """
        root_resultados = tk.Toplevel()
        root_resultados.title(title)

        columns = ('Id Consulta', 'Proveedor', 'Fecha consulta', 'Identificación', 'DV')
        tree = ttk.Treeview(root_resultados, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

            # Obtener el ancho máximo del contenido en cada columna
            max_width = max(len(str(row[columns.index(col)])) for row in resultados)

            # Establecer un ancho mínimo para la columna (puedes ajustar este valor)
            tree.column(col, width=max_width * 10)  # Ajusta el ancho multiplicando por un factor adecuado

        for resultado in resultados:
            tree.insert('', 'end', values=resultado)

        tree.pack(expand=True, fill='both')
        root_resultados.mainloop()
