import pygame.sprite

from settings import GameObject, Vector2, explo1, explo2, explo3, explo4, explo5, explo6, explo7, explo8, explo9, explo10, missil_sprite

class Missil(GameObject):

    def __init__(self, position, velocity):
        """
        Initialise le missile et ses différenttes caractéristiques
        """
        super().__init__(position, missil_sprite, velocity)

class Explosion(pygame.sprite.Sprite):

    def __init__(self, posX, posY):
        """
        Les images qui se déplacent sans exploser et crée le cas si il explosait
        """
        super().__init__()
        self.attack_animation = False
        self.sprites = []
        self.sprites.append(explo1)
        self.sprites.append(explo2)
        self.sprites.append(explo3)
        self.sprites.append(explo4)
        self.sprites.append(explo5)
        self.sprites.append(explo6)
        self.sprites.append(explo7)
        self.sprites.append(explo8)
        self.sprites.append(explo9)
        self.sprites.append(explo10)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [posX, posY]


    def attack(self):
        self.attack_animation = True
        """
        Si le vaisseau est touché une animation se produira
        """


    def update(self, speed):
        """
        Update les 10 sprite pour faire l'animation afin qu'elle ne se répète pas
        """
        if self.attack_animation == True:
            self.current_sprite += speed
            print("asd")
            if int(self.current_sprite) >= len(self.sprites):
                print(1)
                self.current_sprite = 0
                self.attack_animation = False

        self.image = self.sprites[int(self.current_sprite)]
