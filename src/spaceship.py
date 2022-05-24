from settings import GameObject, Vector2, UP, vso_sprite, pygame, GREEN
from pygame.transform import rotozoom
from laser import Laser
from missile import Missil


class Spaceship(GameObject):
    maneuverability = 5
    acceleretion = 4
    laser_speed = 6
    missile_speed = 4

    def __init__(self, position, shoot_laser, shoot_missil):
        # Make a copy of the original UP vector
        self.shoot_missil = shoot_missil
        self.shoot_laser = shoot_laser
        self.direction = Vector2(UP)
        self.angle = 0

        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 30, 30))
        self.rect = self.image.get_rect(center=(400, 400))
        self.current_health = 1000
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

        super().__init__(position, vso_sprite, Vector2(0))

    def rotate(self, clockwise=True):
        """
        Fait que le vaisseau tourne quand voulu 
        """
        sign = 1 if clockwise else -1
        self.angle = self.maneuverability * sign
        self.direction.rotate_ip(self.angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self.acceleretion

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
            transition_color = GREEN

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = - int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(10, 45, health_bar_width, 25)
        transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)
        pygame.draw.rect(screen, transition_color, transition_bar)
        pygame.draw.rect(screen, (255, 255, 255), (10, 45, self.health_bar_length, 25), 4)


    def shoot(self):
        """
        Définit la vitesse, direction et accélération des lasers tirés
        """
        laser_velocity = self.direction * self.laser_speed + self.velocity
        laser = Laser(self.position, laser_velocity)
        self.shoot_laser(laser)

    def shoot_Missile(self):
        """
        Définit la vitesse, direction et accélération du missile 
        """
        missile_velocity = self.direction * self.missile_speed + self.velocity
        missile = Missil(self.position, missile_velocity)
        self.shoot_missil(missile)