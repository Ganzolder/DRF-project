from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from course.models import Course, Lesson, Subscription
from users.models import User
from contextlib import contextmanager
from django.contrib.auth.models import Group

@contextmanager
def user_in_group(user, group_name):

    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    try:
        yield
    finally:
        user.groups.remove(group)

class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='eeeddd@example.com')
        self.course = Course.objects.create(name='Курс шинника', owner=self.user)
        self.lesson = Lesson.objects.create(name='Сцепление', description='От чего зависит сцепление', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('course:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data['name'], self.lesson.name)

    def test_lesson_create(self):
        url = reverse('course:lesson_create')
        data = {
            'name': 'Комфорт',
            'description': 'От чего зависит комфорт',
            'owner': self.user.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        url = reverse('course:lesson_update', args=(self.lesson.pk,))
        data = {
            'name': 'Шумность',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get('name'), 'Шумность')

    def test_lesson_delete(self):
        url = reverse('course:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('course:lesson')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCourseCRUD(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Курс 1', owner=self.user)

    def test_create_course(self):
        url = reverse('course:course-list')
        data = {
            'name': 'Новый курс',
            'owner': self.user.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)  # Assuming initially there was 1 course

    def test_retrieve_course(self):
        url = reverse('course:course-detail', args=[self.course.pk])
        with user_in_group(self.user, 'moders'):
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.course.name)

    def test_update_course(self):
        url = reverse('course:course-detail', args=[self.course.pk])
        updated_name = 'Новое имя'
        data = {
            'name': updated_name
        }
        with user_in_group(self.user, 'moders'):
            response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_name)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='password')
        self.course = Course.objects.create(name='Тестовый курс', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_course(self):
        url = reverse('course:subscribe', args=(self.course.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_course(self):
        # Сначала подписываемся на курс
        Subscription.objects.create(user=self.user, course=self.course)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Теперь отписываемся от курса
        url = reverse('course:subscribe', args=(self.course.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_course_retrieve_with_subscription(self):
        # Подписываемся на курс
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('course:course-detail', args=(self.course.pk,))
        with user_in_group(self.user, 'moders'):
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsNone(data.get('is_subscribed'))

    def test_course_retrieve_without_subscription(self):
        url = reverse('course:course-detail', args=(self.course.pk,))
        with user_in_group(self.user, 'moders'):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertFalse(data.get('is_subscribed'))