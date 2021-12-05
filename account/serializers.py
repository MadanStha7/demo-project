from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Skill, Student
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = self.user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]

    def validate(self, attrs):
        name = attrs.get("name")
        if Skill.objects.filter(name=name).exists():
            raise ValidationError({"error": ["Skill with this name already exists"]})
        return attrs


class StudentSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True, read_only=True)
    student_name = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ("id", "student_name", "roll_no", "grade", "address", "phone", "skill")
