import random

import sys

from pathlib import Path



import pygame



import collision

import config

import renderer

from level import load_level

from save_manager import load_best_score, update_best_score

from snake import Snake



LEVEL_PATHS = [

    "data/levels/level_01.json",

    "data/levels/level_02.json",

    "data/levels/level_03.json",

]

SAVE_PATH = Path("data/save.json")



DIRECTION_BY_KEY = {

    pygame.K_UP: (0, -1),

    pygame.K_DOWN: (0, 1),

    pygame.K_LEFT: (-1, 0),

    pygame.K_RIGHT: (1, 0),

}





def spawn_energy_cell(snake_body, walls, exit_cell, grid_cols, grid_rows):

    occupied = set(snake_body) | walls | {exit_cell}

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



    in_menu = True

    best_score = load_best_score(SAVE_PATH)

    current_level_index = 0

    score = 0

    collected_energy = 0

    game_over = False

    level_complete = False

    victory = False

    last_move_time = pygame.time.get_ticks()



    level = None

    snake = None

    energy_cell = None



    def start_current_level():

        nonlocal level, snake, energy_cell, collected_energy, last_move_time

        level = load_level(LEVEL_PATHS[current_level_index])

        snake = Snake(level.start[0], level.start[1])

        collected_energy = 0

        energy_cell = spawn_energy_cell(

            snake.body, level.walls, level.exit, config.GRID_COLS, config.GRID_ROWS

        )

        last_move_time = pygame.time.get_ticks()



    def restart_campaign():

        nonlocal current_level_index, score, game_over, level_complete, victory

        current_level_index = 0

        score = 0

        game_over = False

        level_complete = False

        victory = False

        start_current_level()



    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False

                elif in_menu and event.key == pygame.K_RETURN:

                    in_menu = False

                    restart_campaign()

                elif not in_menu and (game_over or victory) and event.key == pygame.K_r:

                    restart_campaign()

                elif (

                    not in_menu

                    and level_complete

                    and event.key == pygame.K_RETURN

                ):

                    if current_level_index < len(LEVEL_PATHS) - 1:

                        current_level_index += 1

                        level_complete = False

                        start_current_level()

                    else:

                        level_complete = False

                        victory = True

                        best_score = update_best_score(SAVE_PATH, score)

                elif (

                    not in_menu

                    and not game_over

                    and not level_complete

                    and not victory

                    and event.key in DIRECTION_BY_KEY

                ):

                    snake.request_direction(DIRECTION_BY_KEY[event.key])



        if (

            not in_menu

            and not game_over

            and not level_complete

            and not victory

        ):

            now = pygame.time.get_ticks()

            if now - last_move_time >= config.MOVE_INTERVAL_MS:

                head_col, head_row = snake.body[0]

                dx, dy = snake.next_direction

                next_col = head_col + dx

                next_row = head_row + dy



                if collision.is_out_of_bounds(

                    next_col, next_row, config.GRID_COLS, config.GRID_ROWS

                ) or collision.is_self_collision(

                    next_col, next_row, snake.body

                ) or collision.is_wall_collision(next_col, next_row, level.walls):

                    game_over = True

                    best_score = update_best_score(SAVE_PATH, score)

                elif energy_cell is not None and (next_col, next_row) == energy_cell:

                    snake.grow()

                    snake.move()

                    score += 1

                    collected_energy += 1

                    energy_cell = spawn_energy_cell(

                        snake.body,

                        level.walls,

                        level.exit,

                        config.GRID_COLS,

                        config.GRID_ROWS,

                    )

                elif (

                    (next_col, next_row) == level.exit

                    and collected_energy >= level.energy_goal

                ):

                    snake.move()

                    level_complete = True

                else:

                    snake.move()

                last_move_time = now



        if in_menu:

            renderer.draw_start_menu(screen, best_score)

        else:

            exit_unlocked = collected_energy >= level.energy_goal



            renderer.draw_grid(screen)

            renderer.draw_walls(screen, level.walls)

            renderer.draw_exit(screen, level.exit[0], level.exit[1], exit_unlocked)

            if energy_cell is not None:

                renderer.draw_energy_cell(screen, energy_cell[0], energy_cell[1])

            renderer.draw_snake(screen, snake)

            renderer.draw_hud(

                screen,

                level.name,

                current_level_index + 1,

                len(LEVEL_PATHS),

                score,

                collected_energy,

                level.energy_goal,

                best_score,

            )

            if game_over:

                renderer.draw_game_over(screen, score, best_score)

            elif level_complete:

                renderer.draw_level_complete(screen)

            elif victory:

                renderer.draw_victory(screen, score, best_score)



        pygame.display.flip()

        clock.tick(config.FPS)



    pygame.quit()

    sys.exit()





if __name__ == "__main__":

    main()

