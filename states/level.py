import pygame
from pathlib import PurePath
from states.state import State

class GameLevel(State):
    def __init__(self, game):
        State.__init__(self, game)
    
    def update(self):
        pass

    def render(self, surface):
        pass

class Player():
    pass

class Ball():
    pass

class Block():
    pass

class Powerup():
    pass
