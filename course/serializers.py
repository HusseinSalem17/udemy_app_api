from rest_framework import serializers
from authentication.serializers import UserSerializer
from course.models import Course, CourseType, Video


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, required=False)
    type = CourseTypeSerializer(many=True, read_only=True)
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        videos_data = self.context["request"].FILES.getlist("videos")
        course = Course.objects.create(teacher=user, **validated_data)
        print("videos_data", videos_data)
        for video_data in videos_data:
            Video.objects.create(course=course, video=video_data)

        return course

    def update(self, instance, validated_data):
        videos_data = self.context["request"].FILES.getlist("videos")
        instance = super().update(instance, validated_data)

        for video_data in videos_data:
            Video.objects.create(course=instance, video=video_data)

        return instance
