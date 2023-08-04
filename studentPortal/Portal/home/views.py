from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Student, Faculty
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, ListView
from .forms import StudentSignUpForm, FacultySignUpForm, DeptForm, CreateSemesterForm, AssignCourseForm
from .forms import StudentSignUpForm, FacultySignUpForm, DeptForm, CreateSemesterForm, AssignCourseForm
from advising.models import Course, Department, Create_Semester, DropSemesterRequest, TakeCourse, DropStatus
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import date, datetime
from django.http import JsonResponse
from csv import reader
from django.db import transaction


def Homepage(request):
    with open('templates/csv/student_file.csv', 'r') as csv_file:
        csvf = reader(csv_file)
        with transaction.atomic():
            for username, password, FirstName, LastName, semester, department, *__ in csvf:
                u = User.objects.filter(username=username)
                if not u:
                    user = User(username=username, first_name=FirstName, last_name=LastName)
                    user.is_student = True
                    user.set_password(password)
                    user.save()

                    dept = Department(name=department)
                    smstr = Create_Semester(semester=semester)
                    student = Student(user=user, dept=dept, admitted_Semester=smstr)
                    student.save()

    with open('templates/csv/faculty_file.csv', 'r') as csv_f_file:
        csvf2 = reader(csv_f_file)
        with transaction.atomic():
            for username, password, FirstName, LastName, department, *__ in csvf2:
                f = User.objects.filter(username=username)
                if not f:
                    user = User(username=username, first_name=FirstName, last_name=LastName)
                    user.is_faculty = True
                    user.set_password(password)
                    user.save()

                    faculty = Faculty(user=user, dept=department)
                    faculty.save()

    return render(request, 'home/homepage.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'home/student_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('home')


class FacultySignUpView(CreateView):
    model = User
    form_class = FacultySignUpForm
    template_name = 'home/faculty_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'faculty'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('home')


@login_required
def Profile(request):
    student = Student.objects.filter(user=request.user)
    faculty = Faculty.objects.filter(user=request.user)
    print(faculty)

    context = {
        'student': student,
        'faculty': faculty
    }
    return render(request, 'home/profile.html', context)


def DeptView(request):
    form = DeptForm
    if request.method == 'POST':
        deptform = DeptForm(request.POST)
        print(deptform)
        if deptform.is_valid():
            deptform.save()
            messages.success(request, 'submit successfully')
            return redirect('department')

    return render(request, 'home/department.html', {'form': form})


def CreateSemesterView(request):
    form = CreateSemesterForm
    if request.method == 'POST':
        semesterform = CreateSemesterForm(request.POST)

        if semesterform.is_valid():
            semesterform.save()
            messages.success(request, 'submit successfully')
            return redirect('create_semester')

    return render(request, 'home/create_semester.html', {'form': form})


def AssignCourseView(request):
    form = AssignCourseForm
    if request.method == 'POST':
        assignform = AssignCourseForm(request.POST)

        if assignform.is_valid():
            assignform.save()
            messages.success(request, 'submit successfully')
            return redirect('advised_course')

    return render(request, 'home/advised_course.html', {'form': form})


@csrf_exempt
def Schedule(request):
    semester = Create_Semester.objects.values()

    obj = {
        'semesters': semester,
        'courses': 'Null'
    }
    if request.method == 'POST':
        s = request.POST['semester']

        course = (TakeCourse.objects.filter(student_info=request.user.id, current_semester=s))

        obj = {
            'semesters': semester,
            'courses': course
        }
    return render(request, 'home/classSchedule.html', obj)


@csrf_exempt
def semester_drop(request):
    semester = Create_Semester.objects.values()

    obj = {
        'semesters': semester,
        'courses': 'Null'
    }
    if request.method == 'POST':
        s = request.POST['semester']
        msg = request.POST['msg']
        saved = DropSemesterRequest(student_info=request.user, message=msg, semester=s)
        saved.save()

    return render(request, 'home/semester_drop.html', obj)


def Grade_Report(request):
    taken = TakeCourse.objects.filter(student_info=request.user)
    course_list = []
    for x in taken:
        course_list.append(x.course)  # CSE103 , GEN201
    course = Course.objects.filter(course_code__in=course_list)
    # getting unique semesters
    semester_set = []
    for x in taken:
        semester_set.append(x.current_semester)
    semester_set = set(semester_set)
    detail = {}
    grade_c = {"A+": 4, "A": 4, "A-": 3.7, "B+": 3.30, "B": 3.0, "B-": 2.67, "C+": 2.33, "C": 2.0, "C-": 1.67,
               "D+": 1.33, "D": 1.0, "F": 0, 'Did not assign': 1.2}
    sum = 0
    count = 0
    sem_cg = {}
    credit = 0
    for sem in semester_set:
        sum = 0
        credit = 0
        for x in taken:
            for y in course:
                if y.course_code == x.course and sem == x.current_semester:
                    sum += grade_c[x.grade] * x.credit
                    credit += x.credit
        sem_cg[sem] = {"cg": sum / credit}
    #print(sem_cg['Spring-2019'])

    print(semester_set)

    d = datetime.now().strftime("%d %b, %Y")
    print(course)
    obj = {
        "date": d,
        'detail': detail,
        "semesters": semester_set,
        "user": request.user,
        "courses": taken,
        "course_detail": course,
        "semester_cg": sem_cg
    }
    return render(request, 'home/grade_report.html', obj)


def gpa_calculator(grades):
    points = 0
    i = 0
    grade_c = {"A": 4, "A-": 3.7, "B+": 3.33, "B": 3.0, "B-": 2.67, "C+": 2.33, "C": 2.0, "C-": 1.67, "D+": 1.33,
               "D": 1.0, "F": 0}
    if grades != []:
        for grade in grades:
            points += grade_c[grade]
        gpa = points / len(grades)
        return gpa
    else:
        return None


grades = ['A', 'B', 'A', 'C']
print(gpa_calculator(grades))

grades = ['A', 'B', 'C', 'F', 'A', 'B+']
print(gpa_calculator(grades))