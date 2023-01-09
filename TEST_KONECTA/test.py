from tkinter import *
from tkinter import filedialog
import os 

def seleccionar_carpeta():
    global ruta
    ruta = filedialog.askdirectory()
    ruta = str(ruta)
    print(ruta)

    if ruta:
        notif.config(fg="green", text="Carpeta Seleccionada")
    else:
        notif.config(fg="red", text="Carpeta No Seleccionada")

def resumen():
    try:


        #Imprimimos tiempo
        tiempo=round((time.time() - start_time),2)
        texto="Proceso completado, tomó "+str(tiempo)+" segundos"
        notif.config(fg="green", text=texto)

    except Exception:
        if "ruta" in globals():
            notif.config(fg="red", text="Error en el proceso")
        else:
            notif.config(fg="red", text="No ha seleccionado una carpeta")


###############
# Pantalla Principal
master = Tk()
master.title("Inteligencia Comercial")
master.geometry("370x300")

# Etiquetas
Label(master, text="Proceso Automático Logística", fg="black", font=("Calibri", 18,"bold")).grid(padx=40,row=0,column=1,pady=20)


notif = Label(master, font=("Calibri", 14,"bold"))
notif.grid(sticky=N, pady=20, row=12, column=1)
notif.config(fg="green", text="Inicio")

# Botones

Button(master, width=20,fg="white", text="Actualizar Datos",bg="#002060", font=("Calibri", 12,"bold"), command=actualizar).grid(row=9, column=1,pady=10,padx=0)

Button(master, width=20,fg="white", text="Crear Resumen",bg="#002060", font=("Calibri", 12,"bold"), command=resumen).grid(row=10, column=1,pady=10,padx=0)

Button(master, width=20,fg="white", text="Seleccionar Carpeta",bg="#002060", font=("Calibri", 12,"bold"), command=seleccionar_carpeta).grid(row=11, column=1,pady=10,padx=60)

master.mainloop()


