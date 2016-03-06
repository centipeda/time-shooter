"""Holds class definitions for all HUD elements in time-shooter."""

import pygame

from tsconst import *

class HudElementGroup(pygame.sprite.Group):
    def __init__(self):
        super(HudElementGroup,self).__init__()

class HudElement(pygame.sprite.DirtySprite):
    def __init__(self):
        super(HudElement,self).__init__()
        self.width = 0
        self.height = 0
        self.xpos = 0
        self.ypos = 0
        self.color = None
        self.rect = None
        self.image = None

    def update(self):
        """Sets rect attribute of HUD element.
        """
        self.rect = pygame.Rect(self.xpos,self.ypos,
                                self.width,self.height)

class HealthBar(HudElement):
    """Health bar, can be decreased and increased."""
    def __init__(self):
        super(HealthBar,self).__init__()
        self.xpos = HEALTHLOCATION[0]
        self.ypos = HEALTHLOCATION[1]
        self.width = HEALTHBARWIDTH
        self.height = HEALTHBARHEIGHT
        self.color = EMPTYHEALTHBARCOLOR
        self.fillcolor = HEALTHBARCOLOR
        self.health = DEFHEALTH

    def update(self):
        """Draws health bar as empty, then fills in amount of health needed."""
        self.rect = pygame.Rect((self.xpos,self.ypos,
                                 self.width,self.height))
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.color)
        filledarea = pygame.Rect((0,0,self.health,self.height))
        self.image.fill(self.fillcolor,filledarea)
        
    def increment_health(self,increase):
        """Increases health attribute. For readability."""
        self.health += increase
        
    def decrement_health(self,decrease):
        """Decreases health attribute. For readability."""
        self.health -= decrease


class ScoreCounter(HudElement):
    def __init__(self):
        super(ScoreCounter,self).__init__()
        self.xpos = SCORELOCATION[0]
        self.ypos = SCORELOCATION[1]
        self.fontsize = SCORESIZE
        self.text = pygame.font.Font(None,self.fontsize)
        self.score = 0
        self.color = SCORECOLOR

    def update(self):
        """Updates text attribute with current score value."""
        updated = self.text.render(str(self.score),False,self.color,BGCOLOR)
        self.image = updated
        self.rect = updated.get_rect()
        return self.image

    def increment_score(self,increase):
        """Increments score attribute, then adjusts image to fit.
        """
        self.score += increase
