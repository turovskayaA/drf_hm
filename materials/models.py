from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=35, verbose_name="Названия")
    image = models.ImageField(upload_to="users/", verbose_name="Картинка", **NULLABLE)
    description = models.CharField(max_length=100, verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=35, verbose_name="Названия")
    description = models.CharField(max_length=100, verbose_name="Описание", **NULLABLE)
    image = models.ImageField(upload_to="users/", verbose_name="Картинка", **NULLABLE)
    link_video = models.URLField(
        max_length=100, verbose_name="Ссылка на видео", **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", **NULLABLE
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
