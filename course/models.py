from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="course/preview",
        **NULLABLE,
        verbose_name="Превью",
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        verbose_name="Описание", **NULLABLE, help_text="Введите описание курса"
    )
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор", help_text="Укажите автора")


class Lesson(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="course/preview",
        **NULLABLE,
        verbose_name="Превью",
        help_text="Загрузите превью урока",
    )
    description = models.TextField(
        verbose_name="Описание", **NULLABLE, help_text="Введите описание урока"
    )
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.SET_NULL, **NULLABLE
    )
    video = models.URLField(
        **NULLABLE,
        verbose_name="Ссылка на видео",
        help_text="Прикрепите ссылку на видео урока",
    )
    objects = models.Manager()

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор",
                              help_text="Укажите автора")
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
