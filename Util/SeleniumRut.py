import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import tkinter as tk
from tkinter import messagebox
from Persistence.SentenciasRut import SentenciasRUT


class SeleniumRut:
    def __init__(self):
        # Configuración para ejecutar en modo headless
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")  # Habilitar el modo headless

    def limpiar_identificacion(self, identificacion):
        identificacion_limpia = identificacion.replace('.', '').replace('-', '')
        return identificacion_limpia

    def consultar_rut_con_selenium_headless(self, entry_identificacion):
        identificacion_limpia = self.limpiar_identificacion(entry_identificacion.get()) if isinstance(entry_identificacion, tk.Entry) else self.limpiar_identificacion(entry_identificacion)

        if not identificacion_limpia:
            messagebox.showinfo("Error", "Por favor, ingrese una identificación.")
            return None

        try:
            with webdriver.Chrome(options=self.chrome_options) as driver:
                driver.get("https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")

                input_identificacion = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit")
                input_identificacion.send_keys(identificacion_limpia)

                boton_buscar = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar")
                boton_buscar.click()

                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//font[contains(text(), 'El NIT')]")))
                    mensaje_error = driver.find_element(By.XPATH, "//font[contains(text(), 'El NIT')]").text
                    messagebox.showinfo("Error en la identificación", mensaje_error)
                    return None  # Retorna None para indicar que no se obtuvo información

                except TimeoutException:
                    pass

                razonSocial_element = None
                try:
                    razonSocial_element = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:razonSocial")
                except NoSuchElementException:
                    pass

                if razonSocial_element:
                    numNit_element = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit")
                    numNit = numNit_element.get_attribute("value")
                    dv = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv").text
                    razonSocial = razonSocial_element.text
                    fecha_actual_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Fecha Actual')]/following-sibling::td[@class='tipoFilaNormalVerde']")
                    fecha_str = fecha_actual_element.text if fecha_actual_element else "Fecha no encontrada"

        

                    # Formatear la fecha en un formato reconocido por MySQL (por ejemplo, 'YYYY-MM-DD HH:MM:SS')
                    estado = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado").text

                    consulta_rut = SentenciasRUT()  # Crear una instancia de SentenciasRUT
                    if consulta_rut:
                        consulta_rut.conectar()  # Intentar establecer la conexión aquí

                        if consulta_rut.conexion.connection:  # Verificar si la conexión se estableció
                            # Utilizar la función correcta para la inserción
                            consulta_rut.insertar_proveedorrut_primera(numNit, razonSocial, dv, estado)
                        else:
                            messagebox.showerror("Error", "No se pudo establecer la conexión a la base de datos.")
                            return None  # Retorna None para indicar que no se pudo realizar la consulta

                    # Construir la información en el formato deseado
                    data = (
                        f"Razón Social: {razonSocial}\n"
                        f"NIT: {numNit}-{dv}\n"
                        f"Fecha de Consulta: {fecha_str}\n"
                        f"Estado: {estado}"
                    )

                    return data  # Retornar la información como una cadena de texto

                else:
                    # Recolectar información adicional
                    numNit = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit").get_attribute("value")
                    dv = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv").text

                    # Apellidos
                    primer_apellido = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerApellido").text
                    segundo_apellido = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:segundoApellido").text
                    apellidos = f"{primer_apellido} {segundo_apellido}"

                    # Nombres
                    primer_nombre = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerNombre").text
                    otros_nombres = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:otrosNombres").text
                    nombres = f"{primer_nombre} {otros_nombres}"

                    # Fecha
                    fecha_actual_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Fecha Actual')]/following-sibling::td[@class='tipoFilaNormalVerde']")
                    fecha_str = fecha_actual_element.text if fecha_actual_element else "Fecha no encontrada"

                    # Convertir la cadena de fecha a un objeto de fecha
                    fecha_dt = None
                    if fecha_str != "Fecha no encontrada":
                        try:
                            fecha_dt = datetime.datetime.strptime(fecha_str, "%d/%m/%Y %H:%M:%S")
                        except ValueError:
                            fecha_dt = None

                    # Formatear la fecha en un formato reconocido por MySQL (por ejemplo, 'YYYY-MM-DD HH:MM:SS')
                    fecha_str_mysql = fecha_dt.strftime("%Y-%m-%d %H:%M:%S") if fecha_dt else None
                    estado = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado").text

                    consulta_rut = SentenciasRUT()  # Crear una instancia de SentenciasRUT
                    with consulta_rut:
                        if consulta_rut.conexion.connection:  # Verificar si la conexión se estableció
                            # Utilizar la función correcta para la inserción
                            consulta_rut.insertar_proveedorrut_segunda(numNit, apellidos, nombres, dv, estado, fecha_dt)
                        else:
                            messagebox.showerror("Error", "No se pudo establecer la conexión a la base de datos.")
                            return None  # Retorna None para indicar que no se pudo realizar la consulta

                    # Construir la información en el formato deseado
                    data = (
                        f"Nombre Completo: {nombres} {apellidos}\n"
                        f"NIT: {numNit}-{dv}\n"
                        f"Fecha de Consulta: {fecha_str}\n"
                        f"Estado: {estado}"
                    )

                    return data  # Retornar la información como una cadena de texto

        except TimeoutException:
            messagebox.showerror("Error", "Tiempo de espera agotado. La página puede haber tardado demasiado en cargar.")
            return None  # Retorna None para indicar que no se pudo realizar la consulta
        except NoSuchElementException as e:
            messagebox.showerror("Error", f"No se pudo encontrar el elemento: {type(e).__name__} - {str(e)}")
            return None  # Retorna None para indicar que no se pudo realizar la consulta
        except WebDriverException as e:
            messagebox.showerror("Error", f"Excepción del WebDriver: {str(e)}")
            return None  # Retorna None para indicar que no se pudo realizar la consulta
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error en la consulta: {type(e).__name__} - {str(e)}")
            return None  # Retorna None para indicar que no se pudo realizar la consulta
