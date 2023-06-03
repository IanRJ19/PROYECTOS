import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
WIDTH = 800
HEIGHT = 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Crear la ventana
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Figuras")

clock = pygame.time.Clock()

class Figure:
    def __init__(self):
        self.size = random.randint(50, 100)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

    def draw(self):
        pass

    def move(self):
        pass

class Triangle(Figure):
    def draw(self):
        pygame.draw.polygon(window, self.color, [(self.x, self.y), (self.x + self.size, self.y), (self.x + self.size / 2, self.y + self.size)])

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

class Circle(Figure):
    def draw(self):
        pygame.draw.circle(window, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

class Ellipse(Figure):
    def draw(self):
        pygame.draw.ellipse(window, self.color, pygame.Rect(self.x, self.y, self.size, self.size // 2))

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size // 2, self.y))

class Square(Figure):
    def draw(self):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

class Rectangle(Figure):
    def __init__(self):
        super().__init__()
        self.width = random.randint(50, 100)
        self.height = random.randint(50, 100)

    def draw(self):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))

# Lista de figuras
figures = []

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                triangle = Triangle()
                figures.append(triangle)
            elif event.key == pygame.K_c:
                circle = Circle()
                figures.append(circle)
            elif event.key == pygame.K_e:
                ellipse = Ellipse()
                figures.append(ellipse)
            elif event.key == pygame.K_d:
                square = Square()
                figures.append(square)
            elif event.key == pygame.K_r:
                rectangle = Rectangle()
                figures.append(rectangle)

    window.fill(WHITE)

    for figure in figures:
        figure.move()
        figure.draw()

    pygame.display.flip()

pygame.quit()
