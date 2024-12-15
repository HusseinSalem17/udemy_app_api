from django.urls import path
from .views import CourseDetailView, CourseView, LessonDetailView, LessonView

urlpatterns = [
    path("courses/", CourseView.as_view(), name="course-list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    # path("courses/<int:pk>/", CourseView.as_view(), name="course-detail"),
    path("lessons/", LessonView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
]
