"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class MobGroup(pygame.sprite.Group):
    def __init__(self):
        super(MobGroup,self).__init__()

    def slow_down(self):
        for sprite in self.sprites():
            sprite.slow = True

    def speed_up(self):
        for sprite in self.sprites():
            sprite.slow = False

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

    def in_bounds(self,area,bound):
        """Checks if Mob is inside area (Rect)"""
        if bound == "all":
            return self.rect.colliderect(area)
        elif bound == "left":
            if self.rect.left > area.left:
                return True
        elif bound == "right":
            if self.rect.right < area.right:
                return True
        elif bound == "top":
            if self.rect.top > area.top:
                return True
        elif bound == "bottom":
            if self.rect.bottom < area.bottom:
                return True

            
class Ship(Mob):
    """Class for the player ship."""
    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Ship,self).__init__(xpos,ypos,xvel,yvel)
        self.width = 30
        self.height = 40
        self.color = WHITE
        self.sketch()
        self.defspeed = 8
        self.shootdelay = 50
        self.ticks = pygame.time.get_ticks()

    def check_controls(self,keystate,screen):
        """Alters velocity attributes according to keypresses.

        keystate should be the list returned by
        pygame.key.get_pressed()."""

        if (keystate[pygame.K_UP] or keystate[pygame.K_w]) and \
           (self.in_bounds(screen,"top")):
            self.yvel = self.defspeed
        elif (keystate[pygame.K_DOWN] or keystate[pygame.K_s]) and \
             (self.in_bounds(screen,"bottom")):
            self.yvel = self.defspeed * -1
        else:
            self.yvel = 0

        if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and \
           (self.in_bounds(screen,"left")):
            self.xvel = self.defspeed * -1
        elif (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) \
             and (self.in_bounds(screen,"right")):
            self.xvel = self.defspeed
        else:
            self.xvel = 0

    def check_weapons(self,keystate):
        if keystate[pygame.K_SPACE]:
            return self.fire_bullet()

    def fire_bullet(self):
        now = pygame.time.get_ticks()
        if now - self.ticks > self.shootdelay:
            self.ticks = pygame.time.get_ticks()
            fired = Bullet(self.rect.center[0],
                           self.rect.center[1] + 10)
            fired.fire()
            return fired


class Enemy(Mob):
    """Base class for all enemies."""
    def __init__(self,behavior="stop"):
        super(Enemy,self).__init__(xpos,ypos,xvel=0,yvel=0)
        self.behavior = behavior
        self.width = 30
        self.height = 30
        self.sketch()

    def ai_accel(self):
        if self.behavior == "stop":
            self.xvel = 0
            self.yvel = 0
        elif self.behavior == "straightdown":
            self.xvel = 0
            self.yvel = self.defspeed * -1
        elif self.behavior == "straightup":
            self.xvel = 0
            self.yvel = self.defspeed
        # etcetera

class Bullet(Mob):
    """Base class for all bullets."""
    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Bullet,self).__init__(xpos,ypos,xvel,yvel)
        self.width = 5
        self.height = 10
        self.color = WHITE
        self.defspeed = 10
        self.sketch()

    def fire(self):
        self.yvel = self.defspeed
