"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class Mob(pygame.sprite.DirtySprite):
    """Base class for all mobile objects in time-shooter."""

    self.defspeed = 0
    self.slowfactor = SLOWFACTOR
    self.height = None
    self.width = None
    self.rect = None
    self.color = None

    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Mob,self).__init__()
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.dirty = 2 # All mobs update

    def update(self,slow):
        """Updates xpos and ypos attributes according to xvel and yvel."""
        # Can be called with "slow" to divide velocity by slowfactor
        # to "slow down" time
        if slow:
            xpos += (xvel / self.slowfactor)
            ypos += ((yvel / self.slowfactor) / -1)
        else:
            xpos += xvel
            ypos += yvel * -1
            
class Ship(Mob):
    """Class for the player ship."""
    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Ship,self).__init__(xpos,ypos,xvel,yvel)

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
