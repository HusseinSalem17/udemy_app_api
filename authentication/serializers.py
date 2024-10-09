from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField


class UserRegisterSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "avatar",
            "type",
            "open_id",
            "name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return data

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            name=validated_data["name"],
            avatar=validated_data.get(
                "avatar",
                "profile_pics/default.png",
            ),
            open_id=validated_data.get("open_id"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def validate(self, data):
        request = self.context.get("request")
        email = data.get("email")
        password = data.get("password")
        if request.user.is_authenticated:
            return serializers.ValidationError("User already logged in")
        elif email and password:
            user = authenticate(email=email, password=password)
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Email and password are required")
        return data

    def create(self, validated_data):
        email = validated_data["email", None]
        password = validated_data["password", None]
        user = authenticate(email=email, password=password)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "avatar",
            "type",
            "open_id",
            "name",
            "email",
            "verified_at",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "verified_at": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
