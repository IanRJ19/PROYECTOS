import tkinter
import customtkinter
from tkinter import filedialog

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("350x260")
app.title("Inteligencia Comercial")
ventana = customtkinter.CTkFrame(master=app)
ventana.pack(pady=0, padx=0, fill="both", expand=True)


def seleccionar_carpeta():
    global ruta
    ruta = filedialog.askdirectory()
    ruta = str(ruta)
    print(ruta)
    if ruta:
        label_1 = customtkinter.CTkLabel(master=ventana, justify=tkinter.LEFT,text="Carpeta Seleccionada",text_font=("Calibri",14,"bold"),text_color="#007E06")
        label_1.pack(pady=12, padx=10)
    else:
        label_1 = customtkinter.CTkLabel(master=ventana, justify=tkinter.LEFT,text="Carpeta No Seleccionada",text_font=("Calibri",14,"bold"),text_color="#C00000")
        label_1.pack(pady=12, padx=10)

def script():
    try:
        import pandas as pd
        import time
        import os
        import time
        start_time = time.time()
        
        #Lectura de archivos
        archivos=os.listdir(ruta)
        df_BBVA_C = []
        df_BBVA_M = []
        df_SCOT_C_TBK_PROV = []
        df_SCOT_C_TBK_VAR = []
        df_SCOT_C_EMP_PROV = []
        df_SCOT_C_EMP_VAR = []
        df_SCOT_M_TBK_PROV = []
        df_SCOT_M_TBK_VAR = []
        df_SCOT_M_EMP_PROV = []
        df_SCOT_M_EMP_VAR = []
        
        for i in range(len(archivos)):
            a=archivos[i]
            if ("BBVA" in a):
                if ("Macro" in a):
                    print(a)
                    b=pd.read_excel(ruta+"/"+a,skiprows=4,dtype=str,sheet_name="Detalle")
                    df_BBVA_M.append(b)

                else:
                    print(a)
                    b=pd.read_excel(ruta+"/"+a,skiprows=32,dtype=str)

                    #LECTURA PARA ADICIONALES
                    d=pd.read_excel(ruta+"/"+a,skiprows=15,dtype=str)
                    
                    #CAPTANDO OPERACION
                    op1=d.iloc[0,0]
                    op2=d.iloc[6,1]
                    op=op2+op1
                    b["CÓDIGO OPERACIÓN"]=op

                    #CAPTANDO NOMBRE OZ
                    nombre=d.iloc[0,2]
                    b["OZ"]=nombre

                    #CAPTANDO FECHA
                    fecha=d.iloc[7,1][0:10]
                    b["FECHA PAGO"]=fecha

                    #ADICIONANDO
                    df_BBVA_C.append(b)
                    

            elif ("Scot" in a):
                if ("Macro" in a):
                    if ("TBK" in a):
                        if ("Varios" in a):
                            b=pd.read_excel(ruta+"/"+a,skiprows=6,dtype=str)
                            df_SCOT_M_TBK_VAR.append(b)

                        else:# Prov
                            b=pd.read_excel(ruta+"/"+a,skiprows=6,dtype=str)
                            df_SCOT_M_TBK_PROV.append(b) 
                            fecha_SCOT_M_Prov_TBK=a
                    else:# EMP
                        print(a)
                        if ("Varios" in a):
                            b=pd.read_excel(ruta+"/"+a,skiprows=7,dtype=str)
                            df_SCOT_M_EMP_VAR.append(b)

                        else:# Prov
                            b=pd.read_excel(ruta+"/"+a,skiprows=6,dtype=str)
                            df_SCOT_M_EMP_PROV.append(b)

                else: #CONSTANCIAS  
                    if ("Telebanking" in a):
                        if ("Varios" in a):
                            b=pd.read_excel(ruta+"/"+a,skiprows=19,nrows=78,dtype=str)
                            
                            ##LECTURA PARA ADICIONALES SCOT Telebanking
                            d=pd.read_excel(ruta+"/"+a,skiprows=0,dtype=str)

                            #CAPTANDO NOMBRE OZ
                            nombre=d.iloc[7,1]
                            b["OZ"]=nombre

                            #CAPTANDO OPERACIÓN
                            op=d.iloc[3,0][21:30]
                            b["CÓDIGO OPERACIÓN"]=op
                            
                            #CAPTANDO FECHA
                            fecha=d.iloc[8,5][0:10]
                            b["FECHA PAGO"]=fecha
                            
                            #ADICIONANDO
                            df_SCOT_C_TBK_VAR.append(b)
                        else:# Prov
                            b=pd.read_excel(ruta+"/"+a,skiprows=19,nrows=78,dtype=str)
                            
                            #LECTURA PARA ADICIONALES SCOT Telebanking
                            d=pd.read_excel(ruta+"/"+a,skiprows=0,dtype=str)

                            #CAPTANDO NOMBRE OZ
                            nombre=d.iloc[7,1]
                            b["OZ"]=nombre
                            
                            #CAPTANDO OPERACIÓN
                            op=d.iloc[3,0][21:30]
                            b["CÓDIGO OPERACIÓN"]=op

                            #CAPTANDO FECHA
                            fecha=d.iloc[8,5][0:10]
                            b["FECHA PAGO"]=fecha
                            
                            #ADICIONANDO
                            df_SCOT_C_TBK_PROV.append(b)
                    else:# EMP
                        print(a)
                        if ("Varios" in a):
                            b=pd.read_table(ruta+"/"+a,skiprows=0,dtype=str,on_bad_lines='skip',encoding= 'unicode_escape')

                            #CAPTANDO NOMBRE OZ
                            nombre=b.iloc[3,0][9:40]
                            b["OZ"]=nombre

                            #CAPTANDO OPERACIÓN
                            op=b.iloc[0,0][72:84]
                            b["CÓDIGO OPERACIÓN"]=op

                            #CAPTANDO FECHA
                            fecha=b.iloc[2,0][25:33]
                            b["FECHA PAGO"]=fecha
                            #%m/%d/%y
                            #%m/%d/%Y
                            b["FECHA PAGO"]=pd.to_datetime(b["FECHA PAGO"]).dt.strftime('%m/%d/%Y')


                            #ADICIONANDO
                            df_SCOT_C_EMP_VAR.append(b)
                        else:# Prov
                            b=pd.read_table(ruta+"/"+a,skiprows=0,dtype=str,on_bad_lines='skip',encoding= 'unicode_escape')

                            #CAPTANDO NOMBRE OZ
                            nombre=b.iloc[3,0][9:40]
                            b["OZ"]=nombre
                            
                            #CAPTANDO OPERACIÓN
                            op=b.iloc[0,0][72:84]
                            b["CÓDIGO OPERACIÓN"]=op
                            
                            #CAPTANDO FECHA
                            fecha=b.iloc[2,0][25:33]
                            b["FECHA PAGO"]=fecha
                            b["FECHA PAGO"]=pd.to_datetime(b["FECHA PAGO"]).dt.strftime('%m/%d/%Y')

                            #ADICIONANDO
                            df_SCOT_C_EMP_PROV.append(b)


        ############################################################################################
        #BBVA CONSTANCIA 
        if df_BBVA_C:
            BBVA_C=BBVA_C=pd.concat(df_BBVA_C)
            BBVA_C=BBVA_C.rename(columns={'Doc.Identidad': 'DNI',"Importe":"IMPORTE","Situación":"ESTADO","Titular(Archivo)":"BENEFICIARIO"})
            BBVA_C["MONEDA"]="S/"
            BBVA_C["TIPO DE DOCUMENTO"]=BBVA_C["DNI"].str.slice(start=0, stop=2)
            BBVA_C["DNI"]=BBVA_C["DNI"].str.slice(start=3, stop=15)
            BBVA_C=BBVA_C[["DNI","BENEFICIARIO","MONEDA","IMPORTE","ESTADO","TIPO DE DOCUMENTO","OZ","CÓDIGO OPERACIÓN","FECHA PAGO"]]
            BBVA_C["BANCO"]="BBVA"

            #BBVA MACRO 
            BBVA_M=pd.concat(df_BBVA_M)
            BBVA_M=BBVA_M.rename(columns={'DOI Número': 'DNI',"Nombre de Beneficiario":"BENEFICIARIO","Importe Abonar":"IMPORTE","Indicador Aviso":"ESTADO","Referencia":"REF"})
            BBVA_M = BBVA_M[["DNI", "BENEFICIARIO","IMPORTE","REF"]]
            BBVA_M=BBVA_M[BBVA_M["DNI"].notnull()]
        else:
            BBVA_M=pd.DataFrame()
            BBVA_C=pd.DataFrame()

        ############################################################################################
        if df_SCOT_C_TBK_VAR:
            #SCOT CONSTANCIA TBK VARIOS
            SCOT_C_TBK_VAR=pd.concat(df_SCOT_C_TBK_VAR)
            SCOT_C_TBK_VAR=SCOT_C_TBK_VAR.rename(columns={'Documento': 'DNI',"Moneda":"MONEDA","Importe":"IMPORTE","Estado":"ESTADO","Beneficiario":"BENEFICIARIO"})
            SCOT_C_TBK_VAR=SCOT_C_TBK_VAR.drop(['Unnamed: 7','Unnamed: 8'], axis=1)
            SCOT_C_TBK_VAR["TIPO DE DOCUMENTO"]="L"
            SCOT_C_TBK_VAR=SCOT_C_TBK_VAR[["DNI","BENEFICIARIO","MONEDA","IMPORTE","ESTADO","TIPO DE DOCUMENTO","OZ","CÓDIGO OPERACIÓN","FECHA PAGO"]]
            SCOT_C_TBK_VAR["BANCO"]="SCOTIABANK"


            #SCOT MACRO TBK VARIOS
            SCOT_M_TBK_VAR = pd.concat(df_SCOT_M_TBK_VAR)
            SCOT_M_TBK_VAR = SCOT_M_TBK_VAR.loc[:, ['DOCUMENTO DE IDENTIDAD', 'NOMBRE DEL EMPLEADO', 'MONTO A PAGAR', 'REFERENCIA']]
            SCOT_M_TBK_VAR = SCOT_M_TBK_VAR.loc[SCOT_M_TBK_VAR['DOCUMENTO DE IDENTIDAD'].notnull()]
            SCOT_M_TBK_VAR.columns = ['DOC','NOMBRE','IMPORTE','REF']
            SCOT_M_TBK_VAR['DOC'] = SCOT_M_TBK_VAR['DOC'].astype('str')
            SCOT_M_TBK_VAR['T_DOC'] = 'DNI'
        else:
            SCOT_C_TBK_VAR=pd.DataFrame()
            SCOT_M_TBK_VAR=pd.DataFrame()

        ###########################################################################################
        if df_SCOT_C_TBK_PROV:
            #SCOT CONSTANCIA TBK PROV
            SCOT_C_TBK_PROV=pd.concat(df_SCOT_C_TBK_PROV)
            SCOT_C_TBK_PROV=SCOT_C_TBK_PROV.rename(columns={'Documento/Nro Fact': 'DNI',"Moneda":"MONEDA","Monto":"IMPORTE","Estado":"ESTADO","Beneficiario/F. Fact - Vencimiento ":"BENEFICIARIO"})
            SCOT_C_TBK_PROV=SCOT_C_TBK_PROV.drop(['Unnamed: 7','Unnamed: 8'], axis=1)

            SCOT_C_TBK_PROV["TIPO DE DOCUMENTO"]="R"
            SCOT_C_TBK_PROV=SCOT_C_TBK_PROV[["DNI","BENEFICIARIO","MONEDA","IMPORTE","ESTADO","TIPO DE DOCUMENTO","OZ","CÓDIGO OPERACIÓN","FECHA PAGO"]]

            SCOT_C_TBK_PROV = SCOT_C_TBK_PROV[SCOT_C_TBK_PROV["ESTADO"].notnull()]
            SCOT_C_TBK_PROV=SCOT_C_TBK_PROV[SCOT_C_TBK_PROV["ESTADO"].str.contains("A|E|I|O|U", case=True, regex=True)]


            SCOT_C_TBK_PROV["BANCO"]="SCOTIABANK"
            #SCOT MACRO TBK PROV
            SCOT_M_TBK_PROV = pd.concat(df_SCOT_M_TBK_PROV)
            SCOT_M_TBK_PROV = SCOT_M_TBK_PROV.loc[:, ['RUC / \nCOD. VENDOR', 'RAZON SOCIAL', 'MONTO A PAGAR', 'NRO FACTURA']]
            SCOT_M_TBK_PROV.columns = ['DOC','NOMBRE','IMPORTE','REF']
            SCOT_M_TBK_PROV['T_DOC'] = 'DNI'

            #EXTRAYENDO FECHA
            fecha_SCOT_M_Prov_TBK=fecha_SCOT_M_Prov_TBK.replace(" ", "/")
            fecha_SCOT_M_Prov_TBK=fecha_SCOT_M_Prov_TBK.rsplit("_",1)[1]
            fecha_SCOT_M_Prov_TBK=fecha_SCOT_M_Prov_TBK.rsplit('.', 1)[0]
            SCOT_M_TBK_PROV["FECHA PAGO"]=fecha_SCOT_M_Prov_TBK
        else:
            SCOT_M_TBK_PROV=pd.DataFrame()
            SCOT_C_TBK_PROV=pd.DataFrame()

        ###########################################################################################
        if df_SCOT_C_EMP_PROV:
            #SCOT CONSTANCIA EMP PROV
            SCOT_C_EMP_PROV= pd.concat(df_SCOT_C_EMP_PROV)
            SCOT_C_EMP_PROV=SCOT_C_EMP_PROV[(SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[40:42]=="S/") & (SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[67:68]=='.')]

            SCOT_C_EMP_PROV = SCOT_C_EMP_PROV[SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[0:4] != ' COM']

            SCOT_C_EMP_PROV = pd.DataFrame({'BENEFICIARIO' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[1:26],'DNI' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[27:38],'IMPORTE' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[48:58],'ESTADO' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[99:103],"OZ":SCOT_C_EMP_PROV["OZ"],"TIPO DE DOCUMENTO":"R","CÓDIGO OPERACIÓN":SCOT_C_EMP_PROV["CÓDIGO OPERACIÓN"],"FECHA PAGO":SCOT_C_EMP_PROV["FECHA PAGO"]})

            SCOT_C_EMP_PROV['IMPORTE']= SCOT_C_EMP_PROV['IMPORTE'].str.replace(",", "")
            SCOT_C_EMP_PROV["BANCO"]="SCOTIABANK"

            #SCOT MACRO EMP PROV
            SCOT_M_EMP_PROV = pd.concat(df_SCOT_M_EMP_PROV)
            SCOT_M_EMP_PROV = SCOT_M_EMP_PROV.loc[:, ['RUC DEL\nPROVEEDOR', 'NOMBRE DEL\nPROVEEDOR','IMPORTE', 'REFERENCIA O\nFACTURA']]
            SCOT_M_EMP_PROV.columns = ['DOC','NOMBRE','IMPORTE','REF']
            SCOT_M_EMP_PROV['T_DOC'] = 'RUC'
        else:
            SCOT_M_EMP_PROV=pd.DataFrame()
            SCOT_C_EMP_PROV=pd.DataFrame()


        ###########################################################################################
        if df_SCOT_C_EMP_VAR:
            # SCOT CONSTANCIA EMP VAR
            # LEEMOS Y ACOMODAMOS EL NOMBRE DEL TXT RECIBIDO
            SCOT_C_EMP_VAR= pd.concat(df_SCOT_C_EMP_VAR)
            SCOT_C_EMP_VAR=SCOT_C_EMP_VAR[(SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[40:42]=="S/") & (SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[67:68]=='.')]

            SCOT_C_EMP_VAR = SCOT_C_EMP_VAR[SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[0:4] != ' COM']

            SCOT_C_EMP_VAR = pd.DataFrame({'BENEFICIARIO' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[1:26],'DNI' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[27:38],'IMPORTE' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[48:58],'ESTADO' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[99:103],"OZ":SCOT_C_EMP_VAR["OZ"],"TIPO DE DOCUMENTO":"L","CÓDIGO OPERACIÓN":SCOT_C_EMP_VAR["CÓDIGO OPERACIÓN"],"FECHA PAGO":SCOT_C_EMP_VAR["FECHA PAGO"]})

            SCOT_C_EMP_VAR['IMPORTE']= SCOT_C_EMP_VAR['IMPORTE'].str.replace(",", "")
            SCOT_C_EMP_VAR["BANCO"]="SCOTIABANK"

            #SCOT MACRO EMP VAR
            SCOT_M_EMP_VAR = pd.concat(df_SCOT_M_EMP_VAR)
            SCOT_M_EMP_VAR = SCOT_M_EMP_VAR.loc[:, ['TIPO DE\nDOCUMENTO', 'DOCUMENTO IDENTIDAD',    'NOMBRE\nBENEFICIARIO', 'IMPORTE\n', 'REFERENCIA O\nFACTURA']]
            SCOT_M_EMP_VAR.columns = ['T_DOC','DOC','NOMBRE','IMPORTE','REF']
        else:
            SCOT_M_EMP_VAR=pd.DataFrame()
            SCOT_C_EMP_VAR=pd.DataFrame()



        ###########################################################################################

        #UNIENDO EN UN SOLO DF
        macros_unidos = SCOT_M_EMP_PROV.append(SCOT_M_EMP_VAR)
        macros_unidos = macros_unidos.append(SCOT_M_TBK_PROV)
        macros_unidos = macros_unidos.append(SCOT_M_TBK_VAR)

        #DANDOLE FORMATO

        macros_unidos=macros_unidos.rename(columns={'DOC': 'DNI',"NOMBRE":"BENEFICIARIO"})
        macros_unidos=macros_unidos[macros_unidos["DNI"].notnull()]
        macros_unidos=macros_unidos[macros_unidos["BENEFICIARIO"].notnull()]
        macros_unidos = macros_unidos[["DNI", "BENEFICIARIO","IMPORTE","REF"]]
        macros_unidos = macros_unidos.append(BBVA_M)
        macros_unidos=macros_unidos[macros_unidos["IMPORTE"].notnull()]
        macros_unidos=macros_unidos.reset_index()


        #UNIENDO EN UN SOLO DF
        frames = [SCOT_C_TBK_VAR, SCOT_C_TBK_PROV,SCOT_C_EMP_PROV,SCOT_C_EMP_VAR,BBVA_C]
        constancias_unidas = pd.concat(frames)
        constancias_unidas["DNI"]=constancias_unidas["DNI"].str.replace(" ", "")
        constancias_unidas=constancias_unidas.reset_index()


        constancias_unidas['IMPORTE'] = constancias_unidas['IMPORTE'].astype('float64')
        constancias_unidas['IMPORTE'] = constancias_unidas['IMPORTE'].round(2)
        constancias_unidas['IMPORTE'] = constancias_unidas['IMPORTE'].astype('str')
        macros_unidos['IMPORTE'] = macros_unidos['IMPORTE'].astype('float64')
        macros_unidos['IMPORTE'] = macros_unidos['IMPORTE'].round(2)
        macros_unidos['IMPORTE'] = macros_unidos['IMPORTE'].astype('str')



        import numpy as np
        macros_unidos["FECHA"] = np.where(macros_unidos["REF"].map(len) >10, macros_unidos["REF"].str.slice(start=9, stop=19), macros_unidos["REF"].str.slice(start=0, stop=10))
        macros_unidos["REF"] = np.where(macros_unidos["REF"].map(len) >10, macros_unidos["REF"].str.slice(start=0, stop=8), 0)
        macros_unidos["FECHA"]=macros_unidos["FECHA"].str.replace("-", "")

        #CREANDO LAS KEY
        constancias_unidas['KEY'] = constancias_unidas['DNI'] + constancias_unidas['IMPORTE']
        macros_unidos['KEY'] = macros_unidos['DNI'] + macros_unidos['IMPORTE']

        ###########################################################################################

        #HACIENDO EL EMPAREJAMIENTO
        cruce_info = pd.merge(macros_unidos,constancias_unidas,how='inner',on='KEY')
        toda_info = pd.merge(macros_unidos,constancias_unidas,how='outer',on='KEY')

        #ARREGLANDO FORMATO


        macros_unidos=macros_unidos.drop(['index',"KEY"], axis=1)
        constancias_unidas=constancias_unidas.drop(['index',"KEY"], axis=1)
        cruce_info=cruce_info.drop(['index_x',"KEY",'index_y',"BENEFICIARIO_y","IMPORTE_y","DNI_y"], axis=1)
        toda_info=toda_info.drop(['index_x',"KEY",'index_y',"BENEFICIARIO_y","IMPORTE_y","DNI_y"], axis=1)
        cruce_info=cruce_info.rename(columns={"DNI_x":"DNI / RUC","BENEFICIARIO_x":"AGENTE","IMPORTE_x":"IMPORTE EN SOLES","OZ":"OPERADOR ZONAL","FECHA":"PERIODO DE FACTURACIÓN","TIPO DE DOCUMENTO":"COMPROBANTE","REF":"ID AGENTE"})
        toda_info=toda_info.rename(columns={"DNI_x":"DNI / RUC","BENEFICIARIO_x":"AGENTE","IMPORTE_x":"IMPORTE EN SOLES","OZ":"OPERADOR ZONAL","FECHA":"PERIODO DE FACTURACIÓN","TIPO DE DOCUMENTO":"COMPROBANTE","REF":"ID AGENTE"})

        #AÑADIENDO CAMBIOS A CONSTANCIA CONSOLIDADA
        constancias_unidas=constancias_unidas.rename(columns={"DNI":"DNI / RUC","BENEFICIARIO":"AGENTE","IMPORTE":"IMPORTE EN SOLES","TIPO DE DOCUMENTO":"COMPROBANTE","OZ":"OPERADOR ZONAL"})
        macros_unidos=macros_unidos.rename(columns={"DNI":"DNI / RUC","BENEFICIARIO":"AGENTE","IMPORTE":"IMPORTE EN SOLES","REF":"ID AGENTE","FECHA":"PERIODO DE FACTURACIÓN"})


        #ORDENANDO POSICIÓN DE COLUMNAS
        constancias_unidas=constancias_unidas.reindex(columns=["AGENTE","DNI / RUC","FECHA PAGO","OPERADOR ZONAL","BANCO","IMPORTE EN SOLES","ESTADO","COMPROBANTE","CÓDIGO OPERACIÓN"])

        macros_unidos=macros_unidos.reindex(columns=["ID AGENTE", "AGENTE","DNI / RUC","IMPORTE EN SOLES","PERIODO DE FACTURACIÓN"])
        cruce_info=cruce_info.reindex(columns=["ID AGENTE", "AGENTE","DNI / RUC","OPERADOR ZONAL","FECHA PAGO","BANCO","IMPORTE EN SOLES","ESTADO","PERIODO DE FACTURACIÓN","COMPROBANTE","CÓDIGO OPERACIÓN"])
        toda_info=toda_info.reindex(columns=["ID AGENTE", "AGENTE","DNI / RUC","OPERADOR ZONAL","FECHA PAGO","BANCO","IMPORTE EN SOLES","ESTADO","PERIODO DE FACTURACIÓN","COMPROBANTE","CÓDIGO OPERACIÓN"])

        #DANDO COLORES Y ALINEACIÓN
        propiedades= {"border": "2px solid gray", "color": "black", "font-size": "14.5px","text-align":"center",'background-color': '#F2F2F2'}
        toda_info=toda_info.style.set_properties(**propiedades)
        cruce_info=cruce_info.style.set_properties(**propiedades)
        macros_unidos=macros_unidos.style.set_properties(**propiedades)
        constancias_unidas=constancias_unidas.style.set_properties(**propiedades)

        #CONVIERTIENDO EN ARCHIVOS
        macros_unidos.to_excel(ruta+"/RESULTADOS/"+"Macro consolidado.xlsx",sheet_name='Resultados',startrow=0, startcol=0)
        constancias_unidas.to_excel(ruta+"/RESULTADOS/"+"Constancia de pago consolidado.xlsx",sheet_name='Resultados',startrow=0, startcol=0)

        with pd.ExcelWriter(ruta+"/RESULTADOS/"+"Resultados.xlsx") as writer:
            cruce_info.to_excel(writer, sheet_name="Cruce")  
            toda_info.to_excel(writer, sheet_name="Todo")  


        #Imprimimos tiempo
        tiempo=round((time.time() - start_time),2)
        texto="Proceso completado, tomó "+str(tiempo)+" segundos"
        text_var = tkinter.StringVar(value=texto)
        label_1 = customtkinter.CTkLabel(master=ventana, justify=tkinter.LEFT,textvariable=text_var,text_font=("Calibri",14,"bold"),text_color="#007E06")
        label_1.pack(pady=12, padx=10)
    except Exception:
        if "ruta" in globals():
            text_var = tkinter.StringVar(value="Error en el proceso")
            label_1 = customtkinter.CTkLabel(master=ventana, justify=tkinter.LEFT,textvariable=text_var,text_font=("Calibri",14,"bold"),text_color="#C00000")
            label_1.pack(pady=12, padx=10)
        else:
            text_var = tkinter.StringVar(value="No ha seleccionado una carpeta")
            label_1 = customtkinter.CTkLabel(master=ventana, justify=tkinter.LEFT,textvariable=text_var,text_font=("Calibri",14,"bold"),text_color="#C00000")
            label_1.pack(pady=12, padx=10)
                        
###############
# Etiquetas
label_1 = customtkinter.CTkLabel(master=ventana, justify=tkinter.LEFT,text="Consolidación de Pagos OZ",text_font=("Calibri",20,"bold"),text_color="black")#,bg_color="#002060",width=350,height=50)
label_1.pack(pady=12, padx=10)


# Botones
button_1 = customtkinter.CTkButton(master=ventana, command=script,text="Ejecutar Script",text_font=("Calibri",10,"bold"),fg_color="#002060",text_color="white",border_color="black",border_width=2)
button_1.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=ventana, command=seleccionar_carpeta,text="Seleccionar Carpeta",text_font=("Calibri",10,"bold"),fg_color="#002060",text_color="white",border_color="black",border_width=2)
button_1.pack(pady=12, padx=10)

app.mainloop()


