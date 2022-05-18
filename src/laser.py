from settings import GameObject, laser_sprite

class Laser(GameObject):

    def __init__(self, position, velocity):
        super().__init__(position, laser_sprite, velocity)