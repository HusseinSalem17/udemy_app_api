from django.urls import path
from .views import CourseDetailView, CourseView

urlpatterns = [
    path("courses/", CourseView.as_view(), name="course-list-create"),
    # path("courses/<int:pk>/", CourseView.as_view(), name="course-detail"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
]
