# from django import forms
# from django.forms import modelformset_factory
# from .models import FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity

# class FacultyMonthlyReviewForm(forms.ModelForm):
#     class Meta:
#         model = FacultyMonthlyReview
#         fields = ['user', 'batch', 'start_date', 'end_date', 'total_students', 'review_month']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#         }

# class FacultyMonthlyMetricForm(forms.ModelForm):
#     class Meta:
#         model = FacultyMonthlyMetric
#         fields = ['metric_name', 'metric_value']

# class FacultyMonthlyActivityForm(forms.ModelForm):
#     class Meta:
#         model = FacultyMonthlyActivity
#         fields = ['activity', 'day', 'planned_date', 'completed_date', 'status', 'participation', 'remarks']
#         widgets = {
#             'planned_date': forms.DateInput(attrs={'type': 'date'}),
#             'completed_date': forms.DateInput(attrs={'type': 'date'}),
#         }

# FacultyMonthlyMetricFormSet = modelformset_factory(FacultyMonthlyMetric, form=FacultyMonthlyMetricForm, extra=5)
# FacultyMonthlyActivityFormSet = modelformset_factory(FacultyMonthlyActivity, form=FacultyMonthlyActivityForm, extra=5)





# forms.py

from django import forms
from django.forms import modelformset_factory
from .models import FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity

class FacultyMonthlyReviewForm(forms.ModelForm):
    class Meta:
        model = FacultyMonthlyReview
        fields = ['user', 'batch', 'start_date', 'end_date', 'total_students', 'review_month']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FacultyMonthlyMetricForm(forms.ModelForm):
    class Meta:
        model = FacultyMonthlyMetric
        fields = ['metric_name', 'metric_value']

class FacultyMonthlyActivityForm(forms.ModelForm):
    class Meta:
        model = FacultyMonthlyActivity
        fields = ['activity', 'day', 'planned_date', 'completed_date', 'status', 'participation', 'remarks']
        widgets = {
            'planned_date': forms.DateInput(attrs={'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }

FacultyMonthlyMetricFormSet = modelformset_factory(
    FacultyMonthlyMetric, form=FacultyMonthlyMetricForm, extra=0
)

FacultyMonthlyActivityFormSet = modelformset_factory(
    FacultyMonthlyActivity, form=FacultyMonthlyActivityForm, extra=0
)
