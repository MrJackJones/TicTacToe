import unittest

from .models import Game


class GameTestCase(unittest.TestCase):
    def test_blank_field(self):
        """Пустое поле."""
        field = ' ' * 9
        self.assertEqual(Game.check_combinations(field), -1)

    def test_no_winner(self):
        """Частично заполненное поле."""
        field = 'xxoo     '
        self.assertEqual(Game.check_combinations(field), -1)

    def test_a_draw(self):
        """Полностью заполненное поле, без победителя."""
        field = 'xxoooxxox'
        self.assertEqual(Game.check_combinations(field), 0)

    def test_horizontal_winner(self):
        """Проверка победителя по горизонтали."""
        field = 'x' * 3 + ' ' * 6
        self.assertEqual(Game.check_combinations(field), 1)
        field = 'o' * 3 + ' ' * 6
        self.assertEqual(Game.check_combinations(field), 2)

        field = ' ' * 3 + 'x' * 3 + ' ' * 3
        self.assertEqual(Game.check_combinations(field), 1)
        field = ' ' * 3 + 'o' * 3 + ' ' * 3
        self.assertEqual(Game.check_combinations(field), 2)

        field = ' ' * 6 + 'x' * 3
        self.assertEqual(Game.check_combinations(field), 1)
        field = ' ' * 6 + 'o' * 3
        self.assertEqual(Game.check_combinations(field), 2)

    def test_vertical_winner(self):
        """Проверка победителя по вертикали."""
        field = 'x  x  x  '
        self.assertEqual(Game.check_combinations(field), 1)
        field = 'o  o  o  '
        self.assertEqual(Game.check_combinations(field), 2)

        field = ' x  x  x '
        self.assertEqual(Game.check_combinations(field), 1)
        field = ' o  o  o '
        self.assertEqual(Game.check_combinations(field), 2)

        field = '  x  x  x'
        self.assertEqual(Game.check_combinations(field), 1)
        field = '  o  o  o'
        self.assertEqual(Game.check_combinations(field), 2)

    def test_diagonals_winner(self):
        """Проверка победителя по диагонали."""
        field = 'x   x   x'
        self.assertEqual(Game.check_combinations(field), 1)
        field = 'o   o   o'
        self.assertEqual(Game.check_combinations(field), 2)

        field = '  x x x  '
        self.assertEqual(Game.check_combinations(field), 1)
        field = '  o o o  '
        self.assertEqual(Game.check_combinations(field), 2)
