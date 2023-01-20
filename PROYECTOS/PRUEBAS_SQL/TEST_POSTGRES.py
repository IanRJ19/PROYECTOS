import psycopg2
import pandas as pd
from decouple import config

# Es importante habilitar mi ip en las redes permitidas
# Obtén los detalles de conexión desde la configuración de la instancia de Cloud SQL

connection = psycopg2.connect(
        host=config("URL_POSTGRES_GCP"),
        port=5432,
        user=config("USER_POSTGRES_GCP"),
        password=config("PASS_POSTGRES_GCP"),
        dbname="postgres"
)

data={'name': ['John', 'Mike', 'Emily'],
        'age': [25, 30, 35],
        'city': ['New York', 'Los Angeles', 'Chicago']}
df = pd.DataFrame(data)
df.to_sql("Iris",schema='public', con=connection, if_exists="append", index=False)
# Guardar los cambios en la base de datos
connection.commit()

# Cerrar la conexión
connection.close()