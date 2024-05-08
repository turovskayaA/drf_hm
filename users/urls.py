from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsCreateApiView, PaymentListAPIView, UserCreateApiView, UserUpdateAPIView, \
    UserDeleteAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("register/", UserCreateApiView.as_view(), name="register"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDeleteAPIView.as_view(), name="delete"),

    path("payments/create/", PaymentsCreateApiView.as_view(), name="create"),
    path("payments/", PaymentListAPIView.as_view(), name="list"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + router.urls
