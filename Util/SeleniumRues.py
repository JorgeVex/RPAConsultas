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


class SeleniumRues:
    def __init__(self):
        # Configuración para ejecutar en modo headless
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")  # Habilitar el modo headless
        self.sentencias_rues = SentenciasRUES()

    def limpiar_identificacion(self, identificacion):
        identificacion_limpia = identificacion.replace('.', '').replace('-', '')
        return identificacion_limpia

    def consultar_rues_con_selenium_headless(self, identificacion_limpia_rut):
        if not identificacion_limpia_rut:
            messagebox.showinfo("Error", "Por favor, ingrese una identificación.")
            return None  # Retorna None para indicar que no se pudo realizar la consulta

        try:
            # Iniciar el WebDriver con las opciones configuradas
            with webdriver.Chrome(options=self.chrome_options) as driver:
                driver.get("https://www.rues.org.co/rm")

                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "txtSearchNIT")))

                input_identificacion = driver.find_element(By.ID, "txtSearchNIT")
                input_identificacion.clear()
                input_identificacion.send_keys(identificacion_limpia_rut)

                driver.find_element(By.ID, "btnConsultaNIT").click()

                # Verificar si la consulta no ha retornado resultados
                no_resultado_element = driver.find_elements(By.XPATH, "//div[@id='card-info'][contains(@class, 'notice-info')][contains(text(), 'La consulta por NIT no ha retornado resultados')]")
                if no_resultado_element:
                    messagebox.showinfo("Información", "La consulta por NIT no ha retornado resultados.")
                    return "Información no obtenida"  # Retorna un mensaje indicando que no se obtuvo información

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
                            # Extraer información
                            razon_social = data_cells[0].text.strip()
                            sigla = data_cells[1].text.strip()
                            nit_celda = data_cells[2].text.strip()
                            estado = data_cells[3].text.strip()
                            camara_comercio = data_cells[4].text.strip()
                            matricula = data_cells[5].text.strip()
                            organizacion_juridica = data_cells[6].text.strip()
                            categoria = data_cells[7].text.strip()
                            

                            # Buscar el NIT completo dentro de la celda
                            nit_match = re.search(r'\b\d{8,12}\b', nit_celda)
                            nit_completo = nit_match.group() if nit_match else None

                            # Verificar si el estado es "ACTIVA"
                        # Verificar si el estado es "ACTIVA"
                        if estado == "ACTIVA":
                            # Agregar información al mensaje final
                            
                            driver.find_element(By.CSS_SELECTOR, ".odd > td:nth-child(1)").click()
                            driver.find_element(By.LINK_TEXT, "Ver Detalle").click()
                            
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']/ul[@class='cleanlist']")))
                            actividades_economicas_element = driver.find_element(By.XPATH, "//div[@class='card-body']/ul[@class='cleanlist']")
                            actividades_economicas_lines = actividades_economicas_element.find_elements(By.XPATH, ".//li")
                                
                            actividades_economicas = []
                            for line in actividades_economicas_lines:
                                match = re.search(r'<b>(\d+)<\/b>&nbsp;(.+)', line.get_attribute("innerHTML"))
                                if match:
                                    codigo_actividad = match.group(1)
                                    descripcion_actividad = match.group(2)
                                    actividades_economicas.append((codigo_actividad, descripcion_actividad))

                            # Mover la creación de la cadena fuera del bucle para evitar que se repita
                            actividades_economicas_str = ', '.join([f"{codigo_actividad}: {descripcion_actividad}" for codigo_actividad, descripcion_actividad in actividades_economicas])

                            mensaje_final_rues += (
                                f"Razón Social: {razon_social}\n"
                                f"Sigla: {sigla}\n"
                                f"NIT: {nit_completo}\n"
                                f"Estado: {estado}\n"
                                f"Cámara de Comercio: {camara_comercio}\n"
                                f"Matrícula: {matricula}\n"
                                f"Organización Jurídica: {organizacion_juridica}\n"
                                f"Categoría: {categoria}\n"
                                f"\nActividades Económicas: \n {actividades_economicas_str}\n"
                                f"\n{mensaje_final_rues}"
                            )

                            proveedor_rues = SentenciasRUES()  # Usa la clase SentenciasRUES
                            proveedor_rues.insertar_proveedor_rues_en_db(
                                ProveedorRUES(
                                    nit_completo, razon_social, estado, camara_comercio, matricula, organizacion_juridica, categoria, actividades_economicas_str
                                )
                            )

                return mensaje_final_rues   # Retorna un mensaje indicando que la consulta fue exitosa

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
