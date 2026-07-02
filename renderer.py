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
