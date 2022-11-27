from tkinter import *
from tkinter import filedialog
import os
import time

def seleccionar_carpeta():
    global ruta
    ruta = filedialog.askdirectory()
    ruta = str(ruta)
    print(ruta)

def script():
    semana_inicio=e.get()
    semana_fin=f.get()
    fecha_inicio=g.get()
    fecha_fin=h.get()
    try:
        import pandas as pd
        import time
        import os
        import time
        start_time = time.time()

        #Lectura de archivos
        archivos=os.listdir(ruta)
        df_reporte = []

        for i in range(len(archivos)):
            a=archivos[i]
            if ("ReporteAzteca" in a):
                print(a)
                b=pd.read_excel(ruta+"/"+a,dtype=str,sheet_name="acumulado")
                df_reporte.append(b)
            else:
                print("No es un reporte "+a)

        unido=pd.concat(df_reporte)
        unido=unido.drop_duplicates(subset=unido.columns)
        unido.to_excel(ruta+"/"+"Reportes_UNIDOS.xlsx")

        #INICIAMOS EJECUCIÓN DE FORMATEADO
        tabla=unido

        #Ordenamos por Fecha y Eliminamos DNI duplicados
        tabla["Fecha"]=pd.to_datetime(tabla["Fecha"])

        #Filtramos la fecha
        tabla=tabla[(tabla['Fecha'] >= semana_inicio) & (tabla['Fecha'] <= semana_fin)]
        tabla=tabla.sort_values(["Fecha","Hora"], ascending=True)
        tabla=tabla.drop_duplicates(subset="DNI")

        tabla=tabla[(tabla['Fecha'] >= fecha_inicio) & (tabla['Fecha'] <= fecha_fin)]
        tabla=tabla.sort_values(["Fecha","Hora"], ascending=True)
        tabla=tabla.drop_duplicates(subset="DNI")


        #Cortamos la fecha
        tabla["Fecha"] =tabla["Fecha"].astype("str")
        tabla["Fecha"] = tabla["Fecha"].str.slice(start=0, stop=10)

        #Creando F1
        tabla["F1"]=tabla["Terminal"]+tabla["Fecha"]

        #Acá crearemos los resultados y agruparemos los comunes de F1
        #No ponemos estado, porque queremos sumar el conjunto final
        final=pd.DataFrame()
        final["Min Diario"]=tabla.groupby(['F1',"Zona","Provincia","Distrito","Departamento","Agencia","Empresa"])['F1'].count()


        #Ordenamos de mayor a menor los Min Diario
        final=final.sort_values(["Min Diario","F1"], ascending=False)

        #Es necesario resetear el indice porque no dejará cortar el texto
        final=final.reset_index()
        final["Fecha"]=final["F1"].str.slice(start=6, stop=16)


        #Cortamos el texto que ya no es necesario
        final["F1"] =final["F1"].astype("str")
        final["F1"]=final["F1"].str.slice(start=0, stop=6)

        #Pivoteamos
        final = pd.pivot_table(final, index=['F1', "Departamento","Provincia","Distrito",'Zona',"Agencia","Empresa"],columns=['Fecha'], aggfunc= 'sum', margins = True, margins_name='Total')

        #Eliminamos Encabezados que sobran
        final=final.droplevel(level=0, axis=1)
        final=final.reset_index()

        #Renombramos
        final=final.rename(columns={'F1': 'Terminal',"Zona":"Región"})
        #Ordenamos
        final=final.sort_values("Total", ascending=False)

        final=final[final["Terminal"]!="Total"]

        #Ya no es necesario porque se acomodó el ordén antes del pivot
        #final = final.reindex(columns=['Terminal', 'Departamento','Provincia', 'Distrito', 'Región',  'Agencia', 'Empresa', '2022-10-29', '2022-10-30', '2022-10-31', '2022-11-01', '2022-11-02', '2022-11-03', '2022-11-04','Total'])

        #Eliminamos duplicados por region
        final1=final.drop_duplicates(subset="Región")

        ##############################################################################################
        from xlsx2csv import Xlsx2csv
        from io import StringIO
        import pandas as pd

        path=ruta+"/"+"ReporteDiarioAgentes.xlsx"
        def read_excel(path: str, sheet_name: str) -> pd.DataFrame:
            buffer = StringIO()
            Xlsx2csv(path, outputencoding="utf-8", sheet_name=sheet_name).convert(buffer)
            buffer.seek(0)
            agentes = pd.read_csv(buffer)
            return agentes

        agentes=read_excel(path,"Hoja 1")
        agentes=agentes.reset_index()
        agentes["KEY"]=agentes['Código Tienda']
        agentes["KEY"]=agentes["KEY"].fillna(0)
        agentes["KEY"]=agentes["KEY"].round(0)
        agentes["KEY"]=agentes["KEY"].astype("int")
        agentes["KEY"]=agentes["KEY"].astype("str")
        
        final['KEY'] = final['Terminal']      
        final1['KEY'] = final1['Terminal']
        report_1 = pd.merge(agentes,final,how='inner',on='KEY')
        report_1=report_1.rename(columns={'Terminal':"ID","Nombre Comercio":"AGENTE","Departamento":"DEPARTAMENTO","Provincia":"PROVINCIA","Distrito":"DISTRITO","Región":"REGIÓN","Total":"TOTAL"})
        report_1=report_1.reset_index()
        ad1=report_1["AGENTE"]
        report_1=report_1.drop(["index", "level_0","KEY","Agencia","Empresa","Código Tienda","AGENTE"], axis=1)
        report_1.insert(1,"AGENTE",ad1)
        report_1=report_1.sort_values(["TOTAL"], ascending=[False])

        report_2 = pd.merge(agentes,final1,how='inner',on='KEY')
        report_2=report_2.rename(columns={'Terminal':"ID","Nombre Comercio":"AGENTE","Departamento":"DEPARTAMENTO","Provincia":"PROVINCIA","Distrito":"DISTRITO","Región":"REGIÓN","Total":"TOTAL"})
        report_2=report_2.reset_index()
        ad2=report_2["AGENTE"]
        report_2=report_2.drop(["index", "level_0","KEY","Agencia","Empresa","Código Tienda","AGENTE"], axis=1)
        report_2.insert(1,"AGENTE",ad2)
        report_2=report_2.sort_values(["TOTAL"], ascending=[False])

        #Cambiamos Indice
        report_1 = report_1.set_index("ID")
        report_2 = report_2.set_index("ID")

        #Alineamos
        propiedades= {"border": "2px solid gray", "color": "black", "font-size": "14.5px","text-align":"center",'background-color': '#F2F2F2'}
        report_1=report_1.style.set_properties(**propiedades)
        report_2=report_2.style.set_properties(**propiedades)


        with pd.ExcelWriter(ruta+"/"+"Resultados.xlsx") as writer:
            report_1.to_excel(writer, sheet_name="Resultados")
            report_2.to_excel(writer, sheet_name="Ganadores")

        

        ###########################################################################

        #Imprimimos tiempo
        tiempo=round((time.time() - start_time),2)
        notif.config(fg="green", text="Proceso completado, tomó "+str(tiempo)+" segundos")

    except Exception:
        if "ruta" in globals():
            notif.config(fg="red", text="Error en el proceso")
        else:
            notif.config(fg="red", text="No ha seleccionado una carpeta")

    
###############
# Pantalla Principal
master = Tk()
master.title("Inteligencia Comercial")
master.geometry("400x300")

# Etiquetas
Label(master, text="Captación Agentes ACK", fg="#002060", font=("Calibri", 15)).grid(padx=10,row=0,column=2)
Label(master, text="Introduce las fechas", fg="red", font=("Calibri", 15)).grid(padx=10,row=1,column=2)

Label(master, text="En formato aaaa-mm-dd", fg="#000000", font=("Calibri", 10)).grid(padx=10,row=3,column=2)

Label(master, text="Inicio Evento").grid(sticky=W, padx=1,row=5, column=1)
Label(master, text="Fin Evento").grid( sticky=W,padx=1,row=6, column=1)

Label(master, text="Inicio Captación").grid(sticky=W, padx=1,row=7, column=1)
Label(master, text="Fin Captación").grid( sticky=W,pady=1,row=8, column=1)

notif = Label(master, font=("Calibri", 12))
notif.grid(sticky=N, pady=1, row=11, column=2)


# Variables y añadimos el por DEFECTO

e=StringVar(value='2022-10-17')
f=StringVar(value='2022-11-04')
g=StringVar(value="2022-10-29")
h=StringVar(value="2022-11-04")

# Entradas
#Entry(master, width=50, textvariable=data).grid(padx=2,row=2)
Entry(master, width=40,textvariable=e).grid(padx=5, row=5, column=2)
Entry(master, width=40,textvariable=f).grid(padx=5, row=6, column=2)
Entry(master, width=40,textvariable=g).grid(padx=5, row=7, column=2)
Entry(master, width=40,textvariable=h).grid(padx=5, row=8, column=2)

# Botones

Button(master, width=20, text="Ejecutar Script", font=("Calibri", 12), command=script).grid(row=9, column=2,pady=10)
Button(master, width=20, text="Seleccionar carpeta", font=("Calibri", 12), command=seleccionar_carpeta).grid(row=10, column=2)

master.mainloop()



