from django.db import models
from users.models import UserAccount

# Create your models here.
class SemesterCourses(models.Model):
    studentID = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='StudentID2StudentID')
    courseName = models.CharField(max_length=100)
    courseCode = models.CharField(max_length=15)
    creditHours = models.PositiveIntegerField()
    lecturerID = models.CharField(max_length=200)
    
    def __str__(self):
        return self.courseName
    
class Attendance(models.Model):
    studentID = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    indexNumber = models.CharField(max_length=10)
    courseCode = models.CharField(max_length=15)
    courseName = models.CharField(max_length=100)
    atendanceTime = models.DateTimeField(auto_now=True)
    invigilator = models.CharField(max_length=100)
    isPresent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.indexNumber