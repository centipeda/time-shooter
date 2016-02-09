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
        self.defspeed = 0
        self.rect = None
        self.color = None
        self.slow = False
        self.slowfactor = SLOWFACTOR
    
    def draw(self,surf):
        """Sets the rect attribute to the current position of the Mob."""
        self.rect = pygame.Rect(self.posx,self.posy,
                                self.width,self.height)
        pygame.draw.rect(surf,self.color,self.rect)

    def move(self):
        """Adjusts posx and posy based on velx and vely.
        Affected by slow attribute."""
        if self.slow:
            self.posx += self.velx / self.slowfactor
            self.posy += ((-1 * self.vely) / self.slowfactor)
        else:
            self.posx += self.velx
            self.posy += (-1 * self.vely)
    
    def in_bounds(self,side,bounds):
        """Checks whether Mob is within a certain boundary."""
        if side == 'left':
            if self.rect.left > bounds.left:
                return True
        elif side == 'right':
            if self.rect.right < bounds.right:
                return True
        elif side == 'top':
            if self.rect.top > bounds.top:
                return True
        elif side == 'bottom':
            if self.rect.bottom < bounds.bottom:
                return True
        else:
            return False

    def in_area(self,rect):
        return self.rect.colliderect(rect)

    def set_velx(self,velocity):
        self.velx = velocity

    def set_vely(self,velocity):
        self.vely = velocity

class Ship(Mob):
    """Class for the player ship."""
    def __init__(self,posx,posy):
        Mob.__init__(self,posx,posy)
        self.height = SHIPH
        self.width = SHIPW
        self.color = WHITE
        self.defspeed = 6
        self.slowfactor = 1
        self.timeNow = pygame.time.get_ticks()

    def fire_bullet(self,surf):
        """Spawns a Bullet object in front of the Ship."""
        bullet = Bullet(self.rect.center[0],self.rect.top + 10)
        bullet.draw(surf)
        bullet.set_vely(bullet.defspeed)
        return bullet
    
class Enemy(Mob):
    """Base class for all enemies."""
    def __init__(self,posx,posy):
        Mob.__init__(self,posx,posy)
        self.width = 30
        self.height = 30
        self.color = GREEN
        self.behavior = None
        self.defspeed = 3
        self.createTime = pygame.time.get_ticks()

    def ai_accel(self):
        """Defines basic movement behaviors for enemies."""
        # Basic movement behaviors
        if self.behavior == "stop":
            self.velx = 0
            self.vely = 0
        elif self.behavior == "straightdown":
            self.velx = 0
            self.vely = -1 * self.defspeed
        elif self.behavior == "straightup":
            self.velx = 0
            self.vely = self.defspeed
        elif self.behavior == "straightright":
            self.velx = self.defspeed
            self.vely = 0
        elif self.behavior == "straightleft":
            self.velx = -1 * self.defspeed
            self.vely = 0
        elif self.behavior == "random":
            margin = 10
            self.velx = randint(self.defspeed * -1,self.defspeed)
            self.vely = randint(self.defspeed * -1,self.defspeed)
        elif self.behavior == "bounce":
            pass
        elif self.behavior == "zigzag":
            pass

class Bullet(Mob):
    """Base class for all bullets."""
    def __init__(self,posx,posy):
        Mob.__init__(self,posx,posy)
        self.width = BULW
        self.height = BULH
        self.color = WHITE
        self.defspeed = 8
        self.slowfactor += 2
# Specific class definitions

class SquareEnemy(Enemy):
    def __init__(self,posx,posy):
        Enemy.__init__(posx,posy)

class TriEnemy(Enemy):
    def __init__(self,posx,posy):
        Enemy.__init__(posx,posy)

class CircEnemy(Enemy):
    def __init__(self,posx,posy):
        Enemy.__init__(posx,posy)
