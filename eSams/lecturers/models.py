from django.db import models

from users.models import UserAccount


class LecturerSemeterCourses(models.Model):
    lecturerID = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    level = models.IntegerField()
    className = models.CharField(max_length=200)
    courseCode = models.CharField(max_length=10)
    courseName = models.CharField(max_length=200)
    creditHours = models.IntegerField()
    
    def __str__(self):
        return self.courseName 
    
    

class Invigilator(models.Model):
    invigilatorID = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='invigilator_courses')
    courseCode = models.CharField(max_length=15)
    courseName = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.courseName