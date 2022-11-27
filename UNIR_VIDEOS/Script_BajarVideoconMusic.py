from pytube import YouTube
import ffmpeg
from os import remove

link = "https://www.youtube.com/watch?v=tz82xbLvK_k"
yt = YouTube(link)

# se muestra informacion del video
print("Su video es:")
print("\tTitulo:",yt.title)
print("\tAutor:",yt.author)
duracion = yt.length # seg
horas = int(duracion/60/60)
duracion -= horas*60*60
minutos = int((duracion)/60)
duracion -= minutos*60
segundos = int(duracion)

print("\tDuracion:",f"{horas}:{minutos}:{segundos}")

print("Descargando")

print("\t",yt.streams.filter(adaptive=True).order_by("resolution").desc().first())
print("\t",yt.streams.filter(only_audio=True).order_by("abr").desc().first())

video = yt.streams.filter(adaptive=True).order_by("resolution").desc().first().download(output_path="C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS")
audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first().download(output_path="C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS")

print("Termino, adios!")


