from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decouple import config
import time
import pandas as pd 

# Inicializar el driver de Selenium
driver = webdriver.Chrome()

# Ir a la página de inicio de LinkedIn
driver.get("https://www.linkedin.com/uas/login/")


user =config("USER_LKN")
clave =config("PASS_LKN")

# Encontrar el campo de inicio de sesión y enviar credenciales
username = driver.find_element(By.ID,"username")
username.send_keys(user)
password = driver.find_element(By.ID,"password")
password.send_keys(clave)

time.sleep(9)

# Hacer clic en el botón de inicio de sesión
boton=driver.find_element(By.CLASS_NAME,"btn__primary--large.from__button--floating")
boton.click()

time.sleep(9)
# Ir a la página de búsqueda de trabajos
driver.get("https://www.linkedin.com/jobs/")
time.sleep(9)

# Encontrar el campo de búsqueda y enviar términos de búsqueda
search_field = driver.find_element(By.CLASS_NAME,"jobs-search-box__text-input.jobs-search-box__keyboard-text-input")
search_field.send_keys("Data")
search_field.send_keys(Keys.ENTER)
time.sleep(9)

job_elements = driver.find_elements(By.CSS_SELECTOR,"[class*='job-card-container']")
jobs = []

# Iterar sobre los elementos de las ofertas de trabajo
for job_element in job_elements:
    title_elements = job_element.find_elements(By.CSS_SELECTOR,"[class*='list__title']")
    company_elements = job_element.find_elements(By.CSS_SELECTOR,"[class*='company-name']")
    location_elements = job_element.find_elements(By.CSS_SELECTOR,"[class*='metadata-item']")
    title = title_elements[0].text if title_elements else None
    company = company_elements[0].text if company_elements else None
    location = location_elements[0].text if location_elements else None
    jobs.append({"title": title, "company": company, "location": location})


# Almacenar los datos en un DataFrame de Pandas
jobs_df = pd.DataFrame(jobs)

print(job_elements)

print(jobs_df)