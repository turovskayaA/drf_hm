from rest_framework import viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.permissions import IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator
from materials.tasks import send_update


class CourseViewSet(viewsets.ModelViewSet):
    """ Viewset for Course"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        user = serializer.save()
        user.owner = self.request.user
        user.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if not self.request.user.groups.filter(name='moderator'):
            return Course.objects.filter(owner=self.request.user)
        elif self.request.user.groups.filter(name='moderator'):
            return Course.objects.all()

    def perform_update(self, serializer):
        course = serializer.save()
        course_id = course.id
        send_update.delay(course_id)


class LessonCreateApiView(CreateAPIView):
    """Create Lessons"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]

    def perform_create(self, serializer):
        user = serializer.save()
        user.owner = self.request.user
        user.save()


class LessonListApiView(ListAPIView):
    """List Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = MaterialsPaginator


class LessonRetrieveApiView(RetrieveAPIView):
    """Get for Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    """Edit for Lessons"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    """Delete Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(CreateAPIView):
    """Create Subscriptions"""
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        """ Активация или деактивация подписки """
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(course=course).first()

        if subs_item:
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})
