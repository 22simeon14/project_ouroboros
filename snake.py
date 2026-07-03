import config


class Snake:
    def __init__(self, start_col=None, start_row=None):
        if start_col is None:
            start_col = config.GRID_COLS // 2
        if start_row is None:
            start_row = config.GRID_ROWS // 2
        self.body = [
            (start_col, start_row),
            (start_col - 1, start_row),
            (start_col - 2, start_row),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.pending_growth = 0

    def grow(self):
        self.pending_growth += 1

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
        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.body.pop()
