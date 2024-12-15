# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Lesson, Course


# @receiver(post_save, sender=Lesson)
# def update_course_video_length(sender, instance, **kwargs):
#     course = instance.course
#     print("video length nowwww111", instance.title)
#     print("video length nowwww111", instance.video_length)
#     if instance and instance.video.name.endswith((".mp4", ".avi", ".mov", "mkv")):
#         print("video length nowwww", instance.video_length)
#         total_video_length = sum(
#             video.video_length or 0 for video in course.videos.all() if video.video
#         )
#         course.videos_length = total_video_length
#     else:
#         course.down_num += 1
#     course.lesson_num = course.videos.count()
#     course.save()


# @receiver(post_delete, sender=Lesson)
# def update_course_video_length_on_delete(sender, instance, **kwargs):
#     course = instance.course
#     print("video length nowwww", instance.video_length)
#     if instance and instance.video.name.endswith((".mp4", ".avi", ".mov", "mkv")):
#         print("video length nowwww", instance.video_length)
#         total_video_length = sum(
#             video.video_length or 0 for video in course.videos.all() if video.video
#         )
#         course.videos_length = total_video_length
#     else:
#         course.down_num -= 1
#     course.lesson_num = course.videos.count()
#     course.save()
