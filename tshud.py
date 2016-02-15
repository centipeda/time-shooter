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

    def update(self):
        """Sets rect attribute and image attribute of HUD element.
        """
        self.rect = pygame.Rect(self.xpos,self.ypos,
                                self.width,self.height)

class HealthBar(HudElement):
    def __init__(self):
        super(HealthBar,self).__init__()
        self.width = HEALTHBARWIDTH
        self.height = HEALTHBARHEIGHT
        self.color = HEALTHBARCOLOR
        self.health = DEFHEALTH

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
        updated = self.text.render(str(self.score),False,self.color,BGCOLOR)
        self.image = updated
        self.rect = updated.get_rect()
        return self.image

    def increment_score(self,increase):
        """Increments score attribute, then adjusts image to fit.
        """
        self.score += increase
