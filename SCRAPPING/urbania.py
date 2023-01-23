from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
driver = webdriver.Chrome(chrome_options=options)

# Crea una instancia de la clase webdriver.Chrome()

driver.get("https://urbania.pe/")
time.sleep(10)
# Imprime el título de la página web
print(driver.title)

#REEMPLAZAR ESPACIOS POR PUNTOS
#element = driver.find_element(By.CSS_SELECTOR,"CustomInput-sc-hd4j3y-7 fmLrhF")
element =driver.find_element(By.CSS_SELECTOR,".CustomInput-sc-hd4j3y-7.fmLrhF")
time.sleep(10)
element.send_keys("San Miguel, Lima, Lima")
time.sleep(10)
#element.send_keys(Keys.RETURN)
#element.send_keys(Keys.ENTER)

#time.sleep(100)

#search_button = driver.find_element(By.CLASS_NAME,"search-button")

#search_button = driver.find_element(By.CSS_SELECTOR,".sc-kMjNwy.gxFhbn.btn-primary.btn-full")
#search_button.click()
time.sleep(10)
search_button = driver.find_element(By.CSS_SELECTOR,"button[data-qa='search-button']")
time.sleep(10)
search_button.click()
#time.sleep(500)
# Cierra el navegador
#driver.quit()