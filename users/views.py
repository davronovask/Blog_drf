from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import User
from .models import CustomUser
from .serializers import CustomUserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Только для чтения (без create/update)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']  # Позволяет фильтровать по ?search=...

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        target_user = self.get_object()
        profile = request.user.profile

        if target_user == request.user:
            return Response({'detail': 'Нельзя лайкать себя'}, status=400)

        if target_user in profile.liked_users.all():
            profile.liked_users.remove(target_user)
            liked = False
        else:
            profile.liked_users.add(target_user)
            liked = True

        return Response({'liked': liked})