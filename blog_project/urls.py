from django.contrib import admin
from blog_project import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Регистрация, получение данных пользователя и другие фичи Djoser
    path('api/v1/auth/', include('djoser.urls')),           # /users/, /users/me/, /users/activate/
    # JWT: логин, обновление токена, выход
    path('api/v1/auth/', include('djoser.urls.jwt')),       # /jwt/create/, /jwt/refresh/, /jwt/verify/

    path('api/v1/', include(router.urls)),  # подключаем users через роутер

    path('api/v1/', include('posts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

