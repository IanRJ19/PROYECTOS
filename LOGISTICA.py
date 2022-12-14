
#PIVOT CON NUMERO DE SERIE POR CADA ESTADO SG
df1=df.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], columns="ESTADO SG", aggfunc="count",fill_value=0, margins=True)
df1=df1.reset_index()

#ASIGNANDO DATA
df1_POS_DISP=df1[["MODELO","Disponible"]]
df1 = df1[18:]
df1_TOTAL_SG=df1
df1_POS_INICIAL=df1["All"]

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
df1_TOTAL_SG=df1_TOTAL_SG.drop(["All","OC","MODELO"], axis=1)
df1_TOTAL_SG=df1_TOTAL_SG.transpose()
df1_TOTAL_SG=df1_TOTAL_SG.reset_index()
df1_TOTAL_SG.columns=["DESCRIPCIÓN","CANTIDAD"]
