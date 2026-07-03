import pygame

import config


def draw_grid(screen):
    screen.fill(config.BACKGROUND_COLOR)

    for col in range(config.GRID_COLS + 1):
        x = col * config.CELL_SIZE
        pygame.draw.line(
            screen,
            config.GRID_LINE_COLOR,
            (x, 0),
            (x, config.WINDOW_HEIGHT),
        )

    for row in range(config.GRID_ROWS + 1):
        y = row * config.CELL_SIZE
        pygame.draw.line(
            screen,
            config.GRID_LINE_COLOR,
            (0, y),
            (config.WINDOW_WIDTH, y),
        )


def draw_snake(screen, snake):
    for col, row in snake.body:
        x = col * config.CELL_SIZE
        y = row * config.CELL_SIZE
        rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(screen, config.SNAKE_COLOR, rect)


def draw_game_over(screen):
    font = pygame.font.SysFont(None, 48)
    title = font.render("Game Over", True, (240, 240, 240))
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press R to restart", True, (200, 200, 200))

    title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 20))
    hint_rect = hint.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 25))
    screen.blit(title, title_rect)
    screen.blit(hint, hint_rect)
