from rest_framework import status, serializers, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from udemy_app_api.utils import handle_validation_error
from .models import Course
from .serializers import CourseSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class CourseView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CourseSerializer

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data,
                context={
                    "request": request,
                },
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    "msg": "Course created successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)

    # def put(self, request, pk):
    #     try:
    #         course = Course.objects.get(pk=pk)
    #     except Course.DoesNotExist:
    #         return Response(
    #             {"error": "Course not found"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     try:
    #         serializer = CourseSerializer(course, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except serializers.ValidationError as e:
    #         return handle_validation_error(e)

    # @ratelimit(key="user", rate="60/m", method="ALL")
    # def delete(self, request, pk):
    #     try:
    #         course = Course.objects.get(pk=pk)
    #     except Course.DoesNotExist:
    #         return Response(
    #             {"error": "Course not found"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     course.delete()
    #     return Response(
    #         {"msg": "Course deleted successfully"},
    #         status=status.HTTP_204_NO_CONTENT,
    #     )


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        serializer.save(teacher=self.request.user)