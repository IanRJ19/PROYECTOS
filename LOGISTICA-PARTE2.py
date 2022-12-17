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
DF_POS_DISPONIBLE=df1[["MODELO","Disponible"]]
DF_TOTAL_SG=df1
DF_POS_INICIAL=df1
DF_ASIGNADOS_CLIENTES=Base[Base["Tipo"].isin(["RUC(Empresa)", "RUC(Entidad Financiera)"])]
DF_ASIGNADOS_PERSONAL=Base[Base["Tipo"]=="DNI"]
DF_INSTALADOS_1=Base[(Base["Estado terminal"]=="Instalado") & (Base["ESTADO SG"].isin(["Despachado","Asignado"]))]
DF_ESTADO_BYS=Base.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="Estado terminal",fill_value=0, margins=True)
DF_ESTADO_DEBAJA=Base[Base["MODELO"].isin(["ICT 220", "ICT 250","APOS"])]


#POS FINAL DISPONIBLES
DF_POS_DISPONIBLE=DF_POS_DISPONIBLE.replace(['ICT 220','ICT 250'], "POS final (disponible) ICT")
DF_POS_DISPONIBLE=DF_POS_DISPONIBLE.replace(['APOS'], "POS final (disponible) APOS")
DF_POS_DISPONIBLE=DF_POS_DISPONIBLE.replace(['DX8000'], "POS final (disponible) DX8000")
DF_POS_DISPONIBLE=DF_POS_DISPONIBLE.groupby(["MODELO"])["Disponible"].sum()
DF_POS_DISPONIBLE=DF_POS_DISPONIBLE.reset_index()
DF_POS_DISPONIBLE=DF_POS_DISPONIBLE.drop(DF_POS_DISPONIBLE.index[0])
DF_POS_DISPONIBLE.columns=["DESCRIPCIÓN","CANTIDAD"]

#POS INICIAL
DF_POS_INICIAL=df1
DF_POS_INICIAL=DF_POS_INICIAL.set_index("OC")
DF_POS_INICIAL=DF_POS_INICIAL.loc["All":]
DF_POS_INICIAL=DF_POS_INICIAL.drop(["MODELO","Despachado","Disponible","Asignado",'Bloqueado', 'De baja', 'En mantenimiento', 'Malogrado', 'Por Ubicar'], axis=1)
DF_POS_INICIAL=DF_POS_INICIAL.reset_index()
DF_POS_INICIAL.columns=["DESCRIPCIÓN","CANTIDAD"]
DF_POS_INICIAL=DF_POS_INICIAL.replace("All", "POS INICIAL")

#TOTALES POR ESTADO SG
DF_TOTAL_SG=DF_TOTAL_SG.set_index("OC")
DF_TOTAL_SG=DF_TOTAL_SG.loc["All":]
DF_TOTAL_SG=DF_TOTAL_SG.reset_index()
DF_TOTAL_SG=DF_TOTAL_SG.drop(["All","OC","MODELO","Despachado","Disponible","Asignado"], axis=1)
DF_TOTAL_SG=DF_TOTAL_SG.transpose()
DF_TOTAL_SG=DF_TOTAL_SG.reset_index()
DF_TOTAL_SG.columns=["DESCRIPCIÓN","CANTIDAD"]
DF_TOTAL_SG=DF_TOTAL_SG.replace('Bloqueado', "Irreparables")
DF_TOTAL_SG=DF_TOTAL_SG.replace('De baja', "De baja (Venta/Robo)")

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

#Instalados AKN (1) y (+2)
DF_INSTALADOS_1=DF_INSTALADOS_1.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="x",fill_value=0, margins=True)
DF_INSTALADOS_2=DF_INSTALADOS_1
DF_INSTALADOS_1=DF_INSTALADOS_1.reset_index()
DF_INSTALADOS_1=DF_INSTALADOS_1.replace('ICT 220', "Instalados AKN (1) ICT")
DF_INSTALADOS_1=DF_INSTALADOS_1.replace('ICT 250', "Instalados AKN (1) ICT")
DF_INSTALADOS_1=DF_INSTALADOS_1.replace('APOS', "Instalados AKN (1) APOS")
DF_INSTALADOS_1=DF_INSTALADOS_1.groupby("MODELO").sum()
DF_INSTALADOS_1=DF_INSTALADOS_1.reset_index()
DF_INSTALADOS_1=DF_INSTALADOS_1.drop(0, axis=0)
DF_INSTALADOS_1=DF_INSTALADOS_1.drop([2,3,"All"], axis=1)
DF_INSTALADOS_1.columns=["DESCRIPCIÓN","CANTIDAD"]


DF_INSTALADOS_2["SUMA"]=DF_INSTALADOS_2[2]+DF_INSTALADOS_2[3]
DF_INSTALADOS_2=DF_INSTALADOS_2.reset_index()
DF_INSTALADOS_2=DF_INSTALADOS_2.drop(["All",1,2,3], axis=1)
DF_INSTALADOS_2=DF_INSTALADOS_2.replace('ICT 250', "Instalados AKN (+1)")
DF_INSTALADOS_2=DF_INSTALADOS_2.replace('ICT 220', "Instalados AKN (+1)")
DF_INSTALADOS_2=DF_INSTALADOS_2.replace('APOS', "Instalados AKN (+1)")
DF_INSTALADOS_2=DF_INSTALADOS_2.groupby("MODELO").sum()
DF_INSTALADOS_2=DF_INSTALADOS_2.reset_index()
DF_INSTALADOS_2=DF_INSTALADOS_2.drop(0, axis=0)
DF_INSTALADOS_2.columns=["DESCRIPCIÓN","CANTIDAD"]


#POS PRE AGENTE Y SUSPENDIDOS
DF_ESTADO_BYS=DF_ESTADO_BYS.reset_index()
DF_ESTADO_BYS=DF_ESTADO_BYS.set_index("OC")
DF_ESTADO_BYS=DF_ESTADO_BYS.loc["All":]
DF_ESTADO_BYS=DF_ESTADO_BYS.reset_index()
DF_ESTADO_BYS=DF_ESTADO_BYS.drop(['OC', 'MODELO', '', '-', 'Baja', 'Instalado', 'All'], axis=1)
DF_ESTADO_BYS=DF_ESTADO_BYS.transpose()
DF_ESTADO_BYS=DF_ESTADO_BYS.reset_index()
DF_ESTADO_BYS=DF_ESTADO_BYS.replace('Pre Agente', "Instalados AKN preagente")
DF_ESTADO_BYS=DF_ESTADO_BYS.replace('Suspendido', "AKN suspendidos")
DF_ESTADO_BYS.columns=["DESCRIPCIÓN","CANTIDAD"]
print(DF_ESTADO_BYS)

#POS DE BAJA AKN
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="Estado terminal",fill_value=0, margins=True)
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.reset_index()
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.replace("ICT 220", "Por recuperar AKN de baja ICT")
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.replace('ICT 250', "Por recuperar AKN de baja ICT")
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.replace('APOS', "Por recuperar AKN de baja APOS")
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.groupby("MODELO").sum()
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.reset_index()
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.drop(['Pre Agente', 'Suspendido', '', '-', 'Instalado', 'All'], axis=1)
DF_ESTADO_DEBAJA.columns=["DESCRIPCIÓN","CANTIDAD"]
DF_ESTADO_DEBAJA=DF_ESTADO_DEBAJA.drop(0, axis=0)


#UNIENDO ALL Y SUBIENDO
UNIDO=pd.concat([DF_POS_INICIAL,DF_INSTALADOS_1,DF_INSTALADOS_2,DF_ASIGNADOS_CLIENTES,DF_ASIGNADOS_PERSONAL,DF_ESTADO_BYS,DF_ESTADO_DEBAJA,DF_TOTAL_SG,DF_POS_DISPONIBLE])
UNIDO=UNIDO.reset_index()
UNIDO=UNIDO.drop("index", axis=1)
print(UNIDO)
wsheet.update([UNIDO.columns.values.tolist()]+UNIDO.values.tolist())