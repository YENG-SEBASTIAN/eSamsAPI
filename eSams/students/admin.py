from django.contrib import admin

from students.models import SemesterCourses, Attendance

class SemesterCoursesAdmin(admin.ModelAdmin):
    list_display = ("studentID", "courseName", "courseCode", "creditHours", "lecturerID")
    search_fields = ("studentID", "courseCode", "lecturerID")
    list_filter = ("studentID", "courseCode")
    

admin.site.register(SemesterCourses, SemesterCoursesAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("studentID", "indexNumber", "courseCode", "courseName", "atendanceTime", "isPresent", "invigilator")
    search_fields = ("studentID", "courseCode", "indexNumber")
    list_filter = ("studentID", "indexNumber", "courseCode")
    

admin.site.register(Attendance, AttendanceAdmin)