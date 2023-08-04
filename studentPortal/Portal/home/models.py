from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dept = models.ForeignKey('advising.Department', on_delete=models.CASCADE, default='')
    admitted_Semester = models.ForeignKey('advising.Create_Semester', on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.user.username


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dept = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.user.username
