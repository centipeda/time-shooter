"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class Ship():
    def __init__(self,posx,posy):
        self.height = SHIPH
        self.width = SHIPW
        self.posx = posx
        self.posy = posy
        self.rect = None
        self.color = WHITE
        
    def draw_basic(self):
        self.rect = pygame.Rect(self.posx,self.posy,
                                self.width,self.height)
        return self.rect

class _Enemy(): # meant for subclassing
    def __init__(self):
        pass

class Bullet():
    def __init__(self):
        pass

