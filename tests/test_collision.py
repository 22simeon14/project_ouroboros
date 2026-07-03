import unittest

from collision import is_out_of_bounds, is_self_collision, is_wall_collision


class TestOutOfBounds(unittest.TestCase):
    def test_left_boundary(self):
        self.assertTrue(is_out_of_bounds(-1, 5, 20, 20))

    def test_right_boundary(self):
        self.assertTrue(is_out_of_bounds(20, 5, 20, 20))

    def test_top_boundary(self):
        self.assertTrue(is_out_of_bounds(5, -1, 20, 20))

    def test_bottom_boundary(self):
        self.assertTrue(is_out_of_bounds(5, 20, 20, 20))

    def test_inside_grid(self):
        self.assertFalse(is_out_of_bounds(0, 0, 20, 20))
        self.assertFalse(is_out_of_bounds(19, 19, 20, 20))


class TestWallCollision(unittest.TestCase):
    def test_position_on_wall(self):
        walls = {(3, 4), (5, 6)}
        self.assertTrue(is_wall_collision(3, 4, walls))

    def test_free_position_not_on_wall(self):
        walls = {(3, 4), (5, 6)}
        self.assertFalse(is_wall_collision(1, 1, walls))


class TestSelfCollision(unittest.TestCase):
    def test_position_on_body(self):
        body = [(5, 5), (4, 5), (3, 5)]
        self.assertTrue(is_self_collision(4, 5, body))

    def test_free_position(self):
        body = [(5, 5), (4, 5), (3, 5)]
        self.assertFalse(is_self_collision(6, 5, body))


if __name__ == "__main__":
    unittest.main()
