import requests
import pandas as pd

url = "https://urbania.pe/mapas/alquiler-de-departamentos-en-san-miguel--lima--lima/data.json"

# Realizar una solicitud a la URL y obtener la respuesta JSON
response = requests.get(url)
data = response.json()

# Crear un DataFrame a partir de la respuesta JSON
departments_df = pd.DataFrame(data)
