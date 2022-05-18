from settings import GameObject, WHITE, UP, Vector2, laser_sprite
from pygame.transform import rotozoom

class Laser(GameObject):
    acceleretion = 4

    def __init__(self, angle, position, color = WHITE):
        self.color = color
        self.length = 10
        self.angle = angle
        self.direction = Vector2(UP)

        super().__init__(position, laser_sprite, Vector2(10, 0))

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
