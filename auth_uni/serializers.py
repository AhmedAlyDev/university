from django.db.models.fields import CharField
from auth_uni.models import User
from rest_framework import serializers

from faculties.models import faculty

class RegisterUserSerializer(serializers.Serializer):

    STUDENT = 'Student'
    PROFESSOR = 'Professor'
    TEACHING_ASSISTANT = 'TA'
    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
        (TEACHING_ASSISTANT, 'TA'),
    )

    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)

class EditPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class LogInUserSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

class AddFacultySerializer(serializers.Serializer):
    # email = serializers.EmailField()
    faculty_id = serializers.IntegerField()



    