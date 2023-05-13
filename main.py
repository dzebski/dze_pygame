import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

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
COLOR_RED = 255, 0, 0
COLOR_GREEN = 0, 255, 0

def change_color():
    player_color = random.sample(range(0, 256), 3)
    player.fill(player_color)

# Player
PLAYER_SIZE = 20, 20

player = pygame.Surface(PLAYER_SIZE)
player_color = COLOR_WHITE
player.fill(player_color)

player_rect = player.get_rect()
player_move_down = [0, 3]
player_move_up = [0, -3]
player_move_right = [3, 0]
player_move_left = [-3, 0]

# Enemy
def create_enemy():
    ENEMY_SIZE = 30, 30

    enemy = pygame.Surface(ENEMY_SIZE)
    enemy_color = COLOR_RED
    enemy.fill(enemy_color)

    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *ENEMY_SIZE)
    enemy_move = [random.randint(-6, -1), 0]

    return [enemy, enemy_rect, enemy_move]

# Bonus
def create_bonus():
    BONUS_SIZE = 60, 20

    bonus = pygame.Surface(BONUS_SIZE)
    bonus_color = COLOR_GREEN
    bonus.fill(bonus_color)

    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *BONUS_SIZE)
    bonus_move = [0, random.randint(1, 3)]

    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 1

pygame.time.set_timer(CREATE_ENEMY, 1000)
pygame.time.set_timer(CREATE_BONUS, 3000)

enemies = []
bonuses = []

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_BONUS:
            enemies.append(create_bonus())
    
    main_display.fill(COLOR_BLACK)
    keys = pygame.key.get_pressed()

    # Player
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    main_display.blit(player, player_rect)

    # Enemy
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
    
    # Bonus
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].left < 0:
            bonus.pop(bonus.index(enemy))
