import time

from selenium import webdriver

from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir=C:/Users/Rayzek/AppData/Local/Google/Chrome/User Data/Default")

options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"


driver = webdriver.Chrome(chrome_options=options)

driver.get('https://urbania.pe/')

time.sleep(50)

#driver.quit()