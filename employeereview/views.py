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

# from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# from settings_app.models import Batch, FacultyProfile
# from .models import Metric, CourseMilestoneActivity, FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity, BatchActivity
# from django.contrib.auth.models import Group
# from .forms import FacultyMonthlyReviewForm, FacultyMonthlyMetricFormSet
# from datetime import date
from django.http import JsonResponse
from django.contrib import messages

# @login_required
# def create_monthly_review(request, batch_id):
#     batch = get_object_or_404(Batch, id=batch_id)
#     faculty = get_object_or_404(FacultyProfile, user=request.user)

#     # Get group(s) of current user
#     groups = request.user.groups.all()
#     metrics = Metric.objects.filter(group__in=groups, isactive=True)
#     activities = CourseMilestoneActivity.objects.filter(group__in=groups, isactive=True)

#     if request.method == 'POST':
#         review_month = request.POST.get('review_month')
#         total_students = request.POST.get('total_students')
#         start_date = request.POST.get('start_date') or batch.start_date
#         end_date = request.POST.get('end_date') or batch.end_date


#         # Create main review
#         review = FacultyMonthlyReview.objects.create(
#             user=faculty,
#             batch=batch,
#             start_date=start_date,
#             end_date=end_date,
#             total_students=total_students,
#             review_month=review_month,
#             created_user=request.user,
#         )

#         # Metrics
#         for metric in metrics:
#             value = request.POST.get(f'metric_{metric.metric_name}')
#             FacultyMonthlyMetric.objects.create(
#                 monthly_review=review,
#                 metric_name=metric.metric_name,
#                 metric_value=value
#             )

#         # Activities
#         for i, activity in enumerate(activities):
#             FacultyMonthlyActivity.objects.create(
#                 monthly_review=review,
#                 activity=activity.activity,
#                 day=activity.day,
#                 planned_date=request.POST.get(f'planned_date_{i}') or None,
#                 completed_date=request.POST.get(f'completed_date_{i}') or None,
#                 status=request.POST.get(f'status_{i}') or None,
#                 participation=request.POST.get(f'participation_{i}') or None,
#                 remarks=request.POST.get(f'remarks_{i}') or None,
#             )

#         return redirect('faculty_dashboard')  # or any success page

#     context = {
#         'batch': batch,
#         'faculty': faculty,
#         'metrics': metrics,
#         'activities': activities,
#         'months': [m[0] for m in FacultyMonthlyReview._meta.get_field('review_month').choices]
#     }
#     return render(request, 'create_monthly_review.html', context)

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Batch, FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity, Metric, BatchActivity
# from .forms import FacultyMonthlyReviewForm, FacultyMonthlyMetricFormSet, FacultyMonthlyActivityFormSet
# from datetime import date
# from django.forms import modelformset_factory

# @login_required
# def create_or_edit_monthly_review(request, batch_id):
#     batch = get_object_or_404(Batch, id=batch_id)
#     trainer = batch.faculty  # assuming Batch has a ForeignKey to FacultyProfile
#     today = date.today()

#     # Check if review already exists for this trainer and batch and month
#     review = FacultyMonthlyReview.objects.filter(batch=batch, user=trainer, review_month=today.month).first()
#     if review:
#         form = FacultyMonthlyReviewForm(instance=review)
#         metric_formset = FacultyMonthlyMetricFormSet(instance=review)
#         activity_formset = FacultyMonthlyActivityFormSet(instance=review)
#     else:
#         form = FacultyMonthlyReviewForm(initial={
#             'trainer': trainer,
#             'batch': batch,
#             'month': today.month
#         })
#         metric_formset = FacultyMonthlyMetricFormSet()
#         # Create formset for each BatchActivity for this batch
#         batch_activities = BatchActivity.objects.filter(batch=batch)
#         FacultyActivityFormSet = modelformset_factory(FacultyMonthlyActivity, form=FacultyMonthlyActivityFormSet.form, extra=0, can_delete=False)
#         activity_formset = FacultyActivityFormSet(queryset=FacultyMonthlyActivity.objects.none(), initial=[
#             {
#                 'activity': ba.activity,
#                 'day': ba.day,
#                 'planned_date': ba.planned_date
#             } for ba in batch_activities
#         ])

#     if request.method == 'POST':
#         form = FacultyMonthlyReviewForm(request.POST, instance=review if review else None)
#         metric_formset = FacultyMonthlyMetricFormSet(request.POST, instance=review if review else None)
#         activity_formset = FacultyMonthlyActivityFormSet(request.POST, instance=review if review else None)

#         if form.is_valid() and metric_formset.is_valid() and activity_formset.is_valid():
#             review = form.save()
#             metric_formset.instance = review
#             metric_formset.save()
#             activity_formset.instance = review
#             activity_formset.save()
#             return redirect('monthly_review_success')

#     return render(request, 'monthly_review_form.html', {
#         'form': form,
#         'metric_formset': metric_formset,
#         'activity_formset': activity_formset,
#         'batch': batch,
#         'trainer': trainer
#     })


# from django.shortcuts import render, get_object_or_404, redirect
# from django.forms import modelformset_factory
# from django.utils.timezone import now
# from .models import *
# from .forms import FacultyMonthlyReviewForm, FacultyMonthlyMetricForm, FacultyMonthlyActivityForm
# from datetime import timedelta, date


# Utility: Calculate working days between two dates
# def calculate_working_days(start_date, end_date):
#     working_days = 0
#     current = start_date
#     while current <= end_date:
#         if current.weekday() < 5:  # Monday=0, Sunday=6
#             working_days += 1
#         current += timedelta(days=1)
#     return working_days


# def create_monthly_review(request, batch_id):
#     batch = get_object_or_404(Batch, id=batch_id)
#     # faculty = request.user.facultyprofile
#     faculty = get_object_or_404(FacultyProfile, user=request.user)

#     # Base form
#     if request.method == "POST":
#         review_form = FacultyMonthlyReviewForm(request.POST)
#         MetricFormSet = modelformset_factory(FacultyMonthlyMetric, form=FacultyMonthlyMetricForm, extra=0)
#         ActivityFormSet = modelformset_factory(FacultyMonthlyActivity, form=FacultyMonthlyActivityForm, extra=0)

#         metric_formset = MetricFormSet(request.POST, prefix='metrics')
#         activity_formset = ActivityFormSet(request.POST, prefix='activities')

#         if review_form.is_valid() and metric_formset.is_valid() and activity_formset.is_valid():
#             monthly_review = review_form.save(commit=False)
#             monthly_review.user = faculty
#             monthly_review.batch = batch
#             monthly_review.start_date = batch.start_date
#             monthly_review.end_date = batch.end_date
#             monthly_review.total_students = batch.total_students
#             monthly_review.save()

#             # Save metric forms
#             for form in metric_formset:
#                 metric = form.save(commit=False)
#                 metric.monthly_review = monthly_review
#                 metric.save()

#             # Save activity forms
#             for form in activity_formset:
#                 activity = form.save(commit=False)
#                 activity.monthly_review = monthly_review
#                 activity.save()

#             return redirect('monthly_review_list')
#     else:
#         # Initial form
#         review_form = FacultyMonthlyReviewForm(initial={
#             'start_date': batch.start_date,
#             'end_date': batch.end_date,
#             'total_students': batch.total_students,
#         })

#         # Prefill metrics
#         all_metrics = Metric.objects.all()
#         metric_data = []
#         today = date.today()
#         for m in all_metrics:
#             value = ""
#             if m.name == "Days till to finish as per LMS":
#                 value = calculate_working_days(batch.start_date, today)
#             metric_data.append({'metric_name': m.name, 'metric_value': value})

#         MetricFormSet = modelformset_factory(FacultyMonthlyMetric, form=FacultyMonthlyMetricForm, extra=len(metric_data))
#         metric_formset = MetricFormSet(initial=metric_data, queryset=FacultyMonthlyMetric.objects.none(), prefix='metrics')

#         # Prefill activities from BatchActivity
#         batch_activities = BatchActivity.objects.filter(batch=batch).order_by('day')
#         activity_data = []
#         for a in batch_activities:
#             activity_data.append({
#                 'activity': a.activity,
#                 'day': a.day,
#                 'planned_date': a.planned_date,
#             })

#         ActivityFormSet = modelformset_factory(FacultyMonthlyActivity, form=FacultyMonthlyActivityForm, extra=len(activity_data))
#         activity_formset = ActivityFormSet(initial=activity_data, queryset=FacultyMonthlyActivity.objects.none(), prefix='activities')

#     return render(request, 'monthly_review_form.html', {
#         'review_form': review_form,
#         'metric_formset': metric_formset,
#         'activity_formset': activity_formset,
#         'batch': batch
#     })

from django.shortcuts import render, get_object_or_404, redirect
# from .models import FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity, Metric, BatchActivity
from .forms import FacultyMonthlyReviewForm
from django.forms import modelformset_factory

import calendar
from settings_app.models import Batch, FacultyProfile, StudentProfile, Course, PlacementProfile, SalesProfile

# def working_days(start_date, end_date):
#     delta = (end_date - start_date).days + 1
#     return sum(1 for i in range(delta)
#                if (start_date + timedelta(days=i)).weekday() < 5)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Metric, BatchActivity, FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity, TrainerMonthlyReview, TrainerMonthlyMetric, TrainerMonthlyActivity, PlacementMonthlyReview, PlacementMonthlyMetric, SalesTarget
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from .forms import FacultyMonthlyReviewForm, SalesTargetForm


def get_working_days(start_date, end_date):
    day_count = 0
    current = start_date
    while current <= end_date:
        if current.weekday() not in (5, 6):  # 5 = Saturday, 6 = Sunday
            day_count += 1
        current += timedelta(days=1)
    return day_count


@login_required
def monthly_review_view(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    faculty = get_object_or_404(FacultyProfile, user=request.user)

    if request.method == 'POST':
        form = FacultyMonthlyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = faculty
            review.batch = batch            
            review.start_date = batch.start_date
            review.end_date = batch.end_date
            review.total_students = batch.total_students
            review.save()

            # Save metrics
            metric_names = request.POST.getlist('metric_name')
            metric_values = request.POST.getlist('metric_value')
            for name, value in zip(metric_names, metric_values):
                FacultyMonthlyMetric.objects.create(
                    monthly_review=review,
                    metric_name=name,
                    metric_value=value
                )

            # Save activities
            activity_ids = request.POST.getlist('activity_id')
            completed_dates = request.POST.getlist('completed_date')
            statuses = request.POST.getlist('status')
            participations = request.POST.getlist('participation')
            remarks = request.POST.getlist('remarks')

            batch_activities = BatchActivity.objects.filter(batch=batch)
            for idx, act in enumerate(batch_activities):
                FacultyMonthlyActivity.objects.create(
                    monthly_review=review,
                    activity=act.activity,
                    day=act.day,
                    planned_date=act.planned_date,
                    completed_date=completed_dates[idx] or None,
                    status=statuses[idx],
                    participation=participations[idx],
                    remarks=remarks[idx]
                )

            return redirect('faculty_dashboard')
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        
        form = FacultyMonthlyReviewForm()

    # For initial display
        # Get group(s) of current user
    groups = request.user.groups.all()
    metrics = Metric.objects.filter(group__in=groups, isactive=True)
    metric_data = []

    for metric in metrics:
        metric_value = ''
        readonly = False
        
        if metric.metric_name.strip().lower() == "days till to finish as per lms":
            working_days = get_working_days(batch.start_date, date.today())
            metric_value = working_days
            readonly = True
        
        metric_data.append({
            'metric': metric,
            'value': metric_value,
            'readonly': readonly,
        })
    
    batch_activities = BatchActivity.objects.filter(batch=batch)

    return render(request, 'monthly_review_form.html', {
        'form': form,
        'batch': batch,
        'faculty': faculty,
        'metrics': metric_data,
        'activities': batch_activities,
    })


# views.py
# from django.http import JsonResponse
# from datetime import date
from dateutil.relativedelta import relativedelta
from calendar import month_name
# from .models import FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity, Metric, BatchActivity
# from .utils import get_working_days
@login_required
def get_review_prefill_data(request):
    # print("Hello")
    batch_id = request.GET.get("batch_id")
    review_month_str = request.GET.get("review_month")  # e.g., 'August'
    

    month_map = {
        'January': 1, 'February': 2, 'March': 3,
        'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9,
        'October': 10, 'November': 11, 'December': 12,
    }

    try:
        current_month_num = month_map[review_month_str]        
        today = date.today()
        current_month_date = date(today.year, current_month_num, 1)
        previous_month_date = current_month_date - relativedelta(months=1)
        previous_month_str = month_name[previous_month_date.month]  # e.g., "July"
    except Exception as e:
        # print("Error:", e)
        return JsonResponse({'error': 'Invalid month'}, status=400)
    
    # Check if review already exists for selected month
    # existing_review = FacultyMonthlyReview.objects.filter(
    #     batch_id=batch_id,
    #     review_month=review_month_str
    # ).first()

    # if existing_review:
    #     # Do NOT allow prefill if review exists
    #     return JsonResponse({
    #         'is_prefilled': True,
    #         'message': 'Review already submitted for the selected month.',
    #         'metrics': [],
    #         'activities': []
    #     })

    
    
     # Try to prefill from previous month
    previous_review = FacultyMonthlyReview.objects.filter(
        batch_id=batch_id,
        review_month=previous_month_str
    ).first()

    # Try current month first, then previous
    # review = FacultyMonthlyReview.objects.filter(batch_id=batch_id, review_month=review_month_str).first()
    # is_prefilled = True

    # if not review:
    #     review = FacultyMonthlyReview.objects.filter(batch_id=batch_id, review_month=previous_month_str).first()
    #     is_prefilled = False

    is_prefilled = False
    metrics_data = []
    activities_data = []

    block_submission = False
    message = ""

    if FacultyMonthlyReview.objects.filter(batch_id=batch_id).exists() == False:
        block_submission = False
    elif FacultyMonthlyReview.objects.filter(batch_id=batch_id, review_month=review_month_str).exists():
        block_submission = True
        message = "Review already submitted for the selected month."
    elif not previous_review:  # Means: no previous month review either
        block_submission = True
        message = "No previous data available. Cannot submit review."
    


    if block_submission:
        # Return this in JsonResponse:
        return JsonResponse({
            'is_prefilled': is_prefilled,
            'metrics': metrics_data,
            'activities': activities_data,
            'block_submission': block_submission,
            'message': message,
        })

    # Get allowed metrics for user
    user_groups = request.user.groups.all()
    metrics = Metric.objects.filter(group__in=user_groups, isactive=True)

    for metric in metrics:
        value = ''
        readonly = False

        if metric.metric_name.strip().lower() == "days till to finish as per lms":
            batch = Batch.objects.get(id=batch_id)
            value = get_working_days(batch.start_date, date.today())
            readonly = True
        elif previous_review:
            is_prefilled = True
            prev_metric = FacultyMonthlyMetric.objects.filter(
                monthly_review=previous_review,
                metric_name=metric.metric_name
            ).first()
            if prev_metric:
                value = prev_metric.metric_value

        metrics_data.append({
            'metric_id': metric.id,
            'metric_name': metric.metric_name,
            'value': value,
            'readonly': readonly,
        })
    
    # Activities
    batch_activities = BatchActivity.objects.filter(batch_id=batch_id)
    for act in batch_activities:
        completed_date = ''
        status = ''
        participation = ''
        remarks = ''

        if previous_review:
            prev_act = FacultyMonthlyActivity.objects.filter(
                monthly_review=previous_review,
                activity=act.activity
            ).first()
            if prev_act:
                is_prefilled = True
                completed_date = prev_act.completed_date
                status = prev_act.status
                participation = prev_act.participation
                remarks = prev_act.remarks

        activities_data.append({
            'activity_id': act.id,
            'activity': act.activity,
            'day': act.day,
            'planned_date': act.planned_date,
            'completed_date': completed_date,
            'status': status,
            'participation': participation,
            'remarks': remarks,
        })

    return JsonResponse({
        'is_prefilled': is_prefilled,
        'message': 'Prefilled from previous month.' if is_prefilled else 'No previous data available.',
        'metrics': metrics_data,
        'activities': activities_data,
        'block_submission': block_submission,
    })

    # Metrics
    # groups = request.user.groups.all()
    # metrics = Metric.objects.filter(group__in=groups, isactive=True)
    # metrics_data = []
    # for metric in metrics:
    #     value = ''
    #     readonly = False

    #     if metric.metric_name.strip().lower() == "days till to finish as per lms":
    #         from .models import Batch
    #         batch = Batch.objects.get(id=batch_id)
    #         value = get_working_days(batch.start_date, date.today())
    #         readonly = True
    #     elif review:
    #         m = FacultyMonthlyMetric.objects.filter(monthly_review=review, metric_name=metric.metric_name).first()
    #         if m:
    #             value = m.metric_value

    #     metrics_data.append({
    #         'metric_id': metric.id,
    #         'metric_name': metric.metric_name,
    #         'value': value,
    #         'readonly': readonly,
    #     })

    # Activities
    # activities_data = []
    # activities = BatchActivity.objects.filter(batch_id=batch_id)
    # for act in activities:
    #     completed_date = ''
    #     status = ''
    #     participation = ''
    #     remarks = ''

    #     if review:
    #         a = FacultyMonthlyActivity.objects.filter(monthly_review=review, activity=act.activity).first()
    #         if a:
    #             completed_date = a.completed_date
    #             status = a.status
    #             participation = a.participation
    #             remarks = a.remarks

    #     activities_data.append({
    #         'activity_id': act.id,
    #         'activity': act.activity,
    #         'day': act.day,
    #         'planned_date': act.planned_date,
    #         'completed_date': completed_date,
    #         'status': status,
    #         'participation': participation,
    #         'remarks': remarks,
    #     })

    # return JsonResponse({
    #     'is_prefilled': is_prefilled,
    #     'metrics': metrics_data,
    #     'activities': activities_data,
    # })



@login_required
def monthly_review_report(request):

    faculties = FacultyProfile.objects.all()

    user = request.user

    # Get only used months in reviews
    # months = FacultyMonthlyReview.objects.values_list('review_month', flat=True).distinct()
    months = []

    batches = []
    review = None
    metrics = []
    # Add a flag to each metric for highlighting
    highlighted_metrics = []
    activities = []

    # Determine if current user is a faculty
    is_faculty = hasattr(user, 'faculty_user')
    
    # faculty_id = None
    faculty_id = request.GET.get("faculty_id") or (user.faculty_user.id if is_faculty else None)
    batch_id = request.GET.get("batch_id")
    # print(request.POST)
    # if is_faculty:
        
    #     faculty_id = user.faculty_user.id  # Auto-select
    #     batches = Batch.objects.filter(faculty=user.faculty_user)

    # Restrict batches based on faculty role
    if faculty_id:
        batches = Batch.objects.filter(faculty_id=faculty_id)

    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id") or faculty_id
        batch_id = request.POST.get("batch_id") or batch_id
        batches = Batch.objects.filter(faculty_id=faculty_id)
        review_month = request.POST.get("review_month")

        # Filter batches based on selected faculty (or current user if faculty)
        # if faculty_id:
        #     batches = Batch.objects.filter(faculty_id=faculty_id)

        # Load months only if batch and faculty are selected
        if faculty_id and batch_id:
            # batches = Batch.objects.filter(faculty_id=faculty_id)
            months = FacultyMonthlyReview.objects.filter(
        user_id=faculty_id,
        batch_id=batch_id
    ).values_list("review_month", flat=True).distinct()
            review = FacultyMonthlyReview.objects.filter(
                user_id=faculty_id,
                batch_id=batch_id,
                review_month=review_month
            ).first()

    # Convert string numbers to int safely
            def safe_int(val):
                try:
                    return int(val)
                except:
                    return 0

            if review:
                metrics = FacultyMonthlyMetric.objects.filter(monthly_review=review)
                # Create a dict to find comparison values
                metric_dict = {m.metric_name: m.metric_value for m in metrics}
                actual_finish = safe_int(metric_dict.get("Actual finished Day", 0))
                expected_finish = safe_int(metric_dict.get("Days till to finish as per LMS", 0))
                # print(actual_finish)
                # print(expected_finish)

                
                for m in metrics:
                    highlight = False
                    if m.metric_name == "Actual finished Day" and actual_finish > expected_finish:
                        highlight = True
                        # print(highlight)
                    highlighted_metrics.append({
                            'metric_name': m.metric_name,
                            'metric_value': m.metric_value,
                            'highlight': highlight
                            })

                # print(len(highlighted_metrics))
                activities = FacultyMonthlyActivity.objects.filter(monthly_review=review)
    # print(batches)
    context = {
        "faculties": faculties,
        "batches": batches,
        "months": months,
        "review": review,
        "metrics": highlighted_metrics,
        "activities": activities,
        "is_faculty": is_faculty,
        "selected_faculty_id": faculty_id,
        "selected_batch_id": batch_id,
    }

    return render(request, "monthly_review_report.html", context)

@login_required
def get_batches_by_faculty(request):
    faculty_id = request.GET.get('faculty_id')
    batches = Batch.objects.filter(faculty_id=faculty_id)
    batch_list = [{'id': b.id, 'name': b.name} for b in batches]
    return JsonResponse(batch_list, safe=False)

@login_required
def get_review_months(request):
    faculty_id = request.GET.get("faculty_id")
    batch_id = request.GET.get("batch_id")

    months = FacultyMonthlyReview.objects.filter(
        user_id=faculty_id,
        batch_id=batch_id
    ).values_list("review_month", flat=True).distinct()

    return JsonResponse(list(months), safe=False)

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import FacultyMonthlyReview, FacultyMonthlyMetric, FacultyMonthlyActivity

@login_required
def export_review_pdf(request, faculty_id, batch_id, review_month):
    review = FacultyMonthlyReview.objects.filter(
        user_id=faculty_id,
        batch_id=batch_id,
        review_month=review_month
    ).first()

    if not review:
        return HttpResponse("No review data available.", status=404)

    metrics = FacultyMonthlyMetric.objects.filter(monthly_review=review)
    activities = FacultyMonthlyActivity.objects.filter(monthly_review=review)

    context = {
        'review': review,
        'metrics': metrics,
        'activities': activities,
    }

    template_path = 'monthly_review_pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="review_{review_month}.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed. Check template syntax or CSS compatibility.')
    return response


@login_required
def all_month_reviews(request):
    faculties = FacultyProfile.objects.all()
    batches = Batch.objects.all()
    reviews_data = []

    user = request.user

    # Determine if current user is a faculty
    is_faculty = hasattr(user, 'faculty_user')

    print(is_faculty)

    # Get params from GET or POST
    faculty_id = request.POST.get("faculty_id") or request.GET.get("faculty_id") or (user.faculty_user.id if is_faculty else None)
    print(faculty_id)
    batch_id = request.POST.get("batch_id") or request.GET.get("batch_id")

    if faculty_id and batch_id:
        reviews = FacultyMonthlyReview.objects.filter(
            user_id=faculty_id, 
            batch_id=batch_id
        ).order_by('-created_date')

        for review in reviews:
            metrics = FacultyMonthlyMetric.objects.filter(monthly_review=review)
            activities = FacultyMonthlyActivity.objects.filter(monthly_review=review)
            reviews_data.append({
                'review': review,
                'metrics': metrics,
                'activities': activities
            })

        return render(request, "all_months_review.html", {
            "faculties": faculties,
            "batches": batches,
            "selected_faculty_id": faculty_id,
            "selected_batch_id": batch_id,
            "reviews": [{
                'review_month': r['review'].review_month,
                'user': r['review'].user,
                'batch': r['review'].batch,
                'total_students': r['review'].total_students,
                'start_date': r['review'].start_date,
                'end_date': r['review'].end_date,
                'metrics': r['metrics'],
                'activities': r['activities'],
            } for r in reviews_data],
            "is_trainer_view":is_faculty,
        })

    return render(request, "all_months_review.html", {
        "faculties": faculties,
        "batches": batches,
        "selected_faculty_id": faculty_id,
        "selected_batch_id": batch_id,
        "is_trainer_view":is_faculty,
    })


@login_required
def faculty_monthly_review_report(request, faculty_id):
    faculty = FacultyProfile.objects.get(id=faculty_id, user=request.user)

    batches = Batch.objects.filter(faculty=faculty)

    reviews = []
    if request.method == "POST":
        batch_id = request.POST.get("batch_id")
        if batch_id:
            reviews = MonthlyReview.objects.filter(
                batch_id=batch_id,
                user=faculty
            ).select_related('batch', 'user')

    return render(request, "monthly_review_report.html", {
        "faculties": [faculty],  # single trainer
        "batches": batches,
        "reviews": reviews,
        "selected_faculty_id": faculty.id,
        "is_trainer_view": True
    })

# @login_required
# def sales_add_monthly_review(request):
#     pass

from django.views.decorators.http import require_GET
from django.utils.dateformat import DateFormat

@login_required
@require_GET
def get_sales_member_months(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return JsonResponse({"months": []})
    
    sales_user = get_object_or_404(SalesProfile, id=user_id)
    # Get distinct months which have reviews
    review_dates = SalesMonthlyReview.objects.filter(user=sales_user).dates("review_date", "month")
    
    months = [{"value": date.strftime("%Y-%m"), "label": date.strftime("%B %Y")} for date in review_dates]
    return JsonResponse({"months": months})

@login_required
def sales_all_months_review_report(request):
    # Check if Manager or Superuser
    is_manager = request.user.is_superuser or request.user.groups.filter(name="Manager").exists()
    sales_team = SalesProfile.objects.all() if is_manager else None

    selected_user = None
    reviews = None
    disable_dropdown = False

    if is_manager:
        if request.method == "POST":
            user_id = request.POST.get("sales_member")
            if user_id:
                selected_user = get_object_or_404(SalesProfile, id=user_id)
                reviews = SalesMonthlyReview.objects.filter(user=selected_user).order_by("review_date")
    else:
        # Sales Team Member login
        selected_user = get_object_or_404(SalesProfile, user=request.user)
        reviews = SalesMonthlyReview.objects.filter(user=selected_user).order_by("review_date")
        disable_dropdown = True

    return render(request, "reports/sales_all_months_review_report.html", {
        "sales_team": sales_team,
        "selected_user": selected_user,
        "reviews": reviews,
        "disable_dropdown": disable_dropdown,
    })


@login_required
def sales_monthly_review_report(request):
    is_manager = request.user.is_superuser or request.user.groups.filter(name="Manager").exists()
    sales_team = SalesProfile.objects.all() if is_manager else None

    selected_user = None
    selected_month = None
    reviews = None
    available_months = []

    if is_manager:
        if request.method == "POST":
            user_id = request.POST.get("sales_member")
            selected_month = request.POST.get("month")
            if user_id:
                selected_user = get_object_or_404(SalesProfile, id=user_id)
                # Load all months with reviews for this user
                available_months = SalesMonthlyReview.objects.filter(user=selected_user)\
                    .dates("review_date", "month")
                if selected_month:
                    reviews = SalesMonthlyReview.objects.filter(
                        user=selected_user,
                        review_date__month=int(selected_month.split('-')[1]),
                        review_date__year=int(selected_month.split('-')[0])
                    ).order_by("review_date")
    else:
        # Sales Team Member
        selected_user = get_object_or_404(SalesProfile, user=request.user)
        disable_dropdown = True
        available_months = SalesMonthlyReview.objects.filter(user=selected_user).dates("review_date", "month")
        if request.method == "POST":
            selected_month = request.POST.get("month")
            if selected_month:
                reviews = SalesMonthlyReview.objects.filter(
                    user=selected_user,
                    review_date__month=int(selected_month.split('-')[1]),
                    review_date__year=int(selected_month.split('-')[0])
                ).order_by("review_date")

    return render(request, "reports/sales_monthly_review_report.html", {
        "sales_team": sales_team if is_manager else [selected_user],
        "selected_user": selected_user,
        "reviews": reviews,
        "available_months": available_months,
        "selected_month": selected_month,
        "disable_dropdown": not is_manager,
    })

# from .forms import SalesMonthlyReviewForm
# from .models import SalesProfile

# @login_required
# def sales_add_monthly_review(request):
#     sales_profile = SalesProfile.objects.get(user=request.user)

#     if request.method == "POST":
#         form = SalesMonthlyReviewForm(request.POST, user=sales_profile)
#         if form.is_valid():
#             form.save()
#             return redirect("my_monthly_reviews")
#     else:
#         form = SalesMonthlyReviewForm(user=sales_profile)

#     return render(request, "sales/add_review.html", {"form": form})

import datetime

from .models import SalesProfile, SalesMonthlyReview, SalesMonthlyMetric, Metric

@login_required
def sales_add_monthly_review(request):
    sales_profile = SalesProfile.objects.get(user=request.user)

    if request.method == "POST":
        review_month = request.POST.get("review_month")  # format YYYY-MM
        if review_month:
            review_date = datetime.date(int(review_month.split("-")[0]), int(review_month.split("-")[1]), 1)
        else:
            review_date = None

        # Create Review entry
        review = SalesMonthlyReview.objects.create(
            user=sales_profile,
            review_date=review_date
        )

        # Save Metrics
        metrics = Metric.objects.filter(group__name="Sales").order_by("order")
        for metric in metrics:
            value = request.POST.get(f"metric_{metric.id}", "")
            if not value:
                # return JsonResponse({"error": f"{metric.name} is required"}, status=400)
                messages.error(request, f"{metric.metric_name} is required")
                return render(request, "sales/add_review.html")


        for metric in metrics:
            value = request.POST.get(f"metric_{metric.id}", "")
            SalesMonthlyMetric.objects.create(
                monthly_review=review,
                metric=metric,
                metric_value=value
            )
        
        messages.success(request, "Review added successfully!")

        # return redirect("my_monthly_reviews")  # redirect to review list

    return render(request, "sales/add_review.html")

from django.http import JsonResponse

@login_required
def get_sales_metrics(request):
    """Return Sales metrics for a given month (AJAX)"""
    review_month = request.GET.get("review_month")  # YYYY-MM
    user = request.user

    try:
        sales_profile = user.sales_user  # related_name="sales_user"
    except SalesProfile.DoesNotExist:
        return JsonResponse({"error": "You are not assigned as Sales"}, status=400)
    
    if not review_month:
        return JsonResponse({"error": "Please select a month."}, status=400)

    year, month = map(int, review_month.split("-"))
    review_date = datetime.date(year, month, 1)

    # ---------- Validation 1: Duplicate Month ----------
    if SalesMonthlyReview.objects.filter(
        user=sales_profile,
        review_date__year=year,
        review_date__month=month
    ).exists():
        return JsonResponse({
            "error": f"A review for {review_date.strftime('%B %Y')} already exists."
        }, status=400)

    # ---------- Validation 2: Continuous Months ----------
    last_review = SalesMonthlyReview.objects.filter(user=sales_profile).order_by("-review_date").first()
    if last_review:
        expected_next_month = last_review.review_date + relativedelta(months=1)
        if review_date != expected_next_month:
            return JsonResponse({
                "error": f"Please add reviews sequentially. Next review should be for {expected_next_month.strftime('%B %Y')}."
            }, status=400)

    # ---------- Auto-calc metrics ----------
    metrics = Metric.objects.filter(group__name="Sales").order_by("order")

    # Admissions & dropouts
    admissions_count = StudentProfile.objects.filter(
        sales_person=sales_profile,
        admission_date__year=year,
        admission_date__month=month
    ).count()

    dropouts_count = StudentProfile.objects.filter(
        sales_person=sales_profile,
        dropout_date__year=year,
        dropout_date__month=month,
        drop_out=True
    ).count()

    # ---------- Sales Target lookup ----------
    sales_target = (
        SalesTarget.objects.filter(
            sales_person=sales_profile,
            target_date__lte=review_date
        )
        .order_by("-target_date")
        .first()
    )
    target_value = sales_target.target_value if sales_target else ""

    data = []
    for metric in metrics:
        readonly = False
        value = ""

        if metric.metric_name == "Total Admissions":
            value = admissions_count
            readonly = True
        elif metric.metric_name == "Dropouts":
            value = dropouts_count
            readonly = True
        elif metric.metric_name == "Conversion Rate":
            value = "0"
            readonly = True
        elif metric.metric_name == "Monthly Sales Target":
            value = target_value
            readonly = True
        else:
            readonly = False

        data.append({
            "id": metric.id,
            "name": metric.metric_name,
            "datatype": metric.metric_datatype,
            "readonly": readonly,
            "value": value,
        })

    return JsonResponse({"metrics": data})


@login_required
def trainer_add_review(request, batch_id):
    # trainer = request.user.facultyprofile
    # batch = get_object_or_404(Batch, id=batch_id)
    trainer = get_object_or_404(FacultyProfile, user=request.user)
    batch = get_object_or_404(Batch, id=batch_id)
    total_students = StudentProfile.objects.filter(batch=batch).count()

    context = {
        "trainer": trainer,
        "batch": batch,
        # "total_students": total_students,
    }
    return render(request, "trainer_add_review.html", context)




def working_days_between(start_date, end_date):
    """Count working days (Mon-Fri) between two dates, inclusive of start_date."""
    if start_date > end_date:
        return 0
    day_count = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # 0=Monday, 6=Sunday
            day_count += 1
        current += timedelta(days=1)
    return day_count


# from datetime import datetime, date, timedelta
from calendar import monthrange

from dateutil.relativedelta import relativedelta


@login_required
def get_trainer_metrics(request):
    batch_id = request.GET.get("batch_id")
    month = request.GET.get("review_month")  # YYYY-MM
    trainer = get_object_or_404(FacultyProfile, user=request.user)
    batch = get_object_or_404(Batch, id=batch_id)

    review_date = datetime.datetime.strptime(month + "-01", "%Y-%m-%d").date()

    # --- Check if review already exists for selected month ---
    exists = TrainerMonthlyReview.objects.filter(
        user=trainer, batch=batch,
        review_date__year=review_date.year,
        review_date__month=review_date.month
    ).exists()
    if exists:
        return JsonResponse({"status": "exists", "message": "Review for the selected month already exists."})

    # Check previous review for the batch
    last_review = TrainerMonthlyReview.objects.filter(
    user=trainer, batch=batch
    ).order_by("-review_date").first()
    
    selected_date = datetime.datetime.strptime(month + "-01", "%Y-%m-%d").date()

    if last_review:
        
        # Expected next month
        year, month_num = last_review.review_date.year, last_review.review_date.month
        if month_num == 12:
            expected_next = datetime.datetime(year + 1, 1, 1).date()
        else:
            expected_next = datetime.datetime(year, month_num + 1, 1).date()

        if selected_date != expected_next:
            # print("Hello")
            return JsonResponse({
            "status": "blocked",
            "message": f"You cannot skip months. Please add review for {expected_next.strftime('%B %Y')} first."
            })

    # --- Check previous month review for pre-fill ---
    prev_month_date = review_date - relativedelta(months=1)
    prev_review = TrainerMonthlyReview.objects.filter(
        user=trainer, batch=batch,
        review_date__year=prev_month_date.year,
        review_date__month=prev_month_date.month
    ).first()

    previous_metrics = {}
    previous_activities = {}
    prev_message = ""

    if prev_review:
        prev_message = f"Previous month {prev_month_date.strftime('%B %Y')} data is pre-filled."

        # Metrics
        for m in prev_review.trainermonthlymetric_set.all():
            previous_metrics[m.metric_id] = m.metric_value

        # Student-activity completion
        for a in prev_review.trainermonthlyactivity_set.all():
            key = f"{a.activity_id}_{a.student_id}"
            previous_activities[key] = {
                "done": "on" if a.completed_date else "off",
                "date": a.completed_date.strftime("%Y-%m-%d") if a.completed_date else ""
            }

    # Fetch metrics for Faculty group
    metrics = Metric.objects.filter(group__name="Faculty").order_by("order")
    metrics_data = []
    for m in metrics:
        value = previous_metrics.get(m.id, "")
        # readonly = m.metric_name == "Days till to finish as per LMS"
        readonly = m.metric_name in ["Days till to finish as per LMS", "Placements"]
        # if readonly:
        if m.metric_name == "Days till to finish as per LMS":
            today = date.today()
            value = working_days_between(batch.start_date, today)
        elif m.metric_name == "Placements":
            value = 0
        metrics_data.append({
            "id": m.id,
            "name": m.metric_name,
            "datatype": m.metric_datatype,
            "readonly": readonly,
            "value": value
        })

    # Batch activities
    activities = list(BatchActivity.objects.filter(batch=batch).values("id", "activity", "day", "planned_date"))
    # print(activities)

    # Students
    students = list(StudentProfile.objects.filter(batch=batch).values("id", "user__first_name", "user__last_name"))

    return JsonResponse({
        "status": "ok",
        "metrics": metrics_data,
        "activities": activities,
        "students": students,
        "previous_data": {
            "activities": previous_activities
        },
        "message": prev_message
    })


from django.core.exceptions import ValidationError
import json

@login_required
def save_trainer_review(request):
    # print("Hello")
    if request.method != "POST":
        print("error")
        return JsonResponse({"error": "Invalid request method."}, status=400)

    data = request.POST
    # print(data)
    trainer = get_object_or_404(FacultyProfile, user=request.user)
    batch = get_object_or_404(Batch, id=data.get("batch_id"))
    review_month = data.get("review_month")  # YYYY-MM
    remarks = data.get("remarks", "").strip()

    if not review_month:
        return JsonResponse({"error": "Review month is required."}, status=400)

    try:
        review_date = datetime.datetime.strptime(review_month + "-01", "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid review month format."}, status=400)

    # print("=============")
    # Prevent duplicate
    if TrainerMonthlyReview.objects.filter(
        user=trainer, batch=batch,
        review_date__year=review_date.year, review_date__month=review_date.month
    ).exists():
        return JsonResponse({"error": "Review for this month already exists."}, status=400)
    # print("aaaaaaaa")
    # Validate metrics
    metric_keys = [key for key in data if key.startswith("metric_")]
    for key in metric_keys:
        if not data[key].strip():
            return JsonResponse({"error": f"All metric fields are required. Missing: {key}"}, status=400)
    # print("bbbbbbbbb")
    # Validate student-activity consistency
    activity_keys = [key for key in data if key.startswith("activity_") and "_student_" in key]
    for key in activity_keys:
        try:
            value_dict = json.loads(data[key])
            done = value_dict.get("done") == "on"
            date = value_dict.get("date")
            if done and not date:
                return JsonResponse({"error": "Completion date is required for all checked activities."}, status=400)
            if not done and date:
                return JsonResponse({"error": "Please check the box if a completion date is entered."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid activity data format."}, status=400)
    # print("cccccccc")
    # Extra validation: total students consistency
    try:
        # print(str(Metric.objects.get(metric_name="Active Students", group__name="Faculty").id))
        active_students = int(data.get("metric_" + str(Metric.objects.get(metric_name="Active Students", group__name="Faculty").id), 0))
        
        dropouts = int(data.get("metric_" + str(Metric.objects.get(metric_name="Dropouts", group__name="Faculty").id), 0))
        # print(dropouts)
        batch_change = int(data.get("metric_" + str(Metric.objects.get(metric_name="Batch Change", group__name="Faculty").id), 0))
        # print(batch_change)
    except (Metric.DoesNotExist, ValueError):
        return JsonResponse({"error": "Metrics required: Active Students, Dropouts, Batch Change."}, status=400)

    expected_total = active_students + (dropouts + batch_change)
    # print(expected_total)
    # print(batch.total_students)
    if expected_total != batch.total_students:
        # print("error")
        return JsonResponse({
            "error": f"Validation failed. Total students ({batch.total_students}) must equal Active Students ({active_students}) + (Dropouts {dropouts} + Batch Change {batch_change})"
        }, status=400)

    # print("************************")
    # Create review
    review = TrainerMonthlyReview.objects.create(
        user=trainer,
        batch=batch,
        review_date=review_date,
        start_date=batch.start_date,
        end_date=batch.end_date,
        total_students=batch.total_students,
        remarks=remarks
    )

    # Save metrics
    for key in metric_keys:
        metric_id = int(key.split("_")[1])
        value = data[key].strip()
        TrainerMonthlyMetric.objects.create(
            monthly_review=review,
            metric_id=metric_id,
            metric_value=value
        )

    # Save student-activity records with activity FK
    for key in activity_keys:
        parts = key.split("_")
        activity_id = int(parts[1])
        student_id = int(parts[3])
        value_dict = json.loads(data[key])
        done = value_dict.get("done") == "on"
        date = value_dict.get("date") or None

        if done and date:
            TrainerMonthlyActivity.objects.create(
                monthly_review=review,
                student_id=student_id,
                activity_id=activity_id,
                completed_date=date
            )

            # 🔹 Sync with StudentProfile
            student = StudentProfile.objects.filter(id=student_id).first()
            if student:
                activity = BatchActivity.objects.filter(id=activity_id).first()
                if activity:
                    if activity.activity.lower() == "drop out":
                        student.drop_out = True
                        student.dropout_date = date
                        student.save(update_fields=["drop_out", "dropout_date"])

                    elif activity.activity.lower() == "batch changed":
                        student.batch_change = True
                        student.batch_change_date = date
                        student.save(update_fields=["batch_change", "batch_change_date"])
                    
                    elif activity.activity.lower() == "placement pool entry":
                        student.placement_pool_added = True
                        student.placement_pool_added_date = date
                        student.save(update_fields=["placement_pool_added", "placement_pool_added_date"])


    return JsonResponse({"success": "Review saved successfully!"})

# =============Trainer new reports========
@login_required
def trainer_review_report(request):
    user = request.user
    trainers = FacultyProfile.objects.all()

    selected_trainer = None
    selected_batch = request.GET.get("batch_id")
    selected_month = request.GET.get("month")  # e.g. "2025-07"
    batches = []

    # If the logged in user is a trainer, preselect them
    if hasattr(user, "faculty_user"):
        selected_trainer = user.faculty_user.id
        batches = Batch.objects.filter(faculty=user.faculty_user)

    return render(
        request,
        "reports/trainer_review_report.html",
        {
            "trainers": trainers,
            "selected_trainer": selected_trainer,
            "batches": batches,
            "selected_batch": selected_batch,
            "selected_month": selected_month,
        },
    )


@login_required
def get_batches_for_trainer(request):
    faculty_id = request.GET.get('trainer_id')
    batches = Batch.objects.filter(faculty_id=faculty_id)
    batch_list = [{'id': b.id, 'name': b.name} for b in batches]
    print(batch_list)
    return JsonResponse(batch_list, safe=False)

@login_required
def get_months_for_batch(request):
    batch_id = request.GET.get("batch_id")
    reviews = TrainerMonthlyReview.objects.filter(batch_id=batch_id).values("id", "review_date")
    months = [
        {
            "id": r["id"],
            "month": get_month_name(r["review_date"].month),
            "month_number":r["review_date"].month,
            "year": r["review_date"].year,
        }
        for r in reviews
    ]
    return JsonResponse(months, safe=False)

@login_required
def view_review_report(request):
    review_id = request.GET.get("review_id")
    review = get_object_or_404(TrainerMonthlyReview, id=review_id)

    metrics = review.trainermonthlymetric_set.all()

    # All students in the batch
    students = review.batch.studentprofile_set.all().order_by("user__first_name")

    # All activities for this batch
    batch_activities = BatchActivity.objects.filter(batch=review.batch).order_by("day")

    # Fetch completions
    completions = review.trainermonthlyactivity_set.all().select_related("student", "activity")
    # print(completions)
    # completion_map = {(c.student_id, c.activity_id): c.completed_date for c in completions}
    # print(completion_map)
    completion_map = {}
    for c in completions:
        completion_map.setdefault(c.student_id, {})[c.activity_id] = c.completed_date

    return render(request, "reports/review_report.html", {
        "review": review,
        "metrics": metrics,
        "students": students,
        "batch_activities": batch_activities,
        "completion_map": completion_map,
    })



def get_month_name(month_num):
    import calendar
    return calendar.month_name[month_num]

# views.py
@login_required
def all_months_review_report(request):
    user = request.user
    trainers = FacultyProfile.objects.all()

    # If logged-in user is a trainer, preselect them
    selected_trainer = None
    if hasattr(user, "faculty_user"):  # logged in user is a trainer
        selected_trainer = user.faculty_user.id
        
        batches = Batch.objects.filter(faculty=user.faculty_user)
    else:
        batches = []

    return render(
        request,
        "reports/all_months_review_report.html",
        {
            "trainers": trainers,
            "selected_trainer": selected_trainer,
            "batches": batches,
        },
    )

@login_required
def view_all_months_report(request):
    trainer_id = request.GET.get("trainer_id")
    batch_id = request.GET.get("batch_id")

    batch = get_object_or_404(Batch, id=batch_id)

    # All reviews for this batch
    reviews = TrainerMonthlyReview.objects.filter(batch=batch).order_by("review_date")

    # Get students and activities
    students = batch.studentprofile_set.all().order_by("user__first_name")
    batch_activities = BatchActivity.objects.filter(batch=batch).order_by("day")

    # Map review -> metrics, student -> activity -> completed_date
    all_data = {}
    for review in reviews:
        completions = review.trainermonthlyactivity_set.all().select_related("student", "activity")
        # completion_map = {(c.student_id, c.activity_id): c.completed_date for c in completions}
        completion_map = {}
        for c in completions:
            completion_map.setdefault(c.student_id, {})[c.activity_id] = c.completed_date

        metrics = review.trainermonthlymetric_set.all()  # add metrics

        all_data[review.id] = {
            "review": review,
            "completion_map": completion_map,
            "metrics": metrics
        }

    return render(request, "reports/view_all_months_report.html", {
        "batch": batch,
        "students": students,
        "batch_activities": batch_activities,
        "all_data": all_data
    })
from .models import CourseMilestoneActivity, BatchActivity
from settings_app.utils import calculate_working_day
@login_required
def sync_course_activities(request, pk):
    """Sync CourseMilestoneActivity into BatchActivity for all batches of this course."""
    course = get_object_or_404(Course, pk=pk)
    batches = Batch.objects.filter(course=course)

    new_count = 0
    updated_count = 0

    course_activities = CourseMilestoneActivity.objects.filter(course=course)

    for batch in batches:
        # map of (activity_name) -> BatchActivity
        existing_activities = { (b.activity): b for b in BatchActivity.objects.filter(batch=batch) }

        for act in course_activities:
            planned_date = calculate_working_day(batch.start_date, act.day)

            if act.activity in existing_activities:
                batch_act = existing_activities[act.activity]

                # update if day has changed (so planned_date also changes)
                if batch_act.day != act.day:
                    batch_act.day = act.day
                    batch_act.planned_date = planned_date
                    batch_act.save(update_fields=["day", "planned_date"])
                    updated_count += 1

            else:
                # create new activity
                BatchActivity.objects.create(
                    batch=batch,
                    activity=act.activity,
                    day=act.day,
                    planned_date=planned_date,
                    created_user=request.user
                )
                new_count += 1

    if new_count or updated_count:
        messages.success(
            request,
            f"✅ Sync complete: {new_count} new activities added, {updated_count} updated."
        )
    else:
        messages.info(request, "No changes found to sync.")

    return redirect("course_edit", pk=course.pk)

# @login_required
# def placement_all_months_review_report(request):
#     pass

# @login_required
# def placement_monthly_review_report(request):
#     pass

# @login_required
# def placement_add_monthly_review(request):
#     pass

@login_required
def placement_add_monthly_review(request):
    """Render placement monthly review screen"""
    placement = get_object_or_404(PlacementProfile, user=request.user)
    
    # All students in placement pool but not placed
    students = StudentProfile.objects.filter(
        placement_pool_added=True, placed=False
    ).select_related("batch__course", "batch__faculty__user")

    return render(request, "placement_add_review.html", {
        "placement": placement,
        "students": students
    })


@login_required
def get_placement_metrics(request):
    """Return placement metrics dynamically"""
    placement = get_object_or_404(PlacementProfile, user=request.user)
    review_month = request.GET.get("review_month")

    # Prevent duplicate review for the same month
    existing_review = PlacementMonthlyReview.objects.filter(
        user=placement, review_date__startswith=review_month
    ).first()

    if existing_review:
        # Convert YYYY-MM to 'Month, Year'
        year, month = map(int, review_month.split("-"))
        month_str = f"{calendar.month_name[month]}, {year}"
        return JsonResponse({
            "status": "exists",
            "message": f"Review for <b>{month_str}</b> already exists."
        })
    
    # from dateutil.relativedelta import relativedelta

    # Check continuous monthly review
    latest_review = PlacementMonthlyReview.objects.filter(user=placement).order_by("-review_date").first()
    if latest_review:
        year, month = map(int, review_month.split("-"))
        selected_date = datetime.date(year, month, 1)

        next_allowed_month = latest_review.review_date + relativedelta(months=1)
        if selected_date != next_allowed_month:
            allowed_str = f"{calendar.month_name[next_allowed_month.month]}, {next_allowed_month.year}"
            return JsonResponse({
                "status": "invalid",
                "message": f"Please add reviews continuously. Next review must be for <b>{allowed_str}</b>."
            })


    # Placement metrics
    metrics = Metric.objects.filter(group__name="Placement").values("id", "metric_name")

    # Students in placement pool
    students = StudentProfile.objects.filter(
        placement_pool_added=True, placed=False
    )

    total_pool = students.count()
    # total_placed = students.filter(placed=True).count()
    total_placed = 0
    # conversion_rate = round((total_placed / total_pool) * 100, 2) if total_pool > 0 else 0
    conversion_rate = 0

    response_metrics = []
    for m in metrics:
        if m["metric_name"] == "Total Students in Placement Pool":
            value = total_pool
            readonly = True
        elif m["metric_name"] == "Total Placements":
            value = total_placed
            readonly = True
        elif m["metric_name"] == "Conversion Rate":
            value = conversion_rate
            readonly = True
        else:
            value = ""
            readonly = False

        response_metrics.append({
            "id": m["id"],
            "name": m["metric_name"],
            "value": value,
            "readonly": readonly,
            "datatype": "Number"
        })

    return JsonResponse({
        "status": "ok",
        "metrics": response_metrics,
    })


@login_required
def save_placement_review(request):
    """Save placement monthly review + metrics + placements"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    placement = get_object_or_404(PlacementProfile, user=request.user)
    review_month = request.POST.get("review_month")
    remarks = request.POST.get("remarks", "")
    # print()
    # print(review_month)

    try:
        review_date = datetime.datetime.strptime(review_month + "-01", "%Y-%m-%d").date()
    except:
        return JsonResponse({"error": "Invalid month"}, status=400)

    review = PlacementMonthlyReview.objects.create(
        user=placement,
        review_date=review_date,
        remarks=remarks
    )

    # Save metrics
    for key, value in request.POST.items():
        if key.startswith("metric_"):
            metric_id = key.replace("metric_", "")
            PlacementMonthlyMetric.objects.create(
                monthly_review=review,
                metric_id=metric_id,
                metric_value=value
            )

    # Save placed students
    placed_ids = request.POST.getlist("placed_students[]")
    # StudentProfile.objects.filter(id__in=placed_ids).update(
    #     placed=True, placed_date=datetime.datetime.today()
    # )
    placed_students = StudentProfile.objects.filter(id__in=placed_ids)
    placed_students.update(
        placed=True, 
        # placed_date=datetime.datetime.today()
        placed_date=review_date
    )
     # ---- Update Trainer's Monthly Review "Placements" Metric ----
    if placed_students.exists():
        try:
            placement_metric = Metric.objects.get(metric_name__iexact="Placements", group__name="Faculty")
        except Metric.DoesNotExist:
            placement_metric = None

        for student in placed_students:
            faculty = getattr(student.batch, "faculty", None)
            if faculty and placement_metric:
                trainer_review = TrainerMonthlyReview.objects.filter(
                    user=faculty,
                    batch=student.batch,
                    review_date__year=review_date.year,
                    review_date__month=review_date.month
                ).first()

                if trainer_review:
                    trainer_metric, created = TrainerMonthlyMetric.objects.get_or_create(
                        monthly_review=trainer_review,
                        metric=placement_metric,
                        defaults={"metric_value": "0"}
                    )

                    # Increment placement count
                    try:
                        current_val = int(trainer_metric.metric_value or 0)
                    except ValueError:
                        current_val = 0

                    trainer_metric.metric_value = str(current_val + 1)
                    trainer_metric.save()
    

    return JsonResponse({"success": "Placement review saved successfully!"})


# from .models import PlacementProfile, PlacementMonthlyReview

# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.shortcuts import render, get_object_or_404
# from .models import PlacementProfile, PlacementMonthlyReview
# from django.contrib.auth.models import Group

@login_required
def placement_monthly_review_report(request):
    user = request.user
    is_manager = user.groups.filter(name="Manager").exists()
    is_placement = user.groups.filter(name="Placement").exists()

    placement_users = PlacementProfile.objects.all()

    selected_user = None
    selected_review = None
    metrics = []
    placed_students = []

    # Determine selected user
    if is_placement:
        selected_user = get_object_or_404(PlacementProfile, user=user)
    else:
        placement_user_id = request.GET.get("placement_user")
        if placement_user_id:
            selected_user = get_object_or_404(PlacementProfile, id=placement_user_id)

    # Determine selected review
    review_id = request.GET.get("review_month")
    if selected_user and review_id:
        selected_review = get_object_or_404(PlacementMonthlyReview, id=review_id, user=selected_user)
        metrics = selected_review.placementmonthlymetric_set.select_related("metric")
        placed_students = StudentProfile.objects.filter(
            placed=True, 
            placed_date__year=selected_review.review_date.year,
            placed_date__month=selected_review.review_date.month
        )

    context = {
        "is_manager": is_manager,
        "is_placement": is_placement,
        "placement_users": placement_users,
        "selected_user": selected_user,
        "selected_review": selected_review,
        "metrics": metrics,
        "placed_students": placed_students,
    }
    return render(request, "reports/placement_monthly_review_report.html", context)




@login_required
def placement_all_months_review_report(request):
    user = request.user
    is_manager = user.groups.filter(name="Manager").exists()
    is_placement = user.groups.filter(name="Placement").exists()

    placement_users = PlacementProfile.objects.all()
    selected_user = None
    reviews = []

    # Determine selected user
    if is_placement:
        selected_user = get_object_or_404(PlacementProfile, user=user)
    else:
        placement_user_id = request.GET.get("placement_user")
        if placement_user_id:
            selected_user = get_object_or_404(PlacementProfile, id=placement_user_id)

    # Fetch reviews
    if selected_user:
        reviews_qs = PlacementMonthlyReview.objects.filter(user=selected_user).order_by("review_date")

        # For each review, attach placed students dynamically
        reviews = []
        for review in reviews_qs:
            review.placed_students = StudentProfile.objects.filter(
                placed=True,
                placed_date__year=review.review_date.year,
                placed_date__month=review.review_date.month
            )
            reviews.append(review)

    context = {
        "is_manager": is_manager,
        "is_placement": is_placement,
        "placement_users": placement_users,
        "selected_user": selected_user,
        "reviews": reviews,
    }
    return render(request, "reports/placement_all_months_review_report.html", context)



@login_required
def get_placement_review_months(request, user_id):
    """AJAX: Return all review months for a given placement user"""
    placement_user = get_object_or_404(PlacementProfile, id=user_id)
    reviews = PlacementMonthlyReview.objects.filter(user=placement_user).order_by("review_date")

    months = []
    for r in reviews:
        months.append({
            "id": r.id,
            "month": r.review_date.strftime("%B %Y")  # e.g. "September 2025"
        })

    return JsonResponse({"months": months})

def is_reporting_officer(user):
    return SalesProfile.objects.filter(reporting_officers=user).exists()

@login_required
def sales_target_list(request):
    if not is_reporting_officer(request.user):
        return HttpResponseForbidden("You are not authorized to manage sales targets.")
    targets = SalesTarget.objects.filter(
        sales_person__reporting_officers=request.user
    )
    return render(request, "sales/target_list.html", {"targets": targets})


@login_required
def sales_target_create(request):
    if not is_reporting_officer(request.user):
        return HttpResponseForbidden("You are not authorized to manage sales targets.")
    print("Hello")
    if request.method == "POST":
        print("Hello")
        form = SalesTargetForm(request.POST, user=request.user)
        if form.is_valid():
            target = form.save(commit=False)
            target.created_by = request.user
            target.save()
            messages.success(request, "Sales target added successfully.")
            return redirect("sales_target_list")
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = SalesTargetForm(user=request.user)

    return render(request, "sales/target_form.html", {"form": form})


@login_required
def sales_target_edit(request, pk):
    if not is_reporting_officer(request.user):
        return HttpResponseForbidden("You are not authorized to manage sales targets.")
    target = get_object_or_404(
        SalesTarget,
        pk=pk,
        sales_person__reporting_officers=request.user
    )
    if request.method == "POST":
        form = SalesTargetForm(request.POST, instance=target, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Sales target updated successfully.")
            return redirect("sales_target_list")
    else:
        form = SalesTargetForm(instance=target, user=request.user)

    return render(request, "sales/target_form.html", {"form": form, "edit": True})


@login_required
def sales_target_delete(request, pk):
    if not is_reporting_officer(request.user):
        return HttpResponseForbidden("You are not authorized to manage sales targets.")
    target = get_object_or_404(
        SalesTarget,
        pk=pk,
        sales_person__reporting_officers=request.user
    )
    if request.method == "POST":
        target.delete()
        messages.success(request, "Sales target deleted successfully.")
        return redirect("sales_target_list")

    return render(request, "sales/target_confirm_delete.html", {"target": target})