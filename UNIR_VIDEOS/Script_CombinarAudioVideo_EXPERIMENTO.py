
import ffmpeg
import sys
import os

sys.path.append("C:/Program Files/ffmpeg-n4.4-latest-win64-gpl-4.4/bin")

stream = ffmpeg.input("C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS/Undertale_V.mp4")

stream1 = stream.trim(start = 10, duration=15).filter('setpts', 'PTS-STARTPTS')

stream2 = ffmpeg.output(stream1,"C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS/output.mp4")

ffmpeg.run(stream2)

#contenido = os.listdir("C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS/")
#print(contenido)