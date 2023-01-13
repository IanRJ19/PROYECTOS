#AGREGAR PESTAÑA
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account(filename="H:\Mi unidad\LLAVES\ActivarGoogleSheetIan.json")
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1nrBiUTSpcuDBb_w9AY-io_akpm0jLEcv695QG_IFrvk")

actual = gsheet.worksheet("Actual").get_all_records()
base2= pd.DataFrame(actual)

anterior = gsheet.worksheet("Anterior").get_all_records()
base1= pd.DataFrame(anterior)

# INSTAURAMOS EL CONTROLADOR DE PESTAÑA
wsheet = gsheet.worksheet("Final 2022")

#departamentos=base1["Departamento"]
#base1=base1.drop(["Departamento"], axis=1)
#base1=base1.astype("int")

base1=base1.rename(columns={'1': '01',"2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09"})
base2=base2.rename(columns={'1': '01',"2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09"})

base1 = base1.set_index('Departamento').cumsum(axis=1)
base2 = base2.set_index('Departamento').cumsum(axis=1)

data=base2-base1
data=data.reset_index()
data=data.fillna("")
data=data.sort_values(["18", "17"], ascending=[True, True])
#data.insert(0,"Departamentos",departamentos)
wsheet.update([data.columns.values.tolist()]+data.values.tolist())







################################
actual = gsheet.worksheet("DIC-2021").get_all_records()
base2= pd.DataFrame(actual)

anterior = gsheet.worksheet("NOV-2021").get_all_records()
base1= pd.DataFrame(anterior)

# INSTAURAMOS EL CONTROLADOR DE PESTAÑA
wsheet = gsheet.worksheet("Final 2021")

#departamentos=base1["Departamento"]
#base1=base1.drop(["Departamento"], axis=1)
#base1=base1.astype("int")

base1=base1.rename(columns={'1': '01',"2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09"})
base2=base2.rename(columns={'1': '01',"2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09"})

base1 = base1.set_index('Departamento').cumsum(axis=1)
base2 = base2.set_index('Departamento').cumsum(axis=1)

data=base2-base1
data=data.reset_index()
data=data.fillna("")
data=data.sort_values(["18", "17"], ascending=[True, True])
#data.insert(0,"Departamentos",departamentos)
wsheet.update([data.columns.values.tolist()]+data.values.tolist())