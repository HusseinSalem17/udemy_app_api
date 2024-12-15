import logging
from tempfile import NamedTemporaryFile
from django.db import models
from moviepy.editor import VideoFileClip
from authentication.models import CustomUser
from course.utils import (
    get_upload_path_course_thumbnail,
    get_upload_path_course_thumbnails,
    get_upload_path_course_videos,
)


class CourseType(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        upload_to=get_upload_path_course_thumbnail,
        null=True,
        blank=True,
        max_length=150,
    )
    type = models.ManyToManyField(
        CourseType,
        related_name="courses",
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    type_id = models.SmallIntegerField(null=True, blank=True)
    price = models.FloatField()
    lesson_num = models.SmallIntegerField(null=True, blank=True)
    follow = models.SmallIntegerField(default=0, null=True, blank=True)
    score = models.FloatField(default=0, null=True, blank=True)
    videos_length = models.SmallIntegerField(null=True, blank=True)
    down_num = models.SmallIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE,
    )
    video = models.FileField(
        upload_to=get_upload_path_course_videos,
        null=True,
        blank=True,
        max_length=150,
    )
    thumbnail = models.ImageField(
        upload_to=get_upload_path_course_thumbnails,
        null=True,
        blank=True,
        max_length=150,
    )
    video_length = models.SmallIntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Lesson, self).save(
            *args, **kwargs
        )  # Save the instance first to ensure the file is available
        if self.video and self.video.name.endswith((".mp4", ".avi", ".mov", "mkv")):
            try:
                with NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(self.video.read())
                    temp_file.flush()
                    video_clip = VideoFileClip(temp_file.name)
                    self.video_length = int(video_clip.duration)
                    video_clip.close()
                super(Lesson, self).save(update_fields=["video_length"])
            except Exception as e:
                logging.error(f"Failed to read the video file: {e}")
                self.video_length = 0
