"""
URL configuration for hirestack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hireapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register, name='register'),
    path('login/',views.loginn,name='login'),
    path('home/', views.home, name='home'),

    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.landingpage,name='landing'),
    # path('users/', views.users, name='users'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('emregister/',views.emregister,name='emregister'),
    path('emlogin/',views.emlogin,name='emlogin'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('addexp/',views.addexp,name='addexp'),
    path('jobposting/',views.jobposting,name='jobposting'),
    path('userlogout/',views.logout_view,name='logout'),
    path('emland/',views.emland,name='emland'),
    path('emprofile/', views.emprofile, name='emprofile'),
    path('emlogout/',views.logout_vieww,name='emlogout'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('reject/<int:app_id>/', views.reject_application, name='reject_application'),
    
    path('create-test/<int:job_id>/', views.create_test, name='create_test'),
    path('add-questions/<int:test_id>/', views.add_questions, name='add_questions'),
    path('attend-test/<int:test_id>/', views.attend_test, name='attend_test'),
    path('test-result/<int:result_id>/', views.test_result, name='test_result'),

    path('admindash/',views.admindash,name='admindash'),
    path('about/',views.about,name='about'),
    path("block-user/<int:id>/", views.block_user, name="block_user"),
    path("block-employee/<int:id>/", views.block_employee, name="block_employee"),
    path("delete-job/<int:id>/", views.delete_job, name="delete_job"),








    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
