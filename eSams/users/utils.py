from users.models import UserAccount
from students.models import Attendance, SemesterCourses
from lecturers.models import Invigilator


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

# def has_signed(invigilator, student):
#     try:
#         invigilator_course = invigilator.invigilator_courses.all().latest("created_at")
#         student_course = SemesterCourses.objects.filter(studentID=student, courseCode=invigilator_course.courseCode).first()
#     except (UserAccount.DoesNotExist, Invigilator.DoesNotExist, SemesterCourses.DoesNotExist):
#         return None
    
#     attendance = Attendance.objects.get(studentID=student, courseCode=student_course.courseCode, isPresent=True)
#     print(attendance)
#     if attendance:
#         return True
#     return False


#Updated has_signed codes
def has_signed(invigilator, student):
    try:
        invigilator_course = invigilator.invigilator_courses.all().latest("created_at")
        student_course = SemesterCourses.objects.filter(studentID=student, courseCode=invigilator_course.courseCode).first()
        
        if student_course:
            attendance = Attendance.objects.get(studentID=student, courseCode=student_course.courseCode, isPresent=True)
            # print("Attendance found:", attendance)
            return True
        else:
            print("Student course not found")
            return False
    except (UserAccount.DoesNotExist, Invigilator.DoesNotExist, SemesterCourses.DoesNotExist):
        # print("Exception occurred: UserAccount, Invigilator, or SemesterCourses does not exist.")
        return None
    except Attendance.DoesNotExist:
        # print("Attendance not found")
        return False
    except Exception as e:
        # print(f"An unexpected error occurred: {e}")
        return None
