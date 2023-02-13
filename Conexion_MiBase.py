import pandas as pd
from decouple import config
from sqlalchemy import create_engine

df=pd.read_csv('DATASETS\Iris.csv')

DB_USER='postgres'
DB_PASSWORD='cetroian'
DB_NAME="Datasets"
DB_HOST='localhost'
DB_PORT=5432
cadena0  = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(cadena0)
connection = engine.connect()

#base = pd.read_sql_query(f"SELECT * FROM public.mseg", con=connection)

df.to_sql("Iris", con=engine, if_exists="append", index=False)
connection.close()


