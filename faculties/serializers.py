from rest_framework import fields, serializers
from auth_uni.models import Instructor
from faculties.models import course
from faculties.models.course import Course

from faculties.models.faculty import Faculty

class FacultySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Faculty
        fields = '__all__'

class CreateCourseSerializer(serializers.Serializer):
    course_name = serializers.CharField()

class EditCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=True)
    new_course_name = serializers.CharField()

class CourseIdSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=True)

class AssignAndUnAssignUserToACourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class AddAssessmentToCourseSerializer(serializers.Serializer):
    assessment_name = serializers.CharField(max_length=50)
    grade = serializers.FloatField()
    weight = serializers.FloatField()
    course_id = serializers.IntegerField()

class RemoveAssessmentSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()

class EditAssessmentSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    assessment_name = serializers.CharField(max_length=50)
    grade = serializers.FloatField()
    weight = serializers.FloatField()

class AddGradeToStudentAssessment(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    grade = serializers.FloatField()

class EditAssessmentGrade(serializers.Serializer):
    assessment_grade_id = serializers.IntegerField()
    grade = serializers.FloatField()


