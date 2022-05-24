from settings import GameObject, Vector2, UP, astro_sprite, random_speed
from pygame.transform import rotozoom


class Astero(GameObject):
    radius = 50

    def __init__(self,position, stage = 3):
        self.stage = stage
        self.direction = Vector2(UP)
        self.angle = 0
        super().__init__(position, astro_sprite, random_speed(1, 3))
        """
        Init de la classe de l'astéroide
        position : position de l'astéroide 
        Stage : Vitesse 
        Direction : Vecteur de la direction de l'asteroide 
        """

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        """
        définit l'astéroide et le fait se déplacer 
        angle avec lequel il arrive : angle 
        position : position
        """