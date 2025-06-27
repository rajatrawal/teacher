from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Student, StudentMark
from django.core.exceptions import ValidationError


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
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    student_marks = StudentMark.objects.select_related('student').all()
    return render(request, 'core/dashboard.html', {'student_marks': student_marks})


@login_required
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        marks = int(request.POST.get('marks'))
       
        student, isStudentCreated = Student.objects.get_or_create(name=name)

        student_mark = StudentMark.objects.filter(student=student, subject=subject).first()
        if student_mark:
                student_mark.marks += marks
        else:
                student_mark = StudentMark(student=student,subject=subject,marks=marks)

        
        try:
            student_mark.full_clean()
            student_mark.save()
        except ValidationError as e:
            print(e)
            
            return redirect('dashboard')

        return redirect('dashboard')

    return redirect('dashboard')



@login_required
def update_student_ajax(request):
    if request.method == 'POST':
        mark_id = request.POST.get('id')
        marks = request.POST.get('marks')

        try:
            marks = int(marks)

            student_mark = StudentMark.objects.get(pk=mark_id)
            student_mark.marks = marks

            student_mark.full_clean()

            student_mark.save()
            return JsonResponse({'status': 'success'})
        except (ValueError, StudentMark.DoesNotExist) as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Student mark not found '})
        except ValidationError as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Marks must be less than equal to 100'})

    return JsonResponse({'status': 'invalid'})


@login_required
def delete_student(request, id):
    StudentMark.objects.filter(id=id).delete()
    return redirect('dashboard')
