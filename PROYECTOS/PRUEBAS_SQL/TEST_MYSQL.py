import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as sql

# engine = create_engine('mysql+pymysql://username:password@host/database')
# or in your case-
engine = create_engine('mysql+pymysql://user:pw@124685.eu-central-1.rds.amazonaws.com/db_name')

db_connection = sql.connect(host='124685.eu-central-1.rds.amazonaws.com', 
        database="db_name", user='user', password='pw')

query = 'SELECT * FROM table_name'
df = pd.read_sql(sql=query, con=db_connection)
df["Person_Name"] = "xx"

df.to_sql(con=engine, name='table_name', if_exists='replace')