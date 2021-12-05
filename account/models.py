from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, related_name="student", on_delete=models.CASCADE)
    roll_no = models.IntegerField()
    grade = models.IntegerField()
    address = models.CharField(max_length=225, null=True, blank=True)
    phone = models.CharField(max_length=225, null=True, blank=True)
    skill = models.ManyToManyField(Skill, related_name="student", blank=True)

    def __str__(self):
        return self.user.username
