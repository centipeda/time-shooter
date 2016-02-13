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
import time
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

    # Groups for holding mobs
    allMobs = MobGroup()
    enemies = MobGroup()
    bullets = MobGroup()

    # ship starting position
    playerShip = Ship((WINWIDTH / 2),450)
    playerShip.add(allMobs)

    # Testing

    # Initializes mobs
    allMobs.update()
    allMobs.draw(SCREEN)
    pygame.display.update()

    while True: # main event loop
        to_update = []
        keystate = pygame.key.get_pressed()

        # Handling for events from the event queue
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
               (event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()


        # Slow down time if either shift key is held
        if keystate[pygame.K_LSHIFT] or keystate[pygame.K_RSHIFT]:
            allMobs.slow_down()
            # pass
        else:
            allMobs.speed_up()
            

        # Ship controls
        playerShip.check_controls(keystate,SCREEN.get_rect())
        blasted = playerShip.check_weapons(keystate)
        if blasted is not None:
            blasted.update()
            blasted.add(bullets)
            blasted.add(allMobs)

        # Testing
        if keystate[pygame.K_q]:
            spawn = SquareEnemy(300,300)
            spawn.color = random_color()
            spawn.sketch()
            spawn.behavior = "home"
            spawn.target = playerShip.rect.center
            spawn.update()
            spawn.add(allMobs)
            spawn.add(enemies)
            one = False


        # Enemy actions
        for enemy in enemies:
            enemy.ai_accel()
            if enemy.behavior == "home":
                enemy.target = playerShip.rect.center


        # Collision detection
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    to_update.append(SCREEN.fill(BGCOLOR,enemy.rect))
                    to_update.append(SCREEN.fill(BGCOLOR,bullet.rect))
                    enemy.kill()
                    bullet.kill()


        # Dirty rect animation
        for mob in allMobs.sprites():
            # kills mob if offscreen
            if not mob.rect.colliderect(SCREEN.get_rect()):
                mob.kill()
            SCREEN.fill(BGCOLOR,rect=mob.rect)
            to_update.append(mob.rect)
        allMobs.update()
        allMobs.draw(SCREEN)
        for mob in allMobs.sprites():
            to_update.append(mob.rect)

        pygame.display.update(to_update)

        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
