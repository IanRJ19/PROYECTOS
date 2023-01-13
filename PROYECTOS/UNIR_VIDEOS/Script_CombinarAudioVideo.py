import ffmpeg



input_video = ffmpeg.input("C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS/Undertale Ost 087 - Hopes and Dreams.mp4")

input_audio = ffmpeg.input("C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS/Undertale Ost 087 - Hopes and Dreams.webm")


ffmpeg.concat(input_video, input_audio, v=1, a=1).output("C:/Users/Rayzek/Documents/PROYECTOS_PROGRAMACIÓN/UNIR_VIDEOS/final.mp4").run()



