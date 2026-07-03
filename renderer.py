import pygame

import config


def _cell_rect(col, row, padding=0):
    x = col * config.CELL_SIZE
    y = row * config.CELL_SIZE
    rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
    if padding:
        rect = rect.inflate(-padding, -padding)
    return rect


def _draw_lab_frame(screen):
    screen.fill(config.BACKGROUND_COLOR)
    grid_rect = pygame.Rect(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    pygame.draw.rect(screen, config.GRID_BG_COLOR, grid_rect)

    pygame.draw.rect(screen, config.BORDER_COLOR, grid_rect, 2)

    corner_len = 18
    corners = [
        ((2, 2), (corner_len, 2), (2, corner_len)),
        ((config.WINDOW_WIDTH - corner_len, 2), (config.WINDOW_WIDTH - 2, 2), (config.WINDOW_WIDTH - 2, corner_len)),
        ((2, config.WINDOW_HEIGHT - corner_len), (2, config.WINDOW_HEIGHT - 2), (corner_len, config.WINDOW_HEIGHT - 2)),
        (
            (config.WINDOW_WIDTH - 2, config.WINDOW_HEIGHT - corner_len),
            (config.WINDOW_WIDTH - 2, config.WINDOW_HEIGHT - 2),
            (config.WINDOW_WIDTH - corner_len, config.WINDOW_HEIGHT - 2),
        ),
    ]
    for points in corners:
        pygame.draw.lines(screen, config.ACCENT_COLOR, False, points, 1)


def draw_grid(screen):
    _draw_lab_frame(screen)

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
        outer = _cell_rect(col, row)
        pygame.draw.rect(screen, config.WALL_OUTER_COLOR, outer)

        inner = outer.inflate(-4, -4)
        pygame.draw.rect(screen, config.WALL_INNER_COLOR, inner)

        pygame.draw.line(
            screen,
            config.WALL_HIGHLIGHT_COLOR,
            (outer.left + 1, outer.top + 1),
            (outer.right - 2, outer.top + 1),
        )
        pygame.draw.line(
            screen,
            config.WALL_HIGHLIGHT_COLOR,
            (outer.left + 1, outer.top + 1),
            (outer.left + 1, outer.bottom - 2),
        )

        pygame.draw.line(
            screen,
            config.WALL_ACCENT_COLOR,
            (outer.right - 2, outer.top + 3),
            (outer.right - 2, outer.bottom - 2),
            1,
        )


def draw_energy_cell(screen, col, row):
    center_x = col * config.CELL_SIZE + config.CELL_SIZE // 2
    center_y = row * config.CELL_SIZE + config.CELL_SIZE // 2
    outer_radius = config.CELL_SIZE // 2 - 3
    inner_radius = config.CELL_SIZE // 4

    pygame.draw.circle(screen, config.ENERGY_RING_COLOR, (center_x, center_y), outer_radius)
    pygame.draw.circle(screen, config.ENERGY_CORE_COLOR, (center_x, center_y), inner_radius)


def _draw_locked_exit(screen, rect):
    pygame.draw.rect(screen, config.EXIT_LOCKED_BASE, rect)
    inner = rect.inflate(-6, -6)
    pygame.draw.rect(screen, config.EXIT_LOCKED_INNER, inner)

    lock_center_x = rect.centerx
    lock_top = rect.centery - 2
    lock_body = pygame.Rect(lock_center_x - 5, lock_top, 10, 8)
    pygame.draw.rect(screen, config.EXIT_LOCKED_MARKER, lock_body)
    pygame.draw.arc(
        screen,
        config.EXIT_LOCKED_MARKER,
        pygame.Rect(lock_center_x - 5, lock_top - 6, 10, 10),
        3.14,
        0,
        2,
    )

    pygame.draw.line(
        screen,
        config.EXIT_LOCKED_MARKER,
        (rect.left + 4, rect.top + 4),
        (rect.right - 4, rect.bottom - 4),
        1,
    )
    pygame.draw.line(
        screen,
        config.EXIT_LOCKED_MARKER,
        (rect.right - 4, rect.top + 4),
        (rect.left + 4, rect.bottom - 4),
        1,
    )


def _draw_unlocked_exit(screen, rect):
    pygame.draw.rect(screen, config.EXIT_UNLOCKED_BASE, rect)
    inner = rect.inflate(-8, -8)
    pygame.draw.rect(screen, config.EXIT_UNLOCKED_INNER, inner, 2)

    slot_x = rect.centerx
    pygame.draw.line(
        screen,
        config.EXIT_UNLOCKED_GLOW,
        (slot_x, rect.top + 5),
        (slot_x, rect.bottom - 5),
        2,
    )

    arrow_y = rect.centery
    pygame.draw.polygon(
        screen,
        config.EXIT_UNLOCKED_GLOW,
        [
            (rect.centerx - 5, arrow_y - 4),
            (rect.centerx + 5, arrow_y),
            (rect.centerx - 5, arrow_y + 4),
        ],
    )


def draw_exit(screen, col, row, unlocked):
    rect = _cell_rect(col, row, padding=2)
    if unlocked:
        _draw_unlocked_exit(screen, rect)
    else:
        _draw_locked_exit(screen, rect)


def _draw_snake_eyes(screen, head_rect, direction):
    dx, dy = direction
    eye_radius = 2
    offset = 5

    if dx == 1:
        eye_positions = [
            (head_rect.right - offset, head_rect.centery - 4),
            (head_rect.right - offset, head_rect.centery + 4),
        ]
    elif dx == -1:
        eye_positions = [
            (head_rect.left + offset, head_rect.centery - 4),
            (head_rect.left + offset, head_rect.centery + 4),
        ]
    elif dy == -1:
        eye_positions = [
            (head_rect.centerx - 4, head_rect.top + offset),
            (head_rect.centerx + 4, head_rect.top + offset),
        ]
    else:
        eye_positions = [
            (head_rect.centerx - 4, head_rect.bottom - offset),
            (head_rect.centerx + 4, head_rect.bottom - offset),
        ]

    for pos in eye_positions:
        pygame.draw.circle(screen, config.SNAKE_EYE_COLOR, pos, eye_radius + 1)
        pygame.draw.circle(screen, config.SNAKE_EYE_HIGHLIGHT, pos, eye_radius)


def draw_snake(screen, snake):
    padding = config.SNAKE_SEGMENT_PADDING

    for index, (col, row) in enumerate(snake.body):
        segment_rect = _cell_rect(col, row, padding=padding)
        if index == 0:
            pygame.draw.rect(screen, config.SNAKE_HEAD_COLOR, segment_rect)
            _draw_snake_eyes(screen, segment_rect, snake.direction)
        else:
            pygame.draw.rect(screen, config.SNAKE_COLOR, segment_rect)


def draw_start_menu(screen, best_score):
    _draw_lab_frame(screen)

    title_font = pygame.font.SysFont(None, 64)
    title = title_font.render("Ouroboros Project", True, config.MENU_TEXT_COLOR)

    subtitle_font = pygame.font.SysFont(None, 32)
    subtitle = subtitle_font.render(
        "Escape the secret laboratory", True, config.MENU_SUBTITLE_COLOR
    )

    hint_font = pygame.font.SysFont(None, 28)
    start_hint = hint_font.render("Press Enter to start", True, config.MENU_HINT_COLOR)
    quit_hint = hint_font.render("Press Escape to quit", True, config.MENU_HINT_COLOR)
    best_text = hint_font.render(f"Best Score: {best_score}", True, config.SCORE_TEXT_COLOR)

    center_x = config.WINDOW_WIDTH // 2
    screen.blit(title, title.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 90)))
    screen.blit(subtitle, subtitle.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 35)))

    start_hint_rect = start_hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 25))
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        screen.blit(start_hint, start_hint_rect)

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


def draw_game_over(screen, score, best_score):
    font = pygame.font.SysFont(None, 48)
    title = font.render("Game Over", True, config.MENU_TEXT_COLOR)
    info_font = pygame.font.SysFont(None, 32)
    score_text = info_font.render(f"Score: {score}", True, config.SCORE_TEXT_COLOR)
    best_text = info_font.render(f"Best Score: {best_score}", True, config.SCORE_TEXT_COLOR)
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press R to restart campaign", True, config.MENU_HINT_COLOR)

    center_x = config.WINDOW_WIDTH // 2
    screen.blit(title, title.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 55)))
    screen.blit(score_text, score_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 5)))
    screen.blit(best_text, best_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 30)))
    screen.blit(hint, hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 75)))


def draw_level_complete(screen):
    font = pygame.font.SysFont(None, 48)
    title = font.render("Level Complete", True, config.MENU_TEXT_COLOR)
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press Enter to continue", True, config.MENU_HINT_COLOR)

    title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 20))
    hint_rect = hint.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 25))
    screen.blit(title, title_rect)
    screen.blit(hint, hint_rect)


def draw_victory(screen, score, best_score):
    font = pygame.font.SysFont(None, 48)
    title = font.render("You Escaped!", True, config.MENU_TEXT_COLOR)
    info_font = pygame.font.SysFont(None, 32)
    score_text = info_font.render(f"Score: {score}", True, config.SCORE_TEXT_COLOR)
    best_text = info_font.render(f"Best Score: {best_score}", True, config.SCORE_TEXT_COLOR)
    hint_font = pygame.font.SysFont(None, 28)
    hint = hint_font.render("Press R to restart campaign", True, config.MENU_HINT_COLOR)

    center_x = config.WINDOW_WIDTH // 2
    screen.blit(title, title.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 55)))
    screen.blit(score_text, score_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 - 5)))
    screen.blit(best_text, best_text.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 30)))
    screen.blit(hint, hint.get_rect(center=(center_x, config.WINDOW_HEIGHT // 2 + 75)))
