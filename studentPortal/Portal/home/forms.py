from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from advising.models import Create_Semester, Department, AssignedCourse
from .models import Student, User, Faculty
from django.db.models import Q


class StudentSignUpForm(UserCreationForm):
    dept = forms.ModelChoiceField(queryset=Department.objects.filter(~Q(name='Select All')).order_by('name'))
    admitted_Semester = forms.ModelChoiceField(queryset=Create_Semester.objects.all().order_by('semester'))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.admitted_Semester = self.cleaned_data.get('admitted_Semester')
        student.dept = self.cleaned_data.get('dept')
        student.save()

        return user


class FacultySignUpForm(UserCreationForm):
    dept = forms.ModelChoiceField(queryset=Department.objects.filter(~Q(name='Select All')).order_by('name'))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_faculty = True
        user.save()
        faculty = Faculty.objects.create(user=user)
        faculty.admitted_Semester = self.cleaned_data.get('admitted_Semester')
        faculty.save()

        return user


class DeptForm(forms.ModelForm):
    class Meta:
        model = Department
        fields='__all__'


class CreateSemesterForm(forms.ModelForm):
    class Meta:
        model = Create_Semester
        fields='__all__'


class AssignCourseForm(forms.ModelForm):
    class Meta:
        model = AssignedCourse
        fields= '__all__'