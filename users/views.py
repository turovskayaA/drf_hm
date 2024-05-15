from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User, Payments
from users.permissions import IsModerator
from users.serializers import UserSerializer, PaymentsSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_sessions


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateApiView(CreateAPIView):
    """Create Users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    """Edit Users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class UserDeleteAPIView(DestroyAPIView):
    """Delete User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class PaymentsCreateApiView(CreateAPIView):
    """Create Payments"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment.paid_course or payment.paid_lesson)
        price = create_stripe_price(payment.payment_amount, product)
        session_id, payment_link = create_stripe_sessions(price)
        payment.sessions_id = session_id
        payment.link = payment_link
        payment.save()



class PaymentListAPIView(ListAPIView):
    """List Payments"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('date_payment',)
