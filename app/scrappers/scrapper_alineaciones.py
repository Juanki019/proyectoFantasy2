from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Nuevos imports usados por Santiago.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException

# Configuración de Selenium para utilizar el navegador Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Ejecución sin interfaz gráfica
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL de la página web
url = 'https://www.analiticafantasy.com/la-liga/alineaciones-probables'

# Acceder a la página web
driver.get(url)

# Aceptamos la política de privacidad.
wait = WebDriverWait(driver, 30)  # Aumentamos el tiempo de espera a 30 segundos
aceptar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-y8g67k')))
aceptar_button.click()

# Encontrar el elemento "Alineaciones probables" y hacer clic en él
elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[text()='Alineaciones probables']")))

driver.implicitly_wait(10)

for i, element in enumerate(elements, 1):
    # Hacer clic en el elemento utilizando JavaScript
    try:
        driver.execute_script("arguments[0].click();", element)
        # Esperar un momento para que la página se actualice después del clic
        time.sleep(5)  # Espera 5 segundos para que la página se actualice
        # Esperar a que el elemento de la alineación esté completamente visible
        section_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alineaciones-probables-container')))
        screenshot_path = f'C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\ALINEACIONES\\partido{i}.png'
        section_element.screenshot(screenshot_path)
        driver.back()
    except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
        print("Error al hacer clic en el elemento o al capturar la captura de pantalla, intentando de nuevo...")
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[text()='Alineaciones probables']")))
        element = elements[i - 1]
        driver.execute_script("arguments[0].click();", element)
        # Esperar un momento para que la página se actualice después del clic
        time.sleep(5)  # Espera 5 segundos para que la página se actualice
        # Esperar a que el elemento de la alineación esté completamente visible
        section_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alineaciones-probables-container')))
        screenshot_path = f'C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\data\\ALINEACIONES\\partido{i}.png'
        section_element.screenshot(screenshot_path)
        driver.back()

# Cerrar el navegador
driver.quit()