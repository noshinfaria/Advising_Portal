from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.db import models
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from .models import AssignedCourse, Course, TakeCourse, Create_Semester, Department,DropSemesterRequest,DropStatus
from django.db.models import Q
from django.views.generic import CreateView, ListView
from django.contrib import messages
from home.models import Student, User


# def Advising(request):
# return render(request, 'advising/advisingPage.html')


@csrf_exempt
def Advising(request):
    user_info = Student.objects.all()
    # info = AssignedCourse.objects.all().order_by('-course')
    # print(user_info)
    current_s = Create_Semester.objects.all()
    s = []
    if current_s:
        s = current_s[len(current_s) - 1]
    info = AssignedCourse.objects.filter(Q(current_semester=s)).order_by('-course')
    previous_taken = TakeCourse.objects.filter(~Q(current_semester__contains=s))
    # print(previous_taken)
    # taken = TakeCourse.objects.filter(
    #     Q(student_info__contains=request.user) and Q(current_semester__contains=s))
    # taken=TakeCourse.objects.filter(student_info=request.user.id ,current_semester=s)
    taken = TakeCourse.objects.filter(Q(current_semester__contains=s))
    course_taken = TakeCourse.objects.filter(current_semester=s, student_info=request.user.id)
    total_credit = 0
    for course in course_taken:

        total_credit += course.credit

    print(total_credit)
    if request.method == 'POST':

        detail = request.POST['details']

        update = AssignedCourse.objects.get(slug=detail)
        total_credit += update.course.credit
        print(total_credit)
        if taken:
            # print((taken[0].student_info.username))
            for x in taken:

                if (request.user.username == x.student_info.username and update.course.course_code == x.course):
                    # return JsonResponse({"status": 300,"msg":"Alerady Added"})
                    messages.error(request, 'Error! Course Already Added.')
                    return JsonResponse({"status": 300})
        b = False
        if update.course.prerequisite:
            for y in previous_taken:
                if (request.user.username == y.student_info.username and update.course.prerequisite == y.course):
                    b = True
                    break
        else:
            b = True
        print(b)
                # for x in info:
                # if x.slug == detail:
        dataTakeCourse = TakeCourse.objects.filter(
            student_info=request.user,  current_semester=update.current_semester,
                Time_WeekDay=update.Time_WeekDay)


        if dataTakeCourse:
            print(dataTakeCourse)
            print(dataTakeCourse[0].student_info)
            messages.error(request, "time collapse")
            return JsonResponse({"status": 404})

        elif (b == False):
            messages.success(request, 'Sorry, At first finish prerequisite courses.')
            return JsonResponse({"status": 500})

        elif (total_credit > 15):
            messages.success(request, 'Sorry, You can not take above 15 credit.')
            return JsonResponse({"status": 600})

            # print(update.taken<update.available)
        elif (update.taken < update.available):
            order = TakeCourse(student_info=request.user, course=update.course.course_code, section=update.section,
                                credit=update.course.credit,
                                Time_WeekDay=update.Time_WeekDay, Room=update.Room, has_lab=update.has_lab,
                                l_Time_WeekDay=update.l_Time_WeekDay, l_Room=update.l_Room,
                                faculty_initial=update.faculty_initial,
                                current_semester=update.current_semester)
            order.save()
            update.taken = update.taken + 1
            update.save()
            messages.success(request, 'Success! Course Added.')
            return JsonResponse({"status": 200})
        else:
            messages.success(request, 'Sorry, sit fill up.')
            return JsonResponse({"status": 500})
    return render(request, 'advising/advisingPage.html', {'info': info, 'taken': taken, 'user_info': user_info, 'previous_taken': previous_taken})




@csrf_exempt
def deleteTaken(request):
    taken = TakeCourse.objects.filter(
        Q(student_info__contains=request.user) and Q(current_semester__contains='Spring-2019'))
    if request.method == 'POST':
        detail = request.POST['details']
        details = detail.split(",")
        # print(details)
        getCourse=Course.objects.filter(course_code=details[0])
        
        update=AssignedCourse.objects.get(course=getCourse[0].id, section=details[1], current_semester=details[3])
        update.taken=update.taken-1
        update.save()

        dat = TakeCourse.objects.filter(course=details[0], section=details[1], student_info=request.user.id)

        dat.delete()

    return JsonResponse({"status": "delete done"})


@csrf_exempt
def AdvisingByFaculty(request):
    user = User.objects.filter(is_student=True)
    semester = Create_Semester.objects.values()

    context = {
        'user': user,
        'semester': semester,
        'student': 'Null',
        'add': 'Null',

    }

    #print(user)

    if request.method == 'POST':
        
        stu = request.POST['user']
        s = request.POST['semester']


        #st = User.objects.get(username=stu)
        add = AssignedCourse.objects.filter(current_semester=s)
        previous_taken = TakeCourse.objects.filter(~Q(current_semester__contains=s))
        student = Student.objects.filter(user=stu)
        taken = TakeCourse.objects.filter(Q(current_semester__contains=s))
        #print(taken)

        context = {
            'user': user,
            'semester': semester,
            'previous_taken': previous_taken,
            'student': student,
            'add': add,
            'taken': taken

        }

    return render(request, 'advising/advising_by_faculty.html', context)


@csrf_exempt
def CourseTake(request):
    if request.method == 'POST':
        
        detail = request.POST['details1']
        details = detail.split(",")

        update = AssignedCourse.objects.get(slug=details[0])
        student = Student.objects.get(user=details[1])
        taken = TakeCourse.objects.filter(student_info=details[1], current_semester=details[2])
        previous_taken = TakeCourse.objects.filter(
            ~Q(current_semester=update.current_semester) and Q(student_info=details[1]))
        print(previous_taken)

        total_credit = 0
        for course in taken:
            total_credit += course.credit

        total_credit += update.course.credit
        print(total_credit)

        if taken:
            for x in taken:
                if (update.course.course_code == x.course):
                    # return JsonResponse({"status": 300,"msg":"Alerady Added"})
                    messages.error(request, 'Error! Course Already Added.')
                    return JsonResponse({"status": 300})

        b = False
        if update.course.prerequisite:
            for y in previous_taken:
                if (y.student_info.username == details[1] and update.course.prerequisite == y.course):
                    b = True
                    break
        else:
            b = True

        dataTakeCourse = TakeCourse.objects.filter(student_info=details[1], current_semester=update.current_semester, Time_WeekDay=update.Time_WeekDay)

        if dataTakeCourse:
            messages.error(request, "time collapse")
            return JsonResponse({"status": 404})

        elif (b == False):
            messages.success(request, 'Sorry, At first finish prerequisite courses.')
            return JsonResponse({"status": 500})

        elif (total_credit > 15):
            messages.success(request, 'Sorry, You can not take above 15 credit.')
            return JsonResponse({"status": 600})

        elif (update.taken < update.available):
            order = TakeCourse(student_info=student.user, course=update.course.course_code, section=update.section,
                                credit=update.course.credit, Time_WeekDay=update.Time_WeekDay, Room=update.Room, has_lab=update.has_lab,
                                l_Time_WeekDay=update.l_Time_WeekDay, l_Room=update.l_Room,
                                faculty_initial=update.faculty_initial,
                                current_semester=update.current_semester)

            order.save()
            update.taken = update.taken + 1
            update.save()
            messages.success(request, 'Success! Course Added.')
            return JsonResponse({"status": 200})


        else:
            messages.success(request, 'Sorry, sit fill up.')
            return JsonResponse({"status": 500})

    return render(request, 'advising/advising_by_faculty.html')


@csrf_exempt
def deleteByFaculty(request):
    if request.method == 'POST':
        detail = request.POST['details']
        details = detail.split(",")
        print(details)
        getCourse = Course.objects.filter(course_code=details[0])

        update = AssignedCourse.objects.get(course=getCourse[0].id, section=details[1], current_semester=details[3])
        update.taken = update.taken - 1
        update.save()

        dat = TakeCourse.objects.filter(course=details[0], section=details[1], student_info=details[2], current_semester=details[3])
        print(dat)
        dat.delete()

    return JsonResponse({"status": "delete done"})


@csrf_exempt
def FacultySchedule(request):
    semester = Create_Semester.objects.values()

    obj = {
        'semesters': semester,
        'courses': 'Null'
    }
    if request.method=='POST':
        s = request.POST['semester']

        course = (AssignedCourse.objects.filter(faculty_initial=request.user.id, current_semester=s))

        obj = {
        'semesters': semester,
        'courses': course
        }
    return render(request, 'advising/Faculty_class_schedule.html', obj)


@csrf_exempt
def FacultyGradeReport(request):
    semester = Create_Semester.objects.values()
    course = Course.objects.values()

    obj = {
        'semesters': semester,
        'courses': course,
        'section': 'Null',
        'studentlists': 'Null'
    }
    if 'course' in request.POST:
        s = request.POST['semester']
        c = request.POST['course']
        sec = request.POST['section']

        if sec == '':
            messages.error(request, "Please fill all the field correctly")
        else:
            studentlist = (TakeCourse.objects.filter(course=c, current_semester=s, section=sec,faculty_initial=request.user))

            obj = {
                'semesters': semester,
                'courses': course,
                'section': sec,
                'studentlists': studentlist
            }
    elif 'primaryid' in request.POST:
        primary_id = request.POST['primaryid']
        stu_grade = request.POST['grade']

        obj2 = TakeCourse.objects.get(id=primary_id)
        print(obj2)

        if obj2 != '':
            obj2.grade = stu_grade
            obj2.save()
            return JsonResponse({"status": 700})
        return render(request, 'advising/Faculty_grade_report.html', obj2)
    return render(request, 'advising/Faculty_grade_report.html', obj)


@csrf_exempt
def drop_request(request):
    req = DropSemesterRequest.objects.all()
    user = User.objects.filter(is_student=True)

    semester = Create_Semester.objects.values()

    context = {
        'user': user,
        'semester': semester,
        'student': 'Null',
        'add': 'Null',
        "req": req

    }
    if request.method == 'POST':
        stu = request.POST['user']
        s = request.POST['semester']
        courses = TakeCourse.objects.filter(student_info=stu, current_semester=s)
        # drop=DropStatus(student_info=)

        courses.delete()

        drop = DropStatus(student_info=stu, semester=s, status=True)
        drop.save()
        print(stu, s)
        # print(courses)

    return render(request, 'advising/drop_request.html', context)


@csrf_exempt
def drop_course(request):
    user = User.objects.filter(is_student=True)
    semester = Create_Semester.objects.values()
    current_s = Create_Semester.objects.all()
    s = []
    if current_s:
        s = current_s[len(current_s) - 1]
    taken = ""

    context = {
        'user': user,
        'semester': semester,

        'add': 'Null',
        'taken': taken

    }

    # print(user)

    if request.method == 'POST':
        stu = request.POST['user1']
        print(stu)
        add = ""

        # st = User.objects.get(username=stu)
        # add = AssignedCourse.objects.filter(current_semester=s)
        previous_taken = TakeCourse.objects.filter(~Q(current_semester__contains=s))
        student = Student.objects.get(user=stu)
        taken = TakeCourse.objects.filter(Q(current_semester__contains=s))
        student = str(student)
        context = {
            'user': user,
            'semester': semester,
            'previous_taken': previous_taken,
            'student': student,
            'add': add,
            'taken': taken,
            'stuId': stu

        }
    return render(request, 'advising/drop_course.html', context)


@csrf_exempt
def drop(request):
    if request.method == 'POST':
        detail = request.POST['details']
        details = detail.split(",")

        dat = TakeCourse.objects.get(course=details[0], section=details[1], student_info=details[4])
        dat.withdraw_status = True
        dat.save()
        return JsonResponse({"status": 200})