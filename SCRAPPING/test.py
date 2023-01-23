import time

from selenium import webdriver

from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/Rayzek/AppData/Local/Google/Chrome/User Data/Default")




driver = webdriver.Chrome(options=options)

driver.get('https://urbania.pe/')

time.sleep(50) # Let the user actually see something!

#driver.quit()