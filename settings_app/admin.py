from django.contrib import admin
from .models import Branch, Course, Batch, ManagerProfile, FacultyProfile, StudentProfile



admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(ManagerProfile)
admin.site.register(FacultyProfile)
admin.site.register(StudentProfile)

