
# Teacher Portal

## Repository

GitHub Repository: [https://github.com/rajatrawal/teacher](https://github.com/rajatrawal/teacher)  
Live Demo: [https://teacher-bpae.onrender.com/](https://teacher-bpae.onrender.com/)



## What updated

### Updated model.py

```python
class Student(models.Model):
    # Added unique must be true so that there will not be any duplicate student at model level
    name = models.CharField(max_length=100, unique=True)


class StudentMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

    # this ensure that there will be only one model of same studen and same subject at model level
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject'], name='unique_student_subject')
        ]
````


### 2. Add student logic

```python
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
```

in add student handled MaxValueValidator, it is not working because it is used in django forms and rest framework here they are validated by default but django save() method don't do any custom validation so there is full_clean() method for validation