# SentenciasRues.py
from Database.Conexion import ConexionMySQL
import datetime

class ProveedorRUES:
    def __init__(self, provNit, provNombre, estado, camara_comercio, matricula, organizacion_juridica, categoria, actividades_economicas):
        self.provNit = provNit
        self.provNombre = provNombre
        self.estado = estado
        self.camara_comercio = camara_comercio
        self.matricula = matricula
        self.organizacion_juridica = organizacion_juridica
        self.categoria = categoria
        self.actividades_economicas = actividades_economicas

class SentenciasRUES:
    def __init__(self):
        self.conexion = ConexionMySQL()

    def insertar_proveedor_rues_en_db(self, proveedor):
        conn = self.conexion.conectar()
        cursor = conn.cursor()

        try:
            # Obtener la fecha actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fecha_ultima_actualizacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insertar en la tabla proveedorrues
            cursor.execute(
                f"INSERT INTO proveedorrues (ProvNit, ProvNombre, FechaRegistro, FechaUltimaActualizacion, Estado, CamaraComercio, Matricula, OrganizacionJuridica, Categoria, ActividadesEconomicas) "
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                f"ON DUPLICATE KEY UPDATE ProvNombre = %s, FechaUltimaActualizacion = %s, Estado = %s, CamaraComercio = %s, Matricula = %s, "
                f"OrganizacionJuridica = %s, Categoria = %s, ActividadesEconomicas = %s",
                (
                    proveedor.provNit, proveedor.provNombre, fecha_actual, fecha_ultima_actualizacion, proveedor.estado,
                    proveedor.camara_comercio, proveedor.matricula, proveedor.organizacion_juridica, proveedor.categoria,
                    ', '.join(proveedor.actividades_economicas),  # Convertir la lista a cadena
                    proveedor.provNombre, fecha_ultima_actualizacion, proveedor.estado,
                    proveedor.camara_comercio, proveedor.matricula, proveedor.organizacion_juridica, proveedor.categoria,
                    ', '.join(proveedor.actividades_economicas)  # Convertir la lista a cadena
                )
            )
            conn.commit()  # Guardar cambios en la base de datos

            mensaje = "La información ha sido actualizada correctamente."

        except Exception as e:
            print(f"Error en la inserción en la base de datos: {e}")
            mensaje = f"Error en la inserción en la base de datos: {e}"
        finally:
            # Siempre cierra la conexión, incluso en caso de excepción
            if conn.cursor:
                cursor.close()
            self.conexion.desconectar()

        return mensaje
