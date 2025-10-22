import pygame
import sys
import time
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Название окна
pygame.display.set_caption('Змейка | Flat & Clean')

# Цвета (Новая палитра)
background_color = (240, 240, 240)      # Светло-серый фон
snake_color = (50, 150, 255)           # Синий
snake_head_color = (40, 120, 220)       # Темно-синий для головы
food_color = (255, 120, 50)            # Оранжевый
obstacle_color = (100, 100, 100)        # Серый для препятствий
text_color = (20, 20, 20)              # Почти черный текст
red = (220, 40, 40)                    # Красный для Game Over

# Параметры
block_size = 20
initial_speed = 8
snake_speed = initial_speed

# Параметры змейки
snake_pos = [100, 60]
snake_body = [[100, 60], [80, 60], [60, 60]]
direction = 'RIGHT'
change_to = direction

# Препятствия
obstacles = [
    pygame.Rect(200, 100, 200, block_size),
    pygame.Rect(400, 300, 200, block_size),
    pygame.Rect(200, 500, 200, block_size)
]

# Счет
score = 0

# Функция спавна еды
def spawn_food():
    while True:
        pos = [random.randrange(1, (screen_width//block_size)) * block_size,
               random.randrange(1, (screen_height//block_size)) * block_size]
        food_rect = pygame.Rect(pos[0], pos[1], block_size, block_size)
        if any(obs.colliderect(food_rect) for obs in obstacles) or any(block == pos for block in snake_body):
            continue
        return pos

# Параметры еды
food_pos = spawn_food()

# Функция отображения счета
def show_score():
    # Используем None, чтобы выбрать системный шрифт по умолчанию
    score_font = pygame.font.SysFont(None, 30)
    score_surface = score_font.render(f'Счет: {score} | Скорость: {snake_speed}', True, text_color)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_surface, score_rect)

# Функция завершения игры
def game_over():
    # Используем None, чтобы выбрать системный шрифт по умолчанию
    my_font = pygame.font.SysFont(None, 80, bold=True)
    game_over_surface = my_font.render('КОНЕЦ ИГРЫ', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width/2, screen_height/4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Игровой таймер
clock = pygame.time.Clock()

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to

    if direction == 'UP': snake_pos[1] -= block_size
    if direction == 'DOWN': snake_pos[1] += block_size
    if direction == 'LEFT': snake_pos[0] -= block_size
    if direction == 'RIGHT': snake_pos[0] += block_size

    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        if score % 3 == 0:
            snake_speed += 1
        food_pos = spawn_food()
    else:
        snake_body.pop()

    screen.fill(background_color)

    # Отрисовка змейки, еды, препятствий
    for i, pos in enumerate(snake_body):
        rect = pygame.Rect(pos[0], pos[1], block_size, block_size)
        color = snake_head_color if i == 0 else snake_color
        pygame.draw.rect(screen, color, rect, border_radius=5)

    food_rect = pygame.Rect(food_pos[0], food_pos[1], block_size, block_size)
    pygame.draw.rect(screen, food_color, food_rect, border_radius=8)

    for obs in obstacles:
        pygame.draw.rect(screen, obstacle_color, obs)

    # Проверка на столкновения
    if not (0 <= snake_pos[0] < screen_width and 0 <= snake_pos[1] < screen_height):
        game_over()
    if any(block == snake_pos for block in snake_body[1:]):
        game_over()
    if any(obs.collidepoint(snake_pos[0], snake_pos[1]) for obs in obstacles):
        game_over()

    show_score()
    pygame.display.flip()
    clock.tick(snake_speed)
