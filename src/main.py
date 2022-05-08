from src.settings import *
from spaceship import Spaceship

class EtoilesVSO:
  def __init__(self):
    self._init_pygame()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.clock = pygame.time.Clock()
    self.spaceship = Spaceship((400, 300))

  def _init_pygame(self):
    pygame.init()
    pygame.display.set_caption("Etoiles Vso")
    pygame.time.set_timer(pygame.USEREVENT, 1000)

  def main_loop(self):
    while True:
      self._handle_input()
      self._process_game_logic()
      #self.spaceship.update(self.screen)
      self._draw()


  def _handle_input(self):

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          inputMapVelocity[0] = True;
        if event.key == pygame.K_s:
          inputMapVelocity[1] = True;
        if event.key == pygame.K_a:
          inputMapRotation[0] = True;
        if event.key == pygame.K_d:
          inputMapRotation[1] = True;
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          inputMapVelocity[0] = False;
        if event.key == pygame.K_s:
          inputMapVelocity[1] = False;
        if event.key == pygame.K_a:
          inputMapRotation[0] = False ;
        if event.key == pygame.K_d:
          inputMapRotation[1] = False ;

        if event.key == pygame.K_UP:
          self.spaceship.get_health(200)
        if event.key == pygame.K_DOWN:
          self.spaceship.get_damage(200)


  def _process_game_logic(self):

    # Rotation spaceship
    if inputMapRotation[0]: self.spaceship.rotate(clockwise=False)
    if inputMapRotation[1]: self.spaceship.rotate(clockwise=True)

    # Mouvement spaceship
    self.spaceship.velocity = (0, 0)
    if inputMapVelocity[0]: self.spaceship.accelerate()
    #if inputMapVelocity[1]: self.spaceship.velocity += Vector2(cos(self.spaceship.angle) * 2, sin(self.spaceship.angle) * 2)
    self.spaceship.move()

    if self.spaceship.position.x >= WIDTH: self.spaceship.position.x = 1
    if self.spaceship.position.x <= 0: self.spaceship.position.x = WIDTH
    if self.spaceship.position.y >= HEIGHT: self.spaceship.position.y = 1
    if self.spaceship.position.y <= 0: self.spaceship.position.y = HEIGHT





  def _draw(self):
    self.screen.fill(DARKGRAY)
    self.spaceship.draw(self.screen)
    self.spaceship.advanced_health(self.screen)

    # Flip the display
    self.clock.tick(FPS)
    pygame.display.flip()


if __name__ == "__main__":
  EtoilesVSO().main_loop()