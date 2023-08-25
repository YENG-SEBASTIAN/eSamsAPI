from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from lecturers.models import LecturerSemeterCourses, Invigilator
from lecturers.serializers import AddCourseSerializer, InvigilatorSerializer
from users.models import UserAccount
from students.models import Attendance
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.utils import timezone


# lecturer add semester courses view
@api_view(["POST"])
def lecturer_semester_courses(request):
    if request.method == "POST":
        user = request.user
        data = {
            "lecturerID": user.id,
            "level": request.data['level'],
            "className": request.data['className'],
            "courseCode": request.data['courseCode'],
            "courseName": request.data['courseName'],
            "creditHours": request.data['creditHours']
        }
        serializer = AddCourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# update lecturer semester courses view
@api_view(["PUT"])
def update_lecturer_semester_courses(request, pk):
    try:
        course = LecturerSemeterCourses.objects.get(id=pk)
    except LecturerSemeterCourses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        user = request.user
        data = {
            "lecturerID": user.id,
            "level": request.data['level'],
            "className": request.data['className'],
            "courseCode": request.data['courseCode'],
            "courseName": request.data['courseName'],
            "creditHours": request.data['creditHours']
        }
        serializer = AddCourseSerializer(course, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# get lecturer semester courses view
@api_view(["GET"])
def get_lecturer_semeter_courses(request):
    user = request.user
    try:
        courses = LecturerSemeterCourses.objects.filter(lecturerID=user.id)
    except LecturerSemeterCourses.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == "GET":
        serializer = AddCourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# getting a single courses
@api_view(["GET"])
def get_single_courses(request, pk):
    try:
        course = LecturerSemeterCourses.objects.get(id=pk)
    except LecturerSemeterCourses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = AddCourseSerializer(course)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# delete a semester course
@api_view(["DELETE"])
def delete_course(request, pk):
    try:
        course = LecturerSemeterCourses.objects.get(id=pk)
    except LecturerSemeterCourses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        course.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)



# ================invigilator view==================

# invigilator add courses
@api_view(["POST"])
def invigilator_add_course(request):
    if request.method == "POST":
        user = request.user
        data = {
            "invigilatorID": user.id,
            "courseCode": request.data['courseCode'],
            "courseName": request.data['courseName']
        }
        serializer = InvigilatorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# invigilator update courses
@api_view(["PUT"])
def invigilator_update_course(request, pk):
    try:
        course = Invigilator.objects.get(id=pk)
    except Invigilator.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        user = request.user
        data = {
            "invigilator": user.id,
            "courseCode": request.data['courseCode'],
            "courseName": request.data['courseName']
        }
        serializer = InvigilatorSerializer(course, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# invilator get invigilated courses 
@api_view(["GET"])
def get_invigilator_courses(request):
    user = request.user
    try:
        courses = Invigilator.objects.filter(invigilatorID=user.id)
    except Invigilator.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == "GET":
        serializer = InvigilatorSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# invigilator delete course
@api_view(["DELETE"])
def delete_invigilator_courses(request, pk):
    try:
        course = Invigilator.objects.get(id=pk)
    except Invigilator.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == "DELETE":
        course.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)




#attendance report view
class AttendancePDFReport(APIView):
    def get(self, request, course_code, course_name):
        try:
            user = request.user
            invigilator = UserAccount.objects.get(id=user.id)
            # Fetch attendance data based on course_code
            attendance_data = Attendance.objects.filter(courseCode=course_code, courseName=course_name, invigilator=invigilator.fullName)
            
            # Create a PDF response
            response = FileResponse(self.generate_pdf(attendance_data, course_code), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{course_code}_attendance_report.pdf"'
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def generate_pdf(self, attendance_data, course_code):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{course_code}_attendance_report.pdf"'
        
        # Create a PDF document
        p = canvas.Canvas(response, pagesize=landscape(letter))
        p.drawString(100, 750, f"Attendance Report for Course: {course_code}")
        p.drawString(100, 730, "Generated on: " + timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Table Header
        y_position = 700
        headers = ['Student ID', 'Index Number', 'Course Code', 'Course Name', 'Attendance Time', 'Invigilator', 'Present']
        for header in headers:
            p.drawString(headers.index(header) * 100, y_position, header)
        
        # Loop through attendance data and add to the PDF
        y_position -= 20
        for attendance in attendance_data:
            data = [
                attendance.studentID.username,
                attendance.indexNumber,
                attendance.courseCode,
                attendance.courseName,
                attendance.atendanceTime.strftime('%Y-%m-%d %H:%M:%S'),
                attendance.invigilator,
                'Yes' if attendance.isPresent else 'No'
            ]
            for item in data:
                p.drawString(data.index(item) * 100, y_position, item)
            y_position -= 20
        
        p.showPage()
        p.save()
        return response
