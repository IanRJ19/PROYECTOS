#LOGS
import time
import logging
import os
LOG_FILENAME = os.path.abspath(os.path.dirname(__file__)) + "\Visita.log"
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename=LOG_FILENAME)
inicioTiempo = time.time()


#PONER AL FINAL
finalTiempo = time.time()
totalTiempo = finalTiempo - inicioTiempo
print("Total tiempo: " + str(totalTiempo))
logging.info("Total tiempo: " + str(totalTiempo))


#TRAER SQL

import pyodbc
import pandas as pd
import sqlalchemy as sa

engine ="PASS Y USER"

sqlREAL = "SELECT DISTINCT(FECHAVISITA) FROM TH_VISITA WHERE MESVISITA = FORMAT(GETDATE(), 'yyyyMM') OR MESVISITA = FORMAT(DATEADD(MM,-1,GETDATE()), 'yyyyMM') ORDER BY 1 ASC"
#ASIGNAMOS LOS VALORES AL DATAFRAME
dfFechaVisitas = pd.read_sql_query(sqlREAL, con = engine)
dfFechaVisitas.applymap(str)

#SUBIR AL SQL
dfSubirE.to_sql('TH_Encuesta', con=engine, if_exists='append', index=False )