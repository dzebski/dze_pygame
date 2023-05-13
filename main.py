import random
import pygame
from pygame.constants import QUIT

pygame.init()

FPS = pygame.time.Clock()

# Screen size
WIDTH = 800
HEIGHT = 600

screen_size = WIDTH, HEIGHT
main_display = pygame.display.set_mode(screen_size)

# Colors
COLOR_BLACK = 0, 0, 0
COLOR_WHITE = 255, 255, 255

def change_color():
    player_color = random.sample(range(0, 256), 3)
    player.fill(player_color)

# Player
PLAYER_SIZE = 20, 20

player = pygame.Surface(PLAYER_SIZE)
player_color = COLOR_WHITE
player.fill(player_color)

player_rect = player.get_rect()
player_speed = [3, 3]

def invert_speed_x():
    player_speed[0] = -player_speed[0]

def invert_speed_y():
    player_speed[1] = -player_speed[1]

# On screen frame
playing = True

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
    
    # Screen backgroud draw
    main_display.fill(COLOR_BLACK)
    main_display.blit(player, player_rect)

    # Player draw
    player_rect = player_rect.move(player_speed)

    if player_rect.right >= WIDTH or player_rect.left <= 0:
        invert_speed_x()
        change_color()

    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        invert_speed_y()
        change_color()

    pygame.display.flip()

