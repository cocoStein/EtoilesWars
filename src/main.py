import pygame

from settings import *
from spaceship import Spaceship
from astero import Astero

class EtoilesVSO:
  min_distance_spawn = 350

  def __init__(self):
    self._init_pygame()
    pygame.mixer.music.play(-1)
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.clock = pygame.time.Clock()
    self.laser = []
    self.astero = []
    self.spaceship = Spaceship((WIDTH/2, HEIGHT/2), self.laser.append)
    self.score = 0

    for n in range(10):
      while True:
        postion = random_position(self.screen)
        if postion.distance_to(self.spaceship.position) >= self.min_distance_spawn:
            break
      self.astero.append(Astero(postion))

  def _init_pygame(self):
    pygame.init()
    pygame.display.set_caption("Etoiles Vso")
    pygame.time.set_timer(pygame.USEREVENT, 1000)

  def main_loop(self):
    while True:
      self._handle_input()
      self._process_game_logic()
      self._draw()

  def _handle_input(self):

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          inputMapVelocity[0] = True
        if event.key == pygame.K_s:
          inputMapVelocity[1] = True
        if event.key == pygame.K_a:
          inputMapRotation[0] = True
        if event.key == pygame.K_d:
          inputMapRotation[1] = True
        if event.key == pygame.K_SPACE:
          pygame.mixer.Sound.play(laser_sound)
          self.spaceship.shoot()
        if event.key == pygame.K_UP:
          self.spaceship.get_health(200)
        if event.key == pygame.K_DOWN:
          self.spaceship.get_damage(200)
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          inputMapVelocity[0] = False
        if event.key == pygame.K_s:
          inputMapVelocity[1] = False
        if event.key == pygame.K_a:
          inputMapRotation[0] = False
        if event.key == pygame.K_d:
          inputMapRotation[1] = False

  def _process_game_logic(self):

    # Rotation spaceship
    if inputMapRotation[0]: self.spaceship.rotate(clockwise=False)
    if inputMapRotation[1]: self.spaceship.rotate(clockwise=True)

    # Movement spaceship
    self.spaceship.velocity = (0, 0)
    if inputMapVelocity[0]: self.spaceship.accelerate()
    self.spaceship.move()

    if self.spaceship.position.x >= WIDTH: self.spaceship.position.x = 1
    if self.spaceship.position.x <= 0: self.spaceship.position.x = WIDTH
    if self.spaceship.position.y >= HEIGHT: self.spaceship.position.y = 1
    if self.spaceship.position.y <= 0: self.spaceship.position.y = HEIGHT

    for las in self.laser: las.move()
    for rock in self.astero:
      rock.move()
      if rock.position.x >= WIDTH: rock.position.x = 1
      if rock.position.x <= 0: rock.position.x = WIDTH
      if rock.position.y >= HEIGHT: rock.position.y = 1
      if rock.position.y <= 0: rock.position.y = HEIGHT
      if rock.collides_with(self.spaceship):
        pygame.mixer.Sound.play(damage_sound)
        self.astero.remove(rock)
        self.spaceship.get_damage(100)
    for las in self.laser:
      for rock in self.astero:
        if las.collides_with(rock):
          self.astero.remove(rock)
          self.laser.remove(las)
          self.score += 50

    if len(self.astero) < 9:
      postion = random_position(self.screen)
      if postion.distance_to(self.spaceship.position) >= self.min_distance_spawn:
        pass
      self.astero.append(Astero(postion))

  def _draw(self):
    self.screen.fill(DARKGRAY)
    self.spaceship.draw(self.screen)


    for las in self.laser: las.draw(self.screen)
    for rock in self.astero: rock.draw(self.screen)


    self.spaceship.advanced_health(self.screen)
    draw_text(str(self.score), police, WHITE, self.screen, 980, 50)
    # Flip the display
    self.clock.tick(FPS)
    pygame.display.flip()


if __name__ == "__main__":
  EtoilesVSO().main_loop()