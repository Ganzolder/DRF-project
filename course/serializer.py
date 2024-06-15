from rest_framework.serializers import ModelSerializer, SerializerMethodField

from course.models import Course, Lesson
from users.models import Payment


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):

    lessons_counts_course = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_lessons(self, course):
        lessons = Lesson.objects.filter(course=course)
        return LessonSerializer(lessons, many=True).data
    def get_lessons_counts_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_counts_course", "lessons")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"



