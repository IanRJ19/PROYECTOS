import tkinter
import customtkinter
from tkinter import filedialog

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("500x420")
app.title("Inteligencia Comercial")

def seleccionar_carpeta():
    global ruta
    ruta = filedialog.askdirectory()
    ruta = str(ruta)
    print(ruta)

def button_callback():
    print("Button click")


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=0, padx=0, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT,text="Captación de Agentes ACK",text_font=("Calibri",20,"bold"),text_color="#002060")
label_1.pack(pady=12, padx=10)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT,text="Introduce las fechas",text_font=("Calibri",15,"bold"),text_color="red")
label_1.pack(pady=0, padx=10)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT,text="En formato yyyy-mm-dd",text_font=("Calibri",10,"bold"))
label_1.pack(pady=0, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Inicio Evento")
entry_1.pack(pady=5, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Fin Evento")
entry_1.pack(pady=5, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Inicio Captación")
entry_1.pack(pady=5, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Fin Captación")
entry_1.pack(pady=5, padx=10)


button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback,text="Ejecutar Script",text_font=("Calibri",10,"bold"),fg_color="#002060",text_color="white")
button_1.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=seleccionar_carpeta,text="Seleccionar Carpeta",text_font=("Calibri",10,"bold"),fg_color="#002060",text_color="white")
button_1.pack(pady=12, padx=10)




app.mainloop()