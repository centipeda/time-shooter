"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class Mob():
    """Base class for all mobile objects in time-shooter."""
    def __init__(self,posx,posy):
        self.posx = posx
        self.posy = posy
        self.height = None
        self.width = None
        self.velx = 0
        self.vely = 0
        self.rect = None
        self.color = None
    
    def draw(self,surf):
        self.rect = pygame.Rect(self.posx,self.posy,
                                self.width,self.height)
        pygame.draw.rect(surf,self.color,self.rect)

    def move(self):
        self.posx = self.posx + self.velx
        self.posy = self.posy + -1 * self.vely

    def in_bounds(self,side):
        if side == 'left':
            if self.rect.left > 0:
                return True
        elif side == 'right':
            if self.rect.right < WINWIDTH:
                return True
        elif side == 'top':
            if self.rect.top > 0:
                return True
        elif side == 'bottom':
            if self.rect.bottom < WINHEIGHT:
                return True
        else:
            return False

class Ship(Mob):
    """Class for the player ship."""
    def __init__(self,posx,posy):
        Mob.__init__(self,posx,posy)
        self.height = SHIPH
        self.width = SHIPW
        self.color = WHITE

class Enemy(Mob):
    """Base class for all enemies."""
    def __init__(self,posx,posy):
        Mob.__init__(self,posx,posy)

class Bullet(Mob):
    """Base class for all bullets."""
    def __init__(self,posx,posy):
        Mob.__init__(self,posx,posy)

# Specific class definitions
class SquareEnemy(Enemy):
    def __init__(self,posx,posy):
        Enemy.__init__(posx,posy)
