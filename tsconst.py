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
SHIPH = 30
SHIPW = 20
BULH = 10
BULW = 5
BULDELAY = 100
DEFSHIPSPEED = 6
DEFBULSPEED = 10

# Game engine constants.
FPS = 60

SLOWFACTOR = 5

# Creates random colors.
def random_color():
    return (randint(0,255),randint(0,255),randint(0,255))
