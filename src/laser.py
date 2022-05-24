from settings import GameObject, laser_sprite

class Laser(GameObject):

    def __init__(self, position, velocity):
        super().__init__(position, laser_sprite, velocity)
        """
        Classe laser qui crée le laser et son shoot 
        Position : position 
        Velocity : Vitesse du laser 
        """