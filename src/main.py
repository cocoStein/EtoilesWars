import pygame

from src.settings import *

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

# création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Etoiles Vso")


def main_window():
  GAME_RUNNING = True

  x_pose = 50
  y_pose = 50

  inputMap = [False, False, False, False]

  while GAME_RUNNING:

    # EVENT
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        GAME_RUNNING = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          inputMap[0] = True;
        if event.key == pygame.K_s:
          inputMap[1] = True;
        if event.key == pygame.K_a:
          inputMap[2] = True;
        if event.key == pygame.K_d:
          inputMap[3] = True;
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          inputMap[0] = False;
        if event.key == pygame.K_s:
          inputMap[1] = False;
        if event.key == pygame.K_a:
          inputMap[2] = False;
        if event.key == pygame.K_d:
          inputMap[3] = False;

    vso_speedX = 0
    if inputMap[2]: vso_speedX -= 1.5
    if inputMap[3]: vso_speedX += 1.5
    vso_speedY = 0
    if inputMap[0]: vso_speedY -= 1.5s
    if inputMap[1]: vso_speedY += 1.5

    x_pose += vso_speedX
    y_pose += vso_speedY

        # background
    screen.fill(DARKGRAY)

    #VSO tst
    vso = pygame.Rect(x_pose, y_pose, 50, 50)
    pygame.draw.rect(screen, RED, vso, 25)

    # Flip the display
    pygame.display.flip()


main_window()


#pygame.display.flip()