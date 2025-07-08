# from django.shortcuts import render, redirect
# from .forms import FacultyMonthlyReviewForm, FacultyMonthlyMetricFormSet, FacultyMonthlyActivityFormSet
# from .models import FacultyMonthlyActivity, FacultyMonthlyMetric

# def monthly_review_create(request):
#     if request.method == 'POST':
#         review_form = FacultyMonthlyReviewForm(request.POST)
#         metric_formset = FacultyMonthlyMetricFormSet(request.POST, queryset=FacultyMonthlyMetric.objects.none())
#         activity_formset = FacultyMonthlyActivityFormSet(request.POST, queryset=FacultyMonthlyActivity.objects.none())

#         if review_form.is_valid() and metric_formset.is_valid() and activity_formset.is_valid():
#             review = review_form.save()

#             metrics = metric_formset.save(commit=False)
#             for metric in metrics:
#                 metric.monthly_review = review
#                 metric.save()

#             activities = activity_formset.save(commit=False)
#             for activity in activities:
#                 activity.monthly_review = review
#                 activity.save()

#             return redirect('success_page_or_review_list')  # Change to your URL
#     else:
#         review_form = FacultyMonthlyReviewForm()
#         metric_formset = FacultyMonthlyMetricFormSet(queryset=FacultyMonthlyMetric.objects.none())
#         activity_formset = FacultyMonthlyActivityFormSet(queryset=FacultyMonthlyActivity.objects.none())

#     return render(request, 'monthly_review_form.html', {
#         'review_form': review_form,
#         'metric_formset': metric_formset,
#         'activity_formset': activity_formset,
#     })


# views.py

# from django.shortcuts import render, redirect
# from .models import Metric, MilestoneActivity, FacultyMonthlyMetric, FacultyMonthlyActivity, FacultyMonthlyReview
# from .forms import FacultyMonthlyMetricForm, FacultyMonthlyActivityForm, FacultyMonthlyReviewForm
# from django.forms import modelformset_factory

# def monthly_review_create(request):
#     FacultyMonthlyMetricFormSet = modelformset_factory(FacultyMonthlyMetric, form=FacultyMonthlyMetricForm, extra=0)
#     FacultyMonthlyActivityFormSet = modelformset_factory(FacultyMonthlyActivity, form=FacultyMonthlyActivityForm, extra=0)

#     if request.method == 'POST':
#         review_form = FacultyMonthlyReviewForm(request.POST)
#         metric_formset = FacultyMonthlyMetricFormSet(request.POST, queryset=FacultyMonthlyMetric.objects.none())
#         activity_formset = FacultyMonthlyActivityFormSet(request.POST, queryset=FacultyMonthlyActivity.objects.none())

#         if review_form.is_valid() and metric_formset.is_valid() and activity_formset.is_valid():
#             review = review_form.save()

#             metrics = metric_formset.save(commit=False)
#             for metric in metrics:
#                 metric.monthly_review = review
#                 metric.save()

#             activities = activity_formset.save(commit=False)
#             for activity in activities:
#                 activity.monthly_review = review
#                 activity.save()

#             return redirect('')  # Update this to your page
#     else:
#         review_form = FacultyMonthlyReviewForm()

#         # 🟢 Get active metrics
#         metrics = Metric.objects.filter(isactive=True)
#         metric_initial = [{'metric_name': m.metric_name} for m in metrics]

#         # 🟢 Get active milestone activities
#         activities = MilestoneActivity.objects.filter(isactive=True)
#         activity_initial = [{'activity': a.activity, 'day': a.day} for a in activities]

#         metric_formset = FacultyMonthlyMetricFormSet(
#             queryset=FacultyMonthlyMetric.objects.none(),
#             initial=metric_initial
#         )
#         activity_formset = FacultyMonthlyActivityFormSet(
#             queryset=FacultyMonthlyActivity.objects.none(),
#             initial=activity_initial
#         )

#     return render(request, 'monthly_review_form.html', {
#         'review_form': review_form,
#         'metric_formset': metric_formset,
#         'activity_formset': activity_formset,
#     })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.models import Batch, FacultyProfile
from .models import Metric, MilestoneActivity, FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity
from django.contrib.auth.models import Group
from .forms import FacultyMonthlyReviewForm
from datetime import date

@login_required
def create_monthly_review(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    faculty = get_object_or_404(FacultyProfile, user=request.user)

    # Get group(s) of current user
    groups = request.user.groups.all()
    metrics = Metric.objects.filter(group__in=groups, isactive=True)
    activities = MilestoneActivity.objects.filter(group__in=groups, isactive=True)

    if request.method == 'POST':
        review_month = request.POST.get('review_month')
        total_students = request.POST.get('total_students')
        start_date = request.POST.get('start_date') or batch.start_date
        end_date = request.POST.get('end_date') or batch.end_date


        # Create main review
        review = FacultyMonthlyReview.objects.create(
            user=faculty,
            batch=batch,
            start_date=start_date,
            end_date=end_date,
            total_students=total_students,
            review_month=review_month,
            created_user=request.user,
        )

        # Metrics
        for metric in metrics:
            value = request.POST.get(f'metric_{metric.metric_name}')
            FacultyMonthlyMetric.objects.create(
                monthly_review=review,
                metric_name=metric.metric_name,
                metric_value=value
            )

        # Activities
        for i, activity in enumerate(activities):
            FacultyMonthlyActivity.objects.create(
                monthly_review=review,
                activity=activity.activity,
                day=activity.day,
                planned_date=request.POST.get(f'planned_date_{i}') or None,
                completed_date=request.POST.get(f'completed_date_{i}') or None,
                status=request.POST.get(f'status_{i}') or None,
                participation=request.POST.get(f'participation_{i}') or None,
                remarks=request.POST.get(f'remarks_{i}') or None,
            )

        return redirect('faculty_dashboard')  # or any success page

    context = {
        'batch': batch,
        'faculty': faculty,
        'metrics': metrics,
        'activities': activities,
        'months': [m[0] for m in FacultyMonthlyReview._meta.get_field('review_month').choices]
    }
    return render(request, 'create_monthly_review.html', context)
