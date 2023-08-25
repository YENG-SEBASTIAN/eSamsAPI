from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from students.models import SemesterCourses, Attendance
from users.models import ProfileInfo, UserAccount
from students.serializers import StudentSemesterCoursesSerializer, StudentAttendanceSerializer


# student adding courses view
@api_view(["POST"])
def add_semeter_courses(request):
    if request.method == "POST":
        user = request.user
        data = {
            "studentID": user.id,
            "courseName": request.data['courseName'],
            "courseCode": request.data['courseCode'],
            "creditHours": request.data['creditHours'],
            "lecturerID": request.data['lecturerID']
        }
        serializer = StudentSemesterCoursesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# updating semester courses view
@api_view(["PUT"])
def update_semester_courses(request, pk):
    try:
        course = SemesterCourses.objects.get(id=pk)
    except SemesterCourses.DoesNotExist:
        pass
    if request.method == "PUT":
        user = request.user
        data = {
            "studentID": user.id,
            "courseName": request.data['courseName'],
            "courseCode": request.data['courseCode'],
            "creditHours": request.data['creditHours'],
            "lecturerID": request.data['lecturerID']           
        }
        serializer = StudentSemesterCoursesSerializer(course, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# getting setmester courses
@api_view(["GET"])
def get_semester_courses(request):
    if request.method == "GET":
        user = request.user
        courses = SemesterCourses.objects.filter(studentID=user.id)
        serializer = StudentSemesterCoursesSerializer(courses, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# getting a single courses
@api_view(["GET"])
def get_single_courses(request, pk):
    try:
        course = SemesterCourses.objects.get(id=pk)
    except SemesterCourses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StudentSemesterCoursesSerializer(course)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# deleting a semeter course
@api_view(["DELETE"])
def delete_course(request, pk):
    try:
        course = SemesterCourses.objects.get(id=pk)
    except SemesterCourses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        course.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)



# get student attendance view
@api_view(["GET"])
def get_attendance(request):
    user = request.user
    try:
        attendance = Attendance.objects.filter(studentID=user.id)
    except Attendance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StudentAttendanceSerializer(attendance, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)