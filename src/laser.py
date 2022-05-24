import pygame
from settings import GameObject, laser_sprite

class Laser(GameObject):

     def __init__(self, position, velocity, angle):
        super().__init__(position, pygame.transform.rotate(laser_sprite, angle), velocity)
        """
        Classe laser qui crée le laser et son shoot 
        Position : position 
        Velocity : Vitesse du laser 
        """