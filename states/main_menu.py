import pygame
from pathlib import PurePath

from states.state import State
from states.level import GameLevel
from states.options import MenuOptions
from states.scores import HighScores

class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.menu_options = {0: 'START GAME', 1: 'OPTIONS', 2: 'HIGH SCORES', 3: 'QUIT'}
        self.index = 0

        self.title_font1 = self.set_font('FastHand-lgBMV.ttf', 140)
        self.title_font2 = self.set_font('FastHand-lgBMV.ttf', 150)
        self.title_font3 = self.set_font('FastHand-lgBMV.ttf', 160)
        self.menu_font = self.set_font('PilotCommand-3zn93.ttf', 50)
        self.menu_choose_font1 = self.set_font('PilotCommand-3zn93.ttf', 48)
        self.menu_choose_font2 = self.set_font('PilotCommand-3zn93.ttf', 51)

        self.menu_blip = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'menu_blip.wav'))
    
    def update(self, delta_time, keys):
        self.update_curson(keys)
        if keys['enter']:
            self.transition_state()
        self.game.reset_keys()

    def set_font(self, name, size):
        return self.game.load_font(name, size)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.game.draw_text(surface, self.menu_choose_font1, self.menu_options[self.index], (127, 112, 138), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2 - 90 + self.index*60)
        self.game.draw_text(surface, self.title_font1, 'PYKANOID', (127, 112, 138), self.game.GAME_WIDTH/2, 100)
        self.game.draw_text(surface, self.title_font2, 'PYKANOID', (255, 255, 255), self.game.GAME_WIDTH/2, 100)
        self.game.draw_text(surface, self.title_font3, 'PYKANOID', (77, 155, 230), self.game.GAME_WIDTH/2, 100)
        self.game.draw_text(surface, self.menu_font, 'START GAME', (255, 255, 255), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2 - 90)
        self.game.draw_text(surface, self.menu_font, 'OPTIONS', (255, 255, 255), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2 - 30)
        self.game.draw_text(surface, self.menu_font, 'HIGH SCORES', (255, 255, 255), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2 + 30)
        self.game.draw_text(surface, self.menu_font, 'QUIT', (255, 255, 255), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2 + 90)
        self.game.draw_text(surface, self.menu_choose_font2, self.menu_options[self.index], (77, 155, 230), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2 - 90 + self.index*60)
        # surface.blit(self.circle_surf(200, (20, 20, 20)), (200,200), special_flags=pygame.BLEND_RGB_ADD)
        # surface.blit(self.circle_surf(150, (30, 0, 0)), (200,200), special_flags=pygame.BLEND_RGB_ADD)
    
    def update_curson(self, keys):
        if keys['down']:
            self.menu_blip.play()
            self.index = (self.index + 1) % len(self.menu_options)
        if keys['up']:
            self.menu_blip.play()
            self.index = (self.index - 1) % len(self.menu_options)
    
    def transition_state(self):
        if self.menu_options[self.index] == 'START GAME':
            new_state = GameLevel(self.game)
            new_state.enter_state()
        if self.menu_options[self.index] == 'OPTIONS':
            new_state = MenuOptions(self.game)
            new_state.enter_state()
        if self.menu_options[self.index] == 'HIGH SCORES':
            new_state = HighScores(self.game)
            new_state.enter_state()
        if self.menu_options[self.index] == 'QUIT':
            self.game.playing = False
            self.game.running = False




        
        

        
