# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Batch, Branch, Course, StudentProfile, FacultyProfile

from .forms import BatchForm, CourseForm, BranchForm, StudentProfileForm, EditStudentProfileForm, FacultyProfileForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db import transaction  # Import transaction for rollback

import os
import datetime
# from exams.models import Exam, ExamSubmission
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

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
    elif user.groups.filter(name='Student').exists():
        return redirect('student_dashboard')  # Redirect Student to their dashboard
    else:
        return render(request, 'settings_app/home.html')  # Default landing page

def general_error(request, exception=None):
    print("error")
    return render(request, 'settings_app/general_error.html')

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def no_permission(request):
    return render(request, 'settings_app/no_permission.html')

@user_passes_test(is_manager, login_url='no_permission')
@login_required
def manager_dashboard(request):
    # batches = Batch.objects.all()
    # return render(request, 'manager_dashboard.html', {'batches': batches})
    return render(request, 'settings_app/manager_dashboard.html')
@login_required
def faculty_dashboard(request):
    """Display batches assigned to the logged-in faculty"""
    try:
        faculty = FacultyProfile.objects.get(user=request.user)  # Get faculty profile
        batches = Batch.objects.filter(faculty=faculty)  # Get batches where faculty is assigned
        # exams = Exam.objects.filter(created_by=faculty).order_by('-start_time')[:5]
    except FacultyProfile.DoesNotExist:
        batches = None  # If faculty profile doesn't exist, set batches to None
    return render(request, 'settings_app/faculty_dashboard.html', {'batches': batches})

    # return render(request, 'settings_app/faculty_dashboard.html', {'batches': batches,
    # 'exams': exams})
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
@login_required
def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'settings_app/batch_list.html', {'batches': batches})
@login_required
def add_batch(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch added successfully!")
            # return redirect('batch_list')
    else:
        form = BatchForm()
    return render(request, 'settings_app/add_batch.html', {'form': form})

# Edit batch
@login_required
def edit_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)

    if request.method == "POST":
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch updated successfully!")
            # return redirect('batch_list')
    else:
        form = BatchForm(instance=batch)

    return render(request, 'settings_app/edit_batch.html', {'form': form})

# Delete batch
@login_required
def delete_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)

    if request.method == "POST":
        batch.delete()
        messages.success(request, "Batch deleted successfully!")
        # return redirect('batch_list')

    return render(request, 'settings_app/delete_batch.html', {'batch': batch})





@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'settings_app/add_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to course list page
    else:
        form = CourseForm(instance=course)

    return render(request, 'settings_app/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect('course_list')  # Redirect after deleting
    return render(request, 'settings_app/delete_course.html', {'course': course})

@login_required
def student_list(request):
    """Display list of students with search functionality"""
    students = StudentProfile.objects.all()

    student_id = request.GET.get('student_id')
    username = request.GET.get('username')

    if student_id:
        students = students.filter(student_id__icontains=student_id)
    if username:
        students = students.filter(user__username__icontains=username)

    return render(request, 'settings_app/student_list.html', {'students': students})

@login_required
def add_student(request):
    """Add a new student"""
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)

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
                        password=password
                    )

                    # Add user to Student Group
                    student_group, _ = Group.objects.get_or_create(name='Student')
                    user.groups.add(student_group)

                    # Create Student Profile
                    student = form.save(commit=False)
                    student.user = user
                    student.created_by = request.user  # Assign the logged-in user
                    student.save()
                    form.save_m2m()  # Save ManyToManyField (if any)

                    messages.success(request, "Student added successfully!")
                    # return redirect('student_list')

            except Exception as e:
                print(f"Error adding student: {e}")
                messages.error(request, f"Error adding student: {e}")
        else:
            print("Form errors:", form.errors)  # Debugging line

    else:
        form = StudentProfileForm()

    return render(request, 'settings_app/add_student.html', {'form': form})

@login_required
def edit_student(request, student_id):
    """Edit student details"""
    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details updated successfully!")
            # return redirect('student_list')
    else:
        form = EditStudentProfileForm(instance=student)

    return render(request, 'settings_app/edit_student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, student_id):
    """Delete student"""
    student = get_object_or_404(StudentProfile, id=student_id)
    
    if request.method == 'POST':
        student.user.delete()  # Deletes the associated user as well
        student.delete()
        messages.success(request, "Student deleted successfully!")
        # return redirect('student_list')

    return render(request, 'settings_app/delete_student.html', {'student': student})

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

@login_required
def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'settings_app/batch_list.html', {'batches': batches})

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
        form = FacultyProfileForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty updated successfully!")
            # return redirect('faculty_list')
    else:
        form = FacultyProfileForm(instance=faculty)
    return render(request, 'settings_app/edit_faculty.html', {'form': form, 'faculty': faculty})

@login_required
def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    faculty.user.delete()  # Deletes both FacultyProfile and associated User
    messages.success(request, "Faculty deleted successfully!")
    # return redirect('faculty_list')
