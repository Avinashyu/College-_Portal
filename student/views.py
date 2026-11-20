from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student_table
from .forms import RegistrationForm, StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer


def home(request):
    data1 = {
        'name': "Pratiksha",
        'age': 19,
        'department': "BCA"
    }

    marks = [100, 99, 98]

    return render(request, 'home.html', {
        'data1': data1,
        'marks1': marks
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def forms1(request):
    return manual_student_form(request)


def student_form_dj(request):
    return student_form(request)


def student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student registered successfully.')
            return redirect('student_form')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})


def manual_student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student registered successfully.')
            return redirect('student_form')
    else:
        form = StudentForm()
    return render(request, 'student_form_manual.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now sign in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


@login_required(login_url='login')
def dashboard(request):
    students = Student_table.objects.all().order_by('name')
    return render(request, 'dashboard.html', {'students': students})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return HttpResponse("Invalid request method.")
@api_view(['GET', 'POST'])
def student_api(request):
    if request.method == 'GET':
        students = Student_table.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)