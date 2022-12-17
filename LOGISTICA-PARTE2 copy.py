#AGREGAR PESTAÑA
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account(filename="H:\Mi unidad\LLAVES\ActivarGoogleSheetIan.json")
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JYaYF64CIkWeyS3rpxmTN15WNae5yS0oPHIaXLUi21M")

#CREAMOS LA PESTAÑA DEL RESUMEN
#gsheet.add_worksheet(rows=20,cols=20,title='FINAL')

pestaña = gsheet.worksheet("BD").get_all_records()
Base= pd.DataFrame(pestaña)

# INSTAURAMOS EL CONTROLADOR DE PESTAÑA
wsheet = gsheet.worksheet("FINAL")

#PIVOT CON NUMERO DE SERIE POR CADA ESTADO SG
df1=Base.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], columns="ESTADO SG", aggfunc="count",fill_value=0, margins=True)
df1=df1.reset_index()

#ASIGNANDO DATA
df1_POS_DISP=df1[["MODELO","Disponible"]]
df1 = df1[18:]
df1_TOTAL_SG=df1
df1_POS_INICIAL=df1["All"]
DF_ASIGNADOS_CLIENTES=Base[Base["Tipo"].isin(["RUC(Empresa)", "RUC(Entidad Financiera)"])]
DF_ASIGNADOS_PERSONAL=Base[Base["Tipo"]=="DNI"]


#POS FINAL DISPONIBLES
df1_POS_DISP=df1_POS_DISP.replace(['ICT 220','ICT 250'], "POS final (disponible) ICT")
df1_POS_DISP=df1_POS_DISP.replace(['APOS'], "POS final (disponible) APOS")
df1_POS_DISP=df1_POS_DISP.replace(['DX8000'], "POS final (disponible) DX8000")
df1_POS_DISP=df1_POS_DISP.groupby(["MODELO"])["Disponible"].sum()
df1_POS_DISP=df1_POS_DISP.reset_index()
df1_POS_DISP=df1_POS_DISP.drop(df1_POS_DISP.index[0])
df1_POS_DISP.columns=["DESCRIPCIÓN","CANTIDAD"]

#POS INICIAL
df1_POS_INICIAL=df1_POS_INICIAL.reset_index()
df1_POS_INICIAL.columns=["DESCRIPCIÓN","CANTIDAD"]
df1_POS_INICIAL["DESCRIPCIÓN"]="POS INICIAL"

#TOTALES POR ESTADO SG
df1_TOTAL_SG=df1_TOTAL_SG.drop(["All","OC","MODELO","Despachado","Disponible","Asignado"], axis=1)
df1_TOTAL_SG=df1_TOTAL_SG.transpose()
df1_TOTAL_SG=df1_TOTAL_SG.reset_index()
df1_TOTAL_SG.columns=["DESCRIPCIÓN","CANTIDAD"]
df1_TOTAL_SG=df1_TOTAL_SG.replace('Bloqueado', "Irreparables")
df1_TOTAL_SG=df1_TOTAL_SG.replace('De baja', "De baja (Venta/Robo)")

#POS Asignado a Empresas
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",fill_value=0, margins=True)
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.reset_index()
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES[9:]
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.drop(['OC', 'MODELO'],axis=1 )
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.transpose()
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.reset_index()
DF_ASIGNADOS_CLIENTES.columns=["DESCRIPCIÓN","CANTIDAD"]
DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.replace('NUMERO SERIE', "Asignados a Clientes")

#POS Asignado a Personal Activo y Cesado
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="tipo DNI",fill_value=0, margins=True)
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.reset_index()
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL[13:]
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.transpose()
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.reset_index()
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL[3:5]
DF_ASIGNADOS_PERSONAL.columns=["DESCRIPCIÓN","CANTIDAD"]
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.replace('Activo', "Asignados al Personal")
DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.replace('Cesado', "Asignados al Personal Cesado")


#UNIENDO ALL Y SUBIENDO
total=pd.concat([df1_POS_INICIAL,DF_ASIGNADOS_CLIENTES,DF_ASIGNADOS_PERSONAL,df1_TOTAL_SG,df1_POS_DISP])
total=total.reset_index()
total=total.drop("index", axis=1)
print(total)
wsheet.update([total.columns.values.tolist()]+total.values.tolist())