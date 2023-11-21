from django.contrib import admin
from auth_uni.models import User, UserMobileNumber, Student, Instructor

# Register your models here.
admin.site.register(User)
admin.site.register(UserMobileNumber)
admin.site.register(Student)
admin.site.register(Instructor)