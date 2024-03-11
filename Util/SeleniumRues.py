# SeleniumRues.py
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from tkinter import messagebox
from Persistence.SentenciasRues import SentenciasRUES, ProveedorRUES
import traceback

class SeleniumRues:
    """
    Clase para realizar consultas al Registro Único Empresarial y Social (RUES) utilizando Selenium.
    """
    def __init__(self):
        """
        Constructor de la clase SeleniumRues.
        """
        # Configuración para ejecutar en modo headless
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")  # Habilitar el modo headless
        self.sentencias_rues = SentenciasRUES()

    def limpiar_identificacion(self, identificacion):
        """
        Limpia la identificación removiendo puntos y guiones.

        Parámetros:
            identificacion (str): Identificación a limpiar.

        Retorna:
            str: Identificación sin puntos ni guiones.
        """
        identificacion_limpia = identificacion.replace('.', '').replace('-', '')
        return identificacion_limpia

    def consultar_rues_con_selenium_headless(self, entry_identificacion):
        """
        Consulta la información del RUES utilizando Selenium en modo headless.

        Parámetros:
            entry_identificacion (str): Identificación del proveedor.

        Retorna:
            str: Información del proveedor obtenida del RUES.
        """
        identificacion = entry_identificacion
        identificacion_limpia = self.limpiar_identificacion(identificacion)

        if not identificacion_limpia:
            messagebox.showinfo("Error", "Por favor, ingrese una identificación.")
            return None  # Retorna None para indicar que no se pudo realizar la consulta

        try:
            # Iniciar el WebDriver con las opciones configuradas
            with webdriver.Chrome(self.chrome_options) as driver:
                driver.get("https://www.rues.org.co/rm")

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtSearchNIT")))

                input_identificacion = driver.find_element(By.ID, "txtSearchNIT")
                input_identificacion.clear()
                input_identificacion.send_keys(identificacion_limpia)

                driver.find_element(By.ID, "btnConsultaNIT").click()

                # Verificar si la consulta no ha retornado resultados
                no_resultado_element = driver.find_elements(By.XPATH, "//div[@id='card-info'][contains(@class, 'notice-info')][contains(text(), 'La consulta por NIT no ha retornado resultados')]")
                if no_resultado_element:
                    # Manejar el caso de consulta sin resultados
                    return "Información no obtenida"

                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//table[@id='rmTable2']//tbody//td")))

                table_html = driver.find_element(By.ID, "rmTable2").get_attribute("outerHTML")
                soup = BeautifulSoup(table_html, 'html.parser')

                tbody = soup.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')

                    mensaje_final_rues = ""  # Crear una cadena para almacenar la información obtenida

                    for row in rows:
                        data_cells = row.find_all('td')
                        if data_cells:
                            razon_social = data_cells[0].text.strip()
                            sigla = data_cells[1].text.strip()
                            nit_celda = data_cells[2].text.strip()
                            estado = data_cells[3].text.strip()
                            camara_comercio = data_cells[4].text.strip()
                            matricula = data_cells[5].text.strip()
                            organizacion_juridica = data_cells[6].text.strip()
                            categoria = data_cells[7].text.strip()

                            nit_match = re.search(r'\b\d{8,12}\b', nit_celda)
                            nit_completo = nit_match.group() if nit_match else None

                            if estado == "ACTIVA":
                                try:
                                    # Click en el primer botón "Ver Detalle"
                                    print("Click en el primer botón 'Ver Detalle'")
                                    driver.find_element(By.XPATH, "//*[@id='rmTable2']/tbody/tr[1]/td[1]").click()
                                    driver.find_element(By.LINK_TEXT, "Ver Detalle").click()

                                    # Esperar a que la página cargue después de las nuevas interacciones
                                    WebDriverWait(driver, 30).until(
                                        EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']/ul[@class='cleanlist']"))
                                    )

                                    # Obtener información de actividades económicas
                                    actividades_economicas_element = driver.find_element(By.XPATH, "//div[@class='card-body']/ul[@class='cleanlist']")
                                    actividades_economicas_lines = actividades_economicas_element.find_elements(By.XPATH, ".//li")

                                    # Extraer información de las actividades económicas
                                    actividades_economicas = []
                                    for line in actividades_economicas_lines:
                                        match = re.search(r'<b>(\d+)<\/b>&nbsp;(.+)', line.get_attribute("innerHTML"))
                                        if match:
                                            codigo_actividad = match.group(1)
                                            actividades_economicas.append(codigo_actividad)

                                    # Imprimir las actividades económicas obtenidas
                                    print(f"Actividades Económicas: {actividades_economicas}")

                                    # Insertar la información en la base de datos
                                    proveedor = ProveedorRUES(
                                        provNit=nit_completo, provNombre=razon_social, estado=estado,
                                        camara_comercio=camara_comercio, matricula=matricula,
                                        organizacion_juridica=organizacion_juridica, categoria=categoria,
                                        actividades_economicas=actividades_economicas
                                    )
                                    self.sentencias_rues.insertar_proveedor_rues_en_db(proveedor)

                                    mensaje_final_rues += (
                                        f"Razón Social: {razon_social}\n"
                                        f"Sigla: {sigla}\n"
                                        f"NIT: {nit_completo}\n"
                                        f"Estado: {estado}\n"
                                        f"Cámara de Comercio: {camara_comercio}\n"
                                        f"Matrícula: {matricula}\n"
                                        f"Organización Jurídica: {organizacion_juridica}\n"
                                        f"Categoría: {categoria}\n"
                                        f"Actividades Económicas: {', '.join(actividades_economicas)}\n\n"
                                    )

                                except:
                                    proveedor = ProveedorRUES(
                                        provNit=nit_completo, provNombre=razon_social, estado=estado,
                                        camara_comercio=camara_comercio, matricula=matricula,
                                        organizacion_juridica=organizacion_juridica, categoria=categoria,
                                        actividades_economicas=''
                                    )
                                    self.sentencias_rues.insertar_proveedor_rues_en_db(proveedor)  
                                    
                                    mensaje_final_rues += (
                                        f"Razón Social: {razon_social}\n"
                                        f"Sigla: {sigla}\n"
                                        f"NIT: {nit_completo}\n"
                                        f"Estado: {estado}\n"
                                        f"Cámara de Comercio: {camara_comercio}\n"
                                        f"Matrícula: {matricula}\n"
                                        f"Organización Jurídica: {organizacion_juridica}\n"
                                        f"Categoría: {categoria}\n"
                                        f"\nActividades Económicas: No se encontraron actividades económicas\n\n"
                                        )

                    # Mover el return fuera del bucle
                    return mensaje_final_rues.strip()

                else:
                    return "Información no obtenida"
        except NoSuchElementException:
            return "Error: Elemento no encontrado en la página"


        except Exception as e:
            messagebox.showerror(message='Documento no registrado en el RUES', title='¡Error!')
            

        except Exception as e:
            traceback.print_exc()
            return f"Error inesperado: {str(e)}"
    
    def is_recaptcha_present(self, driver):
        """
        Verifica si el reCAPTCHA está presente en la página.

        Parámetros:
            driver: Objeto WebDriver.

        Retorna:
            bool: True si el reCAPTCHA está presente, False en caso de que no.
        """
        try:
            # Verificar la presencia del elemento que contiene el reCAPTCHA
            driver.find_element(By.XPATH, "/html/body/div[1]/main")
            return True
        except NoSuchElementException:
            return False
