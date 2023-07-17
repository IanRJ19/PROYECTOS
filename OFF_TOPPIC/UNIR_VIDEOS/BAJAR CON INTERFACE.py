from tkinter import *
from pytube import YouTube


# Functions
def download():
    video_url = url.get()
    try:
        yt= YouTube(video_url)
        video = yt.streams.filter(adaptive=True).order_by("resolution").desc().first().download(output_path="C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS")
        audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first().download(output_path="C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS")
        notif.config(fg="green", text="Descarga completa")
    except Exception as e:
        print(e)
        notif.config(fg="red", text="El video no puede ser descargado")

# Main Screen
master = Tk()
master.title("Youtube Video Downloader")

# Labels
Label(master, text="Youtube Video Downloader", fg="red", font=("Calibri", 15)).grid(sticky=N, padx=100, row=0)
Label(master, text="Introduce el link de tu video abajo : ", font=("Calibri", 15)).grid(sticky=N, row=1, pady=15)
notif = Label(master, font=("Calibri", 12))
notif.grid(sticky=N, pady=1, row=4)
# Vars
url = StringVar()
# Entry
Entry(master, width=50, textvariable=url).grid(sticky=N, row=2)
# Button
Button(master, width=20, text="Descargar", font=("Calibri", 12), command=download).grid(sticky=N, row=3, pady=15)
master.mainloop()