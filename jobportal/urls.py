
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_candidate, name='register'),
    path('candidate-dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('company-register/', views.register_company, name='company_register'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('candidate-profile/', views.candidate_profile, name='candidate_profile'),
    path('edit-candidate-profile/', views.edit_candidate_profile, name='edit_candidate_profile'),
    path('login/', views.candidate_login, name='login'),
    path('logout/', views.candidate_logout, name='logout'),
    path('browse-jobs/', views.browse_jobs, name='browse_jobs'),
    path('job-details/<int:job_id>/', views.job_details, name='job_details'),
    path('company/post-job/', views.post_job, name='post_job'),
    path('company/manage-jobs/', views.manage_jobs, name='manage_jobs'),
    path('company/edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('company/delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('company/toggle-job/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('candidate/my-applications/', views.my_applications, name='my_applications'),
    path('company/applications/', views.company_applications, name='company_applications'),
    path('company/applicant/<int:application_id>/', views.applicant_details, name='applicant_details'),
    path('company/update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
]
