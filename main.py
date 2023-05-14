import os
import random

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

FONT = pygame.font.SysFont('Arial Black', 30)

# Screen size
WIDTH = 1370
HEIGHT = 800

screen_size = WIDTH, HEIGHT
main_display = pygame.display.set_mode(screen_size)

# Colors
COLOR_BLACK = 0, 0, 0
COLOR_WHITE = 255, 255, 255
COLOR_RED = 255, 0, 0
COLOR_GREEN = 0, 255, 0

def change_color():
    player_color = random.sample(range(0, 256), 3)
    player.fill(player_color)

# Player
PLAYER_SIZE = 20, 20

IMGAGE_PATH = 'Goose'
PLAYER_IMAGES = os.listdir(IMGAGE_PATH)

player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(x = 100, y = HEIGHT/2)
player_speed = 5

player_move_down = [0, player_speed]
player_move_up = [0, -player_speed]
player_move_right = [player_speed, 0]
player_move_left = [-player_speed, 0]

# Enemy
def create_enemy():
    ENEMY_SIZE = 20, 20

    enemy = pygame.image.load('enemy.png').convert_alpha()

    enemy_rect = pygame.Rect(WIDTH, random.randint(70, HEIGHT-70), *ENEMY_SIZE)
    enemy_move = [random.randint(-6, -1), 0]

    return [enemy, enemy_rect, enemy_move]

# Bonus
def create_bonus():
    BONUS_SIZE = 40, 10

    bonus = pygame.image.load('bonus.png').convert_alpha()

    bonus_rect = pygame.Rect(random.randint(150, WIDTH-150), 0, *BONUS_SIZE)
    bonus_move = [0, random.randint(1, 3)]

    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMG = pygame.USEREVENT + 3

pygame.time.set_timer(CREATE_ENEMY, 400)
pygame.time.set_timer(CREATE_BONUS, 3000)
pygame.time.set_timer(CHANGE_IMG, 200)

enemies = []
bonuses = []
score = 0
lifes = 3

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_start = 0
bg_end = bg.get_width()
bg_move = 2

img_index = 0

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            player = pygame.image.load(os.path.join(IMGAGE_PATH, PLAYER_IMAGES[img_index]))
            img_index += 1
            if img_index >= len(PLAYER_IMAGES):
                img_index = 0
    
    # Background
    bg_start -= bg_move
    bg_end -= bg_move

    if bg_start < -bg.get_width():
        bg_start = bg.get_width()

    if bg_end < -bg.get_width():
        bg_end = bg.get_width()

    main_display.blit(bg, (bg_start, 0))
    main_display.blit(bg, (bg_end, 0))

    # Player
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    main_display.blit(player, player_rect)
    main_display.blit(FONT.render(str(score), True, COLOR_GREEN), (WIDTH-50, 20))
    main_display.blit(FONT.render(str(lifes), True, COLOR_RED), (50, 20))

    # Enemy
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            lifes -= 1
            enemies.pop(enemies.index(enemy))
            if lifes == 0:
                playing = False
    
    # Bonus
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
