from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='link_video')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set',  many=True, read_only=True)
    subscription = SerializerMethodField()

    @staticmethod
    def get_lesson_count(course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, instance):
        user = self.context.get("request").user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
