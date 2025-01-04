from rest_framework import serializers
from authentication.serializers import UserListSerializer
from course.models import Course, CourseType, Lesson
from django.conf import settings


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = "__all__"


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "thumbnail",
            "description",
        ]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

    def validate(self, data):
        user = self.context["request"].user
        if self.instance and self.instance.course.teacher != user:
            raise serializers.ValidationError("You are not the teacher of this course.")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        frontend_url = settings.FRONTEND_URL_MOBILE

        if instance.video:
            representation["video"] = f"{frontend_url}{instance.video.url}"
        if instance.thumbnail:
            representation["thumbnail"] = f"{frontend_url}{instance.thumbnail.url}"

        return representation


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    type = CourseTypeSerializer(many=True, read_only=True)
    teacher = UserListSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def validate(self, data):
        user = self.context["request"].user
        if self.instance and self.instance.teacher != user:
            raise serializers.ValidationError("You are not the teacher of this course.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        course = Course.objects.create(teacher=user, **validated_data)

        lessons_data = self._extract_lessons_data(self.context["request"])
        for lesson_data in lessons_data:
            Lesson.objects.create(course=course, **lesson_data)

        return course

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        lessons_data = self._extract_lessons_data(self.context["request"])
        for lesson_data in lessons_data:
            Lesson.objects.create(course=instance, **lesson_data)

        return instance

    def _extract_lessons_data(self, request):
        lessons_data = []
        index = 0
        while True:
            lesson_data = {
                "title": request.data.get(f"lessons[{index}][title]"),
                "description": request.data.get(f"lessons[{index}][description]"),
                "thumbnail": request.FILES.get(f"lessons[{index}][thumbnail]"),
                "video": request.FILES.get(f"lessons[{index}][video]"),
            }
            if not any(lesson_data.values()):
                break
            lessons_data.append(lesson_data)
            index += 1
        return lessons_data
