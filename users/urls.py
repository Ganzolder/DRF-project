from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import PaymentListApiView
from course.views import CourseViewSet
from course.apps import CourseConfig

app_name = CourseConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path("payment/", PaymentListApiView.as_view(), name="payment"),
]

urlpatterns += router.urls
