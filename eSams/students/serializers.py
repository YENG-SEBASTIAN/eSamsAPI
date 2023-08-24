from rest_framework import serializers


from students.models import SemesterCourses, Attendance


class StudentSemesterCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourses
        fields = ['id', 'studentID', 'courseName', 'courseCode', 'creditHours', 'lecturerID']
        

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'studentID', 'indexNumber', 'courseCode', 'courseName', 'atendanceTime', 'invigilator', 'isPresent']