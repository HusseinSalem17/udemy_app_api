# udemy_app_api/middleware.py

from django.http import JsonResponse
import traceback
from rest_framework import status


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        response_data = {"error": str(exception)}
        # format_exc() returns the traceback of the exception
        print(traceback.format_exc())
        return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
