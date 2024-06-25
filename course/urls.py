from django.urls import path
from rest_framework.routers import SimpleRouter

from course.views import (
    LessonUpdateApiView,
    LessonListApiView,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonRetrieveApiView, SubscriptionView,
)
from course.views import CourseViewSet
from course.apps import CourseConfig

app_name = CourseConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename='course')


urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson_delete"
    ),
    path('subscribe/<int:pk>/', SubscriptionView.as_view(), name='subscribe'),
]

urlpatterns += router.urls
