from states.state import State

class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
    
    def update(self, delta_time, keys):
        if keys['up']:
            print('up')
        if keys['down']:
            print('down')
        self.game.reset_keys()

    def render(self, surface):
        surface.fill((255, 255, 255))
        self.game.draw_text(surface, self.game.title_font, 'PYKANOID', (0, 0, 0), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/10)