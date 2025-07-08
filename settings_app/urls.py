from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home Page URL
    path('login/', auth_views.LoginView.as_view(template_name='settings_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    # path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('no-permission/', views.no_permission, name='no_permission'),

    path('batches/', views.batch_list, name='batch_list'),
    path('batches/add/', views.add_batch, name='add_batch'),
    path('batches/edit/<int:batch_id>/', views.edit_batch, name='edit_batch'),
    path('batches/delete/<int:batch_id>/', views.delete_batch, name='delete_batch'),
    # Course URLs
    path('course/add/', views.add_course, name='add_course'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    # Branch URLs
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/add/', views.add_branch, name='add_branch'),
    path('branches/edit/<int:branch_id>/', views.edit_branch, name='edit_branch'),
    path('branches/delete/<int:branch_id>/', views.delete_branch, name='delete_branch'),

    # Student URLs
    # path('students/', views.student_list, name='student_list'),
    # path('students/add/', views.add_student, name='add_student'),
    # path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    # path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    # Faculty URLs
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.add_faculty, name='add_faculty'),
    path('faculty/edit/<int:faculty_id>/', views.edit_faculty, name='edit_faculty'),
    path('faculty/delete/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),
]

# if settings.DEBUG:  # Only for development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Settings to change the header and title of the Admin site
# admin.site.site_header = settings.ADMIN_SITE_HEADER
# admin.site.site_title = settings.ADMIN_SITE_TITLE
# admin.site.index_title = settings.ADMIN_SITE_TITLE

# # change the 'View Site' link
# admin.site.site_url = settings.ADMIN_SITE_URL