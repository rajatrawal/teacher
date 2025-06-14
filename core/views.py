from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Student


def login_view(request):
 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})

    return render(request, 'core/login.html')


@login_required
def logout_view(request):
  
    logout(request)
    return redirect('login')


def register_view(request):

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not (username and password and confirm_password):
            return render(request, 'core/register.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'core/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'core/register.html')




@login_required
def dashboard(request):

    students = Student.objects.all()
    return render(request, 'core/dashboard.html', {'students': students})


@login_required
def add_student(request):

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        subject = request.POST.get('subject', '').strip()
        marks = request.POST.get('marks', '').strip()

        if not (name and subject and marks):
            return redirect('dashboard')

        try:
            marks = int(marks)
        except ValueError:
            return redirect('dashboard')


        student, created = Student.objects.get_or_create(
            name=name,
            subject=subject,
            defaults={'marks': marks}
        )

        if not created:
            student.marks += marks
            student.save()

        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def update_student_ajax(request):

    if request.method == 'POST':
        student_id = request.POST.get('id')
        marks = request.POST.get('marks')

        try:
            student = Student.objects.get(pk=student_id)
            student.marks = int(marks)
            student.save()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'invalid'})


@login_required
def delete_student(request, id):

    Student.objects.filter(id=id).delete()
    return redirect('dashboard')
