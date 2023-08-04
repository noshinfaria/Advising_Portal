from django.contrib import admin
from .models import Course, AssignedCourse, Create_Semester, Department, TakeCourse, DropSemesterRequest, DropStatus

admin.site.register(Create_Semester)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(AssignedCourse)
admin.site.register(TakeCourse)
admin.site.register(DropStatus)
admin.site.register(DropSemesterRequest)