
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_uni.models import Student, Instructor
from faculties.models.faculty import Faculty
from faculties.models.course import Assessment, AssessmentGrade, Course

from faculties.serializers import EditAssessmentGrade, AddGradeToStudentAssessment, EditAssessmentSerializer, RemoveAssessmentSerializer, AddAssessmentToCourseSerializer, AssignAndUnAssignUserToACourseSerializer, CourseSerializer, CourseIdSerializer, EditCourseSerializer, FacultySerializer, CreateCourseSerializer


# Create your views here.

class FacultyView(APIView):
    
    def post(self, request):

        serialized_data = FacultySerializer(data=request.data)

        if serialized_data.is_valid():
            # try:
            #     faculty_name = serialized_data.validated_data.get('name')
            #     entered_faculty = Faculty.objects.get(name=faculty_name)
            # except :
            #     return Response({'error': 'Faculty already exists'})
            
            faculty = Faculty()
            faculty.name = serialized_data.validated_data.get('name')
            faculty.save()
            return Response({'details':'faculty added successfully','faculty': faculty.name},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'data is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        # faculties = Faculty.objects.all()
        # serialized_data = FacultySerializer(faculties,many=True)

        names = [faculty.name for faculty in Faculty.objects.all()]

        return Response({'faculties': names})


class ProfessorCoursesView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    # Professor creates a course 
    def post(self, request):
        serialized_data = CreateCourseSerializer(data=request.data)
        if serialized_data.is_valid():
            course_name = serialized_data.validated_data.get('course_name')
            try:
                Course.objects.get(name=course_name)
                return Response({'error': 'Course already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except Course.DoesNotExist:
                pass
            
            try:
                user = Instructor.objects.get(user=request.user)
                print('I am in')
                if user.type == Instructor.PROFESSOR:
                    course = Course()
                    course.name = serialized_data.validated_data.get('course_name')
                    course.save()
                    course.instructors.add(user)
                    print('done')
                    return Response({'message': 'Course added successfully','course': course.name},status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'TAs can not create courses'},status=status.HTTP_400_BAD_REQUEST)
            except Instructor.DoesNotExist:
                print('error')
                return Response({'error': 'Only professors who can create a course'},status=status.HTTP_400_BAD_REQUEST)
        print('not valid')
        return Response({'errors': 'Data is not valid','details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Professor edits course name
    def put(self, request):
        serialized_data = EditCourseSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
            except Course.DoesNotExist:
                return Response({'error': 'Course does not exist'},status=status.HTTP_400_BAD_REQUEST)
            new_name = serialized_data.validated_data.get('new_course_name')
            if course.name == new_name:
                return Response({'message': 'No changes applied'}, status=status.HTTP_200_OK)
            course.name = new_name
            course.save()
            return Response({'message': 'Course edited successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    # Professor deletes a course
    def delete(self, request):
        serialized_data = CourseIdSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                course.delete()
                return Response({'message': 'Course deleted successfully'},status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({'error': 'Course already does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Professor assign a TA to a course
    def patch(self, request):
        serialized_data = AssignAndUnAssignUserToACourseSerializer(data=request.data)
        try:
            request_prof = Instructor.objects.get(user=request.user)
        except Instructor.DoesNotExist:
            return Response({'error': 'Instructor Does not exist'},status=status.HTTP_400_BAD_REQUEST)
        if request_prof.type == Instructor.PROFESSOR:
            if serialized_data.is_valid():
                try:
                    course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                    TA = Instructor.objects.get(user_id=serialized_data.validated_data.get('user_id')) 
                    if TA.type == Instructor.TEACHING_ASSISTANT:
                        if TA in course.instructors.all():
                            return Response({'error': 'TA is already an instructor in this course'},status=status.HTTP_400_BAD_REQUEST)
                        course.instructors.add(TA)
                        return Response({'message': 'Teaching Assistant added successfully to course','details':{'course name': course.name,'instructor added': TA.user.first_name}})
                    return Response({'error': 'assigned instructor is not a TA'})
                except Course.DoesNotExist:
                    return Response({'error': 'Course Does not exist'},status=status.HTTP_400_BAD_REQUEST)
                except Instructor.DoesNotExist:
                    return Response({'error': 'Assigned instructor Does not exist'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Professors only who can assign an instructor to a course'}, status=status.HTTP_400_BAD_REQUEST)

    
class ProfessorAssignAndUnAssignUserToACourse(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    # Professor removes himself from a course
    def put(self, request):
        serialized_data = CourseIdSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                instructor = Instructor.objects.get(user=request.user)
                if instructor.type == Instructor.PROFESSOR:
                    if instructor in course.instructors.all():
                        course.instructors.remove(instructor)
                        return Response({'message': 'Instructor removed from course successfully','details': {'course': course.name,'removed': instructor.user.first_name}},status=status.HTTP_200_OK)
                    return Response({'error': 'Already not an instructor to course'},status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Only professor can remove himself'}, status=status.HTTP_400_BAD_REQUEST)
            except Course.DoesNotExist:
                return Response({'error': 'Course does not exist'},status=status.HTTP_400_BAD_REQUEST)
            except Instructor.DoesNotExist:
                return Response({'error': 'Instructor does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Professor removes TA from a course
    def patch(self, request):
        serialized_data = AssignAndUnAssignUserToACourseSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                TA = Instructor.objects.get(user_id=serialized_data.validated_data.get('user_id'))
                professor = Instructor.objects.get(user=request.user)
                if professor.type == Instructor.PROFESSOR:
                    if TA.type == Instructor.TEACHING_ASSISTANT:
                        if professor in course.instructors.all():
                            if TA in course.instructor.all():
                                course.instructors.remove(TA)
                                return Response({'message': 'Teaching Assistance removed from course successfully','details': {'course': course.name,'removed': TA.user.first_name}},status=status.HTTP_200_OK)
                            return Response({'error': 'Already not a TA in course'},status=status.HTTP_400_BAD_REQUEST)
                        return Response({'error': 'Only professors in course can remove a TA in course'},status=status.HTTP_400_BAD_REQUEST)
                    return Response({'error': 'Instructor to remove should be a TA'})
                return Response({'error': 'Only professor can remove a TA'}, status=status.HTTP_400_BAD_REQUEST)
            except Course.DoesNotExist:
                return Response({'error': 'Course does not exist'},status=status.HTTP_400_BAD_REQUEST)
            except Instructor.DoesNotExist:
                return Response({'error': 'Instructor does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    # Professor removes student from a course
    def delete(self, request):
        serialized_data = AssignAndUnAssignUserToACourseSerializer(data=request.data)
        professor = Instructor.objects.get(user=request.user)
        if professor.type == Instructor.PROFESSOR:
            if serialized_data.is_valid():
                try:
                    course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                except Course.DoesNotExist:
                    return Response({'error': 'Course does not exist'},status=status.HTTP_400_BAD_REQUEST)
                if professor in course.instructors.all():
                    try:
                        student = Student.objects.get(user_id=serialized_data.validated_data.get('user_id'))
                    except Student.DoesNotExist:
                        return Response({'error': 'Student does not exist'},status=status.HTTP_400_BAD_REQUEST)
                    if student in course.students.all():
                        course.students.remove(student)
                        return Response({'message': 'Student removed successfully from the course'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'error': 'Student already not enrolled in the course'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Professor is not an instructor to the course'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Only professors can remove students from a course'},status=status.HTTP_400_BAD_REQUEST)


class AddOrDeleteOrEditAnAssessmentToCourseView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    # professor creates an assessment
    def post(self, request):
        serialized_data = AddAssessmentToCourseSerializer(data=request.data)
        try:
            professor = Instructor.objects.get(user=request.user)
        except Instructor.DoesNotExist:
            return Response({'error': 'Instructor does not exist'},status=status.HTTP_400_BAD_REQUEST)
        if professor.type == Instructor.PROFESSOR:
            if serialized_data.is_valid():
                try:
                    course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                except Course.DoesNotExist:
                    return Response({'error': 'Course does not exist'},status=status.HTTP_400_BAD_REQUEST)
                if professor in course.instructors.all():
                    assessment = Assessment()
                    assessment.name = serialized_data.validated_data.get('assessment_name')
                    assessment.grade = serialized_data.validated_data.get('grade')
                    assessment.weight = serialized_data.validated_data.get('weight')
                    assessment.course = course
                    assessment.created_by = professor
                    assessment.save()
                    return Response({'message': 'Assessment created successfully'},status=status.HTTP_200_OK)
                return Response({'error': 'Only course professors can create an assessment'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Only professors can add assessment to a course'},status=status.HTTP_400_BAD_REQUEST) 

    # professor deletes his an assessment
    def delete(self, request):
        serialized_data = RemoveAssessmentSerializer(data=request.data)
        try:
            professor = Instructor.objects.get(user=request.user)
        except Instructor.DoesNotExist:
            return Response({'error': 'Instructor does not exist'},status=status.HTTP_400_BAD_REQUEST)
        if professor.type == Instructor.PROFESSOR:
            if serialized_data.is_valid():
                try:
                    assessment = Assessment.objects.get(id=serialized_data.validated_data.get('assessment_id'))
                except Assessment.DoesNotExist:
                    return Response({'error': 'Assessment does not exist'},status=status.HTTP_400_BAD_REQUEST)
                if professor == assessment.created_by:
                    assessment.delete()
                    return Response({'message': 'Assessment deleted successfully'},status=status.HTTP_200_OK)
                return Response({'error': 'Assessment can be deleted only by its creator'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Only professors can delete an assessment from a course'},status=status.HTTP_400_BAD_REQUEST)

    # professor edits his assessment
    def patch(self, request):
        serialized_data = EditAssessmentSerializer(data=request.data)
        try:
            professor = Instructor.objects.get(user=request.user)
        except Instructor.DoesNotExist:
            return Response({'error': 'Instructor does not exist'},status=status.HTTP_400_BAD_REQUEST)
        if serialized_data.is_valid():
            try:
                assessment = Assessment.objects.get(id=serialized_data.validated_data.get('assessment_id'))
            except Assessment.DoesNotExist:
                return Response({'error': 'Assessment does not exist'},status=status.HTTP_400_BAD_REQUEST)
            if professor == assessment.created_by:
                assessment.name = serialized_data.validated_data.get('assessment_name')
                assessment.grade = serialized_data.validated_data.get('grade')
                assessment.weight = serialized_data.validated_data.get('weight')
                assessment.save()
                return Response({'message': 'Assessment edited successfully'})
            return Response({'error': 'Only assessment creator can edit an assessment'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Data is not valid','details': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)


class AddGradeOnAssessment(APIView):

    permission_classes = [permissions.IsAuthenticated]

    # TA add grade to student assessment
    def post(self, request):
        serialized_data = AddGradeToStudentAssessment(data=request.data)
        try:
            TA = Instructor.objects.get(user=request.user)
            if serialized_data.is_valid():
                assessment = Assessment.objects.get(id=serialized_data.validated_data.get('assessment_id'))
                student = Student.objects.get(user_id=serialized_data.validated_data.get('student_id'))
                assessment_grade = AssessmentGrade()
                assessment_grade.assessment = assessment
                assessment_grade.student = student
                assessment_grade.grade = serialized_data.validated_data.get('grade')
                assessment_grade.added_by = TA
                assessment_grade.save()
                return Response({'message': 'Assessment grade added successfully'},status=status.HTTP_200_OK)
            return Response({'error': 'Data is not valid','details': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
        except Instructor.DoesNotExist:
            return Response({'error': 'Teaching Assistance does not exist'},status=status.HTTP_400_BAD_REQUEST)
        except Assessment.DoesNotExist:
            return Response({'error': 'Assessment does not exist'},status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'error': 'Student does not exist'},status=status.HTTP_400_BAD_REQUEST)

    # TA edit grade to student assessment
    def put(self, request):
        serialized_data = EditAssessmentGrade(data=request.data)
        try:
            TA = Instructor.objects.get(user=request.user)
            if serialized_data.is_valid():
                assessment_grade = AssessmentGrade.objects.get(id=serialized_data.validated_data.get('assessment_grade_id'))
                if TA == assessment_grade.added_by:
                    assessment_grade.grade = serialized_data.validated_data.get('grade')
                    assessment_grade.save()
                    return Response({'message': 'Assessment grade edited successfully'},status=status.HTTP_200_OK)
                return Response({'error': 'Only TA who added assessment grade can edit it'})
            return Response({'error': 'Data is not valid','details': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
        except Instructor.DoesNotExist:
            return Response({'error': 'Instructor-TA- does not exist'},status=status.HTTP_400_BAD_REQUEST)
        except AssessmentGrade.DoesNotExist:
            return Response({'error': 'Assessment grade does not exist'},status=status.HTTP_400_BAD_REQUEST)


class StudentCoursesView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    # student views his courses details
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            courses = Course.objects.all()
            student_courses = []
            response = {}
            for course in courses:
                if student in course.students.all():
                    counter = 1
                    student_courses.append(course)
                    #TODO handel instructors and prerequisite response
                    response[counter] = {'name': course.name, 'prerequisite': 'course.prerequisite.all()', 'instructors': 'course.instructors.all()'}
                continue
            return Response({'courses': response},status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student does not exist'},status=status.HTTP_400_BAD_REQUEST)

    # student views(get) specific course details
    def put(self, request):
        serialized_data = CourseIdSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                return Response({'course': {'name': course.name, 'prerequisite': course.prerequisite, 'instructors': course.instructors}},status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({'error': 'Course Does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Student enrolls in a course
    def post(self,request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Only students can enroll in courses'},status=status.HTTP_400_BAD_REQUEST)
        serialized_data = CourseIdSerializer(data=request.data)
        if serialized_data.is_valid():
            course_id = serialized_data.validated_data.get('course_id')
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({'error': 'Course Does not exist'},status=status.HTTP_400_BAD_REQUEST)
            if student in course.students.all():
                return Response({'error': 'you are already enrolled in this course'},status=status.HTTP_400_BAD_REQUEST)
            course.students.add(student)
            return Response({'message': 'Successfully enrolled in course','details':{'course': course.name}})
        return Response({'error': 'Data is not valid', 'details': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class CourseAssessment(APIView):

    permission_classes = [permissions.IsAuthenticated]

    # Student views his course assessments
    def get(self, request):
        serialized_data = CourseIdSerializer(data=request.data)
        try:
            student = Student.objects.get(user=request.user)
            if serialized_data.is_valid():
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                if student in course.students.all():
                    assessments = [{'assessment name': assessment.name, 'grade': assessment.grade, 'weight': assessment.weight, 'course': assessment.course.name, 'auther name': assessment.created_by.user.first_name} for assessment in Assessment.objects.all() if assessment.course == course]
                    print(assessments)
                    return Response({'course assessments': assessments},status=status.HTTP_200_OK)
                return Response({'error': 'Only enrolled students can view course assessment'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Data is not valid', 'details': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'error': 'Student Does not exist'},status=status.HTTP_400_BAD_REQUEST)            


class CourseStudents(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    # Instructor views his students
    def get(self, request):
        serialized_data = CourseIdSerializer(data=request.data)
        try:    
            instructor =Instructor.objects.get(user=request.user)
            if serialized_data.is_valid():
                course = Course.objects.get(id=serialized_data.validated_data.get('course_id'))
                if instructor in course.instructors.all():
                    students = [{'first-name': student.user.first_name} for student in course.students.all()]
                    return Response({'students': students},status=status.HTTP_200_OK)
                return Response({'error': 'Only course instructors can view its students', 'details': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Data is not valid', 'details': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
        except Instructor.DoesNotExist:
            return Response({'error': 'Instructor Does not exist'},status=status.HTTP_400_BAD_REQUEST)            


class CourseView(APIView):
    
    def get(self, request):
        courses_queryset = Course.objects.get_queryset()
        print(courses_queryset[0].name)
        courses = CourseSerializer(courses_queryset)
        # for course in courses_queryset:

        return Response({'Courses': courses.data})


