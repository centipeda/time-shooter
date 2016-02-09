"""Contains class definitions and various functions for time-shooter game."""

from tsconst import *
import pygame

class Mob():
    """Base class for all mobile objects in time-shooter."""
    def __init__(self):
        pass

class Ship(Mob):
    """Class for the player ship."""
    def __init__(self):
        pass

class Enemy(Mob):
    """Base class for all enemies."""
    def __init__(self):
        pass

class Bullet(Mob):
    """Base class for all bullets."""
    def __init__(self):
        pass
