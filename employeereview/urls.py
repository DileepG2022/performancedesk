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
    path('monthly-review/<int:batch_id>/', views.create_monthly_review, name='create_monthly_review'),

    
]
