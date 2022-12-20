
#TRABAJO EXCEL ARTICULOS
from xlsx2csv import Xlsx2csv
from io import StringIO
import pandas as pd
import time
start_time = time.time()
#Lectura de archivos



def read_excel(path: str, sheet_name: str) -> pd.DataFrame:
    buffer = StringIO()
    Xlsx2csv(path, outputencoding="utf-8", sheet_name=sheet_name).convert(buffer)
    buffer.seek(0)
    agentes = pd.read_csv(buffer)
    return agentes

for i in range(len(archivos)):
    a=archivos[i]
    if ("ReporteArticulos" in a):
        path=ruta+"/"+a
        articulos=read_excel(path,"Hoja 1")
    elif ("ReporteTerminales" in a):
        path=r"H:\Mi unidad\TRABAJO\PROCESOS_AUTOMATICOS\Script_Logistica\ReporteTerminales 2022.12.13.xlsx"
        terminales=read_excel(path,"Hoja 1")

cabeza = articulos.iloc[0]
articulos = articulos[1:]
articulos.columns = cabeza
articulos["MODELO"]=articulos["ARTÍCULO"].str[0:6]
lista = ["AXIUM","APOS A","APOS M","APOS D","ICT220","ICT250"]
condicion = articulos["MODELO"].isin(lista)
articulos=articulos[condicion]
articulos=articulos.drop_duplicates(subset='NUMERO SERIE')


#INSERTANDO DATOS DE ARTICULOS AL GS
import pandas as pd 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
gc = gspread.service_account(filename="H:\Mi unidad\LLAVES\ActivarGoogleSheetIan.json")
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JYaYF64CIkWeyS3rpxmTN15WNae5yS0oPHIaXLUi21M")
wsheet = gsheet.worksheet("articulos 05.12")
wsheet.update([articulos.columns.values.tolist()]+articulos.values.tolist())


#TRABAJO EXCEL TERMINALES

cabeza = terminales.iloc[0]
terminales = terminales[1:]
terminales.columns = cabeza
terminales["x"]=terminales["ARTÍCULO"].str[0:6]
lista = ["AXIUM","APOS A","APOS M","APOS D","ICT220","ICT250"]
condicion = terminales["x"].isin(lista)
terminales=terminales[condicion]
lista2 = ["Creado","Enviada"]
condicion2 = terminales["ESTADO"].isin(lista2)
terminales=terminales[condicion2]
terminales2=terminales
terminales=terminales[["ARTÍCULO","NÚMERO SERIE","CANTIDAD","ESTADO","ACTUALIZADO","TIPO","TERMINAL/DNI/RUC"]]
terminales = terminales.fillna('')
terminales = terminales.drop_duplicates(subset="NÚMERO SERIE")

#INSERTANDO DATOS EN GS ENVIADOS
wsheet = gsheet.worksheet("Enviado 02.12")
wsheet.update([terminales.columns.values.tolist()]+terminales.values.tolist())


#TRABAJO EXCEL TERMINALES
lista3 = ["DNI", "Terminales"]
condicion3=terminales2["TIPO"].isin(lista3)
terminales2 =terminales2[condicion3]
terminales2=terminales2[terminales2["TERMINAL/DNI/RUC"].notnull()]
terminales2=terminales2[['TIPO','TERMINAL/DNI/RUC','AGENTE/EJECUTIVO','UBICACIÓN','ESTADO_TERMINAL','FECHA_ACTUALIZACION_TERMINAL','Estado Personal','FECHA ACTUALIZACION PERSONAL']]
terminales2 = terminales2.fillna('')
terminales2 = terminales2.drop_duplicates(subset='TERMINAL/DNI/RUC')

#INSERTANDO DATOS EN GS TERMINALES
wsheet = gsheet.worksheet("Terminales 02.12")
wsheet.update([terminales2.columns.values.tolist()]+terminales2.values.tolist())

