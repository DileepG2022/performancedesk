# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Batch, Branch, Course, StudentProfile, FacultyProfile, SalesProfile, PlacementProfile

from .forms import BatchForm, CourseForm, CourseMilestoneActivityForm, BranchForm, FacultyProfileForm, FacultyProfileEditForm, SalesProfileForm, SalesProfileEditForm, StudentProfileForm, StudentProfileEditForm, StudentImportForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db import transaction  # Import transaction for rollback
from django.forms import inlineformset_factory
from employeereview.models import CourseMilestoneActivity, BatchActivity, TrainerMonthlyReview, PlacementMonthlyReview, SalesMonthlyReview

import os
import calendar
import datetime
from datetime import date, timedelta

# from exams.models import Exam, ExamSubmission
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .menus import DEPARTMENT_MENUS
import openpyxl
from django.http import HttpResponse
import pandas as pd

def home(request):
    """ Redirect users to their respective dashboards based on roles """
    user = request.user
    print(user)
    if user.is_superuser:
        return redirect('/admin/')  # Redirect superuser to Django Admin Panel
    elif user.groups.filter(name='Manager').exists():
        return redirect('manager_dashboard')  # Redirect Manager to their dashboard
    elif user.groups.filter(name='Faculty').exists():
        return redirect('faculty_dashboard')  # Redirect Faculty to their dashboard
    elif user.groups.filter(name='Sales').exists():
        return redirect('sales_dashboard')  # Redirect Sales team to their dashboard
    elif user.groups.filter(name='Student').exists():
        return redirect('student_dashboard')  # Redirect Student to their dashboard
    elif user.groups.filter(name='Placement').exists():
        return redirect('placement_dashboard')  # Redirect Student to their dashboard
    else:
        return render(request, 'settings_app/home.html')  # Default landing page

def general_error(request, exception=None):
    print("error")
    return render(request, 'settings_app/general_error.html')

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def no_permission(request):
    return render(request, 'settings_app/no_permission.html')

@user_passes_test(is_manager, login_url="no_permission")
@login_required
def manager_dashboard(request):
    trainer_months = TrainerMonthlyReview.objects.dates("review_date", "month")
    sales_months   = SalesMonthlyReview.objects.dates("review_date", "month")
    place_months   = PlacementMonthlyReview.objects.dates("review_date", "month")

    all_months = sorted(set(trainer_months) | set(sales_months) | set(place_months))

    selected_month = request.GET.get("month")
    if selected_month:
        selected_month = date.fromisoformat(selected_month + "-01")
    else:
        selected_month = all_months[-1] if all_months else None

    summary = {}

    if selected_month:
        year = selected_month.year
        month = selected_month.month

        # ---------------------------
        # Trainer Summary (per trainer per batch)
        # ---------------------------
        trainer_summary = []
        trainers = FacultyProfile.objects.all()

        for trainer in trainers:
            trainer_batches = Batch.objects.filter(faculty=trainer)
            # Reviews submitted for this month
            submitted_reviews = TrainerMonthlyReview.objects.filter(
                user=trainer, review_date__year=year, review_date__month=month
            ).values_list("batch_id", flat=True)

            # Find pending batches
            pending_batches = trainer_batches.exclude(id__in=submitted_reviews)

            trainer_summary.append({
                "name": trainer.user.get_full_name() or trainer.user.username,
                "batches": trainer_batches.count(),
                "submitted": len(submitted_reviews),
                "pending": pending_batches.count(),
                "pending_batches": [b.name for b in pending_batches],  # pass names
            })

        summary["trainers"] = trainer_summary

        # ---------------------------
        # Sales Summary
        # ---------------------------
        sales_summary = []
        submitted_sales = 0
        for sp in SalesProfile.objects.all():
            submitted = SalesMonthlyReview.objects.filter(
                user=sp, review_date__year=year, review_date__month=month
            ).exists()
            if submitted:
                submitted_sales += 1
            sales_summary.append({
                "name": sp.user.get_full_name() or sp.user.username,
                "status": "Submitted" if submitted else "Pending"
            })

        summary["sales"] = {
            "list": sales_summary,
            "submitted": submitted_sales,
            "pending": SalesProfile.objects.count() - submitted_sales,
        }

        # ---------------------------
        # Placement Summary
        # ---------------------------
        placement_summary = []
        submitted_place = 0
        for pp in PlacementProfile.objects.all():
            submitted = PlacementMonthlyReview.objects.filter(
                user=pp, review_date__year=year, review_date__month=month
            ).exists()
            if submitted:
                submitted_place += 1
            placement_summary.append({
                "name": pp.user.get_full_name() or pp.user.username,
                "status": "Submitted" if submitted else "Pending"
            })

        summary["placement"] = {
            "list": placement_summary,
            "submitted": submitted_place,
            "pending": PlacementProfile.objects.count() - submitted_place,
        }
    
    return render(request, "settings_app/manager_dashboard.html", {
        "months": all_months,
        "selected_month": selected_month,
        "summary": summary,
    })

@login_required
def faculty_dashboard(request):
    """Display batches assigned to the logged-in faculty"""
    try:
        faculty = FacultyProfile.objects.get(user=request.user)  # Get faculty profile
        batches = Batch.objects.filter(faculty=faculty)  # Get batches where faculty is assigned
        # exams = Exam.objects.filter(created_by=faculty).order_by('-start_time')[:5]
        # ------------------------
        # 1. Find previous month
        # ------------------------
        today = date.today()
        first_day_this_month = today.replace(day=1)
        last_day_prev_month = first_day_this_month - timedelta(days=1)
        prev_month = last_day_prev_month.month
        prev_year = last_day_prev_month.year

        # ------------------------
        # 2. Get all months trainer has reviews for
        # ------------------------
        reviews = TrainerMonthlyReview.objects.filter(user=faculty)
        unique_months = TrainerMonthlyReview.objects.filter(user=faculty).dates('review_date', 'month')
        months = [{"value": dt.strftime("%Y-%m"), "name": f"{calendar.month_name[dt.month]} {dt.year}"} 
          for dt in unique_months]

        # ------------------------
        # Decide default month
        # ------------------------
        if months:
            default_month = months[0]["value"]   # oldest available month (first in sorted list)
        else:
            today = date.today()
            default_month = f"{today.year}-{today.month:02d}"

        # ------------------------
        # 3. Completed & pending reviews for previous month
        # ------------------------
        completed_reviews = TrainerMonthlyReview.objects.filter(
            user=faculty,
            review_date__year=prev_year,
            review_date__month=prev_month
        ).count()

        # pending = total batches - already reviewed
        reviewed_batches = TrainerMonthlyReview.objects.filter(
            user=faculty,
            review_date__year=prev_year,
            review_date__month=prev_month
        ).values_list("batch_id", flat=True)

        pending_reviews = batches.exclude(id__in=reviewed_batches).count()

        context = {
            "batches": batches,
            "months": months,
            # "default_month": f"{prev_year}-{prev_month:02d}",
            "default_month": default_month,
            "completed_reviews": completed_reviews,
            "pending_reviews": pending_reviews,
        }

    except FacultyProfile.DoesNotExist:
        context = {
            "batches": None,
            "months": [],
            "completed_reviews": 0,
            "pending_reviews": 0,
        }
    return render(request, 'settings_app/faculty_dashboard.html', context)

    # return render(request, 'settings_app/faculty_dashboard.html', {'batches': batches,
    # 'exams': exams})
# @login_required
# def sales_dashboard(request):
#     # batches = Batch.objects.all()
#     # return render(request, 'manager_dashboard.html', {'batches': batches})
#     # return render(request, 'settings_app/sales_dashboard.html')
#     # views.py
# from django.http import JsonResponse
from django.db.models.functions import ExtractMonth, ExtractYear
from employeereview.models import SalesMonthlyReview, SalesMonthlyMetric

@login_required
def sales_dashboard(request):
    # Distinct months & years for dropdown
    months_years = (
        SalesMonthlyReview.objects
        .annotate(month=ExtractMonth('review_date'), year=ExtractYear('review_date'))
        .values('month', 'year')
        .distinct()
        .order_by('-year', '-month')
    )

    # Build list with formatted month name
    formatted = []
    for item in months_years:
        display = date(item['year'], item['month'], 1).strftime("%B, %Y")  # e.g., "July, 2025"
        formatted.append({
            "month": item["month"],
            "year": item["year"],
            "display": display
        })

    return render(request, "settings_app/sales_dashboard.html", {"months_years": formatted})

@login_required
def sales_metrics_data(request, year, month):
    try:
        review = SalesMonthlyReview.objects.get(
            user=request.user.sales_user,
            review_date__year=year,
            review_date__month=month
        )
        metrics = SalesMonthlyMetric.objects.filter(monthly_review=review).select_related("metric")

        data = {m.metric.metric_name: m.metric_value for m in metrics}
        return JsonResponse({"success": True, "metrics": data})
    except SalesMonthlyReview.DoesNotExist:
        return JsonResponse({"success": False, "metrics": {}})

# @login_required
# def student_dashboard(request):
#     student = request.user.studentprofile
#     batch = student.batch

#     # All exams for student's batch
#     exams = Exam.objects.filter(batch=batch).order_by('-start_time')

#     # Exams already submitted
#     submitted_exam_ids = ExamSubmission.objects.filter(student=student).values_list('exam_id', flat=True)
#     print(submitted_exam_ids)
#     return render(request, 'settings_app/student_dashboard.html', {
#         'student': student,
#         'exams': exams,
#         'submitted_exam_ids': submitted_exam_ids,
#         'now': timezone.now(),
#     })


from .utils import calculate_working_day

@login_required
def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'settings_app/batch_list.html', {'batches': batches})
@login_required
# def add_batch(request):
#     if request.method == "POST":
#         form = BatchForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Batch added successfully!")
#             # return redirect('batch_list')
#     else:
#         form = BatchForm()
#     return render(request, 'settings_app/add_batch.html', {'form': form})
def add_batch(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            # Auto-create BatchActivity from CourseMilestoneActivity
            course_activities = CourseMilestoneActivity.objects.filter(course=batch.course)
            for act in course_activities:
                planned_date = calculate_working_day(batch.start_date, act.day)
                BatchActivity.objects.create(
                batch=batch,
                activity=act.activity,
                day=act.day,
                planned_date=planned_date,
                created_user=request.user
            )

            messages.success(request, "Batch added successfully!")
            return redirect('batch_list')
    else:
        form = BatchForm()
    return render(request, 'settings_app/add_batch.html', {'form': form})

# Edit batch
@login_required
# def edit_batch(request, batch_id):
#     batch = get_object_or_404(Batch, id=batch_id)

#     if request.method == "POST":
#         form = BatchForm(request.POST, instance=batch)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Batch updated successfully!")
#             # return redirect('batch_list')
#     else:
#         form = BatchForm(instance=batch)

#     return render(request, 'settings_app/edit_batch.html', {'form': form})

def edit_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    old_start_date = batch.start_date

    if request.method == "POST":
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            updated_batch = form.save()
            if old_start_date != updated_batch.start_date:
                # Update planned_dates
                activities = BatchActivity.objects.filter(batch=updated_batch)
                for act in activities:
                    act.planned_date = calculate_working_day(updated_batch.start_date, act.day)
                    # act.planned_date = updated_batch.start_date + timedelta(days=act.day - 1)
                    act.save()
            messages.success(request, "Batch updated successfully!")
            return redirect('batch_list')
    else:
        form = BatchForm(instance=batch)

    return render(request, 'settings_app/edit_batch.html', {'form': form})

# Delete batch
@login_required
# def delete_batch(request, batch_id):
#     batch = get_object_or_404(Batch, id=batch_id)

#     if request.method == "POST":
#         batch.delete()
#         messages.success(request, "Batch deleted successfully!")
#         # return redirect('batch_list')

#     return render(request, 'settings_app/delete_batch.html', {'batch': batch})

def delete_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)

    if request.method == "POST":
        batch.delete()
        BatchActivity.objects.filter(batch=batch).delete()
        messages.success(request, "Batch deleted successfully!")
        return redirect('batch_list')

    return render(request, 'settings_app/delete_batch.html', {'batch': batch})

@login_required
def batch_activity_view(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    activities = BatchActivity.objects.filter(batch=batch).order_by('day')
    return render(request, 'settings_app/batch_activities.html', {
        'batch': batch,
        'activities': activities
    })


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'settings_app/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    CourseMilestoneFormSetCustom = inlineformset_factory(
        Course, CourseMilestoneActivity,
        form=CourseMilestoneActivityForm,
        extra=1, can_delete=True
    )
    if request.method == 'POST':
        form = CourseForm(request.POST)
        formset = CourseMilestoneFormSetCustom(request.POST)
        if form.is_valid() and formset.is_valid():
            course = form.save(commit=False)
            course.created_user = request.user
            course.save()
            formset.instance = course
            formset.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
        formset = CourseMilestoneFormSetCustom()
    return render(request, 'settings_app/course_form.html', {'form': form, 'formset': formset})

@login_required
def course_update(request, pk):
    CourseMilestoneFormSetCustom = inlineformset_factory(
        Course, CourseMilestoneActivity,
        form=CourseMilestoneActivityForm,
        extra=0, can_delete=True  # 👈 Set extra to 0 for edit
    )
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        print("POST")
        form = CourseForm(request.POST, instance=course)
        formset = CourseMilestoneFormSetCustom(request.POST, instance=course)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
        else:
            print("Form errors:", form.errors)  # Debugging line
            print("Formset errors:", formset.errors)  # Debugging line
    else:
        form = CourseForm(instance=course)
        formset = CourseMilestoneFormSetCustom(instance=course)
    return render(request, 'settings_app/course_form.html', {'form': form, 'formset': formset})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, 'Course deleted.')
    return redirect('course_list')

# @login_required
# def add_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'settings_app/add_course.html', {'form': form})

# @login_required
# def edit_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
    
#     if request.method == "POST":
#         form = CourseForm(request.POST, instance=course)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')  # Redirect to course list page
#     else:
#         form = CourseForm(instance=course)

#     return render(request, 'settings_app/edit_course.html', {'form': form, 'course': course})

# @login_required
# def delete_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.method == "POST":
#         course.delete()
#         return redirect('course_list')  # Redirect after deleting
#     return render(request, 'settings_app/delete_course.html', {'course': course})

# @login_required
# def student_list(request):
#     """Display list of students with search functionality"""
#     students = StudentProfile.objects.all()

#     student_id = request.GET.get('student_id')
#     username = request.GET.get('username')

#     if student_id:
#         students = students.filter(student_id__icontains=student_id)
#     if username:
#         students = students.filter(user__username__icontains=username)

#     return render(request, 'settings_app/student_list.html', {'students': students})

# @login_required
# def add_student(request):
#     """Add a new student"""
#     if request.method == 'POST':
#         form = StudentProfileForm(request.POST, request.FILES)

#         # print(form.is_valid())

#         if form.is_valid():
#             try:
#                 with transaction.atomic():  # Start a database transaction
#                     # Extract user data
#                     first_name = form.cleaned_data['first_name']
#                     last_name = form.cleaned_data['last_name']
#                     username = form.cleaned_data['username']
#                     password = form.cleaned_data['password']

#                     # Create User
#                     user = User.objects.create_user(
#                         username=username,
#                         first_name=first_name,
#                         last_name=last_name,
#                         password=password
#                     )

#                     # Add user to Student Group
#                     student_group, _ = Group.objects.get_or_create(name='Student')
#                     user.groups.add(student_group)

#                     # Create Student Profile
#                     student = form.save(commit=False)
#                     student.user = user
#                     student.created_by = request.user  # Assign the logged-in user
#                     student.save()
#                     form.save_m2m()  # Save ManyToManyField (if any)

#                     messages.success(request, "Student added successfully!")
#                     # return redirect('student_list')

#             except Exception as e:
#                 print(f"Error adding student: {e}")
#                 messages.error(request, f"Error adding student: {e}")
#         else:
#             print("Form errors:", form.errors)  # Debugging line

#     else:
#         form = StudentProfileForm()

#     return render(request, 'settings_app/add_student.html', {'form': form})

# @login_required
# def edit_student(request, student_id):
#     """Edit student details"""
#     student = get_object_or_404(StudentProfile, id=student_id)

#     if request.method == 'POST':
#         form = EditStudentProfileForm(request.POST, request.FILES, instance=student)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Student details updated successfully!")
#             # return redirect('student_list')
#     else:
#         form = EditStudentProfileForm(instance=student)

#     return render(request, 'settings_app/edit_student.html', {'form': form, 'student': student})

# @login_required
# def delete_student(request, student_id):
#     """Delete student"""
#     student = get_object_or_404(StudentProfile, id=student_id)
    
#     if request.method == 'POST':
#         student.user.delete()  # Deletes the associated user as well
#         student.delete()
#         messages.success(request, "Student deleted successfully!")
#         # return redirect('student_list')

#     return render(request, 'settings_app/delete_student.html', {'student': student})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'settings_app/course_list.html', {'courses': courses})

# List all branches
@login_required
def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'settings_app/branch_list.html', {'branches': branches})

# Add new branch
@login_required
def add_branch(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch added successfully!")
            # return redirect('branch_list')
    else:
        form = BranchForm()
    return render(request, 'settings_app/add_branch.html', {'form': form})

# Edit branch
@login_required
def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == "POST":
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch updated successfully!")
            # return redirect('branch_list')
    else:
        form = BranchForm(instance=branch)

    return render(request, 'settings_app/edit_branch.html', {'form': form})

# Delete branch
@login_required
def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == "POST":
        branch.delete()
        messages.success(request, "Branch deleted successfully!")
        # return redirect('branch_list')

    return render(request, 'settings_app/delete_branch.html', {'branch': branch})

# @login_required
# def batch_list(request):
#     batches = Batch.objects.all()
#     return render(request, 'settings_app/batch_list.html', {'batches': batches})

from django.core.paginator import Paginator
from django.db.models import Q
# from settings_app.models import Batch, Branch, Course, FacultyProfile

@login_required
def batch_list(request):
    batches = Batch.objects.all()

    # Get filter params
    name = request.GET.get('name', '').strip()
    branch_id = request.GET.get('branch')
    course_id = request.GET.get('course')
    faculty_id = request.GET.get('faculty')
    completed = request.GET.get('completed')
    sort = request.GET.get('sort')  # Default: newest first

    print(sort)

    # Apply filters
    if name:
        batches = batches.filter(name__icontains=name)
    if branch_id:
        batches = batches.filter(branch_id=branch_id)
    if course_id:
        batches = batches.filter(course_id=course_id)
    if faculty_id:
        batches = batches.filter(faculty_id=faculty_id)
    if completed in ['yes', 'no']:
        batches = batches.filter(completed=(completed == 'yes'))
    
    # Sorting
    allowed_sorts = ('start_date', '-start_date', 'end_date', '-end_date')
    if sort not in allowed_sorts:
        sort = '-start_date'  # default
    batches = batches.order_by(sort)

    # print(batches)


    # Pagination
    paginator = Paginator(batches, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build clean querystrings to avoid whitespace/duplication in template
    qs_no_page_no_sort = request.GET.copy()
    qs_no_page_no_sort.pop('page', None)
    qs_no_page_no_sort.pop('sort', None)
    base_qs = qs_no_page_no_sort.urlencode()           # filters only

    qs_no_page = request.GET.copy()
    qs_no_page.pop('page', None)
    qs_keep = qs_no_page.urlencode()                   # filters + current sort

    # Next-sort toggles
    next_sort_start = 'start_date' if sort != 'start_date' else '-start_date'
    next_sort_end   = 'end_date'   if sort != 'end_date'   else '-end_date'

    return render(request, 'settings_app/batch_list.html', {
        'batches': page_obj,
        'branches': Branch.objects.all(),
        'courses': Course.objects.all(),
        'faculties': FacultyProfile.objects.all(),
        'filters': {
            'name': name,
            'branch_id': branch_id,
            'course_id': course_id,
            'faculty_id': faculty_id,
            'completed': completed,
            'sort': sort,  # Pass to template to highlight arrows
        },
        'sort': sort,
        'base_qs': base_qs,
        'qs_keep': qs_keep,
        'next_sort_start': next_sort_start,
        'next_sort_end': next_sort_end,
        'page_obj': page_obj,
    })


@login_required
def faculty_list(request):
    search_query = request.GET.get('search', '')
    branch_filter = request.GET.get('branch', '')

    faculties = FacultyProfile.objects.all()
    branches = Branch.objects.all()

    if search_query:
        faculties = faculties.filter(user__first_name__icontains=search_query) | faculties.filter(user__email__icontains=search_query)

    if branch_filter:
        faculties = faculties.filter(branch__id=branch_filter)

    return render(request, 'settings_app/faculty_list.html', {'faculties': faculties, 'branches': branches})


@login_required
def add_faculty(request):
    if request.method == 'POST':
        form = FacultyProfileForm(request.POST)

        # print(form.is_valid())

        if form.is_valid():
            try:
                with transaction.atomic():  # Start a database transaction
                    # Extract user data
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']

                    # Create User
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=password  # Securely hashed
                    )

                    # Add user to Faculty Group
                    faculty_group, _ = Group.objects.get_or_create(name='Faculty')
                    user.groups.add(faculty_group)

                    # Create Faculty Profile
                    faculty = form.save(commit=False)
                    faculty.user = user
                    faculty.created_by = request.user  # Assign the logged-in user
                    faculty.save()
                    form.save_m2m()  # Save ManyToManyField (courses)

                    messages.success(request, "Faculty added successfully!")
                    # return redirect('faculty_list')

            except Exception as e:
                print(f"Error adding faculty: {e}")
                messages.error(request, f"Error adding faculty: {e}")
        else:
            print("Form errors:", form.errors)  # Debugging line

    else:
        form = FacultyProfileForm()

    return render(request, 'settings_app/add_faculty.html', {'form': form})


@login_required
def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    if request.method == 'POST':
        form = FacultyProfileEditForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty updated successfully!")
            # return redirect('faculty_list')
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = FacultyProfileEditForm(instance=faculty)
    return render(request, 'settings_app/edit_faculty.html', {'form': form, 'faculty': faculty})

@login_required
def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    faculty.user.delete()  # Deletes both FacultyProfile and associated User
    messages.success(request, "Faculty deleted successfully!")
    # return redirect('faculty_list')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_department_menu(request):
    """
    Returns menu items for the selected department.
    Defaults to 'Training' if not set in session.
    """
    department = request.session.get('selected_department', 'Training')
    menu_items = DEPARTMENT_MENUS.get(department, [])
    department_names = list(DEPARTMENT_MENUS.keys())  # <-- All departments

    return Response({
        "department": department,
        "departments": department_names,
        "menu": menu_items
    })

from django.http import JsonResponse

@login_required
def switch_department(request):
    if request.method == "POST":
        department = request.POST.get("department")
        if department:
            request.session["selected_department"] = department
            return JsonResponse({"status": "success", "message": f"Department switched to {department}."})
        return JsonResponse({"status": "error", "message": "Invalid department."}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

@login_required
def sales_list(request):
    from settings_app.models import SalesProfile
    # s = SalesProfile.objects.first()
    # print(type(s.reporting_officers))

    search_query = request.GET.get('search', '')
    branch_filter = request.GET.get('branch', '')

    sales = SalesProfile.objects.all()
    branches = Branch.objects.all()

    if search_query:
        sales = sales.filter(user__first_name__icontains=search_query) | sales.filter(user__email__icontains=search_query)

    if branch_filter:
        sales = sales.filter(branch__id=branch_filter)

    return render(request, 'settings_app/sales_list.html', {'sales': sales, 'branches': branches})


@login_required
def add_sales(request):
    if request.method == 'POST':
        # print("POST")
        form = SalesProfileForm(request.POST)
        # print(form)
        if form.is_valid():
            try:
                with transaction.atomic():  # Start a database transaction
                    # print("Hi")
                    # 1. Create the User first
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                    )

                    # 2. Assign Sales group
                    sales_group, created = Group.objects.get_or_create(name='Sales')
                    user.groups.add(sales_group)

                    # 3. Create SalesProfile
                    sales_profile = form.save(commit=False)
                    sales_profile.user = user
                    sales_profile.save()

                    # 4. Save reporting officers M2M
                    form.save_m2m()

                    messages.success(request, "Sales profile created successfully.")
                    # return redirect('sales_list')
            except Exception as e:
                print(f"Error adding Sales: {e}")
                messages.error(request, f"Error adding Sales Person: {e}")
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = SalesProfileForm()
    return render(request, 'settings_app/add_sales.html', {'form': form})


@login_required
def edit_sales(request, sales_id):
    sales = get_object_or_404(SalesProfile, id=sales_id)
    if request.method == 'POST':
        form = SalesProfileEditForm(request.POST, instance=sales)
        if form.is_valid():
            form.save()
            messages.success(request, "Sales staff updated successfully!")
        else:
            print("Form errors:", form.errors)
    else:
        form = SalesProfileEditForm(instance=sales)
    return render(request, 'settings_app/edit_sales.html', {'form': form, 'sales': sales})


@login_required
def delete_sales(request, sales_id):
    sales = get_object_or_404(SalesProfile, id=sales_id)
    sales.user.delete()  # deletes both SalesProfile and User
    messages.success(request, "Sales staff deleted successfully!")

@login_required
def student_list(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    students = StudentProfile.objects.filter(batch=batch)
    return render(request, "settings_app/student_list.html", {
        "batch": batch,
        "students": students
    })

@login_required
def add_student(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    # print(batch)
    if request.method == "POST":
        form = StudentProfileForm(request.POST)
        # print("POST")
        if form.is_valid():
            try:
                with transaction.atomic():  # Start a database transaction
                    # print("Valid")
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']

                    user = User.objects.create_user(username=username, password=password,
                                                    first_name=first_name, last_name=last_name)
                    # Assign "Student" group if exists
                    student_group, _ = Group.objects.get_or_create(name="Student")
                    user.groups.add(student_group)

                    # # Convert month-year string to date
                    # month_year = form.cleaned_data['admission_date']  # e.g., "2025-08"
                    # print(month_year)
                    # if isinstance(month_year, str) and len(month_year) == 7:
                    #     year, month = map(int, month_year.split('-'))
                    #     student.admission_date = datetime.date(year, month, 1)  # first day of month

                    student = form.save(commit=False)
                    student.user = user
                    student.batch = batch
                    student.save()

                    messages.success(request, "Student added successfully!")
                    return redirect('student_list', batch_id=batch.id)
            except Exception as e:
                print(f"Error adding student: {e}")
                messages.error(request, f"Error adding student: {e}")
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = StudentProfileForm(initial={'batch': batch})
    return render(request, "settings_app/add_student.html", {"form": form, "batch": batch})

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == "POST":
        form = StudentProfileEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list', batch_id=student.batch.id)
    else:
        # Initialize form with Month-Year format for the picker
        initial_data = {
            'admission_date': student.admission_date.strftime('%Y-%m') if student.admission_date else ''
        }
        form = StudentProfileEditForm(instance=student, initial=initial_data)
    return render(request, "settings_app/edit_student.html", {"form": form, "student": student})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    batch_id = student.batch.id
    student.user.delete()  # Deletes linked user too
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('student_list', batch_id=batch_id)

@login_required
def export_students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    students = StudentProfile.objects.filter(batch=batch)

    # Create Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Students"

    # Headers
    headers = ["first_name", "last_name", "username", "mobile_no", "whatsapp_no", "sales_person_username", "admission_date", "drop_out"]
    ws.append(headers)

    # Data rows
    for student in students:
        ws.append([
            student.user.first_name,
            student.user.last_name,
            student.user.username,
            str(student.mobile_no) if student.mobile_no else "",
            str(student.whatsapp_no) if student.whatsapp_no else "",
            student.sales_person.user.username if student.sales_person else "",
            # student.admission_date.strftime("%Y-%m-%d"),
            student.admission_date.strftime("%d-%m-%Y") if student.admission_date else "",
            "Yes" if student.drop_out else "No"
        ])

    # HTTP Response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="students_batch_{batch.id}.xlsx"'
    wb.save(response)
    return response

import pandas as pd
from django.http import HttpResponse
from io import BytesIO

@login_required
def import_students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    # request.session['student_import_errors'] = []
    if request.method == "POST":
        request.session['student_import_errors'] = []
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)

                added, skipped = 0, 0
                student_group, _ = Group.objects.get_or_create(name="Student")
                error_rows = []

                for _, row in df.iterrows():
                    username = str(row.get('username')).strip()
                    if not username or username.lower() == "nan":
                        error_rows.append({**row.to_dict(), "error": "Missing username"})
                        skipped += 1
                        continue

                    if User.objects.filter(username=username).exists():
                        error_rows.append({**row.to_dict(), "error": "Username already exists"})
                        skipped += 1
                        continue

                    try:
                        with transaction.atomic():
                            user = User.objects.create_user(
                                username=username,
                                password=str(row.get('password')).strip(),
                                first_name=str(row.get('first_name')).strip() if pd.notna(row.get('first_name')) else "",
                                last_name=str(row.get('last_name')).strip() if pd.notna(row.get('last_name')) else "",
                            )
                            user.groups.add(student_group)

                            sales_person = None
                            sales_username = row.get('sales_person_username')
                            if pd.notna(sales_username):
                                try:
                                    print(sales_username)
                                    sales_person = SalesProfile.objects.get(user__username=str(sales_username).strip())
                                    
                                except SalesProfile.DoesNotExist:
                                    error_rows.append({**row.to_dict(), "error": f"Sales person '{sales_username}' not found"})
                                    skipped += 1
                                    continue
                            
                            if pd.isna(row.get('admission_date')):
                                error_rows.append({**row.to_dict(), "error": "Missing admission_date"})
                                skipped += 1
                                continue

                            admission_date = None
                            if pd.notna(row.get('admission_date')):
                                try:
                                    admission_date = pd.to_datetime(
                                        str(row.get('admission_date')).strip(),
                                        format="%d-%m-%Y"
                                    ).date()
                                except ValueError:
                                    error_rows.append({**row.to_dict(), "error": "Invalid admission_date format (expected dd-mm-yyyy)"})
                                    skipped += 1
                                    continue

                            StudentProfile.objects.create(
                                user=user,
                                batch=batch,
                                mobile_no=str(row.get('mobile_no')).strip() if pd.notna(row.get('mobile_no')) else None,
                                whatsapp_no=str(row.get('whatsapp_no')).strip() if pd.notna(row.get('whatsapp_no')) else None,
                                sales_person=sales_person,
                                # admission_date=pd.to_datetime(row.get('admission_date')).date() if pd.notna(row.get('admission_date')) else None,
                                admission_date=admission_date,
                                drop_out=True if str(row.get('drop_out')).strip().lower() == 'yes' else False
                            )
                            added += 1
                    except Exception as e:
                        error_rows.append({**row.to_dict(), "error": str(e)})
                        skipped += 1
                        continue

                # Store error rows in session for download
                if error_rows:
                    request.session['student_import_errors'] = error_rows
                    messages.warning(
                        request,
                        f"Import complete. Added: {added}, Skipped: {skipped}. "
                        f"Some rows failed — download the error report below."
                    )
                else:
                    messages.success(request, f"Import complete. Added: {added}, Skipped: {skipped}")

                return redirect('import_students', batch_id=batch.id)

            except Exception as e:
                messages.error(request, f"Error reading Excel file: {e}")
    else:
        form = StudentImportForm()

    return render(request, "settings_app/import_students.html", {"form": form, "batch": batch})


# import openpyxl
# from django.http import HttpResponse
from .utils import export_dataframe_with_text_format

@login_required
def download_student_template(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)

    sample_data = [{
        'first_name': '',
        'last_name': '',
        'username': '',
        'password': '',
        'mobile_no': '',
        'whatsapp_no': '',
        'sales_person_username': '',
        # 'admission_date': '2025-08-26',  # sample YYYY-MM-DD
        'admission_date': '26-08-2025',  # sample DD-MM-YYYY
        'drop_out': 'No'
    }]

    df = pd.DataFrame(sample_data)
    return export_dataframe_with_text_format(
        df,
        filename=f"student_import_template_batch_{batch_id}.xlsx",
        sheet_name="Template"
    )


from .utils import export_dataframe_with_text_format

@login_required
def download_student_import_errors(request, batch_id):
    errors = request.session.get("student_import_errors", [])
    if not errors:
        messages.error(request, "No error report available.")
        return redirect('import_students', batch_id=batch_id)

    df = pd.DataFrame(errors)

    # Format admission_date as dd-mm-yyyy if present
    if "admission_date" in df.columns:
        df["admission_date"] = df["admission_date"].apply(
            lambda x: pd.to_datetime(x).strftime("%d-%m-%Y") if pd.notna(x) else ""
        )

    return export_dataframe_with_text_format(
        df,
        filename=f"student_import_errors_batch_{batch_id}.xlsx",
        sheet_name="Errors"
    )

@login_required
def placement_list(request):
    placements = PlacementProfile.objects.select_related("user", "branch").all()
    return render(request, "settings_app/placement_list.html", {"placements": placements})


@login_required
def add_placement(request):
    branches = Branch.objects.all()
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        branch_id = request.POST.get("branch")
        mobile_no = request.POST.get("mobile_no", "").strip()
        whatsapp_no = request.POST.get("whatsapp_no", "").strip()

        if not (first_name and last_name and username and email and password and branch_id):
            messages.error(request, "All required fields must be filled.")
            return redirect("add_placement")

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        branch = get_object_or_404(Branch, id=branch_id)

        PlacementProfile.objects.create(
            user=user,
            branch=branch,
            mobile_no=mobile_no,
            whatsapp_no=whatsapp_no,
        )

         # ✅ Ensure "Placement" group exists and add user to it
        placement_group, created = Group.objects.get_or_create(name="Placement")
        user.groups.add(placement_group)


        messages.success(request, "Placement staff added successfully!")
        return redirect("placement_list")

    return render(request, "settings_app/placement_form.html", {"branches": branches, "title": "Add Placement"})


@login_required
def edit_placement(request, placement_id):
    placement = get_object_or_404(PlacementProfile, id=placement_id)
    branches = Branch.objects.all()

    if request.method == "POST":
        placement.user.first_name = request.POST.get("first_name", "").strip()
        placement.user.last_name = request.POST.get("last_name", "").strip()
        placement.user.username = request.POST.get("username", "").strip()
        placement.user.email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        if password:
            placement.user.set_password(password)
        placement.user.save()

        branch_id = request.POST.get("branch")
        placement.branch = get_object_or_404(Branch, id=branch_id)
        placement.mobile_no = request.POST.get("mobile_no", "").strip()
        placement.whatsapp_no = request.POST.get("whatsapp_no", "").strip()
        placement.save()

        messages.success(request, "Placement staff updated successfully!")
        return redirect("placement_list")

    return render(request, "settings_app/placement_form.html", {
        "placement": placement,
        "branches": branches,
        "title": "Edit Placement"
    })

@login_required
def delete_placement(request, placement_id):
    placement = get_object_or_404(PlacementProfile, id=placement_id)
    if request.method == "POST":
        placement.user.delete()  # also deletes PlacementProfile
        messages.success(request, "Placement staff deleted successfully!")
        return redirect("placement_list")

    return render(request, "settings_app/delete_placement.html", {"placement": placement})

@login_required
def placement_dashboard(request):
    # batches = Batch.objects.all()
    # return render(request, 'manager_dashboard.html', {'batches': batches})
    return render(request, 'settings_app/placement_dashboard.html')



@login_required
def get_monthly_review_stats(request):
    faculty = FacultyProfile.objects.get(user=request.user)
    batches = Batch.objects.filter(faculty=faculty)

    month_val = request.GET.get("month")  # format YYYY-MM
    if not month_val:
        return JsonResponse({"error": "Month required"}, status=400)

    year, month = map(int, month_val.split("-"))

    # Completed reviews
    completed_qs = TrainerMonthlyReview.objects.filter(
        user=faculty,
        review_date__year=year,
        review_date__month=month
    )
    completed_reviews = completed_qs.count()

    reviewed_batches = list(completed_qs.values_list("batch_id", flat=True))
    pending_batches = list(batches.exclude(id__in=reviewed_batches).values_list("id", flat=True))

    return JsonResponse({
        "completed_reviews": completed_reviews,
        "pending_reviews": len(pending_batches),
        "reviewed_batches": reviewed_batches,
        "pending_batches": pending_batches,
    })
