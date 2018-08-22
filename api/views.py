from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from .serializers import AfterMoveGameSerializer, GameSerializer
from game.models import Game


class APIGameListCreateView(ListCreateAPIView):
    """Список всех игр(GET) и создание(POST)."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class APIGameDetailUpdateView(RetrieveUpdateAPIView):
    """Детальный просмотр конкретной игры и обновление."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AfterMoveGameSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.finished:
            # Посылается только 1 раз за игру
            data = {'finished': True, 'winner': instance.winner}
            return Response(data)
        return Response(serializer.data)
