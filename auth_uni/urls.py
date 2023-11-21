from django.urls import path
from auth_uni.views import AddFacultyView, EditPasswordView, SignUpView, LogInView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LogInView.as_view()),
    path('add-faculty/', AddFacultyView.as_view()),
    path('edit-password/', EditPasswordView.as_view()),

]