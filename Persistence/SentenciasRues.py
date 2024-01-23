# SentenciasRues.py
from Database.Conexion import ConexionMySQL
import datetime

class ProveedorRUES:
    def __init__(self, provNit, provNombre, estado, camara_comercio, matricula, organizacion_juridica, categoria, actividad_economica):
        self.provNit = provNit
        self.provNombre = provNombre
        self.estado = estado
        self.camara_comercio = camara_comercio
        self.matricula = matricula
        self.organizacion_juridica = organizacion_juridica
        self.categoria = categoria
        self.actividad_economica = actividad_economica

class SentenciasRUES:
    def __init__(self):
        self.conexion = ConexionMySQL()

    def insertar_proveedor_rues_en_db(self, proveedor):
        """
        Inserta o actualiza la información de un proveedor RUES en la base de datos.

        :param proveedor: Objeto de la clase ProveedorRUES.
        """
        conn = self.conexion.conectar()
        cursor = conn.cursor()

        try:
            # Obtener la fecha actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fecha_ultima_actualizacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                f"INSERT INTO proveedorrues (ProvNit, ProvNombre, Estado, CamaraComercio, Matricula, OrganizacionJuridica, Categoria, FechaRegistro, FechaUltimaActualizacion, ActividadesEconomicas) "
                f"VALUES ('{proveedor.provNit}', '{proveedor.provNombre}', '{proveedor.estado}', "
                f"'{proveedor.camara_comercio}', '{proveedor.matricula}', '{proveedor.organizacion_juridica}', '{proveedor.categoria}', '{fecha_actual}', '{fecha_ultima_actualizacion}', '{proveedor.ActividadesEconomicas}') "
                f"ON DUPLICATE KEY UPDATE ProvNombre = '{proveedor.provNombre}', Estado = '{proveedor.estado}', "
                f"CamaraComercio = '{proveedor.camara_comercio}', Matricula = '{proveedor.matricula}', "
                f"OrganizacionJuridica = '{proveedor.organizacion_juridica}', Categoria = '{proveedor.categoria}', "
                f"FechaRegistro = '{fecha_actual}', "
                f"FechaUltimaActualizacion = '{fecha_ultima_actualizacion}',"
                f"ActividadesEconomicas = '{proveedor.actividad_economica}'"  # Corregir el nombre del atributo
                )
            
            conn.commit()

        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")
        finally:
            cursor.close()
            self.conexion.desconectar()

