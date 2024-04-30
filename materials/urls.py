from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateApiView,
                             LessonDestroyApiView, LessonListApiView,
                             LessonRetrieveApiView, LessonUpdateApiView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"materials", CourseViewSet, basename="materials")

urlpatterns = [
    path("lesson/create/", LessonCreateApiView.as_view(), name="create"),
    path("lesson/", LessonListApiView.as_view(), name="list"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="get"),
    path("lesson/update/<int:pk>/", LessonUpdateApiView.as_view(), name="update"),
    path("lesson/delete/<int:pk>/", LessonDestroyApiView.as_view(), name="delete"),
] + router.urls
