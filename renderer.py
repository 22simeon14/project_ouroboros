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


def draw_start_menu(screen, best_score):
    screen.fill(config.BACKGROUND_COLOR)

    title_font = pygame.font.SysFont(None, 64)
    title = title_font.render("Ouroboros Project", True, (240, 240, 240))

    subtitle_font = pygame.font.SysFont(None, 32)
    subtitle = subtitle_font.render(
        "Escape the secret laboratory", True, (200, 200, 200)
    )

    hint_font = pygame.font.SysFont(None, 28)
    start_hint = hint_font.render("Press Enter to start", True, (180, 180, 180))
    quit_hint = hint_font.render("Press Escape to quit", True, (180, 180, 180))
    best_text = hint_font.render(f"Best Score: {best_score}", True, config.SCORE_TEXT_COLOR)

    center_x = config.WINDOW_WIDTH // 2
    screen.blit(title, title.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 90)))
    screen.blit(subtitle, subtitle.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 35)))
    screen.blit(start_hint, start_hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 25)))
    screen.blit(quit_hint, quit_hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 60)))
    screen.blit(best_text, best_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 110)))


def draw_hud(
    screen,
    level_name,
    level_number,
    total_levels,
    score,
    collected_energy,
    energy_goal,
    best_score,
):
    font = pygame.font.SysFont(None, 28)

    level_text = font.render(
        f"Level {level_number}/{total_levels} - {level_name}",
        True,
        config.SCORE_TEXT_COLOR,
    )
    score_text = font.render(f"Score: {score}", True, config.SCORE_TEXT_COLOR)
    energy_text = font.render(
        f"Energy: {collected_energy}/{energy_goal}", True, config.SCORE_TEXT_COLOR
    )
    best_text = font.render(f"Best: {best_score}", True, config.SCORE_TEXT_COLOR)

    level_rect = level_text.get_rect(midtop=(config.WINDOW_WIDTH // 2, 8))
    screen.blit(level_text, level_rect)
    screen.blit(score_text, (8, 8))
    screen.blit(energy_text, (8, 36))
    screen.blit(best_text, (config.WINDOW_WIDTH - best_text.get_width() - 8, 8))


def draw_snake(screen, snake):
    for col, row in snake.body:
        x = col * config.CELL_SIZE
        y = row * config.CELL_SIZE
        rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(screen, config.SNAKE_COLOR, rect)


def draw_game_over(screen, score, best_score):
    font = pygame.font.SysFont(None, 48)
    title = font.render("Game Over", True, (240, 240, 240))
    info_font = pygame.font.SysFont(None, 32)
    score_text = info_font.render(f"Score: {score}", True, (220, 220, 220))
    best_text = info_font.render(f"Best Score: {best_score}", True, (220, 220, 220))
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press R to restart campaign", True, (200, 200, 200))

    center_x = config.WINDOW_WIDTH // 2
    screen.blit(title, title.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 55)))
    screen.blit(score_text, score_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 5)))
    screen.blit(best_text, best_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 30)))
    screen.blit(hint, hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 75)))


def draw_level_complete(screen):
    font = pygame.font.SysFont(None, 48)
    title = font.render("Level Complete", True, (240, 240, 240))
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press Enter to continue", True, (200, 200, 200))

    title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 20))
    hint_rect = hint.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 25))
    screen.blit(title, title_rect)
    screen.blit(hint, hint_rect)


def draw_victory(screen, score, best_score):
    font = pygame.font.SysFont(None, 48)
    title = font.render("You Escaped!", True, (240, 240, 240))
    info_font = pygame.font.SysFont(None, 32)
    score_text = info_font.render(f"Score: {score}", True, (220, 220, 220))
    best_text = info_font.render(f"Best Score: {best_score}", True, (220, 220, 220))
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press R to restart campaign", True, (200, 200, 200))

    center_x = config.WINDOW_WIDTH // 2
    screen.blit(title, title.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 55)))
    screen.blit(score_text, score_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 5)))
    screen.blit(best_text, best_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 30)))
    screen.blit(hint, hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 75)))
