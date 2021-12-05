from django.urls import path, include
from .views import RegisterAPIView, UserViewSet, StudentViewSet, SkillViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"skill", SkillViewSet)
router.register(r"student", StudentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterAPIView.as_view()),
]
