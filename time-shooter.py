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

    # set up screenx
    SCREEN = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    pygame.display.set_caption('Time-Shooter')
    SCREEN.fill(BGCOLOR)

    # starting position for ship
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
            if (event.type == pygame.QUIT) or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        ## Sets game-wide time-slowing variable
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
        if keystate[pygame.K_LEFT] and \
        playerShip.in_bounds('left',WINAREA):
            playerShip.set_velx(playerShip.defspeed * -1)
        elif keystate[pygame.K_RIGHT] and \
            playerShip.in_bounds('right',WINAREA):
            playerShip.set_velx(playerShip.defspeed)
        else:
            playerShip.set_velx(0)

        if keystate[pygame.K_UP] and \
            playerShip.in_bounds('top',WINAREA):
            playerShip.set_vely(playerShip.defspeed)
        elif keystate[pygame.K_DOWN] and \
            playerShip.in_bounds('bottom',WINAREA):
            playerShip.set_vely(playerShip.defspeed * -1)
        else:
            playerShip.set_vely(0)

        if keystate[pygame.K_LSHIFT] or keystate[pygame.K_RSHIFT]:
            # Keeps bullet interval fixed
            rightNow = pygame.time.get_ticks()
            if rightNow - playerShip.timeNow > BULDELAY:
                b = playerShip.fire_bullet(SCREEN)
                # b.color = random_color()
                allMobs.append(b)
                playerShip.timeNow = rightNow
        
        moved.append(playerShip)
        ## End ship controls ##

        ## Enemy behavior ##
        ## End enemy behavior ##
    
        ##Testing##
        if keystate[pygame.K_s]:
            t = Enemy(200,300)
            t.draw(SCREEN)
            t.behavior = "straightright"
            allMobs.append(t)
        ##Testing##

        ## Update all positions, velocities

        # If mob ofscreen, delete it
        for mob in allMobs:
            if not mob.in_area(WINAREA):
                allMobs.remove(mob)
                
            # Moves Enemy instances according to ai_accel()
            if isinstance(mob,Enemy):
                mob.ai_accel()
                b = [t.rect for t in allMobs if isinstance(t,Bullet)]
                if mob.rect.collidelist(b) != -1:
                    corpse = mob.rect
                    allMobs.remove(mob)
                    SCREEN.fill(BGCOLOR,rect=corpse)
                b = []
            # Erases mob, then redraws in new area
            SCREEN.fill(BGCOLOR,rect=mob.rect)
            to_update.append(mob.rect)
            mob.move()
            mob.draw(SCREEN)
            to_update.append(mob.rect)

        pygame.display.update(to_update)
        to_update = []
        
        # Prints all of the current mobs on-screen to terminal.
        # Careful, outputs a LOT.
        print allMobs

        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
