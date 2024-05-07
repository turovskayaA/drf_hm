from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsCreateApiView, PaymentListAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("payments/create/", PaymentsCreateApiView.as_view(), name="create"),
    path("payments/", PaymentListAPIView.as_view(), name="list"),

] + router.urls
