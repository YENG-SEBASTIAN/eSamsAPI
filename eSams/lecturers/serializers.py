from rest_framework import serializers

from lecturers.models import LecturerSemeterCourses, Invigilator

class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerSemeterCourses
        fields = ["id", "lecturerID", "level", "className", "courseCode", "courseName", "creditHours"]
        

class InvigilatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invigilator
        fields = ["id", "invigilatorID", "courseCode", "courseName", "created_at"]