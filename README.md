# University Django Rest Framework App

This project is a simple Django Rest Framework (DRF) application for managing a university system.

## Features

- **Courses:** CRUD operations for university courses.
- **Professors:** Manage professors teaching various courses.
- **Students:** Handle student enrollment and details.
- **API Endpoints:** Well-defined endpoints for each entity.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AhmedAliIbrahim53/university.git
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   source venv/Scripts/activate
   # On macOS and Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## Usage

1. Run the development server:

   ```bash
   python manage.py runserver
   ```

2. Access the API endpoints:
   - Faculties: `http://127.0.0.1:8000/faculties/`
   - Courses: `http://127.0.0.1:8000/faculties/courses/`
   - ProfessorsCourses: `http://127.0.0.1:8000/faculties/prof-course/`
   - StudentsCourses: `http://127.0.0.1:8000/faculties/student-course/`
   - ProfessorAssignAndUnAssignUserToACourse: `http://127.0.0.1:8000/faculties/un-assign-user-course/`
   - Assessment: `http://127.0.0.1:8000/faculties/assessment/`
   - AssessmentGrade: `http://127.0.0.1:8000/faculties/assessment-grade/`
   - CourseAssessment: `http://127.0.0.1:8000/faculties/course-assessment/`
   - CourseStudents: `http://127.0.0.1:8000/faculties/course-students/`
   - AddFaculty: `http://127.0.0.1:8000/auth-uni/add-faculty/`

## Contributing

Contributions are welcome! Here's how you can contribute:

- Fork the repository
- Create a new branch (`git checkout -b feature`)
- Make changes and commit (`git commit -am 'Add new feature'`)
- Push to the branch (`git push origin feature`)
- Create a pull request

## License

This project is licensed under the [MIT License](LICENSE).
