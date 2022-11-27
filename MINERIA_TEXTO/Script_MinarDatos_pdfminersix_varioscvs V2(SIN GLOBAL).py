from msilib.schema import Directory
import tkinter
from pdfminer.high_level import extract_text
from tkinter import *
from tkinter import filedialog
import os


#################

path="H:/Mi unidad/TRABAJO/MINERÍA DE DATOS/EJEMPLOS/EJEMPLO MINERIA DE DATOS/CVS/"

def seleccionar_carpeta():
    global path
    path = filedialog.askdirectory()
    path = str(path)
    
    print(path)
    if not path:
        print('Cancelado')

global listadoDirectorio
listadoDirectorio = os.listdir(path)        
print(listadoDirectorio)

def minar():
    info=data.get()
    try:
        for i in listadoDirectorio:
            text = extract_text(path+"/"+i).lower()
            if info in text:
                print("El CV que contiene la palabra"+" "+info+" es: ",i)
                print("------------------------------------")
                notif.config(fg="green", text="Revisión completa, el cv buscado es: "+i)
        

    except Exception as e:
        print(e)
        notif.config(fg="red", text="Los CV'S no pueden ser minados")
    
###############


# Pantalla Principal
master = Tk()
master.title("Filtrado de CV'S")
master.geometry("500x300")


# Etiquetas
l_filtrado=Label(master, text="FILTRADO DE CV'S", fg="red", font=("Calibri", 15)).grid(sticky=N,padx=180,pady=30)
l_buscar=Label(master, text="Introduce la palabra a buscar : ", font=("Calibri", 15)).grid(sticky=N, row=1, pady=15)
notif = Label(master, font=("Calibri", 12))
notif.grid(sticky=N, pady=1, row=4)
# Variables
data = StringVar()
# Entry
Entry(master, width=50, textvariable=data).grid(sticky=N, row=2)
# Button
Button(master, width=20, text="Seleccionar carpeta", font=("Calibri", 12), command=seleccionar_carpeta).grid(sticky=N, row=9, pady=15)
master

Button(master, width=20, text="Empezar a Filtrar", font=("Calibri", 12), command=minar).grid(sticky=N, row=8, pady=0)
master.mainloop()

#probando
