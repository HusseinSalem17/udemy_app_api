from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from udemy_app_api.utils import handle_validation_error
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


@api_view(["POST"])
def user_register(request):
    if request.method == "POST":
        try:
            print("data in user_register:", request.data)
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"msg": "User registered successfully."}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        try:
            serializer = UserLoginSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token is None:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
