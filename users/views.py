from rest_framework import filters
from rest_framework.generics import ListAPIView

from course.serializer import PaymentSerializer
from users.models import Payment


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    serializer_class = PaymentSerializer
    filterset_fields = ['purchased_lesson', 'purchased_course', 'payment_type']
    ordering_fields = ['created_at']
