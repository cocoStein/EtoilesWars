from settings import boss_sprite, GameObject, Vector2, UP, pygame, PURPLE, BLUE
from laser import Laser

class Boss(GameObject):
    laser_speed = 4
    def __init__(self, position, shoot_laser):
        # Make a copy of the original UP vector
        self.shoot_laser = shoot_laser
        self.direction = Vector2(UP)
        self.angle = 0

        self.current_health = 1000
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

        super().__init__(position, boss_sprite, Vector2(0))

    def get_damage(self, amount):
        """
        Encaisse les dégâts subis par le vaisseau
        Amount : Total des dégâts qui vont être encaissés
        """
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        """
        Sert pour soigner le vaisseau d'un certain nombre de HP
        Amount : Taux de soins (valeur)
        """
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def advanced_health(self, screen):
        """
        Dessin de la barre de vie
        """
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = PURPLE

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = - int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(10, 100, health_bar_width, 25)
        transition_bar = pygame.Rect(health_bar.right, 100, transition_width, 25)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)
        pygame.draw.rect(screen, transition_color, transition_bar)
        pygame.draw.rect(screen, BLUE, (10, 100, self.health_bar_length, 25), 4)

    def shoot(self):
        """
        Définit la vitesse, direction et accélération des lasers tirés
        """
        laser_velocity = self.direction * self.laser_speed + self.velocity
        laser = Laser(self.position, laser_velocity, self.direction.angle_to(Vector2(0)))
        self.shoot_laser(laser)