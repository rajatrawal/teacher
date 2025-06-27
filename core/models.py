from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# class Student(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     name = models.CharField(max_length=100)
#     subject = models.CharField(max_length=100)
#     marks = models.IntegerField(validators=[MaxValueValidator(100)])


#     def save(self):
#         if self.marks > 100:
#             raise Exception("The values must be less than 100")
#         return super().save()

#     def __str__(self):
#         return f"{self.name} - {self.subject}"


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
