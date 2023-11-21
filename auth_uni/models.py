from django.db import models
from django.contrib.auth.models import AbstractUser
from faculties.models.faculty import Faculty

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','date_of_birth']

class UserMobileNumber(models.Model):
    mobile_number = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    current_year = models.IntegerField(default=1)

class Instructor(models.Model):

    PROFESSOR = 'Professor'
    TEACHING_ASSISTANT = 'TA'
    USER_TYPE_CHOICES = (
        (PROFESSOR, 'Professor'),
        (TEACHING_ASSISTANT, 'TA'),
    )

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)



