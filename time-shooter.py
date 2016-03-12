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

# In-game imports.
from tsconst import *
from tsmobs import *
from tshud import *
from tsevents import *

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
    hudparts = HudElementGroup()

    # Mob spawner
    mainSpawner = Spawner(0,0)

    # set up HUD
    scoreCounter = ScoreCounter()
    healthBar = HealthBar()
    scoreCounter.add(allMobs)
    scoreCounter.add(hudparts)
    healthBar.add(allMobs)
    healthBar.add(hudparts)

    # Ship starting position
    playerShip = Ship((WINWIDTH / 2),450)
    playerShip.add(allMobs)

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

        # Update HUD elements
        


        # Slow down time if either shift key is held
        if keystate[pygame.K_LSHIFT] or keystate[pygame.K_RSHIFT] and playerShip.alive():
            allMobs.slow_down()
        else:
            allMobs.speed_up()
            

        # Ship controls
        if playerShip.check_health(healthBar):
            playerShip.kill()
        playerShip.check_controls(keystate,WINAREA)
        blasted = playerShip.check_weapons(keystate)
        # Fires bullet if space is held
        if blasted is not None and playerShip.alive():
            blasted.update()
            blasted.add(bullets)
            blasted.add(allMobs)


        # Testing (Spawns enemies if "e" is pressed)
        if keystate[pygame.K_e]:
            o = randint(0,WINWIDTH)
            oo = randint(0,WINWIDTH)
            t = mainSpawner.spawn("SquareEnemy",random_color(),
                                  xoffset=o,yoffset=oo,)
            t.add(allMobs)
            t.add(enemies)
        if keystate[pygame.K_f]:
            line = mainSpawner.spawn_horiz_wall(50,5,100,"SquareEnemy",random_color())
            for a in line:
                a.add(allMobs)
                a.add(enemies)
                        

        # Testing (Respawns ship if "r" is pressed)
        if keystate[pygame.K_r] and not playerShip.alive():
            playerShip.add(allMobs)
            healthBar.health = DEFHEALTH

        # Enemy actions
        for enemy in enemies:
            enemy.ai_accel()
            # Retargets player if Enemy is set to homing.
            if enemy.behavior == "home":
                enemy.target = playerShip.rect.center
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
                    # If bullet is player's and is hitting enemy...
                    scoreCounter.increment_score(ENEMYKILLSCORE)
                    to_update.append(SCREEN.fill(BGCOLOR,enemy.rect))
                    to_update.append(SCREEN.fill(BGCOLOR,bullet.rect))
                    enemy.kill()
                    bullet.kill()
                    break
            if bullet.enemy:
                if playerShip.rect.colliderect(bullet.rect):
                    to_update.append(SCREEN.fill(BGCOLOR,playerShip.rect))
                     # reminder - make damage a class attribute
                    playerShip.take_hit(healthBar,ENEMYDAMAGE)
                    bullet.kill()

        # Dirty rect animation
        for mob in allMobs.sprites():
            # kills mob if offscreen
            if not mob.rect.colliderect(WINAREA):
                mob.kill()
            # Clears screen area where mob used to be
            SCREEN.fill(BGCOLOR,rect=mob.rect)
            to_update.append(mob.rect)
        # Redraws mob in new location
        allMobs.update()
        allMobs.draw(SCREEN)
        for mob in allMobs.sprites():
            to_update.append(mob.rect)

        pygame.display.update(to_update)

        # Keeps game at steady FPS
        fpsClock.tick(MAXFPS)


if __name__ == '__main__':
    main()
