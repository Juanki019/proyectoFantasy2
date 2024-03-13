from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configuración de Selenium para utilizar el navegador Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Ejecución sin interfaz gráfica
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL de la página web
url = 'https://www.analiticafantasy.com/la-liga/alineaciones-probables'

# Acceder a la página web
driver.get(url)


# Encontrar el elemento "Alineaciones probables" y hacer clic en él
elements = driver.find_elements(By.XPATH, "//p[text()='Alineaciones probables']")

driver.implicitly_wait(10)

for i, element in enumerate(elements, 1):
    # Hacer clic en el elemento
    driver.implicitly_wait(10)
    element.click()
    # Esperar un momento para que la página se actualice después del clic
    driver.implicitly_wait(10)
    # Encontrar el elemento de la alineación y capturar la captura de pantalla
    section_element = driver.find_element(By.CLASS_NAME, 'alineaciones-probables-container')
    screenshot_path = f'C:\\UEM - 3\\PROYECTO2\\proyectoFantasy2\\DATABASE\\ALINEACIONES\\partido{i}.png'
    section_element.screenshot(screenshot_path)
    driver.back()


# Cerrar el navegador
driver.quit()