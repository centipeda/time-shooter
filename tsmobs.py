"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class MobGroup(pygame.sprite.Group):
    """Meant to hold all mobs in the game."""
    def __init__(self):
        super(MobGroup,self).__init__()

    def slow_down(self):
        """Sets slow value to True for all mobs in group."""
        for sprite in self.sprites():
            sprite.slow = True

    def speed_up(self):
        """Sets slow value to False for all mobs in group."""
        for sprite in self.sprites():
            sprite.slow = False


class Mob(pygame.sprite.DirtySprite):
    """Base class for all mobile objects in time-shooter."""
    defspeed = 0
    slowfactor = SLOWFACTOR
    height = 0
    width = 0
    rect = None
    color = None
    slow = False

    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Mob,self).__init__()
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.dirty = 2 # All mobs update

    def update(self):
        """Adjusts coordinates according to move(),
        then readjusts rect coordinates."""
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
        """Sets image attribute to a Surface so Group.draw()
        can be called. Also used when recoloring a mob."""
        # Needs to be called during children __init__ to fill
        # image attribute of sprite for initial Group.draw() call.
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.color)

    def in_bounds(self,area,bound):
        """Checks if Mob is inside a given area."""
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
        self.width = SHIPWIDTH
        self.height = SHIPHEIGHT
        self.color = WHITE
        self.sketch()
        self.defspeed = DEFSHIPSPEED
        self.ticks = pygame.time.get_ticks()
        self.shootdelay = PLAYERBULDELAY

    def move(self):
        """Overriden from Mob to make Ship not slowed down by
        slow attribute."""
        self.xpos += self.xvel
        self.ypos += self.yvel * -1

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
        """Calls fire_bullet() if space is held."""
        if keystate[pygame.K_SPACE]:
            fire = self.fire_bullet()
            return fire # Heh.

    def fire_bullet(self):
        """Creates a Bullet object traveling upward if delay
        requirements are met."""
        now = pygame.time.get_ticks()
        if now - self.ticks > self.shootdelay:
            self.ticks = pygame.time.get_ticks()
            fire = Bullet(self.rect.center[0],
                          self.rect.center[1])
            fire.yvel = fire.defspeed
            return fire

    def take_hit(self,healthbar,damage):
        healthbar.decrement_health(damage)
        
    def check_health(self,healthbar):
        if healthbar.health <= 0:
            return True
        
        
class Enemy(Mob):
    """Base class for all enemies."""
    def __init__(self,xpos,ypos,xvel=0,yvel=0,behavior="stop"):
        super(Enemy,self).__init__(xpos,ypos,xvel,yvel)
        self.behavior = behavior
        self.basesize = ENEMYBASESIZE
        self.shootdelay = ENEMYBULDELAY
        self.target = None
        self.ticks = pygame.time.get_ticks()
        self.update()

    def fire_bullet(self):
        """Fires bullet, but colors it red."""
        now = pygame.time.get_ticks()
        if now - self.ticks > self.shootdelay:
            self.ticks = pygame.time.get_ticks()
            fire = Bullet(self.rect.center[0],
                          self.rect.center[1])
            fire.enemy = True
            fire.color = ENEMYBULCOLOR
            fire.yvel = -1 * fire.defspeed
            fire.sketch()
            return fire

    def ai_accel(self):
        """Adjusts velocity attributes according to behavior
        attributes and default speed values."""
        if self.behavior == "stop":
            self.xvel = 0
            self.yvel = 0
        elif self.behavior == "straightdown":
            self.xvel = 0
            self.yvel = -1 * self.defspeed
        elif self.behavior == "straightup":
            self.xvel = 0
            self.yvel = self.defspeed
        elif self.behavior == "straightup":
            self.xvel = 0
            self.yvel = self.defspeed
        elif self.behavior == "straightleft":
            self.xvel = -1 * self.defspeed
            self.yvel = 0
        elif self.behavior == "straightright":
            self.xvel = self.defspeed
            self.yvel = 0
        elif self.behavior == "diagdl":
            # Diagonal, down and to the left at a 45 degree angle.
            self.xvel = -1 * self.defspeed
            self.yvel = -1 * self.defspeed
        elif self.behavior == "diagdr":
            # Diagonal, down and to the right at a 45 degree angle.
            self.xvel = self.defspeed
            self.yvel = -1 * self.defspeed
        elif self.behavior == "random":
            # Random movement.
            # note - enemies tend to move down-left
            # when slow is true for some reason.
            margin = 3 # Changes how random movement is.
            self.xvel = randint(margin * -1,margin)
            self.yvel = randint(margin * -1,margin)
        elif self.behavior == "home":
            # Adjusts velocities to aim at a point.
            distx = self.target[0] - self.rect.center[0]
            disty = self.target[1] - self.rect.center[1]
            if distx == 0:
                distx += 1
            if disty == 0:
                disty += 1
                self.xvel = (distx / self.defspeed) / HOMINGFACTOR
            self.yvel = (( -1 * disty) / self.defspeed) / HOMINGFACTOR


class Bullet(Mob):
    """Base class for all bullets."""
    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(Bullet,self).__init__(xpos,ypos,xvel,yvel)
        self.width = BULWIDTH
        self.height = BULHEIGHT
        self.color = DEFBULCOLOR
        self.sketch()
        self.defspeed = DEFBULSPEED
        self.enemy = None

    
class SquareEnemy(Enemy):
    def __init__(self,xpos,ypos,xvel=0,yvel=0):
        super(SquareEnemy,self).__init__(xpos,ypos,xvel,yvel)
        self.color = GREEN
        self.width = self.basesize
        self.height = self.basesize
        self.sketch()
        self.defspeed = 3
