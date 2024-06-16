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
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    @staticmethod
    def get_lessons_counts_course(course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_counts_course", "lessons")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
