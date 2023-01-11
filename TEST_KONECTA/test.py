from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
train=pd.read_csv("C:/Users/Rayzek/Desktop/TEST/bd_train.csv")
test=pd.read_csv("C:/Users/Rayzek/Desktop/TEST/bd_test.csv")

#ESTABLECEMOS LA VARIABLE OBJETIVO Y LAS VARIABLES DEPENDIENTES
y=train["precio"]
X= train.drop("precio", axis=1)


from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE

# CREAMOS UN OBJETO DE REGRESIÓN LINEAL
model = LinearRegression()

lista_VARS = []
lista_numeros = []
elementos=len(X.columns)

for i in range(elementos):
    # CREAMOS UN OBJETO RFE PARA SELECCIONAR 5 CARACTERÍSTICAS
    rfe = RFE(model,n_features_to_select=i+1)

    # AJUSTAMOS EL MODELO RFE AL CONJUNTO DE DATOS
    X_rfe = rfe.fit_transform(X, y)
    x_train, x_test, y_train, y_test = train_test_split(X_rfe, y,test_size=0.3,random_state=42)

    #ENTRENAMOS EL NUEVO MODELO
    model.fit(x_train, y_train)

    #print(X.columns[(rfe.get_support())])
    y_pred = model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    lista_VARS.append(rmse)
    extra=i+1
    lista_numeros.append(extra)
    #print(str(i+1)+" Variables seleccionadas"+" RMSE: "+ str(rmse))

posicion=pd.Series(lista_VARS).idxmin()
var_usar=lista_numeros[posicion]

# CREAMOS UN OBJETO RFE PARA SELECCIONAR LA CANT DE CARACTERISTICAS IDEALES
rfe = RFE(model,n_features_to_select=var_usar)

# AJUSTAMOS EL MODELO RFE AL CONJUNTO DE DATOS
X_rfe = rfe.fit_transform(X, y)
test=rfe.fit_transform(X, y)
x_train, x_test, y_train, y_test = train_test_split(X_rfe, y,test_size=0.3,random_state=42)
cabeceras_nuevas=X.columns[(rfe.get_support())]
cabeceras_nuevas


from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RANSACRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
import xgboost as xgb

import numpy as np
models = {
    'SVR':SVR(),
    'Ridge':Ridge(),
    'ElasticNet':ElasticNet(),
    'SGDRegressor':SGDRegressor(),
    'BayesianRidge':BayesianRidge(),
    'LinearRegression':LinearRegression(),
    'RandomForestRegressor':RandomForestRegressor(),
    "RANSACRegressor":RANSACRegressor(),
    #"XGBRegressor":xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1, max_depth = 5, alpha = 10, n_estimators = 150)
    
}

#TAKING RESULTS FROM THE MODELS
model_results = []
model_names = []

# TRAINING THE MODEL WITH FUNCTION
for name,model in models.items():
    a = model.fit(x_train,y_train)
    predicted = a.predict(x_test)
    score = np.sqrt(mean_squared_error(y_test, predicted))
    model_results.append(score)
    model_names.append(name)
    
    #CREATING DATAFRAME
    df_results = pd.DataFrame([model_names,model_results])
    df_results = df_results.transpose()
    df_results = df_results.rename(columns={0:'Model',1:'RMSE'}).sort_values(by='RMSE',ascending=False)
    
print(df_results)

ganador=df_results["RMSE"].min()
df_results=df_results.reset_index()
df_results=df_results.drop("index", axis=1)
df_results=df_results.set_index("RMSE")
df_results.index.get_loc(ganador)
df_results=df_results.iloc[7,0]
print("Mejor modelo para el problema: "+ df_results)



model=models[df_results]

predictions = cross_val_predict(model, X_rfe, y, cv=3)

# CALCULATE RMSE
rmse = np.sqrt(mean_squared_error(y, predictions))

print("RMSE: ", rmse)


model.fit(X_rfe, y)
y_pred=model.predict(test)


test=pd.DataFrame(test)
serie=pd.Series(y_pred)
serie=serie.astype(float)
test.columns=cabeceras_nuevas
test["Precio"]=serie
test=test.set_index("metros2")
test.to_csv("C:/Users/Rayzek/Desktop/TEST/bd_test_evaluate.csv")
