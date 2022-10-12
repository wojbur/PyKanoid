import pygame
from pathlib import PurePath
from states.state import State
# from states.main_menu import MainMenu

class GameLevel(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.player = Player(self.game)
    
    def update(self, delta_time, keys):
        # if keys['exit']:
            # new_state = MainMenu(self.game)
            # new_state.enter_state()
        self.player.update(delta_time, keys)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.player.render(surface)

class Player():
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(PurePath(game.sprites_dir, 'player', 'paddle_1.png'))
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
        print(self.rect)


    def render(self, surface):
        surface.blit(self.image, self.rect)
        

class Ball():
    pass

class Block():
    pass

class Powerup():
    pass
