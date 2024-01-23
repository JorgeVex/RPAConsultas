# Consultas.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from Database.Conexion import ConexionMySQL
from Util.SeleniumRut import SeleniumRut
from Util.SeleniumRues import SeleniumRues

class ConsultasDB:
    def __init__(self):
        self.db = ConexionMySQL()

    def ver_consultas_identificacion_db(self, identificacion):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            # Consultar la cantidad de veces que se ha consultado el ID
            cursor.execute(f"SELECT COUNT(*) FROM consultarr WHERE ProveedorId = '{identificacion}'")
            cantidad_consultas = cursor.fetchone()[0]

            if cantidad_consultas > 0:
                # Consultar los detalles de las consultas
                cursor.execute(f"SELECT * FROM consultarr WHERE ProveedorId = '{identificacion}'")
                resultados = cursor.fetchall()

                return resultados  # Retornar los resultados

            else:
                print(f"No hay consultas registradas para el ID {identificacion}")
                return None

        except Exception as e:
            print(f"Error en la consulta de consultas por identificación: {e}")
            return None
        finally:
            cursor.close()
            self.db.desconectar()

    def consultar_todos_los_resultados(self):
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()

            # Consultar todos los resultados de la tabla consultarr
            cursor.execute("SELECT * FROM consultarr")
            resultados = cursor.fetchall()

            return resultados

        except Exception as e:
            print(f"Error en la consulta de todos los resultados: {e}")
            return None
        finally:
            cursor.close()
            self.db.desconectar

# En la clase FuncionesJuntas
class FuncionesJuntas:
    def __init__(self):
        pass

    def funciones_juntas(self, entry_identificacion):
        try:
            # Crear una ventana modal para el mensaje de carga
            loading_window = tk.Toplevel()
            loading_window.title("Cargando")

            # Etiqueta para el mensaje de carga
            loading_label = tk.Label(loading_window, text="Realizando consultas. Por favor, espere...")
            loading_label.pack(padx=20, pady=20)

            # Centrar la ventana de carga en la pantalla
            loading_window.update_idletasks()
            width = loading_window.winfo_width()
            height = loading_window.winfo_height()
            x = (loading_window.winfo_screenwidth() // 2) - (width // 2)
            y = (loading_window.winfo_screenheight() // 2) - (height // 2)
            loading_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

            # Actualizar la interfaz gráfica para que se muestre la etiqueta de carga
            loading_window.update()

            # Consultar RUT
            selenium_rut = SeleniumRut()
            resultado_rut = selenium_rut.consultar_rut_con_selenium_headless(entry_identificacion)

            # Consultar RUES
            selenium_rues = SeleniumRues()
            resultado_rues = selenium_rues.consultar_rues_con_selenium_headless(entry_identificacion)

            # Cerrar la ventana de carga
            loading_window.destroy()

            # Mostrar la información en una nueva ventana
            if resultado_rut or resultado_rues:
                # Crear una ventana modal para mostrar la información
                info_window = tk.Toplevel()
                info_window.title("Información obtenida")

                # Construir el mensaje final
                mensaje_final = ""
                if resultado_rut:
                    mensaje_final += f"Resultados RUT:\n{resultado_rut}\n\n"
                if resultado_rues:
                    mensaje_final += f"Resultados RUES:\n{resultado_rues}"

                # Etiqueta para el mensaje final
                info_label = tk.Label(info_window, text=mensaje_final)
                info_label.pack(padx=20, pady=20)

                # Botón para cerrar la ventana de información
                cerrar_boton = tk.Button(info_window, text="Cerrar", command=info_window.destroy)
                cerrar_boton.pack(pady=10)

                # Centrar la ventana de información en la pantalla
                info_window.update_idletasks()
                width = info_window.winfo_width()
                height = info_window.winfo_height()
                x = (info_window.winfo_screenwidth() // 2) - (width // 2)
                y = (info_window.winfo_screenheight() // 2) - (height // 2)
                info_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

            else:
                messagebox.showinfo("Información", "No se obtuvo información de ninguna consulta.")

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")


    def mostrar_tabla_completa(self):
        consultas_db = ConsultasDB()
        resultados_completos = consultas_db.consultar_todos_los_resultados()

        root_resultados = tk.Toplevel()
        root_resultados.title("Tabla Completa de consultarr")

        columns = ('Id Consulta', 'Proveedor', 'Fecha consulta', 'Identificación', 'DV')
        tree = ttk.Treeview(root_resultados, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

            # Obtener el ancho máximo del contenido en cada columna
            max_width = max(len(str(row[columns.index(col)])) for row in resultados_completos)

            # Establecer un ancho mínimo para la columna (puedes ajustar este valor)
            tree.column(col, width=max_width * 10)  # Ajusta el ancho multiplicando por un factor adecuado

        for resultado in resultados_completos:
            tree.insert('', 'end', values=resultado)

        tree.pack(expand=True, fill='both')
        root_resultados.mainloop()


    def mostrar_resultados(self, resultados, title):
        if resultados:
            root_resultados = tk.Toplevel()
            root_resultados.title(title)

            columns = [desc[0] for desc in resultados.description]
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
        else:
            messagebox.showinfo("Información", "No hay resultados disponibles.")
            
 