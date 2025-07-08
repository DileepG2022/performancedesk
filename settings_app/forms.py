from django import forms

from .models import Course, Branch, Batch, StudentProfile, FacultyProfile

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'branch', 'course', 'faculty','start_date', 'end_date', 'completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'branch', 'course', 'batch', 'photo']
        widgets = {
            
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
class EditStudentProfileForm(forms.ModelForm):
    # student_id = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student ID'})
    # )
    # branch = forms.Select(attrs={'class': 'form-control'})
    # course = forms.Select(attrs={'class': 'form-control'})
    # batch = forms.Select(attrs={'class': 'form-control'})
    # photo = forms.FileInput(attrs={'class': 'form-control'})

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'branch', 'course', 'batch', 'photo']  # Removed username & password
        widgets = {
            
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

# class FacultyForm(forms.ModelForm):
#     class Meta:
#         model = FacultyProfile
#         fields = ['user', 'branch', 'courses']
#         widgets = {
#             'user': forms.Select(attrs={'class': 'form-control'}),
#             'branch': forms.Select(attrs={'class': 'form-control'}),
#             'courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
#         }

class FacultyProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    

    class Meta:
        model = FacultyProfile
        fields = ['branch', 'courses']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }