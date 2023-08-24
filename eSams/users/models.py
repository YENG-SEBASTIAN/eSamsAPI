from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import face_recognition
import json


#customize user model
class ManageUserAccount(BaseUserManager):
    def create_user(self, username, fullName, email, level, role,  password=None, **extra_fields):
        if not username: #as index number
            raise ValueError('Your index number is required')
        if not fullName:
            raise ValueError('Your first name is required')
        if not email:
            raise ValueError('Enter your email address')


        
        email = self.normalize_email(email)
        email = email.lower()
    
        user = self.model(
            username = username, #as index number
            fullName = fullName,
            email = email,
            level =level,
            role = role,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
            
            
    def create_superuser(self, username, fullName, email, level, role, password=None, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")
        
        email = self.normalize_email(email)
        email = email.lower()       
    
        user = self.create_user(
            username = username, #as index number
            fullName = fullName,
            email = email,
            level = level,
            role = role,
            password=password,
            **extra_fields
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class UserAccount(AbstractUser):
    username = models.CharField(max_length=10, unique=True) #as index number
    fullName = models.CharField(max_length = 100)
    email = models.EmailField(max_length=100, unique=True)
    level = models.IntegerField()
    role = models.CharField(max_length=100)



    objects = ManageUserAccount()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullName', 'level', 'role']
    
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    

    
class ProfileInfo(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    programme = models.CharField(max_length=200)
    level = models.IntegerField(default=100)
    about = models.TextField()
    contact = models.CharField(max_length=15)
    picture = models.ImageField(upload_to='profileInfo')
    embedding = models.TextField(blank=True)

    def __str__(self):
        return self.user.fullName
    

    def decode_face(self):
        unknown_face = face_recognition.load_image_file(self.picture)
        face_encoding = face_recognition.face_encodings(unknown_face)[0]
        encoded_data = json.dumps(face_encoding.tolist())
        self.embedding = encoded_data
        self.save()