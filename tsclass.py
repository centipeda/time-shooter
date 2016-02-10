"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class Mob(pygame.sprite.DirtySprite):
    """Base class for all mobile objects in time-shooter."""
    defspeed = 0
    slowfactor = SLOWFACTOR
    height = 0
    width = 0
    rect = None
    color = WHITE
    slow = False

    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Mob,self).__init__()
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.dirty = 2 # All mobs update

    def update(self):
        self.move()
        self.rect = pygame.Rect((self.xpos,self.ypos,
                                 self.width,self.height))

    def move(self):
        """Updates xpos and ypos attributes according to xvel and yvel."""
        # Can be called with "slow" to divide velocity by slowfactor
        # to "slow down" time
        if self.slow:
            self.xpos += (self.xvel / self.slowfactor)
            self.ypos += ((self.yvel / self.slowfactor) / -1)
        else:
            self.xpos += self.xvel
            self.ypos += self.yvel * -1

    def sketch(self):
        # Needs to be called during children __init__ to fill
        # image attribute of sprite.
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.color)
        
            
class Ship(Mob):
    """Class for the player ship."""
    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Ship,self).__init__(xpos,ypos,xvel,yvel)
        self.width = 30
        self.height = 40
        self.color = WHITE
        self.defspeed = 8
        self.sketch()
        

class Enemy(Mob):
    """Base class for all enemies."""
    def __init__(self,behavior="stop"):
        super(Enemy,self).__init__(xpos,ypos,xvel,yvel)
        self.behavior = behavior

    def ai_accel(self):
        if self.behavior == "stop":
            self.xvel = 0
            self.yvel = 0

class Bullet(Mob):
    """Base class for all bullets."""
    def __init__(self):
        super(Bullet,self).__init__(xpos,ypos,xvel,yvel)
