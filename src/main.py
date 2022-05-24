from settings import *
from spaceship import Spaceship
from astero import Astero
from missile import Explosion
from boss import Boss

class EtoilesVSO:
  min_distance_spawn = 350
  number_star = 200
  laser_cost = 5
  missile_cost = 75

  def __init__(self):

    """
    Fonction qui sert a créer tous les objets qui seront actifs dans le jeu et les instancier
    Laser : laser tiré par le vaisseau 
    missile : missile qui pourra endommager le vaisseau 
    astero : asteroide qui se déplacera sur dans le jeu et qui provoquera des dégâts au vaisseau 
    heal : entité qui va régénérer des HP du vaisseau 
    """



    self._init_pygame()
    pygame.mixer.music.play(-1)
    pygame.mixer.Sound.play(intro_sound)
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.background = (pygame.Surface(self.screen.get_size())).convert()
    self.clock = pygame.time.Clock()

    self.laser = []
    self.laserBoss = []
    self.missile = []
    self.astero = []
    self.heal = []
    self.stars = [
        [random.randint(0, WIDTH),random.randint(0, HEIGHT)]
        for x in range(self.number_star)
    ]

    self.number_astro = 6
    self.number_astro_kill = 0
    self.spaceship = Spaceship((WIDTH/2, HEIGHT/2), self.laser.append, self.missile.append)
    self.boss = Boss((WIDTH/2, 50), self.laserBoss.append)

    self.score = 500
    self.running = True
    self.boss_fight = False

    #self.misi = Explosion(posX=500, posY=200)
    self.movingS = pygame.sprite.Group()
    #self.movingS.add(self.misi)

    for n in range(self.number_astro):
      while True:
        postion = random_position(self.screen)
        if postion.distance_to(self.spaceship.position) >= self.min_distance_spawn:
            break
      self.astero.append(Astero(postion))

  def _init_pygame(self):
    """
    initailise le jeu 
    """
    pygame.init()
    pygame.display.set_caption("Etoiles Vso")
    pygame.time.set_timer(pygame.USEREVENT, 1000)

  def main_loop(self):
    """
    Fait que si on ne perd pas le jeu continue 
    """
    while True:
      if self.running == True:
        if self.boss_fight == False:
          self._handle_input()
          self._process_game_logic()
          self._draw()
        else:
          self._handle_input()
          self._game_logig_Boss()
          self._draw_Boss()
      else:
        self._endScreen()
        self._handle_input()

  def _handle_input(self):
    """
    Va s'occuper des mouvements lorsque l'on appuie sur W,A,D et espace
    """

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          inputMapVelocity[0] = True
        # if event.key == pygame.K_s:
        #   inputMapVelocity[1] = True
        if event.key == pygame.K_a:
          inputMapRotation[0] = True
        if event.key == pygame.K_d:
          inputMapRotation[1] = True

        if event.key == pygame.K_q:
          #Check if the player has enough points to shoot
          if self.score >= self.missile_cost:
            #Shoot missile
            self.spaceship.shoot_Missile()
            self.score -= self.missile_cost

        if event.key == pygame.K_SPACE:
          #Check if the player has enough points to shoot
          if self.score >= self.laser_cost:
            #Shoot laser
            pygame.mixer.Sound.play(laser_sound)
            self.spaceship.shoot()
            self.score -= self.laser_cost

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
    """
    Définit toute la logique du jeu, faire que les astéroides font des dégâts lors de la collision 
    Rock : entité représentant un astéroide 
    las : laser tiré par le vaisseau 
    """

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
          try:
            self.astero.remove(rock)
          except:
            pass
          try:
            self.laser.remove(las)
          except:
            pass
          self.score += 50
          self.number_astro_kill += 1

    for las in self.laser:
      las.move()
      if las.position.x >= WIDTH:
        try:
          self.laser.remove(las)
        except:
          pass
      if las.position.x <= 0:
        try:
          self.laser.remove(las)
        except:
          pass
      if las.position.y >= HEIGHT:
        try:
          self.laser.remove(las)
        except:
          pass
      if las.position.y <= 0:
        try:
          self.laser.remove(las)
        except:
          pass

    while len(self.astero) < self.number_astro:
      postion = random_position(self.screen)
      if postion.distance_to(self.spaceship.position) >= self.min_distance_spawn:
        break
      self.astero.append(Astero(postion))

    if self.spaceship.target_health == 0:
      self.running = False

    if random.randint(0, 1500) == 1: self.heal.append(GameObject(random_position(self.screen), heal_sprite, Vector2(0)))

    for h in self.heal:
      if self.spaceship.collides_with(h):
        self.spaceship.get_health(75)
        self.heal.remove(h)

    for mis in self.missile:
      mis.move()
      if mis.position.x >= WIDTH:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)

        except:
          pass
      if mis.position.x <= 0:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
        except:
          pass
      if mis.position.y >= HEIGHT:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
        except:
          pass
      if mis.position.y <= 0:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
        except:
          pass
      for rock in self.astero:
        if mis.collides_with(rock) or mis.position.distance_to(rock.position) <= 64:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
          self.astero.remove(rock)

    if self.spaceship.target_health <= 200:
      pygame.mixer.Sound.play(low_lifeMUsic)

    for n in self.movingS:
      if n.attack_animation == False:
        self.movingS.remove(n)

    if self.score >= 700 and self.boss.target_health != 0:
      self.boss_fight = True
      self.astero = []

  def _draw(self):
    """
        Dessine le background et tous les objets qui ont une utilité
        Heal : objet qui sert a gagner des hp
        Las : le laser qui va etre tiré par la vaisseau
        Rock : asteroide
        Missile : missile qui peut exploser et faire des dêgats
    """

    self.background.fill(BLACK)
    for star in self.stars:
      pygame.draw.line(self.background,
                       WHITE, (star[0], star[1]), (star[0], star[1]))
      star[0] = star[0] - 1
      if star[0] < 0:
        star[0] = WIDTH
        star[1] = random.randint(0, HEIGHT)
    self.screen.blit(self.background, (0, 0))


    self.spaceship.draw(self.screen)



    for h in self.heal: h.draw(self.screen)
    for las in self.laser: las.draw(self.screen)
    for rock in self.astero: rock.draw(self.screen)
    for mis in self.missile: mis.draw(self.screen)

    self.movingS.update(0.2)
    self.movingS.draw(self.screen)

    self.spaceship.advanced_health(self.screen)
    draw_text("Score:", police, WHITE, self.screen, 870, 50)
    draw_text(str(self.score), police, WHITE, self.screen, 980, 50)

    # Flip the display
    self.clock.tick(FPS)
    pygame.display.flip()

  def _game_logig_Boss(self):
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

    for las in self.laser:
      las.move()
      if las.position.x >= WIDTH:
        try:
          self.laser.remove(las)
        except:
          pass
      if las.position.x <= 0:
        try:
          self.laser.remove(las)
        except:
          pass
      if las.position.y >= HEIGHT:
        try:
          self.laser.remove(las)
        except:
          pass
      if las.position.y <= 0:
        try:
          self.laser.remove(las)
        except:
          pass

    for las in self.laser:
      if las.collides_with(self.boss):
        self.score += 50
        self.boss.get_damage(50)
        try:
          self.laser.remove(las)
        except:
          pass
      for rock in self.astero:
        if las.collides_with(rock):
          try:
            self.astero.remove(rock)
          except:
            pass
          try:
            self.laser.remove(las)
          except:
            pass
          self.score += 50
          self.number_astro_kill += 1

    if self.spaceship.target_health == 0:
      self.running = False

    if random.randint(0, 1500) == 1: self.heal.append(GameObject(random_position(self.screen), heal_sprite, Vector2(0)))

    for h in self.heal:
      if self.spaceship.collides_with(h):
        self.spaceship.get_health(75)
        self.heal.remove(h)

    for mis in self.missile:
      mis.move()
      if mis.position.x >= WIDTH:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)

        except:
          pass
      if mis.position.x <= 0:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
        except:
          pass
      if mis.position.y >= HEIGHT:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
        except:
          pass
      if mis.position.y <= 0:
        try:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
        except:
          pass
      for rock in self.astero:
        if mis.collides_with(rock) or mis.position.distance_to(rock.position) <= 64:
          misil = Explosion(mis.position.x, mis.position.y)
          self.movingS.add(misil)
          misil.attack()
          self.missile.remove(mis)
          self.astero.remove(rock)
      if mis.collides_with(self.boss):
        self.score += 150
        misil = Explosion(mis.position.x, mis.position.y)
        self.movingS.add(misil)
        misil.attack()
        self.missile.remove(mis)
        self.boss.get_damage(100)

    if self.spaceship.target_health <= 200:
      pygame.mixer.Sound.play(low_lifeMUsic)

    for n in self.movingS:
      if n.attack_animation == False:
        self.movingS.remove(n)

    if self.boss.target_health <= 0:
      self.boss_fight = False
      self.score += 1000
      self.spaceship.get_health(500)

  def _draw_Boss(self):
    self.background.fill(BLACK)
    for star in self.stars:
      pygame.draw.line(self.background,
                       WHITE, (star[0], star[1]), (star[0], star[1]))
      star[0] = star[0] - 1
      if star[0] < 0:
        star[0] = WIDTH
        star[1] = random.randint(0, HEIGHT)
    self.screen.blit(self.background, (0, 0))

    self.spaceship.draw(self.screen)
    self.boss.draw(self.screen)

    for h in self.heal: h.draw(self.screen)
    for las in self.laser: las.draw(self.screen)
    for rock in self.astero: rock.draw(self.screen)
    for mis in self.missile: mis.draw(self.screen)

    self.spaceship.advanced_health(self.screen)
    self.boss.advanced_health(self.screen)

    # Flip the display
    self.clock.tick(FPS)
    pygame.display.flip()

  def _endScreen(self):
    """
        L'écran d'affichage quand le jeu est terminé
    """
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

