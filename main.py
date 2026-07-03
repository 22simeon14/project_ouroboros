import random
import sys

import pygame

import collision
import config
import renderer
from level import load_level
from snake import Snake

LEVEL_PATH = "data/levels/level_01.json"

DIRECTION_BY_KEY = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def spawn_energy_cell(snake_body, walls, grid_cols, grid_rows):
    occupied = set(snake_body) | walls
    free_cells = [
        (col, row)
        for col in range(grid_cols)
        for row in range(grid_rows)
        if (col, row) not in occupied
    ]
    if not free_cells:
        return None
    return random.choice(free_cells)


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    clock = pygame.time.Clock()

    level = load_level(LEVEL_PATH)
    snake = Snake(level.start[0], level.start[1])
    score = 0
    energy_cell = spawn_energy_cell(
        snake.body, level.walls, config.GRID_COLS, config.GRID_ROWS
    )
    game_over = False
    last_move_time = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_over and event.key == pygame.K_r:
                    snake = Snake(level.start[0], level.start[1])
                    score = 0
                    energy_cell = spawn_energy_cell(
                        snake.body, level.walls, config.GRID_COLS, config.GRID_ROWS
                    )
                    game_over = False
                    last_move_time = pygame.time.get_ticks()
                elif not game_over and event.key in DIRECTION_BY_KEY:
                    snake.request_direction(DIRECTION_BY_KEY[event.key])

        now = pygame.time.get_ticks()
        if not game_over and now - last_move_time >= config.MOVE_INTERVAL_MS:
            head_col, head_row = snake.body[0]
            dx, dy = snake.next_direction
            next_col = head_col + dx
            next_row = head_row + dy

            if collision.is_out_of_bounds(
                next_col, next_row, config.GRID_COLS, config.GRID_ROWS
            ) or collision.is_self_collision(next_col, next_row, snake.body) or collision.is_wall_collision(
                next_col, next_row, level.walls
            ):
                game_over = True
            elif energy_cell is not None and (next_col, next_row) == energy_cell:
                snake.grow()
                snake.move()
                score += 1
                energy_cell = spawn_energy_cell(
                    snake.body, level.walls, config.GRID_COLS, config.GRID_ROWS
                )
            else:
                snake.move()
            last_move_time = now

        renderer.draw_grid(screen)
        renderer.draw_walls(screen, level.walls)
        if energy_cell is not None:
            renderer.draw_energy_cell(screen, energy_cell[0], energy_cell[1])
        renderer.draw_snake(screen, snake)
        renderer.draw_score(screen, score)
        if game_over:
            renderer.draw_game_over(screen)
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
