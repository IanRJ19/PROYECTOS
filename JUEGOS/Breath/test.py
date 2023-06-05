import pygame

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
ventana_ancho = 800
ventana_alto = 600

# Crear la ventana
ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))

# Cargar el sprite
sprite = pygame.image.load("JUEGOS/Breath/player.png")

# Definir el tamaño de cada cuadro de animación
cuadro_ancho = 46
cuadro_alto = 50

# Definir las acciones y sus cuadros correspondientes
acciones = {
    "correr": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "saltar": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "detenerse": [(0, 2)]
}

# Definir la acción actual y el índice del cuadro actual
accion_actual = "detenerse"
indice_cuadro_actual = 0

# Variable para indicar si el personaje está en movimiento o detenido
en_movimiento = False

# Variable de velocidad
velocidad = 2

# Variable para indicar si la tecla de correr está presionada
corriendo = False

# Bucle principal del juego
while True:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                accion_actual = "saltar"
                en_movimiento = True
            elif event.key == pygame.K_r:
                accion_actual = "correr"
                en_movimiento = True
                corriendo = True  # La tecla de correr está presionada
            elif event.key == pygame.K_s:
                accion_actual = "detenerse"
                en_movimiento = False
                corriendo = False  # La tecla de correr no está presionada
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                corriendo = False  # La tecla de correr no está presionada

    # Limpiar la ventana
    ventana.fill((0, 0, 0))  # Rellenar la ventana con color negro

    # Dibujar el cuadro actual en la ventana
    ventana.blit(sprite, (0, 0), (acciones[accion_actual][indice_cuadro_actual][0] * cuadro_ancho,
                                 acciones[accion_actual][indice_cuadro_actual][1] * cuadro_alto,
                                 cuadro_ancho, cuadro_alto))

    # Actualizar el índice del cuadro actual si el personaje está en movimiento
    if en_movimiento:
        # Ajustar la velocidad según la acción actual
        if accion_actual == "saltar":
            velocidad = 1
        elif accion_actual == "correr":
            velocidad = 1 if corriendo else 0  # Si la tecla de correr está presionada, velocidad = 1, sino, velocidad = 0
        else:
            velocidad = 1

        # Actualizar el índice del cuadro actual con la velocidad
        indice_cuadro_actual += velocidad
        if indice_cuadro_actual >= len(acciones[accion_actual]):
            indice_cuadro_actual = 0

    # Actualizar la ventana
    pygame.display.flip()
