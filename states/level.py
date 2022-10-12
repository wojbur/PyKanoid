import pygame
from pathlib import PurePath
from states.state import State
from math import cos, sin
from math import pi as PI

vector = pygame.math.Vector2
# from states.main_menu import MainMenu

class GameLevel(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.player = Player(self.game)
        self.ball = Ball(self.game, game.GAME_WIDTH/2, game.GAME_HEIGHT/2)
    
    def update(self, delta_time, keys):
        if keys['escape']:
            self.exit_state()
        self.player.update(delta_time, keys)
        self.ball.update(delta_time, keys)
        self.game.reset_keys()

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.player.render(surface)
        self.ball.render(surface)

class Player():
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(PurePath(game.sprites_dir, 'player', 'paddle.png'))
        self.rect = self.image.get_rect()
        self.rect.centerx = game.GAME_WIDTH/2
        self.rect.bottom = game.GAME_HEIGHT - 14

        self.width = self.rect[2]
    
    def update(self, delta_time, keys):
        # Scale mouse position to the display surface
        mouse_x = pygame.mouse.get_pos()[0] * (self.game.GAME_WIDTH / self.game.SCREEN_WIDTH)
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.game.GAME_WIDTH:
            self.rect.right = self.game.GAME_WIDTH

    def render(self, surface):
        surface.blit(self.image, self.rect)
        

class Ball():
    def __init__(self, game, x, y):
        self.game = game
        self.image = pygame.image.load(PurePath(game.sprites_dir, 'ball', 'ball.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 400
        self.angle = 0.25*PI

        # Kinematic vectors
        self.position = vector(x, y)
        self.velocity = vector(sin(self.angle)*self.speed, cos(self.angle)*self.speed)
    
    def update(self, delta_time, keys):
        self.position += self.velocity * delta_time
        self.rect.center = self.position

    def render(self, surface):
        surface.blit(self.image, self.rect)


        



class Block():
    pass

class Powerup():
    pass
