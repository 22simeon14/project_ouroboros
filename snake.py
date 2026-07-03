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
        self.next_direction = (1, 0)

    def request_direction(self, new_direction):
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction

    def move(self):
        self.direction = self.next_direction
        head_col, head_row = self.body[0]
        dx, dy = self.direction
        new_col = head_col + dx
        new_row = head_row + dy
        self.body.insert(0, (new_col, new_row))
        self.body.pop()
