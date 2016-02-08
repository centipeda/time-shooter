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

    # Mob list, used for updating
    allMobs = []
    moved = []
    allMobs.append(playerShip)
    moved.append(playerShip)

    while True: # main event loop
        to_update = []
        keystate = pygame.key.get_pressed()

        # Handling for events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Sets game-wide time-slowing variable
        if keystate[pygame.K_SPACE]:
            timeSlow = True
            for mob in allMobs:
                mob.slow = timeSlow
        else:
            timeSlow = False
            for mob in allMobs:
                mob.slow = timeSlow

        ## Ship controls ##

        # Ship movement controls, keeps ship in bounds
        if keystate[pygame.K_LEFT] and playerShip.in_bounds('left'):
            playerShip.set_velx(playerShip.defspeed * -1)
        elif keystate[pygame.K_RIGHT] and playerShip.in_bounds('right'):
            playerShip.set_velx(playerShip.defspeed)
        else:
            playerShip.set_velx(0)

        if keystate[pygame.K_UP] and playerShip.in_bounds('top'):
            playerShip.set_vely(playerShip.defspeed)
        elif keystate[pygame.K_DOWN] and playerShip.in_bounds('bottom'):
            playerShip.set_vely(playerShip.defspeed * -1)
        else:
            playerShip.set_vely(0)

        if keystate[pygame.K_LSHIFT] or keystate[pygame.K_RSHIFT]:
            # Keeps bullet interval fixed
            rightNow = pygame.time.get_ticks()
            if rightNow - playerShip.timeNow> BULDELAY:
                allMobs.append(playerShip.fire_bullet(SCREEN))
                playerShip.timeNow = rightNow

        moved.append(playerShip)

        ## End ship controls ##

        # Update all positions, velocities
        for mob in allMobs:
            SCREEN.fill(BGCOLOR,rect=mob.rect)
            to_update.append(mob.rect)
            mob.move()
            mob.draw(SCREEN)
            to_update.append(mob.rect)

        # currently unecessary and/or inefficient
        """ # Deletes mobs not onscreen
        for mob in allMobs:
            if not mob.in_bound("all"):
                del(mob)"""

        pygame.display.update(to_update)
        to_update = []

        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
