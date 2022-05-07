from settings import *
from pygame.transform import rotozoom

class Spaceship(GameObject):
    maneuverability = 5

    def __init__(self, position):
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, vso_sprites, Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.maneuverability * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)