from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy as sa
from decouple import config

tabla=pd.read_csv("H:\Mi unidad\TRABAJO\BASES DE DATOS\PRUEBASQL.csv",sep=";",names=["id","FECHA","EMPRESA","DEPARTAMENTO","PROVINCIA","TRX"])
tabla=tabla.applymap(str)
print(tabla.head())

DB_USER="adminsql-ian"
DB_PASSWORD=config("DB_PASSWORD_AZURE")
DB_NAME="TestBase"
DB_DRIVER="ODBC Driver 13 for SQL Server"

cadena = f"mssql+pyodbc:///?odbc_connect=Driver={{{DB_DRIVER}}};Server=tcp:basedepruebaian.database.windows.net,1433;Database={DB_NAME};Uid={DB_USER};Pwd={DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"

engine_azure = create_engine(cadena,echo=True)

print('La conexión está correcta')

#print("Subiendo al SQL")
tabla.to_sql('Base_Test', con=engine_azure)


