import pygame
from pygame.locals import *
import sys

def setup_screen():
    pygame.init()
    screen_width = 800
    screen_height = 600
    return pygame.display.set_mode((screen_width, screen_height))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("JUEGOS/Breath/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        # Agrega más lógica para el movimiento, saltos, colisiones, etc.


def main():
    screen = setup_screen()
    player = Player()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Rellena la pantalla con color negro
        player.update()
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
