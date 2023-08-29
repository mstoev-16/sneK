import pygame
import random
import time
import json


def save_score():
    with open('score_records.json', 'r') as records:
        data = json.load(records)
        max_score = data['best_score']
        data['last_score'] = player_current_score
    if player_current_score > max_score:
        data['best_score'] = player_current_score
    with open('score_records.json', 'w') as records:
        data['last_score'] = player_current_score
        json.dump(data, records)


def knights():
    window.blit(KNIGHT, (knights_x_positions[0], knights_y_positions[0]))
    for i in range(len(KNIGHTS_SPAWNED)):
        if KNIGHTS_SPAWNED[i]:
            knights_x_positions[i + 1] = knights_x_initial_positions[i]
            knights_y_positions[i + 1] = knights_y_initial_positions[i]
            window.blit(KNIGHT, (knights_x_positions[i + 1], knights_y_positions[i + 1]))
    return


def apple_coordinates():
    x = random.randint(KNIGHT_SIZE[0], WIDTH - KNIGHT_SIZE[0] - apple_size[0])
    y = random.randint(apple_size[1], HEIGHT - 100 - apple_size[1])
    return x, y


def refresh_screen():
    window.fill(BACKGROUND_COLOR)
    window.blit(PLAYER, (player_x, player_y))

    window.blit(CURRENT_SCORE_LABEL, CURRENT_SCORE_LABEL_POS)
    window.blit(BEST_SCORE_LABEL, BEST_SCORE_LABEL_POS)
    window.blit(LAST_SCORE_LABEL, LAST_SCORE_LABEL_POS)

    window.blit(current_score, CURRENT_SCORE_POS)
    window.blit(best_score, BEST_SCORE_POS)
    window.blit(last_score, LAST_SCORE_POS)

    knights()
    pygame.draw.rect(window, HUD_COLOR, (HUD_POSITION, HUD_DIMENSIONS), HUD_THICKNESS)
    pygame.draw.rect(window, HUD_COLOR, (BORDER_POSITION, BORDER_DIMENSIONS), HUD_THICKNESS)
    return


# Initialize game
pygame.init()

# Window configuration
WIDTH = 800
HEIGHT = 570
BACKGROUND_COLOR = (150, 210, 90)
pygame.display.set_caption("sneK")
window = pygame.display.set_mode((WIDTH, HEIGHT))

# HUD configuration
HUD_THICKNESS = 5
HUD_COLOR = (160, 82, 45)
HUD_DIMENSIONS = (WIDTH, 100)
HUD_POSITION = (0, HEIGHT - 100)
TEXT_COLOR_1 = (255, 100, 30)
TEXT_COLOR_2 = (160, 30, 70)
TEXT_FONT = pygame.font.SysFont('impact', 36)

# Border configuration
BORDER_POSITION = (0, 0)
BORDER_DIMENSIONS = (WIDTH, HEIGHT - (HUD_DIMENSIONS[1] - HUD_THICKNESS))

# Scores Labels configuration
CURRENT_SCORE_LABEL = TEXT_FONT.render('Current Score:', True, TEXT_COLOR_2)
BEST_SCORE_LABEL = TEXT_FONT.render('Best Score:', True, TEXT_COLOR_2)
LAST_SCORE_LABEL = TEXT_FONT.render('Last Score:', True, TEXT_COLOR_2)

CURRENT_SCORE_LABEL_POS = (
    WIDTH // 2 - CURRENT_SCORE_LABEL.get_width() // 2,
    HEIGHT - HUD_DIMENSIONS[1] + HUD_THICKNESS // 2)

BEST_SCORE_LABEL_POS = (
    10 + HUD_THICKNESS,
    HEIGHT - HUD_DIMENSIONS[1] + HUD_THICKNESS // 2)

LAST_SCORE_LABEL_POS = (
    WIDTH - (10 + HUD_THICKNESS) - LAST_SCORE_LABEL.get_width(),
    HEIGHT - HUD_DIMENSIONS[1] + HUD_THICKNESS // 2)

# Score Values configuration
CURRENT_SCORE_POS = (
    CURRENT_SCORE_LABEL_POS[0],
    CURRENT_SCORE_LABEL_POS[1] + CURRENT_SCORE_LABEL.get_height() + HUD_THICKNESS)

BEST_SCORE_POS = (
    BEST_SCORE_LABEL_POS[0],
    BEST_SCORE_LABEL_POS[1] + BEST_SCORE_LABEL.get_height() + HUD_THICKNESS)

LAST_SCORE_POS = (
    LAST_SCORE_LABEL_POS[0],
    LAST_SCORE_LABEL_POS[1] + LAST_SCORE_LABEL.get_height() + HUD_THICKNESS)

# Player configuration
PLAYER = pygame.image.load('alien.png')
PLAYER_SIZE = PLAYER.get_rect().size
player_current_score = 0
player_x = (WIDTH - PLAYER_SIZE[0]) // 2  # starting position
player_y = (BORDER_DIMENSIONS[1] - 2 * HUD_DIMENSIONS[1] - PLAYER_SIZE[1]) // 2
PLAYER_SPEED = 5

# Enemies configuration
KNIGHT = pygame.image.load('knight.png')
KNIGHT_SIZE = KNIGHT.get_rect().size
left_knights_x = HUD_THICKNESS
right_knights_x = WIDTH
knight1_y = (BORDER_DIMENSIONS[1] - HUD_DIMENSIONS[1] + KNIGHT_SIZE[1]) // 2
knight2_y = knight1_y // 2 - KNIGHT_SIZE[1] + HUD_THICKNESS
knight3_y = knight1_y * 1.5 + KNIGHT_SIZE[1] - HUD_THICKNESS
knight4_y = (knight1_y + knight2_y) // 2
knight5_y = (knight1_y + knight3_y) // 2

knights_x_positions = [0] * 5  # the lists will store the positions of the 5 enemies
knights_y_positions = [0] * 5

knight_speed = 6
KNIGHTS_SPAWNED = [False] * 4

# Pickable items configuration
apple = pygame.image.load('green_apple.png')
apple_size = apple.get_rect().size
apple_x = (WIDTH - apple_size[0]) // 2  # starting position
apple_y = (BORDER_DIMENSIONS[1] - HUD_DIMENSIONS[1] + apple_size[1]) // 2
apple_spawn_timer = time.time()
apple_taken = False
score_checkpoints = [3, 6, 9, 12]

# Get score records
with open('score_records.json', 'r') as file:
    data = json.load(file)
    best_score_val = data['best_score']
    last_score_val = data['last_score']

GAME_RUNNING = True
clock = pygame.time.Clock()
while GAME_RUNNING:
    # Take events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score()
            GAME_RUNNING = False

    # Left Knights movement
    if left_knights_x > WIDTH:
        left_knights_x = 0
        if not KNIGHTS_SPAWNED[1]:
            for i in range(len(score_checkpoints)):
                if score_checkpoints[i] <= player_current_score:
                    KNIGHTS_SPAWNED[i] = True
    else:
        left_knights_x += knight_speed

    # Right Knights movement
    if right_knights_x < 0:
        right_knights_x = WIDTH
        if not KNIGHTS_SPAWNED[-1]:
            for i in range(2, len(score_checkpoints)):
                if score_checkpoints[i] <= player_current_score:
                    KNIGHTS_SPAWNED[i] = True
    else:
        right_knights_x -= knight_speed

    # The first knight spawns from the start
    knights_x_positions[0] = left_knights_x
    knights_y_positions[0] = knight1_y

    knights_x_initial_positions = [left_knights_x, left_knights_x, right_knights_x, right_knights_x]
    knights_y_initial_positions = [knight2_y, knight3_y, knight4_y, knight5_y]

    # Check for collision with knights
    for i in range(len(knights_x_positions)):
        if (i > 0 and KNIGHTS_SPAWNED[i - 1]) or i == 0:  # consider collisions only for spawned knights
            if player_x < knights_x_positions[i] + KNIGHT_SIZE[0] and \
                    player_x + PLAYER_SIZE[0] > knights_x_positions[i] and \
                    player_y < knights_y_positions[i] + KNIGHT_SIZE[1] and \
                    player_y + PLAYER_SIZE[1] > knights_y_positions[i]:
                save_score()
                print('dead')
                print(knights_x_positions[1], knights_x_positions[2], knights_x_positions[3], knights_x_positions[4])
                print(knights_y_positions[1], knights_y_positions[2], knights_y_positions[3], knights_y_positions[4])
                GAME_RUNNING = False

    # Controls and moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE[0] - HUD_THICKNESS - 2:
        player_x += PLAYER_SPEED
    if keys[pygame.K_LEFT] and player_x > 0 + HUD_THICKNESS + 3:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_UP] and player_y > 0 + HUD_THICKNESS + 2:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player_y < BORDER_DIMENSIONS[1] - HUD_DIMENSIONS[1] + PLAYER_SIZE[1] - HUD_THICKNESS * 2:
        player_y += PLAYER_SPEED

    # Apple collected
    if player_x + PLAYER_SIZE[0] > apple_x and \
            player_x < apple_x + apple_size[0] and \
            player_y + PLAYER_SIZE[1] > apple_y and \
            player_y < apple_y + apple_size[1]:

        apple_x, apple_y = apple_coordinates()
        apple_taken = True
        apple_spawn_timer = time.time()
        player_current_score += 1
        if player_current_score > score_checkpoints[-1]:
            if player_current_score % 5 == 0:
                knight_speed += 1
    else:
        # Check timer for spawning apple
        if time.time() - apple_spawn_timer >= 2 and apple_taken:
            apple_taken = False
            apple_spawn_timer = time.time()

    # The scores that appear in the HUD
    current_score = TEXT_FONT.render(str(player_current_score), True, TEXT_COLOR_1)
    best_score = TEXT_FONT.render(str(best_score_val), True, TEXT_COLOR_1)
    last_score = TEXT_FONT.render(str(last_score_val), True, TEXT_COLOR_1)

    refresh_screen()
    if not apple_taken:
        window.blit(apple, (apple_x, apple_y))

    pygame.display.update()
    clock.tick(60)
