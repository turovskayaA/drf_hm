from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class MaterialsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.ru",
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        self.user.set_password("12345")
        self.user.save()

        self.course = Course.objects.create(
            title="course 1", description="testing", owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        url = reverse("materials:sub_create")
        response = self.client.post(url, data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(),  {'message': 'Подписка добавлена'})
