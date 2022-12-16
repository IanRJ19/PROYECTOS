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
df1_ASIGNADOS=Base[Base["Tipo"].isin(["RUC(Empresa)", "RUC(Entidad Financiera)"])]
df1_ASIGNADOS_DNI=Base[Base["Tipo"]=="DNI"]
df1_INSTALADOS_1=Base[(Base["Estado terminal"]=="Instalado") & (Base["ESTADO SG"].isin(["Despachado","Asignado"]))]
df1_ESTADOTERM=Base.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="Estado terminal",fill_value=0, margins=True)
df1_ESTADOTERM_2=Base[Base["MODELO"].isin(["ICT 220", "ICT 250","APOS"])]


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
df1_ASIGNADOS=df1_ASIGNADOS.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",fill_value=0, margins=True)
df1_ASIGNADOS=df1_ASIGNADOS.reset_index()
df1_ASIGNADOS=df1_ASIGNADOS[9:]
df1_ASIGNADOS=df1_ASIGNADOS.drop(['OC', 'MODELO'],axis=1 )
df1_ASIGNADOS=df1_ASIGNADOS.transpose()
df1_ASIGNADOS=df1_ASIGNADOS.reset_index()
df1_ASIGNADOS.columns=["DESCRIPCIÓN","CANTIDAD"]
df1_ASIGNADOS=df1_ASIGNADOS.replace('NUMERO SERIE', "Asignados a Clientes")


#POS Asignado a Personal Activo y Cesado
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="tipo DNI",fill_value=0, margins=True)
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI.reset_index()
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI[13:]
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI.transpose()
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI.reset_index()
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI[3:5]
df1_ASIGNADOS_DNI.columns=["DESCRIPCIÓN","CANTIDAD"]
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI.replace('Activo', "Asignados al Personal")
df1_ASIGNADOS_DNI=df1_ASIGNADOS_DNI.replace('Cesado', "Asignados al Personal Cesado")



#Instalados AKN (1) y (+2)
df1_INSTALADOS_1=df1_INSTALADOS_1.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="x",fill_value=0, margins=True)
df1_INSTALADOS_2=df1_INSTALADOS_1
df1_INSTALADOS_1=df1_INSTALADOS_1.reset_index()
df1_INSTALADOS_1=df1_INSTALADOS_1.replace('ICT 220', "Instalados AKN (1) ICT")
df1_INSTALADOS_1=df1_INSTALADOS_1.replace('ICT 250', "Instalados AKN (1) ICT")
df1_INSTALADOS_1=df1_INSTALADOS_1.replace('APOS', "Instalados AKN (1) APOS")
df1_INSTALADOS_1=df1_INSTALADOS_1.groupby("MODELO").sum()
df1_INSTALADOS_1=df1_INSTALADOS_1.reset_index()
df1_INSTALADOS_1=df1_INSTALADOS_1.drop(0, axis=0)
df1_INSTALADOS_1=df1_INSTALADOS_1.drop([2,3,"All"], axis=1)
df1_INSTALADOS_1.columns=["DESCRIPCIÓN","CANTIDAD"]


df1_INSTALADOS_2["SUMA"]=df1_INSTALADOS_2[2]+df1_INSTALADOS_2[3]
df1_INSTALADOS_2=df1_INSTALADOS_2.reset_index()
df1_INSTALADOS_2=df1_INSTALADOS_2.drop(["All",1,2,3], axis=1)
df1_INSTALADOS_2=df1_INSTALADOS_2.replace('ICT 250', "Instalados AKN (+1)")
df1_INSTALADOS_2=df1_INSTALADOS_2.replace('ICT 220', "Instalados AKN (+1)")
df1_INSTALADOS_2=df1_INSTALADOS_2.replace('APOS', "Instalados AKN (+1)")
df1_INSTALADOS_2=df1_INSTALADOS_2.groupby("MODELO").sum()
df1_INSTALADOS_2=df1_INSTALADOS_2.reset_index()
df1_INSTALADOS_2=df1_INSTALADOS_2.drop(0, axis=0)
df1_INSTALADOS_2.columns=["DESCRIPCIÓN","CANTIDAD"]


#ESTADO INSTALADOS AKN Y SUSPENDIDOS
df1_ESTADOTERM=df1_ESTADOTERM.reset_index()
df1_ESTADOTERM=df1_ESTADOTERM.set_index("OC")
df1_ESTADOTERM_PRE=df1_ESTADOTERM.loc["All":]
df1_ESTADOTERM_PRE=df1_ESTADOTERM_PRE.reset_index()
df1_ESTADOTERM_PRE=df1_ESTADOTERM_PRE.drop(['OC', 'MODELO', '', '-', 'Baja', 'Instalado', 'All'], axis=1)
df1_ESTADOTERM_PRE=df1_ESTADOTERM_PRE.transpose()
df1_ESTADOTERM_PRE=df1_ESTADOTERM_PRE.reset_index()
df1_ESTADOTERM_PRE=df1_ESTADOTERM_PRE.replace('Pre Agente', "Instalados AKN preagente")
df1_ESTADOTERM_PRE=df1_ESTADOTERM_PRE.replace('Suspendido', "AKN suspendidos")
df1_ESTADOTERM_PRE.columns=["DESCRIPCIÓN","CANTIDAD"]
print(df1_ESTADOTERM_PRE)

#POR RECUPERAR AKN
df1_ESTADOTERM_2=df1_ESTADOTERM_2.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="Estado terminal",fill_value=0, margins=True)
df1_ESTADOTERM_2=df1_ESTADOTERM_2.reset_index()
df1_ESTADOTERM_2=df1_ESTADOTERM_2.replace("ICT 220", "Por recuperar AKN de baja ICT")
df1_ESTADOTERM_2=df1_ESTADOTERM_2.replace('ICT 250', "Por recuperar AKN de baja ICT")
df1_ESTADOTERM_2=df1_ESTADOTERM_2.replace('APOS', "Por recuperar AKN de baja APOS")
df1_ESTADOTERM_2=df1_ESTADOTERM_2.groupby("MODELO").sum()
df1_ESTADOTERM_2=df1_ESTADOTERM_2.reset_index()
df1_ESTADOTERM_2=df1_ESTADOTERM_2.drop(['Pre Agente', 'Suspendido', '', '-', 'Instalado', 'All'], axis=1)
df1_ESTADOTERM_2.columns=["DESCRIPCIÓN","CANTIDAD"]
df1_ESTADOTERM_2=df1_ESTADOTERM_2.drop(0, axis=0)


#UNIENDO ALL Y SUBIENDO
total=pd.concat([df1_POS_INICIAL,df1_INSTALADOS_1,df1_INSTALADOS_2,df1_ASIGNADOS,df1_ASIGNADOS_DNI,df1_ESTADOTERM_PRE,df1_ESTADOTERM_2,df1_TOTAL_SG,df1_POS_DISP])
total=total.reset_index()
total=total.drop("index", axis=1)
print(total)
#total=total.reindex([1,2,3,4])

wsheet.update([total.columns.values.tolist()]+total.values.tolist())