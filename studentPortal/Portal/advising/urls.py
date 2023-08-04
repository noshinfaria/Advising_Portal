#own create file

from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Advising, name='advising'),
    #path('f_course_advising/', views.F_course_Advising, name='f_course_advising'),
    path('delete/', views.deleteTaken, name='delete'),
    path('advising_by_faculty/', views.AdvisingByFaculty, name='advising_by_faculty'),
    path('course_taken/', views.CourseTake, name='course_taken'),
    path('delete_by_faculty/', views.deleteByFaculty, name='delete_by_faculty'),
    path('f_schedule/', views.FacultySchedule, name='f_schedule'),
    path('f_grade/', views.FacultyGradeReport, name='f_grade'),
    path('drop_request/', views.drop_request, name='drop_request'),
    path('drop_course/', views.drop_course, name='drop_course'),
    path('drop/', views.drop, name='drop'),
]
