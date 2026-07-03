import unittest

from snake import Snake


class TestSnake(unittest.TestCase):
    def test_new_snake_has_three_segments(self):
        snake = Snake()
        self.assertEqual(len(snake.body), 3)

    def test_normal_move_preserves_length(self):
        snake = Snake()
        length_before = len(snake.body)
        snake.move()
        self.assertEqual(len(snake.body), length_before)

    def test_grow_then_move_increases_length_by_one(self):
        snake = Snake()
        length_before = len(snake.body)
        snake.grow()
        snake.move()
        self.assertEqual(len(snake.body), length_before + 1)

    def test_grow_then_move_head_at_correct_position(self):
        snake = Snake()
        head_col, head_row = snake.body[0]
        snake.grow()
        snake.move()
        self.assertEqual(snake.body[0], (head_col + 1, head_row))

    def test_normal_move_removes_last_segment(self):
        snake = Snake()
        old_tail = snake.body[-1]
        snake.move()
        self.assertNotIn(old_tail, snake.body)


if __name__ == "__main__":
    unittest.main()
