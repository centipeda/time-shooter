"""A sh'mup written with Pygame, with a small twist."""

# To-do:
# Add sprites
# Add backgrounds
# Add sounds, music
# Add splash screen, menu

import sys
import time
import pygame
from tsgame import *

def main():

    pygame.init()

    setup_screen()

    if start_menu() == "play":
        setup_game()
        play_game()
    
    nice_exit()

if __name__ == '__main__':
    main()
