import pandas as pd


if df_SCOT_C_EMP_PROV:
    #SCOT CONSTANCIA EMP PROV
    SCOT_C_EMP_PROV= pd.concat(df_SCOT_C_EMP_PROV)
    SCOT_C_EMP_PROV=SCOT_C_EMP_PROV[(SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[40:42]=="S/") & (SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[67:68]=='.')]

    SCOT_C_EMP_PROV = SCOT_C_EMP_PROV[SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[0:4] != ' COM']

    SCOT_C_EMP_PROV = pd.DataFrame({'BENEFICIARIO' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[1:26],'DNI' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[27:38],'IMPORTE' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[48:58],'ESTADO' : SCOT_C_EMP_PROV[' SCOTIABANK PERU S.A.A.'].str[99:],"OZ":SCOT_C_EMP_PROV["OZ"],"TIPO DE DOCUMENTO":"R","CÓDIGO OPERACIÓN":SCOT_C_EMP_PROV["CÓDIGO OPERACIÓN"],"FECHA PAGO":SCOT_C_EMP_PROV["FECHA PAGO"]})

    SCOT_C_EMP_PROV['IMPORTE']= SCOT_C_EMP_PROV['IMPORTE'].str.replace(",", "")
    SCOT_C_EMP_PROV["BANCO"]="SCOTIABANK"
else:
    SCOT_C_EMP_PROV=pd.DataFrame()

if df_SCOT_M_EMP_PROV:
    #SCOT MACRO EMP PROV
    SCOT_M_EMP_PROV = pd.concat(df_SCOT_M_EMP_PROV)
    SCOT_M_EMP_PROV = SCOT_M_EMP_PROV.loc[:, ['RUC DEL\nPROVEEDOR', 'NOMBRE DEL\nPROVEEDOR','IMPORTE', 'REFERENCIA O\nFACTURA']]
    SCOT_M_EMP_PROV.columns = ['DOC','NOMBRE','IMPORTE','REF']
    SCOT_M_EMP_PROV['T_DOC'] = 'RUC'
else:
    SCOT_M_EMP_PROV=pd.DataFrame()
    
###########################################################################################
if df_SCOT_C_EMP_VAR:
    # SCOT CONSTANCIA EMP VAR
    # LEEMOS Y ACOMODAMOS EL NOMBRE DEL TXT RECIBIDO
    SCOT_C_EMP_VAR= pd.concat(df_SCOT_C_EMP_VAR)
    SCOT_C_EMP_VAR=SCOT_C_EMP_VAR[(SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[40:42]=="S/") & (SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[67:68]=='.')]

    SCOT_C_EMP_VAR = SCOT_C_EMP_VAR[SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[0:4] != ' COM']

    SCOT_C_EMP_VAR = pd.DataFrame({'BENEFICIARIO' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[1:26],'DNI' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[27:38],'IMPORTE' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[48:58],'ESTADO' : SCOT_C_EMP_VAR[' SCOTIABANK PERU S.A.A.'].str[99:],"OZ":SCOT_C_EMP_VAR["OZ"],"TIPO DE DOCUMENTO":"L","CÓDIGO OPERACIÓN":SCOT_C_EMP_VAR["CÓDIGO OPERACIÓN"],"FECHA PAGO":SCOT_C_EMP_VAR["FECHA PAGO"]})

    SCOT_C_EMP_VAR['IMPORTE']= SCOT_C_EMP_VAR['IMPORTE'].str.replace(",", "")
    SCOT_C_EMP_VAR["BANCO"]="SCOTIABANK"
else:
    SCOT_C_EMP_VAR=pd.DataFrame()

if df_SCOT_M_EMP_VAR:
    #SCOT MACRO EMP VAR
    SCOT_M_EMP_VAR = pd.concat(df_SCOT_M_EMP_VAR)
    SCOT_M_EMP_VAR = SCOT_M_EMP_VAR.loc[:, ['TIPO DE\nDOCUMENTO', 'DOCUMENTO IDENTIDAD',    'NOMBRE\nBENEFICIARIO', 'IMPORTE\n', 'REFERENCIA O\nFACTURA']]
    SCOT_M_EMP_VAR.columns = ['T_DOC','DOC','NOMBRE','IMPORTE','REF']
else:
    SCOT_M_EMP_VAR=pd.DataFrame()
    

