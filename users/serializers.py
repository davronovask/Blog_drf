from djoser.serializers import UserCreateSerializer, UserSerializer, User
from .models import CustomUser
from rest_framework import serializers, viewsets, filters


class CustomUserCreateSerializer(UserCreateSerializer):
    bio = serializers.CharField(required=False, allow_blank=True)
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'password', 're_password', 'bio')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')  # убираем re_password, чтобы не было ошибки при создании
        return super().create(validated_data)

class CustomUserSerializer(UserSerializer):
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'bio')

class UserProfileSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    liked_by_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'likes_count', 'liked_by_count', 'is_liked']

    def get_likes_count(self, obj):
        # Сколько пользователь лайкнул других
        return obj.profile.liked_users.count()

    def get_liked_by_count(self, obj):
        # Сколько пользователей лайкнули этого пользователя
        return obj.liked_by.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.profile.liked_users.all()
        return False

