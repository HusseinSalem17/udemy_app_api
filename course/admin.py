from django.utils.html import format_html
from django.contrib import admin
from .models import Course, CourseType, Video


class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "description", "order", "created_at", "updated_at")
    search_fields = ("name", "title")
    list_filter = ("created_at", "updated_at")


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


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
    inlines = [VideoInline]

    def thumbnail_image(self, obj):
        if obj.thumbnail:
            return format_html(
                '<div style="text-align: center;"><img src="{}" width="50" height="50" /></div>',
                obj.thumbnail.url,
            )
        return "No Image"

    thumbnail_image.short_description = "Thumbnail"


admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(Course, CourseAdmin)
