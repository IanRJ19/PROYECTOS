
import pandas as pd
from decouple import config
from sqlalchemy import create_engine

# Es importante habilitar mi ip en las redes permitidas
# Obtén los detalles de conexión desde la configuración de la instancia de Cloud SQL

DB_USER=config("USER_POSTGRES_GCP")
DB_PASSWORD=config("PASS_POSTGRES_GCP")
DB_NAME="postgres"
DB_PORT="5432"
DB_HOST=config("URL_POSTGRES_GCP")

cadena  = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(cadena)