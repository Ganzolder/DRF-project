from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from course.models import Course, Lesson, Subscription
from course.validators import validate_materials
from users.models import Payment


class CourseSerializer(ModelSerializer):
    name = CharField(validators=[validate_materials])
    subscription = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['pk', 'name', 'preview', 'description', 'subscription']

    def get_subscription(self, obj):
        user = self.context['request'].user
        try:
            subscription = Subscription.objects.get(user=user, course=obj)
            return SubscriptionSerializer(subscription).data
        except Subscription.DoesNotExist:
            return None


class LessonSerializer(ModelSerializer):
    name = CharField(validators=[validate_materials])
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


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course', 'created_at']
