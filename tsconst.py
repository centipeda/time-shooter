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
ENEMYKILLSCORE = 30
PLAYERBULDELAY = 50
ENEMYBULDELAY = 400
DEFSHIPSPEED = 6
DEFBULSPEED = 8
DEFBULCOLOR = WHITE
ENEMYBULCOLOR = RED

# Game HUD constants.
HEALTHBARWIDTH = 150
HEALTHBARHEIGHT = 30
HEALTHBARCOLOR = GREEN
DEFHEALTH = 100
SCORESIZE = 30
SCORECOLOR = BLUE
SCORELOCATION = (20,20)


# Game engine constants.
MAXFPS = 60
SLOWFACTOR = 3

# Creates random colors. No really practical use.
def random_color():
    return (randint(0,255),randint(0,255),randint(0,255))
