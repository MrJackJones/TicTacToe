from django.db import models


class Game(models.Model):
    SYMBOL_X = 'x'
    SYMBOL_O = 'o'
    SYMBOLS = (SYMBOL_X, SYMBOL_O)

    timestamp = models.DateTimeField( auto_now_add=True, verbose_name='Время создания')
    field = models.CharField(max_length=9, default=' ' * 9, verbose_name='Состояние игры')
    finished = models.BooleanField(default=False, verbose_name='Игра закончена', editable=False)
    _history = models.CharField(default='', max_length=18, verbose_name='История', editable=False)
    last = models.SmallIntegerField(default=0, verbose_name='Последним ходил', editable=False)

    def finish(self):
        """Завершить игру."""
        self.finished = True

    @property
    def history(self) -> list:
        """Возвращает список кортежей всех ходов игры.

        :return: список [(player, position), ..., (player, position)]
        """
        return [(int(self._history[i]), int(self._history[i + 1])) for i in
                range(0, len(self._history), 2)]

    @property
    def winner(self) -> int or None:
        """Возвращает номер победителя."""
        if self.finished is True:
            return self.last
        return None

    @property
    def step(self) -> int:
        """Возвращает номер номер ходящего игрока."""
        return self.last % 2 + 1

    @classmethod
    def _player_symbol(cls, player) -> str:
        """Символ игрока по идентификатору."""
        return cls.SYMBOLS[player // 2]

    def _update_history(self, player, position):
        """Обновляет историю ходов."""
        self._history += f'{player}{position}'

    @classmethod
    def check_combinations(cls, field: str) -> int:
        """Поиск победной комбинации на поле.

        :param field:     строка для проверки

        :return 1|2 :   идентификатор победителя игры
                0   :   победителя нет/ничья
                -1  :   игра не окончена

        """

        def _check_to_win(seq: str, symbol: str) -> bool:
            """Проверяет является или нет комбинация победной.
            После преобразования подстроки seq в set если его длинна не более 1,
            сравнивает с входным символом. При удовлетворении условия будет возвращено
            True, иначе False

            :param seq: подстрока из поля битвы для проверки
            :param symbol: символ для сверки

            :return: True:  комбинация победная
                     False: обычная комбинация
            """
            tmp = set(seq)
            if len(tmp) == 1 and tmp.pop() == symbol:
                return True
            return False

        for i, s in enumerate(cls.SYMBOLS, start=1):
            if any((
                    # все строки
                    any([_check_to_win(field[_::3], s) for _ in range(3)]),
                    # все столбики
                    any([_check_to_win(field[_:_ + 3], s) for _ in
                         range(0, 9, 3)]),
                    _check_to_win(field[::4], s),  # диагональ главная
                    _check_to_win(field[2:8:2], s),  # диагональ побочная
            )):
                return i
            elif field.count(' ') == 0:
                return 0
        return -1

    def move(self, player_index: int, position: int):
        """Делать ход.

        :param player_index: 1 или 2
        :param position: от 0 до 8
        """
        tmp = self.field
        # обновление поля
        self.field = f'{tmp[:position]}' \
                     f'{self._player_symbol(player_index)}' \
                     f'{tmp[position + 1:]}'
        # обновление истории
        self._update_history(player_index, position)
        self.last = player_index

        winner = self.check_combinations(self.field)
        if winner != -1:
            # если есть победитель или ничья присвоить last это значение
            # в случае ничейной ситуации будет присвоен 0
            self.last = winner
            # если есть победитель или ничья окончить игру
            self.finish()
        self.save()
