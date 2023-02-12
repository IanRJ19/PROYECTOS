import pandas as pd
from decouple import config
from sqlalchemy import create_engine

DB_USER='postgres'
DB_PASSWORD='cetroian'
DB_NAME="Datasets"
DB_HOST='localhost'
cadena0  = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(cadena0)
connection = engine.connect()

#base = pd.read_sql_query(f"SELECT * FROM public.mseg", con=connection)

connection.close()
