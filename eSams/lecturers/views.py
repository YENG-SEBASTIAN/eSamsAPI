from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from lecturers.models import LecturerSemeterCourses, Invigilator
from lecturers.serializers import AddCourseSerializer, InvigilatorSerializer
from users.models import UserAccount
from students.models import Attendance
from reportlab.lib.pagesizes import letter, landscape
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, 
                                Image, Preformatted, Spacer, Paragraph )
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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


#generate a pdf report

@api_view(['GET'])
def GeneratePDFView(request, course_code, course_name):
    if request.method == "GET":
        user = request.user
        invigilator = UserAccount.objects.get(id=1)
        print(user)
        # Query the Attendance model to retrieve data
        queryset = Attendance.objects.filter(courseCode=course_code, courseName=course_name, invigilator=invigilator.fullName)

        # Create a PDF buffer
        buffer = BytesIO()

        # Create the PDF object using the buffer
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

        # Create a table to hold the data
        data = []
        data.append(['Name', 'Index Number', 'Course Code', 'Course Name', 'Attendance Time', 'Invigilator', 'Status'])
        
        for attendance in queryset:
            data.append([
                attendance.studentID.fullName,
                attendance.indexNumber,
                attendance.courseCode,
                attendance.courseName,
                attendance.atendanceTime.strftime('%Y-%m-%d %H:%M:%S'),
                attendance.invigilator,
                'Present' if attendance.isPresent else 'Absent'
            ])

        table = Table(data)

        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))

        # Build the PDF document
        elements = []

        # Add a title to the PDF
        title_style = ParagraphStyle(
            "title_style",
            fontSize=20,  # Increase font size
            textColor=colors.blue,  # Set title color to blue
            alignment=1  # Center alignment
        )
        title_text = "<h1><b>Smart E-Attendance System Report</b></h1>"
        title = Paragraph(title_text, title_style)
        elements.append(title)
        
        # Add space between title and table
        elements.append(Spacer(1, 20))

        elements.append(table)
        doc.build(elements)

        # Rewind the buffer
        buffer.seek(0)

        # Create a response with the PDF file
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{course_code} attendance.pdf"'

        return response