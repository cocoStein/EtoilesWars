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
    self.number_astro = 6
    self.number_astro_kill = 0
    self.spaceship = Spaceship((WIDTH/2, HEIGHT/2), self.laser.append)
    self.score = 0
    self.running = True

    for n in range(self.number_astro):
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
      if self.running == True:
        self._handle_input()
        self._process_game_logic()
        self._draw()
      else:
        self._endScreen()

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
          self.score -= 5
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
          self.number_astro_kill += 1

    for las in self.laser:
      las.move()
      if las.position.x >= WIDTH: self.laser.remove(las)
      if las.position.x <= 0: self.laser.remove(las)
      if las.position.y >= HEIGHT: self.laser.remove(las)
      if las.position.y <= 0: self.laser.remove(las)

    if len(self.astero) < self.number_astro:
      postion = random_position(self.screen)
      if postion.distance_to(self.spaceship.position) >= self.min_distance_spawn:
        pass
      self.astero.append(Astero(postion))

    if self.spaceship.target_health == 0:
      self.running = False


  def _draw(self):
    self.screen.fill(DARKGRAY)
    self.spaceship.draw(self.screen)


    for las in self.laser: las.draw(self.screen)
    for rock in self.astero: rock.draw(self.screen)


    self.spaceship.advanced_health(self.screen)
    draw_text("Score:", police, WHITE, self.screen, 870, 50)
    draw_text(str(self.score), police, WHITE, self.screen, 980, 50)
    # Flip the display
    self.clock.tick(FPS)
    pygame.display.flip()

  def _endScreen(self):
    self.screen.fill(BLACK)

    draw_text("GAME OVER", mega_police, RED, self.screen, WIDTH/2 - 300, HEIGHT/2 - 300)
    draw_text("Score:", police, WHITE, self.screen, 150, 200)
    draw_text(str(self.score), police, WHITE, self.screen, 300, 200)
    draw_text("Astéroides détruits:", police, WHITE, self.screen, 150, 250)
    draw_text(str(self.number_astro_kill), police, WHITE, self.screen, 500, 250)

    self.clock.tick(FPS)
    pygame.display.flip()

if __name__ == "__main__":
  EtoilesVSO().main_loop()