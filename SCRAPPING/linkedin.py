from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decouple import config


# Inicializar el driver de Selenium
driver = webdriver.Chrome()

# Ir a la página de inicio de LinkedIn
driver.get("https://www.linkedin.com/uas/login/")


user =config("USER_LKN")
pass =config("PASS_LKN")

# Encontrar el campo de inicio de sesión y enviar credenciales
username = driver.find_element(By.TAG_NAME,"session_key")
username.send_keys(user)
password = driver.find_element(By.TAG_NAME,"session_password")
password.send_keys(pass)

# Hacer clic en el botón de inicio de sesión
driver.find_element_by_xpath("//button[@type='submit']").click()

# Ir a la página de búsqueda de trabajos
driver.get("https://www.linkedin.com/jobs/")

# Encontrar el campo de búsqueda y enviar términos de búsqueda
search_field = driver.find_element_by_xpath("//input[@placeholder='Search jobs']")
search_field.send_keys("Data")
search_field.send_keys(Keys.RETURN)

# Mostrar los resultados de la búsqueda
jobs = driver.find_elements_by_xpath("//a[@class='job-title-link']")
for job in jobs:
    print(job.text)

# Cerrar el navegador
driver.quit()
