from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from course.serializer import PaymentSerializer
from users.models import Payment, User
from users.serializer import UserSerializer


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    serializer_class = PaymentSerializer
    filterset_fields = ['purchased_lesson', 'purchased_course', 'payment_type']
    ordering_fields = ['created_at']


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
