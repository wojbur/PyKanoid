import time, pygame
from pathlib import PurePath

from states.main_menu import MainMenu

class Game():
    def __init__(self):
        '''Initialize the game'''
        pygame.init()
        # Make mouse cursor invisible and lock it in screen boundaries
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        # Set up display
        self.GAME_WIDTH, self.GAME_HEIGHT = 1280, 960
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 960
        self.game_canvas = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # Set up game values
        self.running, self.playing = True, True
        self.keys = {'up': False, 'down': False, 'left': False, 'right': False, 'space': False, 'enter':False, 'escape': False}
        # Set up time values to make the game speed time dependent, not FPS dependent
        self.dt, self.prev_time = 0, 0
        # Set up game stack to contain different game states
        self.state_stack = []
        # 
        self.load_assets()
        self.load_states()

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            # print(1/self.dt) # FPS count for performance testing

    def get_events(self):
        # Lock the mouse inside game boundaries
        pygame.event.set_grab(True)
        
        for event in pygame.event.get():
            # Check if the user wants to quit
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            # Key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keys['up'] = True
                if event.key == pygame.K_DOWN:
                    self.keys['down'] = True
                if event.key == pygame.K_LEFT:
                    self.keys['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.keys['right'] = True
                if event.key == pygame.K_RETURN:
                    self.keys['enter'] = True
                if event.key == pygame.K_ESCAPE:
                    self.keys['escape'] = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keys['up'] = False
                if event.key == pygame.K_DOWN:
                    self.keys['down'] = False
                if event.key == pygame.K_LEFT:
                    self.keys['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.keys['right'] = False
                if event.key == pygame.K_RETURN:
                    self.keys['enter'] = False
                if event.key == pygame.K_ESCAPE:
                    self.keys['escape'] = False
    

    def update(self):
        self.state_stack[-1].update(self.dt, self.keys)
    
    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()
    

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
    

    def draw_text(self, surface, font, text, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)
    
    def load_assets(self):
        # Create pointers to directiries
        self.assets_dir = PurePath('assets')
        self.sprites_dir = PurePath(self.assets_dir, 'sprites')
        self.font_dir = PurePath(self.assets_dir, 'fonts')
        self.sounds_dir = PurePath(self.assets_dir, 'sounds')
    
    def load_font(self, name, size):
        return pygame.font.Font(PurePath(self.font_dir, name), size)
    
    def load_states(self):
        self.main_menu = MainMenu(self)
        self.state_stack.append(self.main_menu)
    

    def reset_keys(self):
        for key in self.keys:
            self.keys[key] = False


if __name__ == '__main__':
    game = Game()
    while game.running:
        game.game_loop()