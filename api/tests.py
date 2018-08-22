from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from game.models import Game


class APIGamesTest(APITestCase):
    def test_create_game(self):
        """Создание игры."""
        url = reverse('api:games')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().pk, 1)
        self.assertEqual(Game.objects.get().field, ' ' * 9)
        expected_data = {
            'pk': 1,
            'history': [],
            'field': ' ' * 9,
            'finished': False,
            'winner': None,
            'step': 1
        }
        self.assertEqual(response.data, expected_data)

    def test_detail_data(self):
        """Просмотр игры."""
        instance = Game.objects.create()
        expected_data = {
            'field': ' ' * 9,
            'history': [],
            'finished': False,
            'pk': instance.id,
            'step': 1,
            'winner': None
        }
        url = reverse('api:detail', args=[instance.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_list_of_games(self):
        """Тестирование списка созданных игр."""
        Game.objects.create()
        Game.objects.create()

        url = reverse('api:games')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Game.objects.count(), 2)
        self.assertEqual(len(response.data), 2)

    def test_make_move_valid_data(self):
        instance = Game.objects.create()
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 0, 'player': 1}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['step'], 2)
        self.assertEqual(response.json()['field'], 'x' + ' ' * 8)

    def test_make_retry_move(self):
        """Повторный ход в ячейку."""
        instance = Game.objects.create(field='x' + ' ' * 8)
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 0, 'player': 2}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.data['error'], 'Поле 0 занято')

    def test_make_move_same_player(self):
        """Делать ход 2 раза одним игроком."""
        instance = Game.objects.create(field='x' + ' ' * 8, last=1)
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 1, 'player': 1}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.data['error'], 'Повторный ход пользователя')

    def test_make_out_of_range_move(self):
        """Позиция вне интервала допустимых значений."""
        instance = Game.objects.create()
        url = reverse('api:detail', args=[instance.id])
        data1 = {'position': 9, 'player': 1}
        data2 = {'position': -1, 'player': 1}
        response1 = self.client.put(url, data=data1, format='json')
        response2 = self.client.put(url, data=data2, format='json')
        self.assertEquals(response1.status_code, response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(response1.json()), len(response2.json()), 1)
        self.assertEquals(response1.data['error'], response2.data['error'], 'Поле position должно быть от 0 до 8')

    def test_make_move_invalid_player_index(self):
        """Ход несуществующим игроком."""
        instance = Game.objects.create()
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 0, 'player': 3}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.data['error'], 'Неправильный код пользователя, должно быть 1 или 2')

    def test_make_move_in_finished_game(self):
        """Ход в оконченной игре."""
        instance = Game.objects.create(finished=True)
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 0, 'player': 3}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.data['error'], 'Игра окончена')

    def test_wining_move_response_code_x(self):
        """Проверка победного хода для игрока 1."""
        instance = Game.objects.create(field=' xx oo ox', last=2)
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 0, 'player': 1}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.data['winner'], 1)
        self.assertEqual(response.data['finished'], True)

    def test_wining_move_response_code_o(self):
        """Проверка победного хода для игрока 2."""
        instance = Game.objects.create(field=' oo xx xo', last=1)
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 0, 'player': 2}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.data['winner'], 2)
        self.assertEqual(response.data['finished'], True)

    def test_make_move_response_code_draw(self):
        """Проверка ничейной ситуации."""
        instance = Game.objects.create(field='xxoooxx x', last=1)
        url = reverse('api:detail', args=[instance.id])
        data = {'position': 7, 'player': 2}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.data['winner'], 0)
        self.assertEqual(response.data['finished'], True)
