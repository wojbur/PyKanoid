import pygame
from pathlib import PurePath
from math import cos, sin
from math import pi as PI
from csv import reader
from time import sleep
import random

from states.state import State


vector = pygame.math.Vector2
# from states.main_menu import MainMenu

class GameLevel(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.game = game
        
        self.stage = 1
        self.lives = 2
        self.score = 0
        self.is_paused = False

        # Define sprite groups
        self.player_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()

        # Initialize player, ball and blocks objects
        self.player = Player(self.game, self)
        self.ball = Ball(self.game, self, self.player.rect.centerx, self.player.rect.top, PI, 400)
        self.create_block_grid(self.stage)

        # Load sounds
        self.bounce_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'bounce.wav'))
        self.hit_block_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'hit_block.wav'))
        self.hit_wall_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'hit_wall.wav'))
        self.lose_live_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'lose_live.wav'))
        self.next_stage_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'next_stage.wav'))

        # Load HUD images
        self.sidebar = pygame.image.load(PurePath(self.game.sprites_dir, 'other', 'sidebar.png'))

        self.sidebar_l_rect = self.sidebar.get_rect()
        self.sidebar_l_rect.topleft = (0, 0)

        self.sidebar_r_rect = self.sidebar.get_rect()
        self.sidebar_r_rect.topright = (self.game.GAME_WIDTH, 0)

        self.live_indicator = pygame.image.load(PurePath(self.game.sprites_dir, 'other', 'live_indicator.png'))

        self.hud_font = self.game.load_font('PilotCommand-3zn93.ttf', 60)
        

    def update(self, delta_time, keys):
        # test spawning multiple balls
        if keys['up']:

            self.spawn_ball(self.player.rect.centerx, self.player.rect.top, PI, 400)
        if keys['escape']:
            self.exit_state()
        self.player.update(delta_time, keys)
        self.ball_group.update(delta_time, keys)
        self.game.reset_keys()
        self.check_stage_completion()
        print(1/delta_time)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.player_group.draw(surface)
        self.ball_group.draw(surface)
        self.block_group.draw(surface)
        self.display_hud(surface)
    
    def create_block_grid(self, stage):
        # Load stage set CSV file
        with open(PurePath('stages', 'test_set1.csv')) as file:
            csv_reader = reader(file, delimiter=";")
            stage_layouts = list(csv_reader)
            start_row = stage + (stage-1)*20
            end_row = start_row + 20
            stage_layout = stage_layouts[start_row:end_row]
        # Create blocks grid
        for i in range(len(stage_layout)):
            for j in range(len(stage_layout[i])):
                if 'STD' in stage_layout[i][j]:
                    Block(self.game, self, stage_layout[i][j], 40+j*60, 80+i*30)
                if 'SPD' in stage_layout[i][j]:
                    SpeedUpBlock(self.game, self, stage_layout[i][j], 40+j*60, 80+i*30)
                if 'SLD' in stage_layout[i][j]:
                    SlowDownBlock(self.game, self, stage_layout[i][j], 40+j*60, 80+i*30)
                if 'ICE' in stage_layout[i][j]:
                    IceBlock(self.game, self, stage_layout[i][j], 40+j*60, 80+i*30)
    
    def lose_live(self):
        if self.lives == 0:
            self.game_over()
        else:
            self.lose_live_sound.play()
            sleep(1)
            self.lives -= 1
            self.reset()
    
    def check_stage_completion(self):
        if len(self.block_group) == 0:
            self.score += 1000*self.stage
            self.stage += 1
            self.start_new_stage(self.stage)
    
    def start_new_stage(self, stage):
        self.next_stage_sound.play()
        sleep(0.5)

        for ball in self.ball_group:
            ball.kill()

        self.player.is_magnetic = True
        self.ball = Ball(self.game, self, self.player.rect.centerx, self.player.rect.top, PI, 400)
        self.create_block_grid(stage)

    
    def spawn_ball(self, x, y, angle, speed):
        Ball(self.game, self, x, y, angle, speed)
    
    def reset(self):
        self.player.is_magnetic = True
        self.ball2 = Ball(self.game, self, self.player.rect.centerx, self.player.rect.top, PI, 400)
    
    def display_hud(self, surface):
        score_text = self.hud_font.render(f'{self.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topleft = (50, 10)
        surface.blit(score_text, score_rect)

        surface.blit(self.sidebar, self.sidebar_l_rect)
        surface.blit(self.sidebar, self.sidebar_r_rect)

        for i in range(self.lives):
            live_indicator_rect = self.live_indicator.get_rect()
            live_indicator_rect.topright = (self.game.GAME_WIDTH-50-i*82, 10)
            surface.blit(self.live_indicator, live_indicator_rect)
        

    def game_over(self):
        # Temporary, for testing
        self.exit_state()


class Player(pygame.sprite.Sprite):
    def __init__(self, game, level):
        super().__init__()
        self.game = game
        self.level = level
        # Make the ball stick to the paddle at the begining of each game
        self.is_magnetic = True
        # Set player sprite and position
        self.image = pygame.image.load(PurePath(self.game.sprites_dir, 'player', 'paddle.png'))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.GAME_WIDTH/2
        self.rect.bottom = self.game.GAME_HEIGHT - 14
        # Add player to player sprite group
        self.level.player_group.add(self)
    
    def update(self, delta_time, keys):
        # Scale mouse position to the display surface
        mouse_x = pygame.mouse.get_pos()[0] * (self.game.GAME_WIDTH / self.game.SCREEN_WIDTH)
        self.rect.centerx = mouse_x
        if self.rect.left < 40:
            self.rect.left = 40
        elif self.rect.right > self.game.GAME_WIDTH-40:
            self.rect.right = self.game.GAME_WIDTH-40
        # Demagnetize paddle to start game     
        if self.is_magnetic:
            if pygame.mouse.get_pressed()[0]:
                self.is_magnetic = False

    def render(self, surface):
        surface.blit(self.image, self.rect)
        

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, level, x, y, angle, speed):
        super().__init__()
        self.game = game
        self.level = level
        self.max_speed = 1000
        self.min_speed = 300

        self.image = pygame.image.load(PurePath(game.sprites_dir, 'ball', 'ball.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = angle

        # Add the ball to player sprite group
        self.level.ball_group.add(self)

        # Kinematic vectors
        self.position = vector(x, y)
        self.velocity = vector(sin(self.angle)*self.speed, cos(self.angle)*self.speed)
    
    def update(self, delta_time, keys):
        if self.level.player.is_magnetic:
            self.rect.centerx = self.level.player.rect.centerx
            self.rect.bottom  = self.level.player.rect.top
            self.position = vector(self.rect.centerx, self.rect.bottom)
        else:
            self.position += self.velocity * delta_time
            self.rect.center = self.position
            self.wall_collide()
            self.player_collide()
            self.block_collide()
            self.crash()

    def render(self, surface):
        surface.blit(self.image, self.rect)
    
    def player_collide(self):
        if pygame.sprite.spritecollide(self, self.level.player_group, False) and self.velocity[1] > 0:
            self.level.bounce_sound.play()
            ball_x = self.rect.centerx
            player_x = self.level.player.rect.centerx
            player_width = self.level.player.rect[2]

            # Set new ball angle depending on collide position - the closer to player center the more vertical the angle
            # The 0.8 is there to ensure min bounce angle is 18deg so that the ball don't bounce too horizontally
            self.angle = PI + 0.8 * PI * (player_x - ball_x)/player_width

            # Speed up the ball
            if self.speed <= self.max_speed:
                self.speed += 10

            # Set new ball velocity
            self.velocity[1] = -abs(self.velocity[1])
            self.velocity = vector(sin(self.angle)*self.speed, cos(self.angle)*self.speed)
    
    def block_collide(self):
        collision_tolerance = 8
        collided_blocks = pygame.sprite.spritecollide(self, self.level.block_group, False)
        if collided_blocks:
            # Check both ball position and direction to ensure no multiple collision detections occur
            # Collision from the bottom
            if abs(collided_blocks[0].rect.bottom - self.rect.top) < collision_tolerance and self.velocity[1] < 0:
                collided_blocks[0].get_hit(self, 'bottom')
            # Collision from the top
            if abs(collided_blocks[0].rect.top - self.rect.bottom) < collision_tolerance and self.velocity[1] > 0:
                collided_blocks[0].get_hit(self, 'top')
            # Collision from the left
            if abs(collided_blocks[0].rect.left - self.rect.right) < collision_tolerance and self.velocity[0] > 0:
                collided_blocks[0].get_hit(self, 'left')
            # Collision from the right
            if abs(collided_blocks[0].rect.right - self.rect.left) < collision_tolerance and self.velocity[0] < 0:
                collided_blocks[0].get_hit(self, 'right')
  
            
    def wall_collide(self):
        # Check both ball position and direction to ensure no multiple collision detections occur
        if self.rect.right >= self.game.GAME_WIDTH-40 and self.velocity[0] > 0:
            self.level.hit_wall_sound.play()
            self.velocity[0] = -abs(self.velocity[0])
        if self.rect.left <= 40 and self.velocity[0] < 0:
            self.level.hit_wall_sound.play()
            self.velocity[0] = abs(self.velocity[0])
        if self.rect.top <= 0 and self.velocity[1] < 0:
            self.level.hit_wall_sound.play()
            self.velocity[1] = abs(self.velocity[1])
    
    def crash(self):
        if self.rect.top > self.game.GAME_HEIGHT+20:
            self.kill()
            if len(self.level.ball_group) == 0:
                self.level.lose_live()




class Block(pygame.sprite.Sprite):
    def __init__(self, game, level, code, x, y):
        super().__init__()
        self.game = game
        self.level = level
        self.code = code
        self.hit_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'hit_block.wav'))

        self.image = pygame.image.load(PurePath(game.sprites_dir, 'blocks', f'{self.code}.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.level.block_group.add(self)

    def render(self, surface):
        surface.blit(self.image, self.rect)
    
    def get_hit(self, ball, side):
        self.hit_sound.play()
        self.level.score += 8
        self.kill()
        if side == 'bottom':
            ball.velocity[1] = abs(ball.velocity[1])
        elif side == 'top':
            ball.velocity[1] = -abs(ball.velocity[1])
        elif side == 'left':
            ball.velocity[0] = -abs(ball.velocity[0])
        elif side == 'right':
            ball.velocity[0] = abs(ball.velocity[0])

class SpeedUpBlock(Block):
    def __init__(self, game, level, code, x, y):
        super().__init__(game, level, code, x, y)
        self.hit_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'speed_up.wav'))
    
    def get_hit(self, ball, side):
        ball.speed = ball.max_speed
        ball.velocity = vector(sin(ball.angle)*ball.speed, cos(ball.angle)*ball.speed)
        super().get_hit(ball, side)

class SlowDownBlock(Block):
    def __init__(self, game, level, code, x, y):
        super().__init__(game, level, code, x, y)
        self.hit_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'slow_down.wav'))
    
    def get_hit(self, ball, side):
        if ball.speed*0.5 > ball.min_speed:
            ball.speed *= 0.5
        else:
            ball.speed = ball.min_speed
        ball.velocity = vector(sin(ball.angle)*ball.speed, cos(ball.angle)*ball.speed)
        super().get_hit(ball, side)

class IceBlock(Block):
    def __init__(self, game, level, code, x, y):
        super().__init__(game, level, code, x, y)
        self.hit_sound = pygame.mixer.Sound(PurePath(self.game.sounds_dir, 'ice_break.wav'))
    
    def get_hit(self, ball, side):
        super().get_hit(ball, side)
        ball_angle = random.uniform(0, 2*PI)
        self.level.spawn_ball(self.rect.centerx, self.rect.centery, ball_angle, ball.speed)





class Powerup():
    pass
