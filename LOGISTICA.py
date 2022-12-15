
df1_INSTALADOS_1=df1_INSTALADOS_1.pivot_table(values='NUMERO SERIE', index=["OC",'MODELO'], aggfunc="count",columns="x",fill_value=0, margins=True)
df1_INSTALADOS_1=df1_INSTALADOS_1.reset_index()
#df1_INSTALADOS_1=df1_INSTALADOS_1[df1_INSTALADOS_1["MODELO"].isin(["ICT 220","ICT 250"])]
df1_INSTALADOS_1=df1_INSTALADOS_1.replace('ICT 220', "Instalados AKN (1) ICT")
df1_INSTALADOS_1=df1_INSTALADOS_1.replace('ICT 250', "Instalados AKN (1) ICT")
df1_INSTALADOS_1=df1_INSTALADOS_1.replace('APOS', "Instalados AKN (1) APOS")
df1_INSTALADOS_1=df1_INSTALADOS_1.groupby("MODELO").sum()
df1_INSTALADOS_1=df1_INSTALADOS_1.reset_index()
df1_INSTALADOS_1=df1_INSTALADOS_1.drop(0, axis=0)
df1_INSTALADOS_1=df1_INSTALADOS_1.drop([2,3,"All"], axis=1)
df1_INSTALADOS_1.columns=["DESCRIPCIÓN","CANTIDAD"]
print(df1_INSTALADOS_1)
