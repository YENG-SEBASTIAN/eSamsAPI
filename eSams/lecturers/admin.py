from django.contrib import admin

from  lecturers.models import LecturerSemeterCourses, Invigilator


class LecturerSemeterCoursesAdmin(admin.ModelAdmin):
    list_display = ("lecturerID", "level", "className", "courseCode", "courseName", "creditHours")
    search_fields = ("lecturerID", "level", "courseCode")
    list_filter = ("lecturerID", "level", "courseCode")
    

admin.site.register(LecturerSemeterCourses, LecturerSemeterCoursesAdmin)

class InvigilatorAdmin(admin.ModelAdmin):
    list_display = ("invigilatorID", "courseCode",  "courseName")
    search_fields = ("invigilatorID", "courseCode", "courseName")
    list_filter = ("invigilatorID", "courseCode", "courseName")
    

admin.site.register(Invigilator, InvigilatorAdmin)