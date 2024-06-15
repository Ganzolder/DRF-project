from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import Lesson, Course

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        "email address", unique=True, help_text="Введите Ваш город"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", **NULLABLE, help_text="Введите Ваш город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите ваш аватар"
    )
    is_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, **NULLABLE
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оплаты"
    )
    purchased_lesson = models.ForeignKey(
        Lesson, verbose_name="Оплаченный урок", on_delete=models.SET_NULL, **NULLABLE
    )
    purchased_course = models.ForeignKey(
        Course, verbose_name="Оплаченный курс", on_delete=models.SET_NULL, **NULLABLE
    )
    payment_sum = models.SmallIntegerField(
        verbose_name="Сумма оплаты", **NULLABLE
    )
    payment_type = models.CharField(
        max_length=50,
        verbose_name="Результат попытки",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
