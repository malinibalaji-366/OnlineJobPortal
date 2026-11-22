from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from candidates.models import CandidateProfile
from django.contrib.auth import logout
from companies.models import CompanyProfile
from .models import UserRole
from django.contrib.auth.decorators import login_required
from candidates.models import CandidateProfile
from django.db.models import Q
from jobs.models import Job ,Application

# Homepage
def home(request):
    return render(request, 'home.html')


# Candidate Registration
def register_candidate(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        phone = request.POST.get('phone')
        education = request.POST.get('education')
        skills = request.POST.get('skills')
        location = request.POST.get('location')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists!'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        UserRole.objects.create(
            user=user,
            role='Candidate'
        )
        
        CandidateProfile.objects.create(
            user=user,
            phone=phone,
            education=education,
            skills=skills,
            location=location
        )

        return redirect('home')

    return render(request, 'register.html')

from django.contrib.auth import authenticate, login


# Candidate and Company Login
def candidate_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Check whether user already has a role
            role_record = UserRole.objects.filter(
                user=user
            ).first()

            # Handle accounts created before role system
            if role_record is None:

                if CandidateProfile.objects.filter(user=user).exists():

                    role_record = UserRole.objects.create(
                        user=user,
                        role='Candidate'
                    )

                elif CompanyProfile.objects.filter(user=user).exists():

                    role_record = UserRole.objects.create(
                        user=user,
                        role='Company'
                    )

            # Redirect according to user role
            if role_record is not None:

                login(request, user)

                if role_record.role == 'Candidate':
                    return redirect('candidate_dashboard')

                elif role_record.role == 'Company':
                    return redirect('company_dashboard')

            return render(request, 'login.html', {
                'error': 'User profile or role not found!'
            })

        else:

            return render(request, 'login.html', {
                'error': 'Invalid username or password!'
            })

    return render(request, 'login.html')

def candidate_logout(request):
    logout(request)
    return redirect('home')


def register_company(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        company_name = request.POST.get('company_name')
        description = request.POST.get('description')
        website = request.POST.get('website')
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        if User.objects.filter(username=username).exists():
            return render(request, 'company_register.html', {
                'error': 'Username already exists!'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        UserRole.objects.create(
            user=user,
            role='Company'
        )
        
        CompanyProfile.objects.create(
            user=user,
            company_name=company_name,
            description=description,
            website=website,
            phone=phone,
            location=location
        )

        return redirect('home')

    return render(request, 'company_register.html')

# Company Dashboard
@login_required(login_url='login')
def company_dashboard(request):

    role_record = UserRole.objects.filter(
        user=request.user
    ).first()

    if role_record is None:
        return redirect('home')

    if role_record.role == 'Candidate':
        return redirect('candidate_dashboard')

    if role_record.role != 'Company':
        return redirect('home')

    return render(request, 'company_dashboard.html')

# Candidate Dashboard
@login_required(login_url='login')
def candidate_dashboard(request):

    role_record = UserRole.objects.filter(
        user=request.user
    ).first()

    if role_record is None:
        return redirect('home')

    if role_record.role == 'Company':
        return redirect('company_dashboard')

    if role_record.role != 'Candidate':
        return redirect('home')

    return render(request, 'candidate_dashboard.html')


# Candidate Profile
@login_required(login_url='login')
def candidate_profile(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Candidate'
    ).exists():
        return redirect('home')

    profile = CandidateProfile.objects.get(
        user=request.user
    )

    return render(request, 'candidate_profile.html', {
        'profile': profile
    })
    
# Edit Candidate Profile
@login_required(login_url='login')
def edit_candidate_profile(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Candidate'
    ).exists():
        return redirect('home')

    profile = CandidateProfile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        profile.phone = request.POST.get('phone')
        profile.education = request.POST.get('education')
        profile.skills = request.POST.get('skills')
        profile.location = request.POST.get('location')

        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('candidate_profile')

    return render(request, 'edit_candidate_profile.html', {
        'profile': profile
    })
# Browse All Jobs

@login_required(login_url='login')
def browse_jobs(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Candidate'
    ).exists():
        return redirect('home')

    jobs = Job.objects.filter(
        is_active=True
    ).select_related('company').order_by('-posted_at')

    keyword = request.GET.get('keyword', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(company__company_name__icontains=keyword)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if job_type:
        jobs = jobs.filter(
            job_type__iexact=job_type
        )

    return render(request, 'browse_jobs.html', {
        'jobs': jobs,
        'keyword': keyword,
        'location': location,
        'selected_job_type': job_type,
        'job_count': jobs.count(),
    })


# Job Details
@login_required(login_url='login')
def job_details(request, job_id):

    if not UserRole.objects.filter(
        user=request.user,
        role='Candidate'
    ).exists():
        return redirect('home')

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    candidate = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    application_exists = Application.objects.filter(
        candidate=candidate,
        job=job
    ).exists()

    return render(request, 'job_details.html', {
        'job': job,
        'application_exists': application_exists,
        'applied_now': request.GET.get('applied') == '1',
        'already_applied': request.GET.get('already') == '1'
    })


# Apply for Job
@login_required(login_url='login')
def apply_job(request, job_id):

    if request.method != 'POST':
        return redirect('browse_jobs')

    if not UserRole.objects.filter(
        user=request.user,
        role='Candidate'
    ).exists():
        return redirect('home')

    candidate = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    application, created = Application.objects.get_or_create(
        candidate=candidate,
        job=job
    )

    if created:
        messages.success(request, 'Your application submitted successfully!')
    else:
        messages.warning(request, 'You have already applied for this job.')

    return redirect('job_details', job_id=job.id)
    
# Post a Job
@login_required(login_url='login')
def post_job(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = CompanyProfile.objects.filter(
        user=request.user
    ).first()

    if not company:
        return redirect('home')

    error = None

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        location = request.POST.get('location', '').strip()
        salary = request.POST.get('salary', '').strip()
        job_type = request.POST.get('job_type', '').strip()

        try:
            vacancies = int(request.POST.get('vacancies', 1))
        except (ValueError, TypeError):
            vacancies = 0

        if not all([
            title, description, requirements,
            location, salary, job_type
        ]):
            error = "Please fill in all fields."

        elif vacancies < 1:
            error = "Vacancies must be at least 1."

        else:
            Job.objects.create(
                company=company,
                title=title,
                description=description,
                requirements=requirements,
                location=location,
                salary=salary,
                job_type=job_type,
                vacancies=vacancies,
                is_active=True
            )
            messages.success(request, 'Job posted successfully!')
            return redirect('company_dashboard')

    return render(request, 'post_job.html', {
        'error': error
    })
    
# Manage Company Jobs
@login_required(login_url='login')
def manage_jobs(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    jobs = Job.objects.filter(
        company=company
    ).order_by('-posted_at')

    return render(request, 'manage_jobs.html', {
        'jobs': jobs
    })


# Edit Job
@login_required(login_url='login')
def edit_job(request, job_id):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        company=company
    )

    if request.method == 'POST':

        job.title = request.POST.get('title', '').strip()
        job.description = request.POST.get('description', '').strip()
        job.requirements = request.POST.get('requirements', '').strip()
        job.location = request.POST.get('location', '').strip()
        job.salary = request.POST.get('salary', '').strip()
        job.job_type = request.POST.get('job_type', '').strip()

        try:
            vacancies = int(request.POST.get('vacancies', 0))
        except (ValueError, TypeError):
            vacancies = 0

        if not all([
            job.title,
            job.description,
            job.requirements,
            job.location,
            job.salary,
            job.job_type
        ]) or vacancies < 1:

            return render(request, 'edit_job.html', {
                'job': job,
                'error': 'Please enter valid details in all fields.'
            })

        job.vacancies = vacancies
        job.save()
        messages.success(request, 'Job edited successfully!')
        return redirect('manage_jobs')

    return render(request, 'edit_job.html', {
        'job': job
    })


# Delete Job
@login_required(login_url='login')
def delete_job(request, job_id):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        company=company
    )

    if request.method == 'POST':
        job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('manage_jobs')


# Activate / Deactivate Job
@login_required(login_url='login')
def toggle_job_status(request, job_id):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        company=company
    )

    if request.method == 'POST':
        job.is_active = not job.is_active
        job.save()

    return redirect('manage_jobs')


# Candidate - My Applications
@login_required(login_url='login')
def my_applications(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Candidate'
    ).exists():
        return redirect('home')

    candidate = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    applications = Application.objects.filter(
        candidate=candidate
    ).select_related(
        'job', 'job__company'
    ).order_by('-applied_at')

    return render(request, 'my_applications.html', {
        'applications': applications
    })


# Company - View All Applicants
@login_required(login_url='login')
def company_applications(request):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    applications = Application.objects.filter(
        job__company=company
    ).select_related(
        'candidate__user', 'job'
    ).order_by('-applied_at')

    return render(request, 'company_applications.html', {
        'applications': applications
    })


# Company - View Applicant Details
@login_required(login_url='login')
def applicant_details(request, application_id):

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company=company
    )

    return render(request, 'applicant_details.html', {
        'application': application,
        'status_updated': request.GET.get('updated') == '1'
    })


# Company - Update Application Status
@login_required(login_url='login')
def update_application_status(request, application_id):

    if request.method != 'POST':
        return redirect('company_applications')

    if not UserRole.objects.filter(
        user=request.user,
        role='Company'
    ).exists():
        return redirect('home')

    company = get_object_or_404(
        CompanyProfile,
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company=company
    )

    new_status = request.POST.get('status')

    valid_statuses = dict(Application.STATUS_CHOICES)

    if new_status in valid_statuses:
        application.status = new_status
        application.save()
        
    messages.success(request, 'Application status updated successfully!')

    return redirect(
        f'/company/applicant/{application.id}/?updated=1'
    )
