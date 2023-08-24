import cv2, face_recognition, numpy as np
import requests
import threading, datetime
import requests
from django.core.exceptions import PermissionDenied
from users.models import ProfileInfo, UserAccount
from rest_framework.response import Response
from rest_framework import status
from students.models import Attendance, SemesterCourses
from lecturers.models import Invigilator
from PIL import Image
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.conf import settings
import os, json
# from keras_facenet import FaceNet


developmentURL = 'http://localhost:8000'
productionURL = 'https://sabs.pythonanywhere.com'





def mark_attendance(invigilator, student):
    try:
        invigilator_course = invigilator.invigilator_courses.all().latest("created_at")
        # print("code:", invigilator_course.courseCode)
        # print("invigilator_course", invigilator_course)
        student_course = SemesterCourses.objects.filter(studentID=student, courseCode=invigilator_course.courseCode).first()
        # print("student_course:", student_course)
    except (UserAccount.DoesNotExist, Invigilator.DoesNotExist, SemesterCourses.DoesNotExist):
        return None
    if student_course:
        attendance = Attendance(studentID=student, indexNumber=student.username, invigilator=invigilator.fullName,
                                 courseCode=invigilator_course.courseCode, courseName=invigilator_course.courseName, isPresent=True)
        attendance.save()
        return True
    return None

def has_signed(invigilator, student):
    try:
        invigilator_course = invigilator.invigilator_courses.all().latest("created_at")
        student_course = SemesterCourses.objects.filter(studentID=student, courseCode=invigilator_course.courseCode).first()
    except (UserAccount.DoesNotExist, Invigilator.DoesNotExist, SemesterCourses.DoesNotExist):
        return None
    
    attendance = Attendance.objects.get(studentID=student, courseCode=student_course.courseCode, isPresent=True)
    print(attendance)
    if attendance:
        return True
    return False