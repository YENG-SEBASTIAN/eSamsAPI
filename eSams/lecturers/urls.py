from django.urls import path


from lecturers.views import (lecturer_semester_courses, update_lecturer_semester_courses,
                             get_lecturer_semeter_courses, delete_course, invigilator_add_course, get_single_courses, 
                             invigilator_update_course, get_invigilator_courses, delete_invigilator_courses,
                             GeneratePDFView)

urlpatterns = [
    # lecturer semester CRUD endpoints
    path('lecturerAddSemesterCourse/', lecturer_semester_courses, name="lecturerSAddemesterCourse"),
    path('lecturerUpdateSemesterCourse/<int:pk>/', update_lecturer_semester_courses, name="lecturerUpdateSemesterCourse"),
    path('lecturerGetSemesterCourse/', get_lecturer_semeter_courses, name="lecturerGetSemesterCourse"),
    path('getCourse/<int:pk>/', get_single_courses, name="getCourse"),
    path('lecturerDeleteSemesterCourse/<int:pk>/', delete_course, name="lecturerDeleteSemesterCourse"),

    # invigilator CRUD endpoints
    path('invigilatorAddCourse/', invigilator_add_course, name="invigilatorAddCourse"),
    path('invigilatorUpdateCourse/', invigilator_update_course, name="invigilatorUpdateCourse"),
    path('invigilatorGetCourse/', get_invigilator_courses, name="invigilatorGetCourse"),
    path('invigilatorDeleteCourse/', delete_invigilator_courses, name="invigilatorDeleteCourse"),

    path('GeneratePDFView/<str:course_code>/<str:course_name>/', GeneratePDFView, name='GeneratePDFView'),
]