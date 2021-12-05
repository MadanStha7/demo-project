from django.db.models import F
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .models import Skill, Student
from account.models import Skill
from .serializers import (
    CustomObtainPairSerializer,
    UserRegisterSerializer,
    UserSerializer,
    SkillSerializer,
    StudentSerializer,
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View for custom token
    """

    serializer_class = CustomObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.pop("user")
            res = {
                "token": serializer.validated_data,
                "user_info": UserSerializer(user).data,
            }
            return Response(res)
        except TokenError as e:
            raise InvalidToken(e.args[0])


class RegisterAPIView(generics.GenericAPIView):
    """
    View for user registration
    """

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {"message": "User registered."}
        return Response(serializer.data, response, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.none()

    def get_queryset(self):
        queryset = Student.objects.all()
        queryset = queryset.annotate(student_name=F("user__username"),)
        return queryset
