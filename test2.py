import pandas as pd
import numpy as np

train=pd.read_csv("C:/Users/ugad.ingenieria2/Desktop/EsSalud/DATASETS/Iris.csv",sep=",")
train.head()
train.info()
train=train.dropna()

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
train['Species'] = le.fit_transform(train['Species'].values)

train.describe()

import matplotlib.pyplot as plt
train.hist(bins=40, figsize=(20,20))
plt.show()
#PODEMOS VER QUE LA GRÁFICA DEL PRECIO, TIENE UNA DISTRIBUCIÓN QUE DETALLAREMOS MÁS ADELANTE

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 10))
ax=sns.countplot(x="Species",data=train)
ax.set_title("Class Distribution")
plt.show()



#GRAFICAREMOS A DETALLE LA GRAFICA DEL PRECIO PARA VER SU DISTRIBUCION Y QUE ES ASIMETRICA POSITIVA. 


import seaborn as sns
correlacion = train
correlacion=correlacion.corr().round(2)
correlacion = correlacion.loc[:,["Species"]]
correlacion = correlacion.sort_values(by="Species", ascending=False)


fig, ax = plt.subplots(figsize=(2,15))

ax=sns.heatmap(correlacion, annot=True,cmap="Blues")

#EN ESTA GRAFICA VEREMOS LA CORRELACION DE LAS VARIABLES CON LA VARIABLE OBJETIVO. 

#ELIMINAMOS LAS VARIABLES QUE NO USAREMOS
train=train.drop("Id",axis=1)

#ESTABLECEMOS LA VARIABLE OBJETIVO Y LAS VARIABLES DEPENDIENTES
y=train["Species"]
X=train.drop("Species", axis=1)
