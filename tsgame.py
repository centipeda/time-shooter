
<<<<<<< HEAD:time-shooter.py
# To-do:
# Add sprites
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

def setup_screen():
    global SCREEN
    SCREEN = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    pygame.display.set_caption('Time-Shooter')
    SCREEN.fill(BGCOLOR)

def start_menu():
    return "play" # For now.

def setup_game():
    # Set global game variables
    global fpsClock
    global allMobs,enemies,bullets,hudparts
    global mainSpawner,eventStarter
    global scoreCounter,healthBar
    global playerShip

    fpsClock = pygame.time.Clock()

    # Groups for holding mobs
    allMobs = MobGroup()
    enemies = MobGroup()
    bullets = MobGroup()
    hudparts = HudElementGroup()

    # Mob spawner
    mainSpawner = Spawner(0,0)

    # Event starter
    eventStarter = EventGenerator()

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


def play_game():
    done = False
    frame = 0
    while not done: # main event loop
        to_update = []
        keystate = pygame.key.get_pressed()

        # Handling for events from the event queue
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        # Prints score to console on death            
        if not playerShip.alive():
            print "Final score: ",scoreCounter.score
            done = True

        # Slow down time if either shift key is held
        if keystate[pygame.K_LSHIFT] or keystate[pygame.K_RSHIFT] and playerShip.alive():
            allMobs.slow_down()
            slow = True
        else:
            allMobs.speed_up()
            slow = False
            

        # Ship controls
        if playerShip.check_dead(healthBar):
            playerShip.kill()
        # Health only regens when time isn't slowed
        elif (healthBar.health < healthBar.maxhealth) and (not slow):
            healthBar.health += 1
        playerShip.check_controls(keystate,WINAREA)
        blasted = playerShip.check_weapons(keystate)
        # Fires bullet if space is held
        if blasted is not None and playerShip.alive():
            blasted.update()
            blasted.add(bullets)
            blasted.add(allMobs)


        # Spawns waves of enemies
        if frame % WAVEDELAY == 0:
            wave = eventStarter.launch_wave(mainSpawner)
            if type(wave) == type([]):
                for mob in wave:
                    mob.add(allMobs)
                    mob.add(enemies)
            else:
                wave.add(allMobs)
                wave.add(enemies)
        mainSpawner.defcolor = random_color()

        # Enemy actions
        for enemy in enemies:
            # Retargets player if Enemy is set to homing.
            if enemy.behavior == "home":
                enemy.target = playerShip.rect.center
            enemy.ai_accel()
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
            
        pygame.display.update()#to_update)
        SCREEN.fill(BGCOLOR)
        
        frame += 1
        # keep it at steady FPS
        fpsClock.tick(MAXFPS)

def nice_exit():
    pygame.quit()
    sys.exit()
