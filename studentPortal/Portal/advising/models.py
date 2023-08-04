from django.db import models
from django.utils.text import slugify
import uuid


class Department(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, primary_key=True,default='')

    def __str__(self):
        return self.name


class Create_Semester(models.Model):
    semester = models.CharField(max_length=100, null=False, blank=False, primary_key=True)
    credit_rate = models.IntegerField( null=False, blank=False)

    def __str__(self):
        return self.semester


class Course(models.Model):
    course_code = models.CharField(max_length=255)
    course_title = models.CharField(max_length=255)
    credit = models.FloatField(blank=False, null=False)
    min_credit_required = models.IntegerField(default=0)
    prerequisite = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.course_code


class AssignedCourse(models.Model):
    slug = models.SlugField(max_length=255, unique=True, default='')
    #assigned_course_id = models.AutoField(primary_key=True, default=False)
    current_semester = models.ForeignKey('Create_Semester', on_delete=models.CASCADE, default=False)
    for_dept = models.ForeignKey('Department', on_delete=models.SET_NULL, null= True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    section = models.IntegerField(blank=False, null=False)
    Time_WeekDay = models.CharField(max_length=255)
    Room = models.CharField(max_length=255)
    available = models.IntegerField(blank=False, null=False)
    taken = models.IntegerField(default=0)
    has_lab = models.BooleanField(default=False)
    l_Time_WeekDay = models.CharField(max_length=255, null=True, blank=True)
    l_Room = models.CharField(max_length=255, null=True, blank=True)
    faculty_initial = models.ForeignKey('home.Faculty', on_delete=models.CASCADE)

    def __str__(self):
        return self.course.course_code

    def save(self):
        self.slug = slugify(str(uuid.uuid4()))
        super(AssignedCourse, self).save()


class TakeCourse(models.Model):
    student_info = models.ForeignKey('home.User', on_delete=models.CASCADE)
    current_semester = models.CharField(max_length=255,default=False)
    course = models.CharField(max_length=255,default=False)
    credit = models.FloatField(blank=False, null=False,default=False)
    section = models.IntegerField(blank=False, null=False,default=False)
    Time_WeekDay = models.CharField(max_length=255,default=False)
    Room = models.CharField(max_length=255, default=False)
    has_lab = models.BooleanField(default=False)
    l_Time_WeekDay = models.CharField(max_length=255, null=True, blank=True)
    l_Room = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=10, blank=True, null=True, default='Did not assign')
    faculty_initial = models.CharField(max_length=255, default='TBA')
    withdraw_status=models.BooleanField(default=False)

    def __str__(self):
        return self.course


class DropSemesterRequest(models.Model):
    student_info=models.ForeignKey('home.User', on_delete=models.CASCADE)
    semester=models.CharField(max_length=255,default=False)
    message=models.CharField(max_length=255,default=False)

    def __str__(self):
        return self.message


class DropStatus(models.Model):
    student_info=models.IntegerField()
    # student_info=models.ForeignKey('home.User',on_delete=models.CASCADE)
    semester=models.CharField(max_length=100,default=False)
    status=models.BooleanField(default=True)