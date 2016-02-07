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

    # set up screen
    SCREEN = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    pygame.display.set_caption('Time-Shooter')
    SCREEN.fill(BGCOLOR)

    # starting positions
    playerShip = Ship(((WINWIDTH / 2) - (SHIPH / 2)),
                      WINHEIGHT - SHIPH)

    pygame.draw.rect(SCREEN,playerShip.color,playerShip.draw_basic())

    while True: # main event loop
        to_update = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        to_update.append(playerShip.rect)
        pygame.display.update(to_update)

if __name__ == '__main__':
    main()
