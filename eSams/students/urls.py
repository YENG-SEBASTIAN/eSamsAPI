from django.urls import path

from students.views import (add_semeter_courses, update_semester_courses, 
                            get_semester_courses, delete_course, get_single_courses,
                            get_attendance)

urlpatterns = [
    # CRUD endpoints  for courses
    path('addSemesterCourses/', add_semeter_courses, name="addSemesterCourses"),
    path('updateSemesterCourses/<int:pk>/', update_semester_courses, name="updateSemesterCourses"),
    path('getSemesterCourses/', get_semester_courses, name="getSemesterCourses"),
    path('getCourse/<int:pk>/', get_single_courses, name="getCourse"),
    path('deleteCourse/<int:pk>/', delete_course, name="deleteCourse"),
    # end of CRUD endpoints for courses

    # CRUD endpoints  for Attendance
    path('getAttendance/', get_attendance, name="getAttendance"),
]