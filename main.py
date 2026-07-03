import sys

import pygame

import collision
import config
import renderer
from snake import Snake

DIRECTION_BY_KEY = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    clock = pygame.time.Clock()

    snake = Snake()
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
                    snake = Snake()
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
            ) or collision.is_self_collision(next_col, next_row, snake.body):
                game_over = True
            else:
                snake.move()
            last_move_time = now

        renderer.draw_grid(screen)
        renderer.draw_snake(screen, snake)
        if game_over:
            renderer.draw_game_over(screen)
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
