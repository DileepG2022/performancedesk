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
    path("get-monthly-review-stats/", views.get_monthly_review_stats, name="get_monthly_review_stats"),
    path('sales_dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path("sales/metrics/<int:year>/<int:month>/", views.sales_metrics_data, name="sales_metrics_data"),
    path('placement_dashboard/', views.placement_dashboard, name='placement_dashboard'),
    # path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('no-permission/', views.no_permission, name='no_permission'),

    path('switch-department/', views.switch_department, name='switch_department'),
    path('department-menu/', views.get_department_menu, name='department_menu'),

    path('batches/', views.batch_list, name='batch_list'),
    path('batches/add/', views.add_batch, name='add_batch'),
    path('batches/edit/<int:batch_id>/', views.edit_batch, name='edit_batch'),
    path('batches/delete/<int:batch_id>/', views.delete_batch, name='delete_batch'),
    path('batches/<int:batch_id>/activities/', views.batch_activity_view, name='batch_activities'),

    # Course URLs
    # path('course/add/', views.add_course, name='add_course'),
    path('course/add/', views.course_create, name='add_course'),
    path('courses/', views.course_list, name='course_list'),
    # path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    # path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('courses/edit/<int:pk>/', views.course_update, name='course_edit'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),

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

    # Sales URLs
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/add/', views.add_sales, name='add_sales'),
    path('sales/edit/<int:sales_id>/', views.edit_sales, name='edit_sales'),
    path('sales/delete/<int:sales_id>/', views.delete_sales, name='delete_sales'),

    # Students URLs
    path('batch/<int:batch_id>/students/', views.student_list, name='student_list'),
    path('batch/<int:batch_id>/students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    
    # urls.py
    path('batch/<int:batch_id>/students/import/', views.import_students, name='import_students'),
    path('batch/<int:batch_id>/students/export/', views.export_students, name='export_students'),
    path('batches/<int:batch_id>/download-template/', views.download_student_template, name='download_student_template'),
    path('batches/<int:batch_id>/download-import-errors/', views.download_student_import_errors, name='download_import_errors'),

    path('placement/', views.placement_list, name='placement_list'),
    path('placement/add/', views.add_placement, name='add_placement'),
    path('placement/edit/<int:placement_id>/', views.edit_placement, name='edit_placement'),
    path('placement/delete/<int:placement_id>/', views.delete_placement, name='delete_placement'),



]

# if settings.DEBUG:  # Only for development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Settings to change the header and title of the Admin site
# admin.site.site_header = settings.ADMIN_SITE_HEADER
# admin.site.site_title = settings.ADMIN_SITE_TITLE
# admin.site.index_title = settings.ADMIN_SITE_TITLE

# # change the 'View Site' link
# admin.site.site_url = settings.ADMIN_SITE_URL