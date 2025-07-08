from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)  # Faculty can teach multiple courses
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="faculty_creator")

    def __str__(self):
        return f"Faculty: {self.user.username} ({self.branch.name})"


class Batch(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)  # 🔥 New Foreign Key
    start_date = models.DateField(null=True, blank=True)  #  Added
    end_date = models.DateField(null=True, blank=True)    #  Added
    completed = models.BooleanField(default=False)  # New field to mark batch completion

    def __str__(self):
        status = " (Completed)" if self.completed else ""
        return f"{self.name} ({self.branch.name} - {self.course.name}){status}"


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manager: {self.user.username}"

def student_photo_path(instance, filename):
    # print(instance)
    # print("hi")
    
    # Save photos directly in 'student_photos/' with student_id in filename
    ext = filename.split('.')[-1]  # Get file extension
    filename = f"{instance.student_id}.{ext}"  # Rename file as student_id.ext
    # print(filename)
    return os.path.join("student_photos", filename)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='student_photos/')
    photo = models.ImageField(upload_to=student_photo_path)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically updated on save
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_creator")

    def __str__(self):
        return f"Student: {self.user.username} - {self.student_id}"