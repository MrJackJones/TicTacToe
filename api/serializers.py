from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from game.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('pk', 'history', 'field', 'finished', 'winner', 'step')


class AfterMoveGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('field', 'step', 'finished')

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

        self.player = int(self.initial_data.get('player'))
        self.position = int(self.initial_data.get('position'))

    def update(self, instance, validated_data):
        instance.move(self.player, self.position)
        return instance

    def is_valid(self, raise_exception=False):
        if self.instance.finished:
            raise ValidationError({'error': 'Игра окончена'})
        if not (0 <= self.position < 9):
            raise ValidationError(
                {'error': 'Поле position должно быть от 0 до 8'})
        if self.player not in (1, 2):
            raise ValidationError(
                {'error': 'Неправильный код пользователя, должно быть 1 или 2'})
        if self.player == self.instance.last:
            raise ValidationError({'error': 'Повторный ход пользователя'})
        if self.instance.field[self.position] in self.instance.SYMBOLS:
            raise ValidationError({'error': f'Поле {self.position} занято'})
        super().is_valid(raise_exception)
