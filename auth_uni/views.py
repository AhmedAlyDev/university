from django.db.models.fields import EmailField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

from auth_uni.models import Instructor, Student, User
from auth_uni.serializers import EditPasswordSerializer, LogInUserSerializer, RegisterUserSerializer, UserSerializer, AddFacultySerializer
from faculties.models import faculty
from faculties.models.faculty import Faculty
from faculties.serializers import FacultySerializer

# Create your views here.

class SignUpView(APIView):

    def post(self, request):

        serialized_data = RegisterUserSerializer(data=request.data)

        if serialized_data.is_valid():
            email = serialized_data.validated_data.get('email')

            try:
                User.objects.get(email=email)
                return Response({'error': 'User with the same email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                pass

            user = User()
            user.email = email
            user.username = email
            user.set_password(serialized_data.validated_data.get('password'))
            user.first_name = serialized_data.validated_data.get('first_name')
            user.last_name = serialized_data.validated_data.get('last_name')
            user.date_of_birth = serialized_data.validated_data.get('date_of_birth')
            user.save()

            type = serialized_data.validated_data.get('type')
            if type == RegisterUserSerializer.STUDENT:
                student = Student()
                student.user = user
                student.save()
            else:
                instructor = Instructor()
                instructor.user = user
                instructor.type = type
                instructor.save()


            token = Token.objects.create(user=user)

            return Response({'message': 'User created successfully', 'data': {'user': UserSerializer(user).data, 'token': token.key}}, status=status.HTTP_200_OK)
        
        return Response({'error': 'data is not valid'}, status=status.HTTP_400_BAD_REQUEST)

class LogInView(APIView):

    def post(self, request):
        serialized_data = LogInUserSerializer(data=request.data)
        if serialized_data.is_valid():
            email = serialized_data.validated_data['email']
            password = serialized_data.validated_data['password']
        
            try:
                login_user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'})
            
            if login_user.check_password(password):
                token = Token.objects.get_or_create(user=login_user)
                print(token)
                return Response({'token': token[0].key, 'email': login_user.email}, status=status.HTTP_201_CREATED)
            else:
                return Response({"4xx": "password is not correct"})
        else:
             return Response({"4xx": "Entered data is not valid"})

class EditPasswordView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serialized_data = EditPasswordSerializer(data=request.data)
        if serialized_data.is_valid():
            user = request.user
            if not user.check_password(serialized_data.validated_data.get('old_password')):
                return Response({'error': 'you entered a wrong password'},status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serialized_data.validated_data.get('new_password'))
            user.save()
            return Response({'message': 'Password updated successfully'},status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class AddFacultyView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serialized_data = AddFacultySerializer(data=request.data)
        if serialized_data.is_valid():
            # email = serialized_data.validated_data.get('email')
            # try:
                # editing_user = User.objects.get(email=email)
            # except User.DoesNotExist:
            #     return Response({'error':'User does not exists'},status=status.HTTP_400_BAD_REQUEST)

            faculty_id = serialized_data.validated_data.get('faculty_id')
            editing_user = User.objects.get(auth_token=request.auth)
            try:
                faculty= Faculty.objects.get(id=faculty_id)
            except Faculty.DoesNotExist:
                return Response({'error':'Faculty does not exist'},status=status.HTTP_400_BAD_REQUEST)
            editing_user.faculty = faculty
            editing_user.save()
            # request.user.faculty = serialized_data.validated_data.get('faculty_id')
            return Response({'message':'Faculty added successfully','user':{'email':editing_user.email,'faculty':editing_user.faculty.id}},status=status.HTTP_200_OK)
        else:
            return Response({'error':'data is not valid'},status=status.HTTP_400_BAD_REQUEST)