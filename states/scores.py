from pathlib import PurePath
from states.state import State

class HighScores(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)

        self.font = self.game.load_font('PilotCommand-3zn93.ttf', 50)
    
    def update(self, delta_time, keys):
        if keys['escape']:
            self.exit_state()
        self.game.reset_keys()

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.game.draw_text(surface, self.font, 'SCORES GO HERE', (255, 255, 255), self.game.GAME_WIDTH/2, self.game.GAME_HEIGHT/2)
