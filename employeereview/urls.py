from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('review/create', views.home, name='home'),  # Home Page URL
    
    # path('monthly-review/', views.monthly_review_create, name='monthly_review_create'),
    # path('monthly-review/<int:batch_id>/', views.create_monthly_review, name='create_monthly_review'),
    path('monthly-review/<int:batch_id>/', views.monthly_review_view, name='create_monthly_review'),
    # path('monthly-review-report/', views.monthly_review_report, name='monthly_review_report'),
    path('ajax/get-batches/', views.get_batches_by_faculty, name='get_batches_by_faculty'),
    path('ajax/get-review-months/', views.get_review_months, name='get_review_months'),
    path('export-review/<int:faculty_id>/<int:batch_id>/<str:review_month>/', views.export_review_pdf, name='export_review_pdf'),
    # path('all-month-reviews/', views.all_month_reviews, name='all_month_reviews'),
    path('get-prefill-data/', views.get_review_prefill_data, name='get_review_prefill_data'),

    path('sales-monthly-review/', views.sales_add_monthly_review, name='sales_add_monthly_review'),
    # path('sales-all-month-reviews/', views.sales_all_month_reviews, name='sales_all_month_reviews'),
    # path('sales-monthly-review-report/', views.sales_monthly_review_report, name='sales_monthly_review_report'),
    path("sales-monthly-get-metrics/", views.get_sales_metrics, name="get_sales_metrics"),

    path("sales-all-month-reviews/", views.sales_all_months_review_report, name="sales_all_months_review_report"),
    path("sales-monthly-review-report/", views.sales_monthly_review_report, name="sales_monthly_review_report"),
    path('ajax/sales-member-months/', views.get_sales_member_months, name='get_sales_member_months'),


    path('trainer/review/add/<int:batch_id>/', views.trainer_add_review, name='trainer_add_review'),
    path('trainer/review/get-metrics/', views.get_trainer_metrics, name='get_trainer_metrics'),
    path('trainer/review/save/', views.save_trainer_review, name='save_trainer_review'),

    # path("monthly-review-report/", views.review_report_view, name="monthly_review_report"),
    # path("report/batches/<int:trainer_id>/", views.get_batches_by_trainer, name="get_batches_by_trainer"),
    # path("report/months/<int:trainer_id>/<int:batch_id>/", views.get_months_by_batch, name="get_months_by_batch"),
    # path("report/generate/<int:review_id>/", views.generate_review_report, name="generate_review_report"),

    path("monthly-review-report/", views.trainer_review_report, name="monthly_review_report"),
    path("get-batches/", views.get_batches_for_trainer, name="get_batches"),
    path("get-months/", views.get_months_for_batch, name="get_months"),
    path("view-review-report/", views.view_review_report, name="view_review_report"),  

    # urls.py
    # path('all-month-reviews/', views.all_month_reviews, name='all_month_reviews'),
    path("all-month-reviews/", views.all_months_review_report, name="all_month_reviews"),
    path("view-all-months-report/", views.view_all_months_report, name="view_all_months_report"),

    path("courses/<int:pk>/sync-activities/", views.sync_course_activities, name="sync_course_activities"),

    path("placement-add-monthly-review/", views.placement_add_monthly_review, name="placement_add_monthly_review"),
    path("placement-all-month-reviews/", views.placement_all_months_review_report, name="placement_all_months_review_report"),
    path("placement-monthly-review-report/", views.placement_monthly_review_report, name="placement_monthly_review_report"),
    path("get-placement-review-months/<int:user_id>/", views.get_placement_review_months, name="get_placement_review_months"),
    path("placement/save_review/", views.save_placement_review, name="save_placement_review"),
    path("placement/get_metrics/", views.get_placement_metrics, name="get_placement_metrics"),

    path("targets/", views.sales_target_list, name="sales_target_list"),
    path("targets/add/", views.sales_target_create, name="sales_target_create"),
    path("targets/<int:pk>/edit/", views.sales_target_edit, name="sales_target_edit"),
    path("targets/<int:pk>/delete/", views.sales_target_delete, name="sales_target_delete"),










    
]
