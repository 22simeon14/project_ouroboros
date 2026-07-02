import sys

import pygame

import config
import renderer
from snake import Snake


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    clock = pygame.time.Clock()

    snake = Snake()
    last_move_time = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()
        if now - last_move_time >= config.MOVE_INTERVAL_MS:
            snake.move()
            last_move_time = now

        renderer.draw_grid(screen)
        renderer.draw_snake(screen, snake)
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
