import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer Game")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Игрок
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size]
player_speed = 10

# Платформы
platform_width = 100
platform_height = 20
platform_color = BLUE
platforms = [
    pygame.Rect(200, 500, platform_width, platform_height),
    pygame.Rect(400, 400, platform_width, platform_height),
    pygame.Rect(600, 300, platform_width, platform_height)
]

# Главный цикл игры
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed

    # Проверка столкновений с платформами
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for platform in platforms:
        if player_rect.colliderect(platform):
            player_pos[1] = platform.top - player_size

    # Отрисовка
    window.fill(WHITE)
    pygame.draw.rect(window, GREEN, player_rect)
    for platform in platforms:
        pygame.draw.rect(window, platform_color, platform)

    pygame.display.flip()
    clock.tick(30)
