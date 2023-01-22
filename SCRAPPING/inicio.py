from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# Crea una instancia de la clase webdriver.Chrome()

driver = webdriver.Chrome()
driver.get("https://urbania.pe/")

# Imprime el título de la página web
print(driver.title)

#REEMPLAZAR ESPACIOS POR PUNTOS
#element = driver.find_element(By.CSS_SELECTOR,"CustomInput-sc-hd4j3y-7 fmLrhF")
element =driver.find_element(By.CSS_SELECTOR,".CustomInput-sc-hd4j3y-7.fmLrhF")

element.send_keys("San Miguel")
element.send_keys(Keys.RETURN)

# Cierra el navegador
#driver.quit()