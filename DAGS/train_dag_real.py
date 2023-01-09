import pandas as pd
import csv
import numpy as np
pd.options.display.max_columns = None
 
from datetime import datetime, timedelta
today = datetime.today() - timedelta(days=1)
# dd/mm/YY
fechaActual = today.strftime("%Y%m%d")

tsvPreguntas = '/home/ian-lx/Descargas/Preguntas.tvs'
excelEncuesta = '/home/ian-lx/Descargas/ReporteEncuesta.xls'

dfEncuesta = pd.read_excel(excelEncuesta)
dfPreguntas = pd.read_csv(tsvPreguntas, sep='\t')

#JUSTIFICAR A LA DERECHA 2 ESPACIOS

#APLICAR APPLYMAP PARA CAMBIAR A TODO EL ARCHIVO Y HACERLO TEXTO
dfPreguntas = dfPreguntas.applymap(str)
dfPreguntas['ID_Pregunta'] = dfPreguntas['ID_Pregunta'].str.rjust(2,'0')


#CREAMOS DATAFRAME EN BLANCO
dfSubirE = pd.DataFrame()

#REEMPLAZAR NULO POR VACIO
dfEncuesta = dfEncuesta.replace(np.nan,'')
dfEncuesta = dfEncuesta.applymap(str)
dfEncuesta["Pregunta"] = dfEncuesta["Pregunta"].str.strip()
dfEncuesta["Pregunta"] = dfEncuesta['Pregunta'].str[:138]

for i in dfEncuesta.index:
    if (dfEncuesta["Pregunta"][i] not in dfPreguntas.values):
        #Capturando la nueva Pregunta
        nuevaPregunta = dfEncuesta["Pregunta"][i]
        #Generando el nuevoID
        nuevoID = dfPreguntas['ID_Pregunta'].iloc[-1]
        nuevoID = nuevoID + 1
        #AGREGANDO EL NUEVO VALOR
        with open(dfPreguntas, 'a+', newline='') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow([nuevaPregunta, nuevoID])
 
 
for i in dfPreguntas.index:
    dfEncuesta.loc[dfEncuesta['Pregunta'] == dfPreguntas['Pregunta'][i], 'ID_Pregunta'] = dfPreguntas['ID_Pregunta'][i]
 
 
########__________DATA FRAME FINAL PARA SUBIR LA ENCUESTA__________#######
dfSubirE['ID_Encuesta'] = "EN" + dfEncuesta['FechaVisita'].str[-2:] + dfEncuesta['FechaVisita'].str[3:5] + dfEncuesta['FechaVisita'].str[:2] + dfEncuesta['HoraVisita'].str.replace(":","") + dfEncuesta['CodigoTienda'] + dfEncuesta['FechaInstalación'].str[6:10] + dfEncuesta['FechaInstalación'].str[3:5] + dfEncuesta['FechaInstalación'].str[0:2] + dfEncuesta['Visita ID'].str[-2:] +  dfEncuesta['ID_Pregunta']
dfSubirE['ID_Visita'] = dfEncuesta['Visita ID']
dfSubirE['MesVisita'] = dfEncuesta['MesVisita']
dfSubirE['FechaVisita'] = dfEncuesta['FechaVisita'].str[-4:] + dfEncuesta['FechaVisita'].str[3:5] + dfEncuesta['FechaVisita'].str[:2]
dfSubirE['HoraVisita'] = dfEncuesta['HoraVisita'].str.replace(':','')
dfSubirE['ID_Agente'] = dfEncuesta['CodigoTienda']
dfSubirE['FechaInstalacion'] = dfEncuesta['FechaInstalación'].str[6:10] + dfEncuesta['FechaInstalación'].str[3:5] + dfEncuesta['FechaInstalación'].str[0:2]
dfSubirE['Usuario'] = dfEncuesta['Usuario'].str[:24]
dfSubirE['Pregunta'] = dfEncuesta['Pregunta']
dfSubirE['Respuesta'] = dfEncuesta['Respuesta']
 
 
##REACOMODAR EL LARGO DEL LOS STRINGS
dfSubirE['ID_Encuesta'] = dfSubirE['ID_Encuesta'].str[:32]
dfSubirE['ID_Visita'] = dfSubirE['ID_Visita'].str[:6]
dfSubirE['MesVisita'] = dfSubirE['MesVisita'].str[:6]
dfSubirE['FechaVisita'] = dfSubirE['FechaVisita'].str[:8]
dfSubirE['HoraVisita'] = dfSubirE['HoraVisita'].str[:6]
dfSubirE['ID_Agente'] = dfSubirE['ID_Agente'].str[:6]
dfSubirE['FechaInstalacion'] = dfSubirE['FechaInstalacion'].str[:8]
dfSubirE['Usuario'] = dfSubirE['Usuario'].str[:24]
dfSubirE['Pregunta'] = dfSubirE['Pregunta'].str[:138]
dfSubirE['Respuesta'] = dfSubirE['Respuesta'].str[:140]
 
#print("Sin filtro fecha: ", dfSubirE.shape)
dfSubirE = dfSubirE.loc[dfSubirE['FechaVisita'] == fechaActual]
#print("Con filtro fecha: ", dfSubirE.shape)
 
dfSubirE.drop_duplicates(subset='ID_Encuesta', keep = 'first', inplace = True)
 
#print("Con filtro fecha y duplicados: ", dfSubirE.shape)
#print(dfSubirE.dtypes)
#print(dfSubirE.shape)
 

#EXPORTAR dfSubirE.to_excel("compilado.xlsx")
print(dfSubirE.head())