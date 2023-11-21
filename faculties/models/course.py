from django.db import models
from auth_uni.models import Instructor, Student

class Course(models.Model):
    name = models.CharField(max_length=100)
    prerequisite = models.ManyToManyField('self', blank=True)
    instructors = models.ManyToManyField(Instructor, blank=True)
    students = models.ManyToManyField(Student, blank=True)

class Assessment(models.Model):
    name = models.CharField(max_length=50)
    grade = models.FloatField()
    weight = models.FloatField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)

class AssessmentGrade(models.Model):
    assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    grade = models.FloatField()
    added_by = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)

# class CourseGrade(models.Model):
#     course = models.ForeignKey(Course,on_delete=models.CASCADE)
#     student = models.ForeignKey(Student,on_delete=models.CASCADE)
#     grade = models.FloatField()
#     added_by = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)

