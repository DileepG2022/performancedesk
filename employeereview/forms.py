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

# FacultyMonthlyMetricFormSet = modelformset_factory(
#     FacultyMonthlyMetric, form=FacultyMonthlyMetricForm, extra=0
# )

# FacultyMonthlyActivityFormSet = modelformset_factory(
#     FacultyMonthlyActivity, form=FacultyMonthlyActivityForm, extra=0
# )

# from django import forms
# from .models import FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity

# class FacultyMonthlyReviewForm(forms.ModelForm):
#     class Meta:
#         model = FacultyMonthlyReview
#         fields = ['user', 'batch', 'review_month']

#         widgets = {
#             'trainer': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'batch': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'month': forms.Select()
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
#             'activity': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'day': forms.TextInput(attrs={'readonly': 'readonly'}),
#             'planned_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date'}),
#             'completed_date': forms.DateInput(attrs={'type': 'date'}),
#         }

# FacultyMonthlyMetricFormSet = forms.inlineformset_factory(
#     FacultyMonthlyReview,
#     FacultyMonthlyMetric,
#     form=FacultyMonthlyMetricForm,
#     extra=0
# )

# FacultyMonthlyActivityFormSet = forms.inlineformset_factory(
#     FacultyMonthlyReview,
#     FacultyMonthlyActivity,
#     form=FacultyMonthlyActivityForm,
#     extra=0
# )

from django import forms
from .models import FacultyMonthlyActivity, FacultyMonthlyMetric, FacultyMonthlyReview, SalesMonthlyReview, SalesTarget

class FacultyMonthlyActivityForm(forms.ModelForm):
    class Meta:
        model = FacultyMonthlyActivity
        fields = ['activity', 'day', 'planned_date', 'completed_date', 'status', 'participation', 'remarks']
        widgets = {
            'activity': forms.TextInput(attrs={'readonly': 'readonly'}),
            'day': forms.TextInput(attrs={'readonly': 'readonly'}),
            'planned_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }


class FacultyMonthlyMetricForm(forms.ModelForm):
    class Meta:
        model = FacultyMonthlyMetric
        fields = ['metric_name', 'metric_value']
        widgets = {
            'metric_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


# class FacultyMonthlyReviewForm(forms.ModelForm):
#     class Meta:
#         model = FacultyMonthlyReview
#         fields = ['review_month', 'start_date', 'end_date', 'total_students']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date'}),
#             'total_students': forms.NumberInput(attrs={'readonly': 'readonly'}),
#         }

class FacultyMonthlyReviewForm(forms.ModelForm):
    class Meta:
        model = FacultyMonthlyReview
        # fields = ['review_month', 'start_date', 'end_date', 'total_students']
        fields = ['review_month',]
        # widgets = {
        #     'start_date': forms.DateInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        #     'end_date': forms.DateInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        #     'total_students': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        #     'review_month': forms.Select(attrs={'class': 'form-control'}),
        # }
        widgets = {
            'review_month': forms.Select(attrs={'class': 'form-control'}),
        }


# from .models import SalesMonthlyReview, SalesMonthlyMetric, Metric
# from datetime import date

# class SalesMonthlyReviewForm(forms.ModelForm):
#     review_date = forms.DateField(
#         widget=forms.SelectDateWidget(
#             years=range(2020, date.today().year + 1),
#             empty_label=("Choose Year", "Choose Month", "Choose Day"),
#         ),
#         help_text="Select the month for your review",
#     )

#     total_leads = forms.IntegerField(label="Total Leads (Manual)", min_value=0)
#     fee_collected = forms.DecimalField(label="Fee Collected", max_digits=10, decimal_places=2, required=False)
#     fee_pending = forms.DecimalField(label="Fee Pending", max_digits=10, decimal_places=2, required=False)

#     class Meta:
#         model = SalesMonthlyReview
#         fields = ["review_date"]

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop("user", None)  # SalesProfile instance
#         super().__init__(*args, **kwargs)

#     def save(self, commit=True):
#         review = super().save(commit=False)
#         review.user = self.user
#         if commit:
#             review.save()

#             # Fetch metrics from DB
#             metrics = Metric.objects.filter(group__name="Sales")

#             # Save metrics: manual inputs
#             SalesMonthlyMetric.objects.update_or_create(
#                 monthly_review=review,
#                 metric=metrics.get(metric_name="Total Leads"),
#                 defaults={"metric_value": str(self.cleaned_data["total_leads"])}
#             )
#             SalesMonthlyMetric.objects.update_or_create(
#                 monthly_review=review,
#                 metric=metrics.get(metric_name="Fee Collected"),
#                 defaults={"metric_value": str(self.cleaned_data["fee_collected"])}
#             )
#             SalesMonthlyMetric.objects.update_or_create(
#                 monthly_review=review,
#                 metric=metrics.get(metric_name="Fee Pending"),
#                 defaults={"metric_value": str(self.cleaned_data["fee_pending"])}
#             )

#             # Auto populate - Admissions
#             total_admissions = self._get_total_admissions(review.review_date)
#             SalesMonthlyMetric.objects.update_or_create(
#                 monthly_review=review,
#                 metric=metrics.get(metric_name="Total Admissions"),
#                 defaults={"metric_value": str(total_admissions)}
#             )

#             # Auto populate - Dropouts
#             dropouts = self._get_total_dropouts(review.review_date)
#             SalesMonthlyMetric.objects.update_or_create(
#                 monthly_review=review,
#                 metric=metrics.get(metric_name="Dropouts"),
#                 defaults={"metric_value": str(dropouts)}
#             )

#             # Auto calculate conversion rate
#             conv_rate = (total_admissions / self.cleaned_data["total_leads"] * 100) if self.cleaned_data["total_leads"] else 0
#             SalesMonthlyMetric.objects.update_or_create(
#                 monthly_review=review,
#                 metric=metrics.get(metric_name="Conversion Rate"),
#                 defaults={"metric_value": f"{conv_rate:.2f}%"}
#             )

#         return review

#     def _get_total_admissions(self, review_date):
#         """Query Manager data for admissions of this Sales member for the given month."""
#         # TODO: Replace with actual batch/student query
#         return 10

#     def _get_total_dropouts(self, review_date):
#         """Query Trainer data for dropouts for this Sales member for the given month."""
#         # TODO: Replace with actual trainer review query
#         return 2

from settings_app.models import SalesProfile
import datetime
class SalesTargetForm(forms.ModelForm):
    # Use CharField to handle type="month" properly
    target_date = forms.CharField(
        widget=forms.DateInput(attrs={"type": "month", "class": "form-control"}),
        help_text="Select month & year for the target"
    )

    class Meta:
        model = SalesTarget
        fields = ["sales_person", "target_date", "target_value"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Limit sales_person choices to those reporting to current user
        if user:
            self.fields["sales_person"].queryset = SalesProfile.objects.filter(
                reporting_officers=user
            )

        # Prepopulate month input correctly when editing
        if self.instance and self.instance.pk:
            target_date = self.instance.target_date
            if target_date:
                # YYYY-MM format for type="month"
                self.initial["target_date"] = target_date.strftime("%Y-%m")

    def clean_target_date(self):
        value = self.cleaned_data["target_date"]
        try:
            # Convert "YYYY-MM" string to datetime.date
            year, month = map(int, value.split("-"))
            return datetime.date(year, month, 1)
        except Exception:
            raise forms.ValidationError("Enter a valid month & year")