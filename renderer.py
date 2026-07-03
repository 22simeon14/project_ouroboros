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


def draw_walls(screen, walls):
    for col, row in walls:
        x = col * config.CELL_SIZE
        y = row * config.CELL_SIZE
        rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(screen, config.WALL_COLOR, rect)


def draw_energy_cell(screen, col, row):
    x = col * config.CELL_SIZE
    y = row * config.CELL_SIZE
    rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
    pygame.draw.rect(screen, config.ENERGY_COLOR, rect)


def draw_exit(screen, col, row, unlocked):
    x = col * config.CELL_SIZE
    y = row * config.CELL_SIZE
    rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
    color = config.EXIT_UNLOCKED_COLOR if unlocked else config.EXIT_LOCKED_COLOR
    pygame.draw.rect(screen, color, rect)
    if unlocked:
        inner = rect.inflate(-config.CELL_SIZE // 3, -config.CELL_SIZE // 3)
        pygame.draw.rect(screen, config.BACKGROUND_COLOR, inner)


def draw_score(screen, score):
    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score}", True, config.SCORE_TEXT_COLOR)
    screen.blit(text, (8, 8))


def draw_level_name(screen, level_name):
    font = pygame.font.SysFont(None, 28)
    text = font.render(level_name, True, config.SCORE_TEXT_COLOR)
    text_rect = text.get_rect(midtop=(config.WINDOW_WIDTH // 2, 8))
    screen.blit(text, text_rect)


def draw_energy_progress(screen, collected_energy, energy_goal):
    font = pygame.font.SysFont(None, 28)
    text = font.render(
        f"Energy: {collected_energy}/{energy_goal}", True, config.SCORE_TEXT_COLOR
    )
    screen.blit(text, (8, 36))


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
    hint = hint_font.render("Press R to restart campaign", True, (200, 200, 200))

    title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 20))
    hint_rect = hint.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 25))
    screen.blit(title, title_rect)
    screen.blit(hint, hint_rect)


def draw_level_complete(screen):
    font = pygame.font.SysFont(None, 48)
    title = font.render("Level Complete", True, (240, 240, 240))
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press Enter to continue", True, (200, 200, 200))

    title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 20))
    hint_rect = hint.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 25))
    screen.blit(title, title_rect)
    screen.blit(hint, hint_rect)


def draw_victory(screen, score):
    font = pygame.font.SysFont(None, 48)
    title = font.render("You Escaped!", True, (240, 240, 240))
    score_font = pygame.font.SysFont(None, 32)
    score_text = score_font.render(f"Score: {score}", True, (220, 220, 220))
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press R to restart campaign", True, (200, 200, 200))

    title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 40))
    score_rect = score_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 5))
    hint_rect = hint.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 45))
    screen.blit(title, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(hint, hint_rect)
