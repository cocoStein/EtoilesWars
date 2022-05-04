from src.settings import *

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

# création de la fenêtre
screen = pygame.display.set_mode((800, 800))
#pygame.display.set_caption("Water Rocket")

while game_run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_run = False



pygame.display.flip()