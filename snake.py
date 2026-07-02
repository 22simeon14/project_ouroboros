import config


class Snake:
    def __init__(self):
        center_col = config.GRID_COLS // 2
        center_row = config.GRID_ROWS // 2
        self.body = [
            (center_col, center_row),
            (center_col - 1, center_row),
            (center_col - 2, center_row),
        ]
        self.direction = (1, 0)

    def move(self):
        head_col, head_row = self.body[0]
        dx, dy = self.direction
        new_col = (head_col + dx) % config.GRID_COLS
        new_row = (head_row + dy) % config.GRID_ROWS
        self.body.insert(0, (new_col, new_row))
        self.body.pop()
