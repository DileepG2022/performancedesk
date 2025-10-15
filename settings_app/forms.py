from django import forms
from django.forms import inlineformset_factory
from employeereview.models import CourseMilestoneActivity
from .models import Course, Branch, Batch, StudentProfile, FacultyProfile, SalesProfile
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import datetime

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['name']
#         widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'isactive']

class CourseMilestoneActivityForm(forms.ModelForm):
    class Meta:
        model = CourseMilestoneActivity
        fields = ['activity', 'day', 'isactive']

# CourseMilestoneFormSet = inlineformset_factory(
#     Course,
#     CourseMilestoneActivity,
#     form=CourseMilestoneActivityForm,
#     extra=1,
#     can_delete=True
# )


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'branch', 'course', 'faculty','start_date', 'end_date', 'total_students', 'completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_students': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class StudentProfileForm(forms.ModelForm):
#     first_name = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
#     )
#     last_name = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
#     )
#     username = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
#     )

#     class Meta:
#         model = StudentProfile
#         fields = ['student_id', 'branch', 'course', 'batch', 'photo']
#         widgets = {
            
#             'student_id': forms.TextInput(attrs={'class': 'form-control'}),
#             'branch': forms.Select(attrs={'class': 'form-control'}),
#             'course': forms.Select(attrs={'class': 'form-control'}),
#             'batch': forms.Select(attrs={'class': 'form-control'}),
#             'photo': forms.FileInput(attrs={'class': 'form-control'}),
#         }
# class EditStudentProfileForm(forms.ModelForm):
#     # student_id = forms.CharField(
#     #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student ID'})
#     # )
#     # branch = forms.Select(attrs={'class': 'form-control'})
#     # course = forms.Select(attrs={'class': 'form-control'})
#     # batch = forms.Select(attrs={'class': 'form-control'})
#     # photo = forms.FileInput(attrs={'class': 'form-control'})

#     class Meta:
#         model = StudentProfile
#         fields = ['student_id', 'branch', 'course', 'batch', 'photo']  # Removed username & password
#         widgets = {
            
#             'student_id': forms.TextInput(attrs={'class': 'form-control'}),
#             'branch': forms.Select(attrs={'class': 'form-control'}),
#             'course': forms.Select(attrs={'class': 'form-control'}),
#             'batch': forms.Select(attrs={'class': 'form-control'}),
#             'photo': forms.FileInput(attrs={'class': 'form-control'}),
#         }

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
        fields = ['branch', 'courses','mobile_no', 'whatsapp_no']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}),
        }
class FacultyProfileEditForm(forms.ModelForm):
       

    class Meta:
        model = FacultyProfile
        fields = ['branch', 'courses','mobile_no', 'whatsapp_no']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'courses': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}),
        }



class SalesProfileForm(forms.ModelForm):
    # User-related fields (not part of SalesProfile model)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    # SalesProfile-related fields
    mobile_no = PhoneNumberField(region='IN')
    whatsapp_no = PhoneNumberField(region='IN')
    

    class Meta:
        model = SalesProfile
        fields = ['branch', 'mobile_no', 'whatsapp_no', 'reporting_officers']
        widgets = {
            'reporting_officers': forms.CheckboxSelectMultiple
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reporting_officers'].queryset = User.objects.filter(
            groups__name__in=['Sales', 'Manager']
        ).distinct()

class SalesProfileEditForm(forms.ModelForm):
    reporting_officers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name__in=['Sales', 'Manager']).distinct(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = SalesProfile
        fields = ['branch', 'mobile_no', 'whatsapp_no', 'reporting_officers']

class StudentProfileForm(forms.ModelForm):
    # User-related fields (only for add form)
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

    # Admission date (Month-Year picker in UI)
    admission_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'form-control'}),
        label="Admission Month & Year"
    )

    class Meta:
        model = StudentProfile
        fields = ['mobile_no', 'whatsapp_no', 'sales_person', 'drop_out', 'admission_date']
        widgets = {
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}),
            'sales_person': forms.Select(attrs={'class': 'form-control'}),
            'drop_out': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_admission_date(self):
        value = self.cleaned_data['admission_date']

        if isinstance(value, datetime.date):
            return value

        # Try YYYY-MM (from <input type="month">)
        try:
            year, month = map(int, str(value).split('-'))
            return datetime.date(year, month, 1)
        except Exception:
            pass

        # Try DD-MM-YYYY (manual typing or external systems)
        try:
            return datetime.datetime.strptime(str(value), "%d-%m-%Y").date()
        except Exception:
            raise forms.ValidationError("Enter a valid date in YYYY-MM (picker) or DD-MM-YYYY format.")



class StudentProfileEditForm(forms.ModelForm):
    admission_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'form-control'}),
        label="Admission Month & Year"
    )

    class Meta:
        model = StudentProfile
        fields = ['mobile_no', 'whatsapp_no', 'sales_person', 'drop_out', 'admission_date']
        widgets = {
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}),
            'sales_person': forms.Select(attrs={'class': 'form-control'}),
            'drop_out': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_admission_date(self):
        value = self.cleaned_data['admission_date']

        if isinstance(value, datetime.date):
            return value

        # Try YYYY-MM
        try:
            year, month = map(int, str(value).split('-'))
            return datetime.date(year, month, 1)
        except Exception:
            pass

        # Try DD-MM-YYYY
        try:
            return datetime.datetime.strptime(str(value), "%d-%m-%Y").date()
        except Exception:
            raise forms.ValidationError("Enter a valid date in YYYY-MM (picker) or DD-MM-YYYY format.")


class StudentImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Select Excel File",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )