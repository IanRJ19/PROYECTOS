from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

train=pd.read_csv("C:/Users/Rayzek/Desktop/TEST/bd_train.csv")
test=pd.read_csv("C:/Users/Rayzek/Desktop/TEST/bd_test.csv")


#ESTABLECEMOS LA VARIABLE OBJETIVO Y LAS VARIABLES DEPENDIENTES
y=train["precio"]
X= train.drop("precio", axis=1)

precio_promedio=y.mean()


#######################ENCONTRANDO LA CANTIDAD DE VARIABLES IDEAL A USAR
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# CREAMOS UN OBJETO DE REGRESIÓN LINEAL
modelo = LinearRegression()

Lista_RMSE = []
Posicion_RMSE = []
elementos=len(X.columns)

#COMENZAREMOS A ITERAR PARA VER CON QUE CANTIDAD DE VARIABLES SE TIENE EL MENOR RMSE
for i in range(elementos):
    # CREAMOS UN OBJETO RFE PARA SELECCIONAR n CARACTERÍSTICAS
    rfe = RFE(modelo,n_features_to_select=i+1)

    # AJUSTAMOS EL MODELO RFE AL CONJUNTO DE DATOS
    X_rfe = rfe.fit_transform(X, y)
    x_train, x_test, y_train, y_test = train_test_split(X_rfe, y,test_size=0.3,random_state=42)

    #ENTRENAMOS EL NUEVO MODELO
    modelo.fit(x_train, y_train)

    y_pred = modelo.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    Lista_RMSE.append(rmse)
    extra=i+1
    Posicion_RMSE.append(extra)

posicion=pd.Series(Lista_RMSE).idxmin()
RMSE_TRAIN=min(Lista_RMSE)
cant_var_usar=Posicion_RMSE[posicion]

#######################TRANSFORMANDO LA DATA A LA CANTIDAD DE VARIABLES IDEALES
#ESTA VEZ APLCIAREMOS OTRA VEZ RFE PERO PARA PODER TRANSFORMAR LA DATA DE X Y test, PARA QUE TENGAN SOLO LAS VARIABLES MÁS UTILES
rfe = RFE(modelo,n_features_to_select=cant_var_usar)


X_rfe = rfe.fit_transform(X, y)
test=rfe.fit_transform(X, y)

x_train, x_test, y_train, y_test = train_test_split(X_rfe, y,test_size=0.3,random_state=42)
cabeceras_nuevas=X.columns[(rfe.get_support())]
print(cabeceras_nuevas)

#######################ITERANDO TODOS LOS MODELOS QUE SE ADAPTAN A NUESTRO PROBLEMA PARA HALLAR EL MEJOR
# YA CON LA DATA TRANSFORMADA, PROCEDEREMOS A ITERAR LOS MODELOS QUE SE AJUSTEN A NUESTRO PROBLEMA PARA ENCONTRAR EL MEJOR

from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RANSACRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict


import numpy as np
modelos = {
    'SVR':SVR(),
    'Ridge':Ridge(),
    'ElasticNet':ElasticNet(),
    'SGDRegressor':SGDRegressor(),
    'BayesianRidge':BayesianRidge(),
    'LinearRegression':LinearRegression(),
    'RandomForestRegressor':RandomForestRegressor(),
    "RANSACRegressor":RANSACRegressor(),
    
}

#CREANDO LAS LISTAS
modelo_resultado = []
modelo_nombre = []

# ENTRENANDO EL MODELO
for nombre,modelo in modelos.items():
    a = modelo.fit(x_train,y_train)
    predicted = a.predict(x_test)
    score = np.sqrt(mean_squared_error(y_test, predicted))
    modelo_resultado.append(score)
    modelo_nombre.append(nombre)
    
    #CREANDO LA LISTA DE RESULTADOS
    df_resultados = pd.DataFrame([modelo_nombre,modelo_resultado])
    df_resultados = df_resultados.transpose()
    df_resultados = df_resultados.rename(columns={0:'Model',1:'RMSE'}).sort_values(by='RMSE',ascending=False)
    
print(df_resultados)

ganador=df_resultados["RMSE"].min()
df_resultados=df_resultados.reset_index()
df_resultados=df_resultados.drop("index", axis=1)
df_resultados=df_resultados.set_index("RMSE")
df_resultados.index.get_loc(ganador)
df_resultados=df_resultados.iloc[7,0]
print("EL MEJOR MODELO PARA EL PROBLEMA ES: "+ df_resultados)

#######################REALIZAMOS LA VALIDACIÓN DEL MODELO
#CREAREMOS EL MODELO GANADOR
#CREAREMOS EL MODELO GANADOR
modelo=modelos[df_resultados]

#PROCEDEREMOS A REALIZAR LA VALIDACIÓN CRUZADA PARA COMPARAR LOS RMSE
prediccion = cross_val_predict(modelo, X_rfe, y, cv=3)
RMSE_TEST = np.sqrt(mean_squared_error(y, prediccion))

#VEMOS QUE LA DIFERENCIA DE RMSE NO ES TAN GRANDE, LO QUE INDICA QUE NUESTRO MODELO ESTÁ BIEN
APRUEBA=RMSE_TRAIN-RMSE_TEST

print("El RMSE DEL TRAIN ES: "+str(RMSE_TRAIN))
print("El RMSE DEL TEST ES: "+str(RMSE_TEST))
print("LA DIFERENCIA DE AMBOS ES: "+str(APRUEBA))


#######################USAMOS EL MODELO GANADOR, LO ENTRENAMOS Y PROCEDEMOS A PREDECIR LOS VALORES DESEADOS

modelo.fit(X_rfe, y)
y_pred=modelo.predict(test)

test=pd.DataFrame(test)
serie=pd.Series(y_pred)
serie=serie.astype(float)
test.columns=cabeceras_nuevas
test["Precio"]=serie
test=test.set_index("metros2")
test.to_csv("C:/Users/Rayzek/Desktop/TEST/bd_test_evaluate.csv")
