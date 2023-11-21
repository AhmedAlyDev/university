from django.urls import path
from faculties.views import CourseView, FacultyView, ProfessorCoursesView, StudentCoursesView, ProfessorAssignAndUnAssignUserToACourse, AddOrDeleteOrEditAnAssessmentToCourseView, AddGradeOnAssessment, CourseAssessment, CourseStudents

urlpatterns = [
    path('', FacultyView.as_view()),
    path('courses', CourseView.as_view()),
    path('prof-course', ProfessorCoursesView.as_view()),
    path('student-course', StudentCoursesView.as_view()),
    path('un-assign-user-course', ProfessorAssignAndUnAssignUserToACourse.as_view()),
    path('assessment', AddOrDeleteOrEditAnAssessmentToCourseView.as_view()),
    path('assessment-grade', AddGradeOnAssessment.as_view()),
    path('course-assessment', CourseAssessment.as_view()),
    path('course-students', CourseStudents.as_view())

]



