def is_out_of_bounds(col, row, grid_cols, grid_rows):
    return col < 0 or col >= grid_cols or row < 0 or row >= grid_rows


def is_self_collision(next_col, next_row, body):
    return (next_col, next_row) in body


def is_wall_collision(col, row, walls):
    return (col, row) in walls
