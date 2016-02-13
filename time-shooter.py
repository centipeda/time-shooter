"""A sh'mup written with Pygame, with a small twist."""

# To-do:
# Add enemies, basic behavior, weapons
# Add HUD
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

    # Ship starting position
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
        else:
            allMobs.speed_up()
            

        # Ship controls
        playerShip.check_controls(keystate,WINAREA)
        blasted = playerShip.check_weapons(keystate)
        # Fires bullet if space is held
        if blasted is not None:
            blasted.update()
            blasted.add(bullets)
            blasted.add(allMobs)


        # Testing (Spawns enemies if "q" is pressed)
        if keystate[pygame.K_q]:
            spawn = SquareEnemy(randint(0,WINWIDTH),20)
            spawn.color = random_color()
            spawn.sketch()
            spawn.behavior = "straightleft"
            spawn.target = playerShip.rect.center
            spawn.update()
            spawn.add(allMobs)
            spawn.add(enemies)
            one = False


        # Enemy actions
        for enemy in enemies:
            enemy.ai_accel()
            # Retargets player if Enemy is set to homing.
            if enemy.behavior == "home":
                enemy.target = playerShip.rect.center
            ## testing ## - bounces enemies between walls.
            if not enemy.in_bounds(WINAREA,"left"):
                enemy.behavior = "straightright"
            elif not enemy.in_bounds(WINAREA,"right"):
                enemy.behavior = "straightleft"
            ## testing ##
            # Periodically fires bullets.
            checkwep = enemy.fire_bullet()
            if checkwep is not None:
                checkwep.update()
                checkwep.add(allMobs)
                checkwep.add(bullets)
            


        # Collision detection
        for bullet in bullets:
            for enemy in enemies:
                if enemy.rect.colliderect(bullet.rect) and not \
                   bullet.enemy:
                    to_update.append(SCREEN.fill(BGCOLOR,enemy.rect))
                    to_update.append(SCREEN.fill(BGCOLOR,bullet.rect))
                    enemy.kill()
                    bullet.kill()
                    break
            if bullet.enemy:
                if playerShip.rect.colliderect(bullet.rect):
                    playerShip.color = random_color()
                    playerShip.sketch()
                else:
                    playerShip.color = WHITE
                    playerShip.sketch()

        # Dirty rect animation
        for mob in allMobs.sprites():
            # kills mob if offscreen
            if not mob.rect.colliderect(WINAREA):
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
