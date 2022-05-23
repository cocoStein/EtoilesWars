import pygame
from pygame.math import Vector2
import random


pygame.font.init()
pygame.mixer.init()

# Variables
WIDTH = 1080
HEIGHT = 720
FPS = 60
UP = Vector2(0, -1)

inputMapVelocity = [False, False]
inputMapRotation = [False, False]

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
vso_sprite = pygame.image.load('../assets/imgs/pixil-frame-0 (1).png')
laser_sprite = pygame.image.load('../assets/imgs/laser.png')
astro_sprite = pygame.image.load('../assets/imgs/astro_sprite.png')
missil_sprite = pygame.image.load('../assets/imgs/missile.png')
heal_sprite = pygame.image.load('../assets/imgs/heal.png')
heal_sprite = pygame.transform.scale(heal_sprite, (64,64))

explo1 = pygame.image.load('../assets/imgs/explo-1.png')
explo2 = pygame.image.load('../assets/imgs/explo-2.png')
explo3 = pygame.image.load('../assets/imgs/explo-3.png')
explo4 = pygame.image.load('../assets/imgs/explo-4.png')
explo5 = pygame.image.load('../assets/imgs/explo-5.png')
explo6 = pygame.image.load('../assets/imgs/explo-6.png')
explo7 = pygame.image.load('../assets/imgs/explo-7.png')
explo8 = pygame.image.load('../assets/imgs/explo-8.png')
explo9 = pygame.image.load('../assets/imgs/explo-9.png')
explo10 = pygame.image.load('../assets/imgs/explo-10.png')


# Sounds
damage_sound = pygame.mixer.Sound('../assets/sounds/damage_snd.mp3')
backR_music = pygame.mixer.music.load('../assets/sounds/bckg_music.mp3')
laser_sound = pygame.mixer.Sound('../assets/sounds/laser.mp3')


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

def random_speed(min, max):
    speed = random.randint(min, max)
    angle = random.randint(0, 360)
    return Vector2(speed, 0).rotate(angle)

def random_position(screen):
    return Vector2(
        random.randrange(screen.get_width()),
        random.randrange(screen.get_height()),
    )