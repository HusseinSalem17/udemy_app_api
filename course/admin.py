from django.utils.html import format_html
from django.contrib import admin
from .models import Course, CourseType, Lesson


class CourseTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "title",
        "description",
        "order",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "title")
    list_filter = ("created_at", "updated_at")


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "course",
        "description",
        "thumbnail_image",
        "video_preview",
        "video_length",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description")
    list_filter = ("video_length", "course", "title")

    def thumbnail_image(self, obj):
        if obj.thumbnail:
            return format_html(
                '<div style="text-align: center;"><a href="{}" target="_blank"><img src="{}" width="80" height="80" /></a></div>',
                obj.thumbnail.url,
                obj.thumbnail.url,
            )
        return "No Image"

    thumbnail_image.short_description = "Thumbnail"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<div style="text-align: center;"><video width="150" height="100" controls style="border-radius: 5px; border: 1px solid #ddd;"><source src="{}" type="video/mp4"></video></div>',
                obj.video.url,
            )
        return "No Video"

    video_preview.short_description = "Video Preview"


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "teacher",
        "thumbnail_image",
        "price",
        "lesson_num",
        "follow",
        "score",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "teacher__username")
    list_filter = ("created_at", "updated_at", "price")
    inlines = [LessonInline]

    def thumbnail_image(self, obj):
        if obj.thumbnail:
            return format_html(
                '<div style="text-align: center;"><a href="{}" target="_blank"><img src="{}" width="80" height="80" /></a></div>',
                obj.thumbnail.url,
                obj.thumbnail.url,
            )
        return "No Image"

    thumbnail_image.short_description = "Thumbnail"


admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
