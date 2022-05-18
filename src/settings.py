import pygame
from pygame.math import Vector2
from math import cos, sin

pygame.font.init()

# Variables
WIDTH = 1080
HEIGHT = 720
FPS = 120
UP = Vector2(0, -1)

inputMapVelocity = [False, False]
inputMapRotation = [False, False]
laserMap = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

# fonts
police = pygame.font.Font(None, 50)
police_subtitle = pygame.font.Font(None, 25)
mini_police = pygame.font.Font(None, 20)
mega_police = pygame.font.Font(None, 150)
FONT = pygame.font.Font(None, 32)

# Sprites
vso_sprite = pygame.image.load('../assets/imgs/vso.png')
laser_sprite = pygame.image.load('../assets/imgs/laser.png')

def draw_text(text, font, color, surface, x, y):
    # draw text on a screen

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position = self.position + self.velocity

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius