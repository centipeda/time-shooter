"""Contains constants for time-shooter game."""
from random import randint
import pygame

# Window constants.
WINHEIGHT = 600
WINWIDTH = 400
WINAREA = pygame.Rect(0,0,WINWIDTH,WINHEIGHT)

# Color constants.
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BGCOLOR = BLACK

# Game sprite constants.
SHIPHEIGHT = 30
SHIPWIDTH = 20
BULHEIGHT = 10
BULWIDTH = 5
ENEMYBASESIZE = 30
ENEMYKILLSCORE = 10 # Points for killing an enemy.
ENEMYDAMAGE = 100
PLAYERBULDELAY = 150 
ENEMYBULDELAY = 400
DEFSHIPSPEED = 6
DEFBULSPEED = 10
DEFBULCOLOR = WHITE
ENEMYBULCOLOR = RED

# Game HUD constants.
DEFHEALTH = 300
HEALTHBARWIDTH = DEFHEALTH
HEALTHBARHEIGHT = 20
HEALTHBARCOLOR = GREEN
EMPTYHEALTHBARCOLOR = RED
HEALTHLOCATION = (10,WINHEIGHT - 30)
SCORESIZE = 30
SCORECOLOR = BLUE
SCORELOCATION = (20,20)


# Game engine constants.
MAXFPS = 60
SLOWFACTOR = 3 # Changes how much time is slowed by.
# Adjusts how quickly enemies home in on a position when behavior is set to "home".
HOMINGFACTOR = 20
WAVEDELAY = 50 # Manages delay between waves of enemies.

# Creates random colors. No really practical use.
def random_color():
    return (randint(0,255),randint(0,255),randint(0,255))
