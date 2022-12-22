from tkinter import *
from tkinter import filedialog
import os 

def seleccionar_carpeta():
    global ruta
    ruta = filedialog.askdirectory()
    ruta = str(ruta)
    print(ruta)

    if ruta:
        notif.config(fg="green", text="Carpeta Seleccionada")
    else:
        notif.config(fg="red", text="Carpeta No Seleccionada")

def actualizar():
    try:
        #TRABAJO EXCEL ARTICULOS
        from xlsx2csv import Xlsx2csv
        from io import StringIO
        import pandas as pd
        import time
        import os
        start_time = time.time()
        #Lectura de archivos
        
        archivos=os.listdir(ruta)
        print(archivos)

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
                path=ruta+"/"+a
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

        #Imprimimos tiempo
        tiempo=round((time.time() - start_time),2)
        texto="Proceso completado, tomó "+str(tiempo)+" segundos"
        notif.config(fg="green", text=texto)

    except Exception:
        if "ruta" in globals():
            notif.config(fg="red", text="Error en el proceso")
        else:
            notif.config(fg="red", text="No ha seleccionado una carpeta")


def resumen():
    try:
        #TRABAJO EXCEL ARTICULOS
        from xlsx2csv import Xlsx2csv
        from io import StringIO
        import pandas as pd
        import time
        start_time = time.time()

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
        DF_POS_INICIAL=DF_POS_INICIAL.drop(["MODELO",'-',"Despachado","Disponible","Asignado",'Bloqueado', 'De baja', 'En mantenimiento', 'Malogrado', 'Por Ubicar'], axis=1)
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
        DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.set_index('OC')
        DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.loc["All":]
        DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.drop(['MODELO'],axis=1 )
        DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.transpose()
        DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.reset_index()
        DF_ASIGNADOS_CLIENTES.columns=["DESCRIPCIÓN","CANTIDAD"]
        DF_ASIGNADOS_CLIENTES=DF_ASIGNADOS_CLIENTES.replace('NUMERO SERIE', "Asignados a Clientes")

        #POS Asignado a Personal Activo y Cesado
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="tipo DNI",fill_value=0, margins=True)
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.reset_index()
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.set_index("OC")
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.loc["All":]
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.transpose()
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.loc["Activo":"Cesado"]
        DF_ASIGNADOS_PERSONAL=DF_ASIGNADOS_PERSONAL.reset_index()
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
        wsheet.update([UNIDO.columns.values.tolist()]+UNIDO.values.tolist())

        #Imprimimos tiempo
        tiempo=round((time.time() - start_time),2)
        texto="Proceso completado, tomó "+str(tiempo)+" segundos"
        notif.config(fg="green", text=texto)

    except Exception:
        if "ruta" in globals():
            notif.config(fg="red", text="Error en el proceso")
        else:
            notif.config(fg="red", text="No ha seleccionado una carpeta")


###############
# Pantalla Principal
master = Tk()
master.title("Inteligencia Comercial")
master.geometry("370x300")

# Etiquetas
Label(master, text="Proceso Automático Logística", fg="black", font=("Calibri", 18,"bold")).grid(padx=40,row=0,column=1,pady=20)


notif = Label(master, font=("Calibri", 14,"bold"))
notif.grid(sticky=N, pady=20, row=12, column=1)
notif.config(fg="green", text="Inicio")

# Botones

Button(master, width=20,fg="white", text="Actualizar Datos",bg="#002060", font=("Calibri", 12,"bold"), command=actualizar).grid(row=9, column=1,pady=10,padx=0)

Button(master, width=20,fg="white", text="Crear Resumen",bg="#002060", font=("Calibri", 12,"bold"), command=resumen).grid(row=10, column=1,pady=10,padx=0)

Button(master, width=20,fg="white", text="Seleccionar Carpeta",bg="#002060", font=("Calibri", 12,"bold"), command=seleccionar_carpeta).grid(row=11, column=1,pady=10,padx=60)

master.mainloop()


