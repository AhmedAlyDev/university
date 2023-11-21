from django.contrib import admin
from faculties.models.course import Course, Assessment, AssessmentGrade
from faculties.models.faculty import Faculty


# Register your models here.
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Assessment)
admin.site.register(AssessmentGrade)


