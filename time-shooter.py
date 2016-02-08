"""A sh'mup written with Pygame, with a small twist."""

# To-do:
# Create main window
# Add player ship, basic controls, weapons
# Add enemies, basic behavior, weapons
# Add HUD
# Add time-slowing functionality
# Add backgrounds
# Add sounds, music
# Add splash screen, menu

import sys
import pygame

from tsconst import *
from tsclass import *

def main():

    pygame.init()

    fpsClock = pygame.time.Clock()

    # set up screen
    SCREEN = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    pygame.display.set_caption('Time-Shooter')
    SCREEN.fill(BGCOLOR)

    # starting positions
    playerShip = Ship(((WINWIDTH / 2) - (SHIPH / 2)),
                      WINHEIGHT - SHIPH)
    playerShip.draw(SCREEN)

    while True: # main event loop
        to_update = []
        keystate = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Sets game-wide time-slowing variable
        if keystate[pygame.K_SPACE]:
            timeSlow = True
        else:
            timeSlow = False

        # Setting ship speed constants
        if timeSlow:
            shipSpeed = SLOWSHIPSPEED
        else:
            shipSpeed = DEFSHIPSPEED

        # Ship speed controls, keeps ship in bounds
        if keystate[pygame.K_LEFT] and playerShip.in_bounds('left'):
            playerShip.velx = -1 * shipSpeed
        elif keystate[pygame.K_RIGHT] and playerShip.in_bounds('right'):
            playerShip.velx = shipSpeed
        else:
            playerShip.velx = 0

        if keystate[pygame.K_UP] and playerShip.in_bounds('top'):
            playerShip.vely = shipSpeed
        elif keystate[pygame.K_DOWN] and playerShip.in_bounds('bottom'):
            playerShip.vely = -1 * shipSpeed
        else:
            playerShip.vely = 0
        
        # Update ship position
        SCREEN.fill(BGCOLOR,rect=playerShip.rect)
        to_update.append(playerShip.rect)
        playerShip.move()
        playerShip.draw(SCREEN)
        to_update.append(playerShip.rect)
        
        # Dirty rect animation
        pygame.display.update(to_update)
        
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
