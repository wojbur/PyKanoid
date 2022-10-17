import pygame
from pathlib import PurePath
from math import cos, sin
from math import pi as PI
from csv import reader

from states.state import State


vector = pygame.math.Vector2
# from states.main_menu import MainMenu

class GameLevel(State):
    def __init__(self, game):
        State.__init__(self, game)

        # Define sprite groups
        self.player_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()

        # Initialize player and ball objects
        self.player = Player(self.game, self)
        self.ball = Ball(self.game, self, self.player.rect.centerx, self.player.rect.top, PI, 400)
        # Load stage layout
        self.stage = 2

        self.is_paused = False

        with open(PurePath('stages', 'standard_set.csv')) as file:
            csv_reader = reader(file, delimiter=";")
            stage_layouts = list(csv_reader)
            start_row = self.stage + (self.stage-1)*20
            end_row = start_row + 20
            self.stage_layout = stage_layouts[start_row:end_row]
        
        # Create blocks grid
        for i in range(len(self.stage_layout)):
            for j in range(len(self.stage_layout[i])):
                if self.stage_layout[i][j]:
                    Block(self.game, self, self.stage_layout[i][j], 40+j*60, 80+i*30)
        
        # Load sounds
        self.bounce_sound = pygame.mixer.Sound(PurePath(game.sounds_dir, 'bounce.wav'))
        self.hit_block_sound = pygame.mixer.Sound(PurePath(game.sounds_dir, 'hit_block.wav'))
        self.hit_wall_sound = pygame.mixer.Sound(PurePath(game.sounds_dir, 'hit_wall.wav'))
        self.lose_live_sound = pygame.mixer.Sound(PurePath(game.sounds_dir, 'lose_live.wav'))
  
    def update(self, delta_time, keys):
        # test spawning multiple balls
        if keys['up']:
            self.spawn_ball(self.player.rect.centerx, self.player.rect.top, PI, 400)

        if self.is_paused:
            if keys['escape']:
                self.exit_state()
            if keys['enter']:
                self.reset()
                self.is_paused = False
        else:
            if keys['escape']:
                self.exit_state()
            self.player.update(delta_time, keys)
            self.ball_group.update(delta_time, keys)
            self.game.reset_keys()

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.player_group.draw(surface)
        self.ball_group.draw(surface)
        self.block_group.draw(surface)
    
    def lose_live(self):
        if self.player.lives == 0:
            self.game_over()
        else:
            self.lose_live_sound.play()
            self.is_paused = True
            self.player.lives -= 1
    
    def spawn_ball(self, x, y, angle, speed):
        print('spawn ballz')
        ball2 = Ball(self.game, self, x, y, angle, speed)
    
    def reset(self):
        self.player.is_magnetic = True
        self.ball2 = Ball(self.game, self, self.player.rect.centerx, self.player.rect.top, PI, 400)

    def game_over(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, game, level):
        super().__init__()
        self.game = game
        self.level = level

        # Set player initial values
        self.lives = 2
    
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
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.game.GAME_WIDTH:
            self.rect.right = self.game.GAME_WIDTH
        
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
        self.max_speed = 800

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
            self.level.hit_block_sound.play()
            # Check both ball position and direction to ensure no multiple collision detections occur
            # Collision from the bottom
            if abs(collided_blocks[0].rect.bottom - self.rect.top) < collision_tolerance and self.velocity[1] < 0:
                self.velocity[1] = abs(self.velocity[1])
                collided_blocks[0].kill()
            # Collision from the top
            if abs(collided_blocks[0].rect.top - self.rect.bottom) < collision_tolerance and self.velocity[1] > 0:
                self.velocity[1] = -abs(self.velocity[1])
                collided_blocks[0].kill()
            # Collision from the left
            if abs(collided_blocks[0].rect.left - self.rect.right) < collision_tolerance and self.velocity[0] > 0:

                self.velocity[0] = -abs(self.velocity[0])
                collided_blocks[0].kill()
            # Collision from the right
            if abs(collided_blocks[0].rect.right - self.rect.left) < collision_tolerance and self.velocity[0] < 0:
                self.velocity[0] = abs(self.velocity[0])
                collided_blocks[0].kill()
  
            
    def wall_collide(self):
        # Check both ball position and direction to ensure no multiple collision detections occur
        if self.rect.right >= self.game.GAME_WIDTH and self.velocity[0] > 0:
            self.level.hit_wall_sound.play()
            self.velocity[0] = -abs(self.velocity[0])
        if self.rect.left <= 0 and self.velocity[0] < 0:
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

        self.image = pygame.image.load(PurePath(game.sprites_dir, 'blocks', f'{self.code}.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.level.block_group.add(self)

    def render(self, surface):
        surface.blit(self.image, self.rect)


class Powerup():
    pass
